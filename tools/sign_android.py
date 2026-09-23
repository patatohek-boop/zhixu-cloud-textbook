"""Sign a locally downloaded unsigned APK. Private signing material never enters GitHub.

Usage: python tools/sign_android.py --apk unsigned.apk --signer apksigner.jar
       --java /path/to/java --keytool /path/to/keytool
       --backup /private/backup/folder --out /path/to/Zhixu.apk
"""
import argparse
import hashlib
import os
from pathlib import Path
import secrets
import subprocess

parser=argparse.ArgumentParser(description=__doc__)
for name in ('apk','signer','java','keytool','backup','out'):
    parser.add_argument('--'+name,required=True)
args=parser.parse_args()
folder=Path(args.backup).resolve()
folder.mkdir(parents=True,exist_ok=True)
keystore=folder/'zhixu-release.p12'
password_file=folder/'signing-password.txt'
if keystore.exists()!=password_file.exists():
    raise SystemExit('Signing backup is incomplete. Recover the matching key and password before continuing.')
if not keystore.exists():
    password=secrets.token_urlsafe(36)
    env=dict(os.environ,ZHIXU_SIGN_PASSWORD=password)
    command=[args.keytool,'-genkeypair','-keystore',str(keystore),'-storetype','PKCS12',
        '-alias','zhixu-release','-keyalg','RSA','-keysize','3072','-sigalg','SHA256withRSA',
        '-validity','10000','-dname','CN=Zhixu Textbook',
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
env=dict(os.environ,ZHIXU_SIGN_PASSWORD=password)
output=Path(args.out).resolve()
output.parent.mkdir(parents=True,exist_ok=True)
subprocess.run([args.java,'-jar',args.signer,'sign','--ks',str(keystore),
    '--ks-key-alias','zhixu-release','--ks-pass','env:ZHIXU_SIGN_PASSWORD',
    '--key-pass','env:ZHIXU_SIGN_PASSWORD','--v4-signing-enabled','false',
    '--out',str(output),args.apk],env=env,check=True,capture_output=True)
verify=subprocess.run([args.java,'-jar',args.signer,'verify','--verbose','--print-certs',str(output)],
    check=True,capture_output=True,text=True)
certificate=folder/'签名证书校验.txt'
certificate.write_text(verify.stdout,encoding='utf-8')
sha=hashlib.sha256(output.read_bytes()).hexdigest()
output.with_suffix('.apk.sha256').write_text(sha+'  '+output.name+'\n',encoding='utf-8')
print('Signed APK:',output.name)
print('SHA-256:',sha)
print(verify.stdout)
