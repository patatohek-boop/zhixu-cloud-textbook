"""Black-box check of the exact published APK in an isolated Android 15 emulator.

Only drives public UI and system file pickers. Never instrument the production app,
copy private signing material, or run this against a personal device.
"""
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import time
import xml.etree.ElementTree as ET

PKG = 'app.zhixu.textbook.independent'
OUT = pathlib.Path('work/signed-release-ui')
OUT.mkdir(parents=True, exist_ok=True)
step = 0


def adb(*args, binary=False, check=True):
    return subprocess.run(['adb', *args], check=check, capture_output=True,
                          text=not binary, timeout=45).stdout


def snapshot(name):
    (OUT / (name + '.png')).write_bytes(adb('exec-out', 'screencap', '-p', binary=True))
    return hierarchy(name)


def hierarchy(name='latest'):
    global step
    step += 1
    adb('shell', 'uiautomator', 'dump', '/sdcard/zhixu-ui.xml')
    raw = adb('exec-out', 'cat', '/sdcard/zhixu-ui.xml')
    (OUT / f'{step:03d}-{name}.xml').write_text(raw)
    return ET.fromstring(raw)


def locate(tree, labels=None, cls=None):
    labels = {x.casefold() for x in labels} if labels else None
    for n in tree.iter('node'):
        a = n.attrib
        values = {a.get('text', '').casefold(), a.get('content-desc', '').casefold()}
        if labels and not (labels & values):
            continue
        if cls and a.get('class') != cls:
            continue
        bounds = [int(v) for v in re.findall(r'\d+', a.get('bounds', ''))]
        if len(bounds) == 4 and bounds[2] > bounds[0] and bounds[3] > bounds[1]:
            return n
    return None


