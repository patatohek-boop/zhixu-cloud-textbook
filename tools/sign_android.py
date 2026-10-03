"""Sign a locally downloaded unsigned APK. Private signing material never enters GitHub.

Usage: python tools/sign_android.py --apk unsigned.apk --signer apksigner.jar
       --java /path/to/java --keytool /path/to/keytool
       --backup /private/backup/folder --out /path/to/Zhixu.apk
"""
import argparse
import hashlib
import os
import re
from pathlib import Path
import secrets
import subprocess


def secure_windows_backup(folder, owner_sid=None):
    """Replace and verify every backup DACL before reading or writing secrets.

    Keep the file owner/group intact. Only the current process account, SYSTEM,
    and the explicitly supplied human owner may access the dedicated folder.
    icacls /grant:r alone would leave unrelated explicit ACEs in place.
    """
    if owner_sid and not re.fullmatch(r'S-1-5-(?:[0-9]+-)*[0-9]+', owner_sid):
        raise SystemExit('Invalid Windows owner SID.')
    script = r'''
$ErrorActionPreference = 'Stop'
# A Python process launched by PowerShell 7 can inherit its module search path.
# Load the Windows PowerShell security module explicitly for this 5.1 host.
Import-Module (Join-Path $PSHOME 'Modules/Microsoft.PowerShell.Security/Microsoft.PowerShell.Security.psd1') -Force
$backupPath = $env:ZHIXU_SIGN_ACL_PATH
$processSid = [System.Security.Principal.WindowsIdentity]::GetCurrent().User.Value
$allowedSids = @($processSid, 'S-1-5-18')
if ($env:ZHIXU_SIGN_OWNER_SID) { $allowedSids += $env:ZHIXU_SIGN_OWNER_SID }
$allowedSids = @($allowedSids | Select-Object -Unique)
$directory = Get-Item -LiteralPath $backupPath -Force
if (-not $directory.PSIsContainer) { throw 'Signing backup is not a directory.' }
$entries = @(Get-ChildItem -LiteralPath $backupPath -Force)
# A signing backup is a flat directory. Do not traverse junctions or apply
# permissions to unrelated subdirectories supplied by a caller.
$targets = @($directory) + $entries
foreach ($target in $targets) {
    if (($target.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
        throw 'Signing backup must not contain reparse points.'
    }
}
if (@($entries | Where-Object { $_.PSIsContainer }).Count) {
    throw 'Signing backup must contain only regular files.'
}
foreach ($target in $targets) {
    $previous = Get-Acl -LiteralPath $target.FullName
    # Build only the DACL, so Set-Acl does not attempt to rewrite an existing
    # owner/group or SACL and require SeSecurityPrivilege on protected files.
    if ($target.PSIsContainer) {
        $acl = [System.Security.AccessControl.DirectorySecurity]::new()
    } else {
        $acl = [System.Security.AccessControl.FileSecurity]::new()
    }
    $acl.SetAccessRuleProtection($true, $false)
    $inheritance = [System.Security.AccessControl.InheritanceFlags]::None
    if ($target.PSIsContainer) {
        $inheritance = [System.Security.AccessControl.InheritanceFlags]::ContainerInherit -bor [System.Security.AccessControl.InheritanceFlags]::ObjectInherit
    }
    foreach ($sid in $allowedSids) {
        $identity = [System.Security.Principal.SecurityIdentifier]::new($sid)
        $rule = [System.Security.AccessControl.FileSystemAccessRule]::new(
            $identity, [System.Security.AccessControl.FileSystemRights]::FullControl,
            $inheritance, [System.Security.AccessControl.PropagationFlags]::None,
            [System.Security.AccessControl.AccessControlType]::Allow)
        $acl.AddAccessRule($rule)
    }
    try {
        Set-Acl -LiteralPath $target.FullName -AclObject $acl
    } catch [System.Security.AccessControl.PrivilegeNotHeldException] {
        # Some restricted Windows tokens cannot use Set-Acl's full-descriptor
        # path, which also requests SACL privileges. This fresh object modifies
        # only the DACL; the .NET API persists only that modified section.
        # No privilege is acquired and the existing owner/group/SACL stay intact.
        if ($target.PSIsContainer) {
            [System.IO.Directory]::SetAccessControl($target.FullName, $acl)
        } else {
            [System.IO.File]::SetAccessControl($target.FullName, $acl)
        }
    }
    $actual = Get-Acl -LiteralPath $target.FullName
    if ($actual.Owner -ne $previous.Owner -or $actual.Group -ne $previous.Group) {
        throw 'Signing backup owner/group unexpectedly changed.'
    }
    $rules = @($actual.GetAccessRules($true, $true, [System.Security.Principal.SecurityIdentifier]))
    if (-not $actual.AreAccessRulesProtected -or $rules.Count -ne $allowedSids.Count) {
        throw 'Signing backup DACL was not replaced exactly.'
    }
    foreach ($sid in $allowedSids) {
        $matches = @($rules | Where-Object { $_.IdentityReference.Value -eq $sid })
        if ($matches.Count -ne 1) { throw 'Signing backup owner access is missing or duplicated.' }
        $rule = $matches[0]
        if ($rule.IsInherited -or $rule.AccessControlType -ne [System.Security.AccessControl.AccessControlType]::Allow -or
            $rule.FileSystemRights -ne [System.Security.AccessControl.FileSystemRights]::FullControl -or
            $rule.InheritanceFlags -ne $inheritance -or
            $rule.PropagationFlags -ne [System.Security.AccessControl.PropagationFlags]::None) {
            throw 'Signing backup contains an unexpected access rule.'
        }
    }
}
'''
    acl_env = dict(os.environ, ZHIXU_SIGN_ACL_PATH=str(folder),
                   ZHIXU_SIGN_OWNER_SID=owner_sid or '')
    acl_env.pop('ZHIXU_SIGN_PASSWORD', None)
    powershell = Path(os.environ.get('SystemRoot', r'C:\Windows')) / 'System32/WindowsPowerShell/v1.0/powershell.exe'
    result = subprocess.run([str(powershell), '-NoProfile', '-NonInteractive', '-Command', script],
                            env=acl_env, capture_output=True)
    if result.returncode:
        # Do not echo external command output or any credential-bearing environment.
        raise SystemExit('Could not enforce the exact signing-backup ACL; signing has stopped.')

