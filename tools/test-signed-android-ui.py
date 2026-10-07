"""Black-box check of the exact published APK in an isolated Android 15 emulator.

Only drives public UI and system file pickers. Never instrument the production app,
copy private signing material, or run this against a personal device.
"""
import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import time
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
TARGET_PKG = 'app.zhixu.textbook.reader'
ORIGINAL_PKG = 'app.zhixu.textbook'
HISTORICAL_PKG = 'app.zhixu.textbook.independent'
HISTORICAL_APK_SHA256 = 'b4f92a1342ac5029e2a8a6c599e676ed414246c76d48c80b5dd50a37705734a0'
PKG = TARGET_PKG
OUT = pathlib.Path('work/signed-release-ui')
FILE_PREFIX = ''
emulator_verified = False
step = 0


def arguments(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('apk', type=pathlib.Path)
    parser.add_argument('--source-package', choices=(ORIGINAL_PKG, HISTORICAL_PKG), default=ORIGINAL_PKG)
    parser.add_argument('--source-apk', type=pathlib.Path, help='Exact archived 1.5.0 APK; only for the independent source scenario')
    parser.add_argument('--out-dir', type=pathlib.Path, help='Scenario-specific screenshots, backups, and result directory')
    parser.add_argument('--aapt', default='aapt', help='Android build-tools aapt executable')
    parser.add_argument('--apksigner', default='apksigner', help='Android build-tools apksigner executable')
    args = parser.parse_args(argv)
    if args.source_package == ORIGINAL_PKG and args.source_apk:
        parser.error('--source-apk is only valid for the archived independent 1.5.0 scenario')
    if args.source_package == HISTORICAL_PKG and args.source_apk is None:
        args.source_apk = ROOT / 'downloads/Zhixu-Independent-1.5.0.apk'
    return args


def verify_historical_source(args):
    """Read only public APK bytes and certificate metadata; never use a private key."""
    apk = args.source_apk
    digest = hashlib.sha256(apk.read_bytes()).hexdigest()
    assert digest == HISTORICAL_APK_SHA256, 'Source must be the exact archived 1.5.0 production APK'
    assert digest == pathlib.Path(str(apk) + '.sha256').read_text().split()[0]
    pin = (ROOT / 'downloads/1.5.0-certificate-sha256.txt').read_text().strip()
    assert re.fullmatch(r'[0-9a-f]{64}', pin), 'Historical certificate pin must be a SHA-256 digest'
    metadata = subprocess.run([args.aapt, 'dump', 'badging', str(apk)], check=True,
                              capture_output=True, text=True, encoding='utf-8', timeout=45).stdout
    signature = subprocess.run([args.apksigner, 'verify', '--verbose', '--print-certs', str(apk)],
                               check=True, capture_output=True, text=True, encoding='utf-8', timeout=45).stdout
    (OUT / 'source-apk-metadata.txt').write_text(metadata, encoding='utf-8')
    (OUT / 'source-apk-signature.txt').write_text(signature, encoding='utf-8')
    assert "name='app.zhixu.textbook.independent' versionCode='8' versionName='1.5.0'" in metadata
    assert "application-label:'知序·独立版'" in metadata and 'application-debuggable' not in metadata
    assert 'Number of signers: 1' in signature
    assert 'Signer #1 certificate SHA-256 digest: ' + pin in signature
    assert 'Verified using v2 scheme (APK Signature Scheme v2): true' in signature
    assert 'Verified using v3 scheme (APK Signature Scheme v3): true' in signature
    return {'kind': 'archived-production-apk', 'package': HISTORICAL_PKG,
            'versionName': '1.5.0', 'versionCode': 8, 'sha256': digest, 'certificate_sha256': pin}


def device_document(name):
    return '/sdcard/Download/' + FILE_PREFIX + name


def push_document(path):
    destination = device_document(path.name)
    adb('push', str(path), destination)
    adb('shell', 'am', 'broadcast', '-a', 'android.intent.action.MEDIA_SCANNER_SCAN_FILE',
        '-d', 'file://' + destination)


def remove_target_if_installed(package):
    assert emulator_verified, 'No installation changes before the emulator safety check'
    assert package in (TARGET_PKG, TARGET_PKG + '.test'), 'Never remove a source application'
    installed = adb('shell', 'pm', 'list', 'packages', package)
    if 'package:' + package in installed.splitlines():
        assert 'Success' in adb('uninstall', package)


def source_and_target_uids(text, source_package):
    packages = dict(re.findall(r'^package:(\S+) uid:(\d+)\s*$', text, re.MULTILINE))
    found = {package: packages[package] for package in (source_package, TARGET_PKG)}
    assert found[source_package] != found[TARGET_PKG], 'Sandboxes must use separate UIDs'
    return found


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
    filename = FILE_PREFIX + name
    # Refuse stale evidence instead of accidentally reading an earlier export
    # when DocumentsUI saves a colliding filename with an automatic suffix.
    exists = adb('shell', 'ls', '-d', device_document(name), check=False)
    assert not exists.strip(), 'Use a fresh isolated emulator/output run; export already exists'
    menu('导出学习备份')
    downloads()
    tap(cls='android.widget.EditText')
    adb('shell', 'input', 'keyevent', 'KEYCODE_MOVE_END')
    adb('shell', 'input', 'keyevent', *(['KEYCODE_DEL'] * 80))
    adb('shell', 'input', 'text', filename)
    adb('shell', 'input', 'keyevent', 'KEYCODE_BACK')
    tap(['Save', '保存'])
    until = time.monotonic() + 15
    while time.monotonic() < until:
        data = adb('exec-out', 'cat', device_document(name), check=False)
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
    select_document(FILE_PREFIX + name)
    time.sleep(2)
    tap(['知道了', 'OK'], wait=5) if locate(hierarchy(), ['知道了', 'OK']) is not None else None


def select_document(filename):
    # The second scenario inherits the first scenario's Downloads directory.
    # Search only the system provider's bounded file list, in both directions;
    # never swipe the reader or another foreground app looking for a filename.
    for toward_bottom in (True, False):
        previous = None
        for _ in range(12):
            tree = hierarchy('select-document')
            nodes = [n for n in tree.iter('node')
                     if n.attrib.get('package', '').endswith('.documentsui')]
            assert nodes, 'Expected DocumentsUI before selecting a backup'
            for n in nodes:
                if n.attrib.get('text') == filename or n.attrib.get('content-desc') == filename:
                    tap_node(n)
                    return
            lists = [n for n in nodes if n.attrib.get('scrollable') == 'true']
            if not lists:
                break
            signature = tuple((n.attrib.get('text'), n.attrib.get('content-desc'), n.attrib.get('bounds')) for n in nodes)
            if signature == previous:
                break
            previous = signature
            bounds = [int(x) for x in re.findall(r'\d+', lists[0].attrib.get('bounds', ''))]
            assert len(bounds) == 4 and bounds[2] > bounds[0] and bounds[3] > bounds[1]
            x = (bounds[0] + bounds[2]) // 2
            upper = bounds[1] + (bounds[3] - bounds[1]) // 4
            lower = bounds[1] + 3 * (bounds[3] - bounds[1]) // 4
            start, end = (lower, upper) if toward_bottom else (upper, lower)
            adb('shell', 'input', 'swipe', str(x), str(start), str(x), str(end), '300')
            time.sleep(0.4)
    raise AssertionError('Backup absent from the bounded Downloads list: ' + filename)


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
    tree = hierarchy('reader-ready')
    button = locate(tree, ['应用菜单'], cls='android.widget.Button')
    assert button is not None and button.attrib.get('package') == PKG, 'Expected package is not the visible native reader'
    title = '知序·独立版 · 离线教材' if PKG == HISTORICAL_PKG else '知序 · 离线教材'
    label = locate(tree, [title], cls='android.widget.TextView')
    assert label is not None and label.attrib.get('package') == PKG, 'Wrong old/new native app title'


def resumed_package():
    activity = adb('shell', 'dumpsys', 'activity', 'activities')
    for field in ('topResumedActivity', 'mResumedActivity', 'ResumedActivity'):
        match = re.search(r'\b' + field + r'[^\n]*?\bu\d+\s+([A-Za-z0-9_.]+)/', activity)
        if match:
            return match.group(1)
    raise AssertionError('Cannot determine the resumed application; refusing to send Back')


def normal_back_exit():
    assert resumed_package() == PKG, 'Source reader must be foreground before its normal exit'
    for _ in range(12):
        # A Back may dismiss a reading overlay or navigate WebView history.
        # Stop immediately once another app is resumed; never send Back there.
        if resumed_package() != PKG:
            hierarchy('source-after-normal-back')
            return
        adb('shell', 'input', 'keyevent', 'KEYCODE_BACK')
        time.sleep(0.8)
    assert resumed_package() != PKG, 'Source reader did not exit after bounded normal Back presses'
    hierarchy('source-after-normal-back')


def main(argv=None):
    global PKG, OUT, FILE_PREFIX, emulator_verified
    args = arguments(argv)
    scenario = 'independent-1.5.0' if args.source_package == HISTORICAL_PKG else 'original-package'
    OUT = args.out_dir or pathlib.Path('work/signed-release-ui') / scenario
    OUT.mkdir(parents=True, exist_ok=True)
    assert not (OUT / 'verification.json').exists(), 'Use a fresh output directory; do not reuse a prior acceptance result'
    FILE_PREFIX = scenario + '-'
    apk = args.apk
    expected = pathlib.Path(str(apk) + '.sha256').read_text().split()[0]
    assert hashlib.sha256(apk.read_bytes()).hexdigest() == expected
    assert 'emulator-' in adb('get-serialno'), 'Only isolated emulator use is permitted'
    assert adb('shell', 'getprop', 'ro.kernel.qemu').strip() == '1'
    emulator_verified = True
    adb('shell', 'svc', 'wifi', 'disable')
    adb('shell', 'svc', 'data', 'disable')
    source_evidence = {'kind': 'current-source-original-package-fixture', 'package': args.source_package}
    if args.source_package == HISTORICAL_PKG:
        source_evidence = verify_historical_source(args)
        # Plain install intentionally refuses to replace an existing historical
        # application. The CI emulator is disposable; source data is never cleared.
        assert 'Success' in adb('install', str(args.source_apk))
    source_runtime = adb('shell', 'dumpsys', 'package', args.source_package)
    (OUT / 'source-runtime-package.txt').write_text(source_runtime, encoding='utf-8')
    if args.source_package == HISTORICAL_PKG:
        assert 'versionCode=8' in source_runtime and 'versionName=1.5.0' in source_runtime
    # Establish the legacy record through the same native import UI a user uses.
    # Its new marker was never present in the earlier instrumentation fixture.
    PKG = args.source_package
    synthetic = {'format': 'zhixu-learning', 'version': 1,
                 'completed': ['calculus-03'], 'bookmarks': ['calculus-04'],
                 'notes': {'calculus-03': 'MIGRATION_SOURCE_NOTE FORMAL_NATIVE_LEGACY_IMPORT 合成记录'},
                 'answers': {'calculus-03': {'choice': 0, 'at': '2026-10-03T00:00:00Z'}}}
    source = OUT / 'legacy-native-input.json'
    source.write_text(json.dumps(synthetic, ensure_ascii=False))
    adb('shell', 'mkdir', '-p', '/sdcard/Download')
    push_document(source)
    launch()
    import_file('legacy-native-input.json')
    # Normal user Back, not Instrumentation.finish's forced target-process exit.
    normal_back_exit()
    launch()
    legacy_before = export('legacy-ui-export.json')
    assert_source(legacy_before)
    assert 'FORMAL_NATIVE_LEGACY_IMPORT' in legacy_before['notes']['calculus-03'], 'Legacy native import was lost after normal Back/reopen'
    snapshot('00-legacy-native-import-reopen')
    PKG = TARGET_PKG
    # Remove only the throw-away independent CI edition, never the legacy app.
    remove_target_if_installed(PKG + '.test')
    remove_target_if_installed(PKG)
    installed = adb('install', str(apk))
    assert 'Success' in installed
    runtime = adb('shell', 'dumpsys', 'package', PKG)
    (OUT / 'runtime-package.txt').write_text(runtime)
    assert 'versionCode=10' in runtime and 'versionName=1.6.1' in runtime
    assert not re.search(r'(?m)^\s*(?:pkgFlags|flags)=.*DEBUGGABLE', runtime)
    uids = adb('shell', 'pm', 'list', 'packages', '-U', 'app.zhixu.textbook')
    (OUT / 'package-uids.txt').write_text(uids)
    found = source_and_target_uids(uids, args.source_package)
    launch()
    snapshot('01-first-offline-launch')
    empty = export('zhixu-empty.json')
    assert records(empty) == {'completed': [], 'bookmarks': [], 'notes': {}, 'answers': {}}, 'Final signed app read legacy records automatically'
    # Choose the actual document exported by the old app, exactly as a user would.
    import_file('legacy-ui-export.json')
    imported = export('zhixu-imported.json')
    assert_source(imported)
    assert records(imported) == records(legacy_before), 'Import did not preserve all four legacy record fields'
    snapshot('02-imported-records')
    menu('导入备份（合并记录）')
    adb('shell', 'input', 'keyevent', 'KEYCODE_BACK')
    time.sleep(1)
    # Cancellation must restore the reader and release its busy flag.
    cancelled = export('zhixu-after-cancel.json')
    assert records(cancelled) == records(imported)
    bad = OUT / 'zhixu-invalid.json'
    bad.write_text('{invalid json')
    push_document(bad)
    import_file('zhixu-invalid.json')
    unchanged = export('zhixu-after-invalid.json')
    assert records(unchanged) == records(imported), 'Malformed import changed records'
    # An independent-only edit must remain separate from legacy data.
    edited = dict(imported)
    edited['notes'] = {'calculus-03': 'INDEPENDENT_ONLY_FORMAL_RELEASE'}
    edit_file = OUT / 'zhixu-edit.json'
    edit_file.write_text(json.dumps(edited))
    push_document(edit_file)
    import_file('zhixu-edit.json')
    adb('shell', 'am', 'force-stop', PKG)
    launch()
    restored = export('zhixu-restored.json')
    assert_source(restored)
    assert 'INDEPENDENT_ONLY_FORMAL_RELEASE' in restored['notes']['calculus-03']
    # Reinstall this same 1.6.1 APK and certificate; this does not test an upgrade from 1.5.0.
    assert 'Success' in adb('install', '-r', str(apk))
    launch()
    updated = export('zhixu-after-reinstall.json')
    assert records(updated) == records(restored)
    PKG = args.source_package
    launch()
    legacy_after = export('legacy-after-independent.json')
    assert records(legacy_after) == records(legacy_before), 'Independent changes modified legacy records'
    snapshot('04-legacy-unchanged')
    PKG = TARGET_PKG
    launch()
    snapshot('03-relaunch-and-reinstall')
    result = {'sha256': expected, 'package': PKG, 'versionName': '1.6.1', 'versionCode': 10,
              'scenario': scenario, 'source': source_evidence,
              'install': True, 'offline_first_launch': True, 'distinct_uids': found,
              'initial_records_empty': True, 'native_json_export_import': True,
              'cancel_and_invalid_import_atomic': True, 'relaunch_and_same_apk_reinstall_preserve_records': True,
              'legacy_records_unchanged': True,
              'legacy_1_5_independent_coexistence_tested': args.source_package == HISTORICAL_PKG,
              'legacy_native_import_normal_exit_reopen': True,
              'boundary': 'Exact production-signed APK driven through public UI; no production-key instrumentation APK.'}
    (OUT / 'verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(json.dumps(result, ensure_ascii=False))
    print('ZHIXU_SIGNED_RELEASE_UI_SUCCESS')


if __name__ == '__main__':
    try:
        main()
    except BaseException:
        if emulator_verified:
            try:
                snapshot('failure')
                (OUT / 'logcat.txt').write_text(adb('logcat', '-d'))
            except Exception:
                pass
        raise