def tap_node(node):
    b = [int(v) for v in re.findall(r'\d+', node.attrib['bounds'])]
    adb('shell', 'input', 'tap', str((b[0]+b[2])//2), str((b[1]+b[3])//2))
    time.sleep(0.7)


def tap(labels=None, cls=None, wait=15):
    until = time.monotonic() + wait
    while time.monotonic() < until:
        n = locate(hierarchy(), labels, cls)
        if n is not None:
            tap_node(n)
            return
        time.sleep(0.5)
    raise AssertionError(f'UI control absent: {labels or cls}')


def menu(action):
    tap(['应用菜单'])
    tap([action])


def downloads():
    tree = hierarchy('file-picker')
    # DocumentsUI may reopen Downloads; use the roots drawer so selection is explicit.
    root = locate(tree, ['Show roots', '显示根目录', '打开抽屉', 'Navigation drawer'])
    if root is not None:
        tap_node(root)
        drawer = hierarchy('picker-roots')
        roots = [n for n in drawer.iter('node')
                 if n.attrib.get('resource-id') == 'android:id/title'
                 and n.attrib.get('text') in ('Downloads', '下载')]
        assert len(roots) == 1, 'Downloads root must be identified inside the open drawer'
        tap_node(roots[0])
        selected = hierarchy('downloads-selected')
        assert locate(selected, ['Files in Downloads', 'Downloads', '下载']) is not None
        assert locate(selected, ['Recent files']) is None, 'Picker is still in Recent, not Downloads'
    elif locate(tree, ['Downloads', '下载']) is None:
        raise AssertionError('Could not identify the system Downloads picker')


def export(name):
    menu('导出学习备份')
    downloads()
    tap(cls='android.widget.EditText')
    adb('shell', 'input', 'keyevent', 'KEYCODE_MOVE_END')
    adb('shell', 'input', 'keyevent', *(['KEYCODE_DEL'] * 80))
    adb('shell', 'input', 'text', name)
    adb('shell', 'input', 'keyevent', 'KEYCODE_BACK')
    tap(['Save', '保存'])
    until = time.monotonic() + 15
    while time.monotonic() < until:
        data = adb('exec-out', 'cat', '/sdcard/Download/' + name, check=False)
        try:
            result = json.loads(data)
            (OUT / name).write_text(data)
            return result
        except json.JSONDecodeError:
            time.sleep(0.5)
    raise AssertionError('System export was not written: ' + name)


def import_file(name):
    menu('导入备份（合并记录）')
    downloads()
    tap([name])
    time.sleep(2)
    tap(['知道了', 'OK'], wait=5) if locate(hierarchy(), ['知道了', 'OK']) is not None else None


def records(data):
    return {k: data[k] for k in ('completed', 'bookmarks', 'notes', 'answers')}


def assert_source(data):
    assert 'calculus-03' in data['completed']
    assert 'calculus-04' in data['bookmarks']
    assert 'MIGRATION_SOURCE_NOTE' in data['notes']['calculus-03']
    assert data['answers']['calculus-03']['choice'] == 0


def launch():
    adb('shell', 'am', 'start', '-W', '-n', PKG + '/app.zhixu.textbook.MainActivity')
    time.sleep(10)
    assert locate(hierarchy('reader-ready'), ['应用菜单']) is not None


def main():
    global PKG
    apk = pathlib.Path(sys.argv[1])
    expected = pathlib.Path(str(apk) + '.sha256').read_text().split()[0]
    assert hashlib.sha256(apk.read_bytes()).hexdigest() == expected
    assert 'emulator-' in adb('get-serialno'), 'Only isolated emulator use is permitted'
    assert adb('shell', 'getprop', 'ro.kernel.qemu').strip() == '1'
    adb('shell', 'svc', 'wifi', 'disable')
    adb('shell', 'svc', 'data', 'disable')
    # Establish the legacy record through the same native import UI a user uses.
    # Its new marker was never present in the earlier instrumentation fixture.
    PKG = 'app.zhixu.textbook'
    synthetic = {'format': 'zhixu-learning', 'version': 1,
                 'completed': ['calculus-03'], 'bookmarks': ['calculus-04'],
                 'notes': {'calculus-03': 'MIGRATION_SOURCE_NOTE FORMAL_NATIVE_LEGACY_IMPORT 合成记录'},
                 'answers': {'calculus-03': {'choice': 0, 'at': '2026-10-03T00:00:00Z'}}}
    source = OUT / 'legacy-native-input.json'
    source.write_text(json.dumps(synthetic, ensure_ascii=False))
    adb('shell', 'mkdir', '-p', '/sdcard/Download')
    adb('push', str(source), '/sdcard/Download/legacy-native-input.json')
    launch()
    import_file('legacy-native-input.json')
    # Normal user Back, not Instrumentation.finish's forced target-process exit.
    adb('shell', 'input', 'keyevent', 'KEYCODE_BACK')
    time.sleep(1)
    launch()
    legacy_before = export('legacy-ui-export.json')
    assert_source(legacy_before)
    assert 'FORMAL_NATIVE_LEGACY_IMPORT' in legacy_before['notes']['calculus-03'], 'Legacy native import was lost after normal Back/reopen'
    snapshot('00-legacy-native-import-reopen')
    PKG = 'app.zhixu.textbook.independent'
    # Remove only the throw-away independent CI edition, never the legacy app.
    adb('uninstall', PKG + '.test')
    adb('uninstall', PKG)
    installed = adb('install', str(apk))
    assert 'Success' in installed
    runtime = adb('shell', 'dumpsys', 'package', PKG)
    (OUT / 'runtime-package.txt').write_text(runtime)
    assert 'versionCode=8' in runtime and 'versionName=1.5.0' in runtime
    assert not re.search(r'(?m)^\s*(?:pkgFlags|flags)=.*DEBUGGABLE', runtime)
    uids = adb('shell', 'pm', 'list', 'packages', '-U', 'app.zhixu.textbook')
    (OUT / 'package-uids.txt').write_text(uids)
    found = dict(re.findall(r'package:(app\.zhixu\.textbook(?:\.independent)?) uid:(\d+)', uids))
    assert found['app.zhixu.textbook'] != found[PKG], 'Sandboxes must use separate UIDs'
    launch()
    snapshot('01-first-offline-launch')
    empty = export('zhixu-empty.json')
    assert records(empty) == {'completed': [], 'bookmarks': [], 'notes': {}, 'answers': {}}, 'Final signed app read legacy records automatically'
    # Choose the actual document exported by the old app, exactly as a user would.
    import_file('legacy-ui-export.json')
    imported = export('zhixu-imported.json')
    assert_source(imported)
    snapshot('02-imported-records')
    menu('导入备份（合并记录）')
    adb('shell', 'input', 'keyevent', 'KEYCODE_BACK')
    time.sleep(1)
    # Cancellation must restore the reader and release its busy flag.
    cancelled = export('zhixu-after-cancel.json')
    assert records(cancelled) == records(imported)
    bad = OUT / 'zhixu-invalid.json'
    bad.write_text('{invalid json')
    adb('push', str(bad), '/sdcard/Download/zhixu-invalid.json')
    adb('shell', 'am', 'broadcast', '-a', 'android.intent.action.MEDIA_SCANNER_SCAN_FILE', '-d', 'file:///sdcard/Download/zhixu-invalid.json')
    import_file('zhixu-invalid.json')
    unchanged = export('zhixu-after-invalid.json')
    assert records(unchanged) == records(imported), 'Malformed import changed records'
    # An independent-only edit must remain separate from legacy data.
    edited = dict(imported)
    edited['notes'] = {'calculus-03': 'INDEPENDENT_ONLY_FORMAL_RELEASE'}
    edit_file = OUT / 'zhixu-edit.json'
    edit_file.write_text(json.dumps(edited))
    adb('push', str(edit_file), '/sdcard/Download/zhixu-edit.json')
    adb('shell', 'am', 'broadcast', '-a', 'android.intent.action.MEDIA_SCANNER_SCAN_FILE', '-d', 'file:///sdcard/Download/zhixu-edit.json')
    import_file('zhixu-edit.json')
    adb('shell', 'am', 'force-stop', PKG)
    launch()
    restored = export('zhixu-restored.json')
    assert_source(restored)
    assert 'INDEPENDENT_ONLY_FORMAL_RELEASE' in restored['notes']['calculus-03']
    # Same-cert replacement install must retain independent records.
    assert 'Success' in adb('install', '-r', str(apk))
    launch()
    updated = export('zhixu-after-reinstall.json')
    assert records(updated) == records(restored)
    PKG = 'app.zhixu.textbook'
    launch()
    legacy_after = export('legacy-after-independent.json')
    assert records(legacy_after) == records(legacy_before), 'Independent changes modified legacy records'
    snapshot('04-legacy-unchanged')
    PKG = 'app.zhixu.textbook.independent'
    launch()
    snapshot('03-relaunch-and-reinstall')
    result = {'sha256': expected, 'package': PKG, 'versionName': '1.5.0', 'versionCode': 8,
              'install': True, 'offline_first_launch': True, 'distinct_uids': found,
              'initial_records_empty': True, 'native_json_export_import': True,
              'cancel_and_invalid_import_atomic': True, 'relaunch_and_same_apk_reinstall_preserve_records': True,
              'legacy_records_unchanged': True, 'legacy_native_import_normal_exit_reopen': True,
              'boundary': 'Exact production-signed APK driven through public UI; no production-key instrumentation APK.'}
    (OUT / 'verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(json.dumps(result, ensure_ascii=False))
    print('ZHIXU_SIGNED_RELEASE_UI_SUCCESS')


try:
    main()
except BaseException:
    try:
        snapshot('failure')
        (OUT / 'logcat.txt').write_text(adb('logcat', '-d'))
    except Exception:
        pass
    raise