parser=argparse.ArgumentParser(description=__doc__)
for name in ('apk','signer','java','keytool','backup','out'):
    parser.add_argument('--'+name,required=True)
parser.add_argument('--create-key', action='store_true', help='Explicitly authorize creating a new release identity only when absent')
parser.add_argument('--owner-sid', help='Windows SID of the human backup owner when the build runs under a sandbox account')
args=parser.parse_args()
os.umask(0o077)
requested_folder=Path(args.backup).absolute()
if any(p.is_symlink() for p in (requested_folder, *requested_folder.parents)):
    raise SystemExit('Signing folder and its parents must not be symlinks.')
folder=requested_folder.resolve()
folder.mkdir(parents=True,exist_ok=True,mode=0o700)
os.chmod(folder,0o700)
if os.name == 'nt':
    secure_windows_backup(folder, args.owner_sid)

root=Path(__file__).resolve().parents[1]
if args.create_key and folder != root/'.private-signing/reader':
    raise SystemExit('New key creation is restricted to this project reader-edition private directory.')
if folder.is_relative_to(root):
    ignored=subprocess.run(['git','check-ignore','--quiet',str(folder/'signing-password.txt')],cwd=root)
    if ignored.returncode != 0:
        raise SystemExit('Signing folder must be explicitly gitignored before creating or reading secrets.')
keystore=folder/'zhixu-release.p12'
password_file=folder/'signing-password.txt'
cert_pin=folder/'certificate-sha256.txt'
if any(p.is_symlink() for p in folder.iterdir()):
    raise SystemExit('Signing files must not be symlinks.')
