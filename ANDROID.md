# 安卓 App

应用名称：知序云教材。包名：`app.zhixu.textbook`。初版：1.0.0。适用 Android 8.0 及以上、具有可正常运行的 Android System WebView 的设备。

## 安装与使用

正式签名 APK 会放在本仓库的 [Releases](https://github.com/patatohek-boop/zhixu-cloud-textbook/releases) 中。下载后在安卓手机打开 APK，按照系统提示允许本次安装。安装包未经应用商店审核，不应关闭系统安全保护来强行安装；如设备有拦截，可先核对来源与公布的 SHA-256。

- 全部 182 节教材、公式字体、22 张示意图和 11 个实验随包内置，首次打开也无需联网。
- 顶部“应用菜单”提供返回书架、备份导入/导出、打印、打开网页版、下载新版与版本说明。
- 学习记录只保存在这个 App 内，与浏览器中的网站记录不自动同步。迁移时先从原位置导出 JSON，再在目标位置导入；不同笔记合并保留。
- 导出和导入使用系统文件选择器，不需要授予整个手机存储的访问权限。
- 打开参考链接或在线新版时使用系统浏览器。App 本身没有联网权限，网页中的外链不能在 App 内执行。
- 升级请覆盖安装相同签名的新版本，不要先卸载。卸载或清除 App 数据会删除本地记录，操作前请导出备份。

## 持续更新

网站更新后立即在网址生效；App 内置的离线课文会在安装新版 APK 后更新，二者不会暗中同步。每次发布新版需增加 `android/app/build.gradle` 中的 `versionCode`，并更新 `versionName`。

GitHub 工作流 `Build Android textbook` 自动构建未经签名的 release 安装包并进行检查。它不包含发布私钥，构建产物中的 debug APK 仅用于模拟器测试，不作为正式下载包。正式发布前，在本机使用原签名密钥完成签名并校验，然后将签名 APK 和 SHA-256 文件上传 Releases。

初次生成的签名密钥与口令仅保存在仓库外、本机的独立签名备份文件夹。务必整体保管，不要公开上传，也不要随 APK 分享。丢失密钥会使原 App 无法用相同身份覆盖升级。

## 构建

使用 JDK 17、Android SDK Platform 37 和 Build Tools 36.0.0。已固定 AGP 9.2.1、Gradle 9.4.1（含下载 SHA-256）及 AndroidX WebKit 1.17.0。

```sh
python tools/build.py
node tools/validate.cjs
node tools/test-learning-state.cjs
python tools/security_check.py
cd android
./gradlew :app:assembleRelease :app:lintRelease
```

`tools/bundle_android.py` 将网站资源复制到生成目录，并仅在 APK 中加载 Android 适配脚本；源码网站不依赖原生环境。不要手动修改 `android/app/build/` 内的生成文件。

本机签名工具见 `python tools/sign_android.py --help`，需要已构建的 release APK、官方 SDK 的 `apksigner.jar`、Java 和私有签名备份目录。工具不会联网或将私钥上传到 GitHub。

## 安全边界

本 App 无账号、广告、埋点、网络/定位/相册/麦克风权限；使用本地 HTTPS 虚拟来源加载内置资源，关闭 file/content 页面访问及混合内容，不暴露 JavaScriptInterface。仅允许可信本地课文在用户点击时请求导入、导出与打印；文件文本经过大小和格式校验，并通过安全引用传入网页，不被当作代码执行。内置静态资源仍遵守网页的 CSP 与 HTML 净化策略。

笔记及导出备份未经应用层加密；Android 应用沙箱不等同于保险箱，请勿写入密码或敏感资料。自动云备份/设备迁移已禁用，以明确的 JSON 导出作为迁移途径。设备系统或 WebView 存在漏洞、被 root 或受到恶意软件控制时，App 不能提供额外安全保证。

## 验证范围

发布构建包含 Android Lint 与平台 Instrumentation 测试：权限、可信 URL 边界、课文和公式加载、异常实验路由、备份导入/导出接口、注入文本与失败原子性、返回保存及重启后持久化。模拟器通过不代表已在全部手机品牌与文件管理器上验证。
