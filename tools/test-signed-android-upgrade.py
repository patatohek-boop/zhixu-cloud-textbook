"""Test the exact 1.5.0 independent -> 1.6.1 independent APK upgrade.

Run only on a disposable emulator. Seed and inspect synthetic records through
public UI; never instrument a production-signed app or access a personal device.
"""
import argparse
import hashlib
import importlib.util
import json
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('signed_ui', ROOT / 'tools/test-signed-android-ui.py')
ui = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ui)
OLD_HASH = 'b4f92a1342ac5029e2a8a6c599e676ed414246c76d48c80b5dd50a37705734a0'
PIN = 'eac09dcca7192a3a7c99bc67de80d9616c9afa9b986fb107d5ef233e7368f376'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('apk', type=pathlib.Path)
    p.add_argument('--old-apk', type=pathlib.Path, default=ROOT / 'downloads/Zhixu-Independent-1.5.0.apk')
    p.add_argument('--out-dir', type=pathlib.Path, default=pathlib.Path('work/signed-release-ui/upgrade-1.5.0'))
    p.add_argument('--aapt', default='aapt')
    p.add_argument('--apksigner', default='apksigner')
    a = p.parse_args()
    ui.OUT = a.out_dir
    ui.OUT.mkdir(parents=True, exist_ok=True)
    assert not (ui.OUT / 'verification.json').exists(), 'Fresh result directory required'
    ui.FILE_PREFIX = 'upgrade-1.5.0-'
    ui.PKG = ui.TARGET_PKG
    assert ui.PKG == 'app.zhixu.textbook.independent'
    evidence = {}
    for name, apk, version, code in [('old', a.old_apk, '1.5.0', 8), ('new', a.apk, '1.6.1', 10)]:
        digest = hashlib.sha256(apk.read_bytes()).hexdigest()
        assert digest == pathlib.Path(str(apk) + '.sha256').read_text().split()[0]
        if name == 'old':
            assert digest == OLD_HASH
        metadata = subprocess.run([a.aapt, 'dump', 'badging', str(apk)], check=True, capture_output=True, text=True).stdout
        signature = subprocess.run([a.apksigner, 'verify', '--verbose', '--print-certs', str(apk)], check=True, capture_output=True, text=True).stdout
        (ui.OUT / f'{name}-metadata.txt').write_text(metadata)
        (ui.OUT / f'{name}-signature.txt').write_text(signature)
        assert f"name='{ui.PKG}' versionCode='{code}' versionName='{version}'" in metadata
        assert "application-label:'知序·独立版'" in metadata and 'application-debuggable' not in metadata
        assert 'Number of signers: 1' in signature
        assert 'Signer #1 certificate SHA-256 digest: ' + PIN in signature
        assert 'Verified using v2 scheme (APK Signature Scheme v2): true' in signature
        assert 'Verified using v3 scheme (APK Signature Scheme v3): true' in signature
        evidence[name] = {'sha256': digest, 'versionName': version, 'versionCode': code, 'certificate_sha256': PIN}
    assert 'emulator-' in ui.adb('get-serialno')
    assert ui.adb('shell', 'getprop', 'ro.kernel.qemu').strip() == '1'
    ui.emulator_verified = True
    ui.adb('shell', 'svc', 'wifi', 'disable')
    ui.adb('shell', 'svc', 'data', 'disable')
    # Remove only this disposable emulator's previous target fixture before
    # installing the genuine older release. There is NO uninstall/clear below.
    ui.remove_target_if_installed(ui.PKG + '.test')
    ui.remove_target_if_installed(ui.PKG)
    assert 'Success' in ui.adb('install', str(a.old_apk))
    synthetic = {'format': 'zhixu-learning', 'version': 1,
                 'completed': ['calculus-03'], 'bookmarks': ['calculus-04'],
                 'notes': {'calculus-03': 'MIGRATION_SOURCE_NOTE UPGRADE_1_5_PRESERVE 合成记录'},
                 'answers': {'calculus-03': {'choice': 0, 'at': '2026-10-07T00:00:00Z'}}}
    source = ui.OUT / 'old-input.json'
    source.write_text(json.dumps(synthetic, ensure_ascii=False))
    ui.adb('shell', 'mkdir', '-p', '/sdcard/Download')
    ui.push_document(source)
    ui.launch()
    ui.import_file(source.name)
    ui.normal_back_exit()
    ui.launch()
    before = ui.export('before-upgrade.json')
    ui.assert_source(before)
    uid_before = ui.adb('shell', 'pm', 'list', 'packages', '-U', ui.PKG).strip()
    ui.snapshot('01-old-release-records')
    # The actual cross-version operation: -r, same package, same pinned cert,
    # increasing versionCode. Android retains the existing application sandbox.
    assert 'Success' in ui.adb('install', '-r', str(a.apk))
    runtime = ui.adb('shell', 'dumpsys', 'package', ui.PKG)
    (ui.OUT / 'new-runtime-package.txt').write_text(runtime)
    assert 'versionCode=10' in runtime and 'versionName=1.6.1' in runtime
    assert not re.search(r'(?m)^\s*(?:pkgFlags|flags)=.*DEBUGGABLE', runtime)
    assert uid_before == ui.adb('shell', 'pm', 'list', 'packages', '-U', ui.PKG).strip()
    ui.launch()
    after = ui.export('after-upgrade.json')
    assert ui.records(after) == ui.records(before), 'Upgrade lost or changed synthetic learning records'
    ui.normal_back_exit()
    ui.launch()
    reopened = ui.export('after-upgrade-reopen.json')
    assert ui.records(reopened) == ui.records(before)
    ui.snapshot('02-upgraded-release-records')
    result = {'package': ui.PKG, 'sha256': evidence['new']['sha256'], 'old': evidence['old'], 'new': evidence['new'],
              'same_certificate': True, 'same_package': True, 'version_code_increased': True,
              'actual_cross_version_install_r': True, 'uid_preserved': True,
              'records_preserved_after_upgrade_and_normal_reopen': True, 'offline': True,
              'synthetic_data_only': True, 'no_clear_or_uninstall_between_versions': True}
    (ui.OUT / 'verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(json.dumps(result, ensure_ascii=False))
    print('ZHIXU_SIGNED_UPGRADE_SUCCESS')


if __name__ == '__main__':
    try:
        main()
    except BaseException:
        if ui.emulator_verified:
            try:
                ui.snapshot('failure')
                (ui.OUT / 'logcat.txt').write_text(ui.adb('logcat', '-d'))
            except Exception:
                pass
        raise