if keystore.exists()!=password_file.exists():
    raise SystemExit('Signing backup is incomplete. Recover the matching key and password before continuing.')
created_new = not keystore.exists()
if created_new:
    if not args.create_key:
        raise SystemExit('No key exists. Explicit --create-key approval is required for a new release identity.')
    password=secrets.token_urlsafe(36)
    env=dict(os.environ,ZHIXU_SIGN_PASSWORD=password)
    command=[args.keytool,'-genkeypair','-keystore',str(keystore),'-storetype','PKCS12',
        '-alias','zhixu-release','-keyalg','RSA','-keysize','3072','-sigalg','SHA256withRSA',
        '-validity','10000','-dname','CN=Zhixu Reader',
        '-storepass:env','ZHIXU_SIGN_PASSWORD','-keypass:env','ZHIXU_SIGN_PASSWORD']
    subprocess.run(command,env=env,check=True,capture_output=True)
    password_file.write_text(password+'\n',encoding='utf-8')
    (folder/'请保管好签名备份.txt').write_text(
        '此文件夹只保存在本机，不属于公开教材仓库。\n'
        'zhixu-release.p12 是 APK 升级签名密钥，signing-password.txt 是对应口令。\n'
        '请整体保存到安全的备份位置。不要上传 GitHub、不要随 APK 分享。\n'
        '后续新版必须使用同一个密钥，才能覆盖安装并保留学习记录。\n'
        '如果密钥遗失，只能更换签名或应用包名；原安装不能直接覆盖升级。\n',encoding='utf-8')
else:
    password=password_file.read_text(encoding='utf-8').strip()
for private_file in folder.iterdir():
    if private_file.is_symlink(): raise SystemExit('Signing folder must not contain symlinks.')
    if private_file.is_file(): os.chmod(private_file,0o600)
env=dict(os.environ,ZHIXU_SIGN_PASSWORD=password)
public_cert=subprocess.run([args.keytool,'-exportcert','-keystore',str(keystore),'-alias','zhixu-release','-storepass:env','ZHIXU_SIGN_PASSWORD'],env=env,check=True,capture_output=True).stdout
cert_sha=hashlib.sha256(public_cert).hexdigest()
if created_new:
    cert_pin.write_text(cert_sha+'\n',encoding='utf-8')
elif not cert_pin.is_file() or cert_pin.read_text(encoding='utf-8').strip()!=cert_sha:
    raise SystemExit('Public certificate pin missing or mismatched. Do not replace the release identity.')
output=Path(args.out).resolve()
output.parent.mkdir(parents=True,exist_ok=True)
subprocess.run([args.java,'-jar',args.signer,'sign','--ks',str(keystore),
    '--ks-key-alias','zhixu-release','--ks-pass','env:ZHIXU_SIGN_PASSWORD',
    '--key-pass','env:ZHIXU_SIGN_PASSWORD','--v4-signing-enabled','false',
    '--out',str(output),args.apk],env=env,check=True,capture_output=True)
verify=subprocess.run([args.java,'-jar',args.signer,'verify','--verbose','--print-certs',str(output)],
    check=True,capture_output=True,text=True)
if ('Signer #1 certificate SHA-256 digest: '+cert_sha) not in verify.stdout:
    raise SystemExit('APK certificate does not match the pinned release identity.')
certificate=folder/'签名证书校验.txt'
certificate.write_text(verify.stdout,encoding='utf-8')
sha=hashlib.sha256(output.read_bytes()).hexdigest()
output.with_suffix('.apk.sha256').write_text(sha+'  '+output.name+'\n',encoding='utf-8')
os.chmod(certificate,0o600)
if os.name == 'nt':
    # Check newly created key, password, pin and certificate files as well.
    secure_windows_backup(folder, args.owner_sid)
print('Signed APK:',output.name)
print('SHA-256:',sha)
print(verify.stdout)
