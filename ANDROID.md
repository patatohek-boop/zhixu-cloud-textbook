# 安卓 App

## 1.5.0 独立版

本轮新增 **知序·独立版**（`app.zhixu.textbook.independent`，1.5.0 / versionCode 8）。它使用新的长期发布证书，与旧包 `app.zhixu.textbook` 并存；不能覆盖升级旧包，也不会自动读取或改写旧包记录。默认构建仍是原包，只有显式 `-Pindependent=true` 才构建独立版。签名 APK 已通过正式安装与迁移验收，下载入口位于仓库根目录 [`downloads/`](downloads/README.md)（不进入离线课文资源）；[完整验收](https://github.com/patatohek-boop/zhixu-cloud-textbook/actions/runs/37123439458)与公开校验文件可逐项复核。

迁移：保留旧App → 在旧App“应用菜单”导出学习备份 JSON → 安装独立版 → 在独立版“应用菜单”导入备份 → 核对笔记、收藏、完成状态及答题记录。不同笔记合并保留，导入失败不会覆盖原记录；迁移不复制个性化主题、字号或最后阅读位置。核对前不要卸载旧版或清除数据，导出的 JSON 也请保留。两个包之后各自保存记录，需要再次同步时手动导出/导入。

发布签名只在获批的私有目录生成一次并长期复用。`sign_android.py` 默认缺密钥即失败，只有显式 `--create-key` 才能生成；目录和文件限制为 0700/0600，并固定核对公开证书指纹。私钥和口令不会上传 GitHub、CI 或随 APK 分享。本轮本地保管不等于已完成外部安全备份。

CI 的临时测试证书仅用于非debug release的详细测试与合成JSON并存迁移；正式下载使用本地长期发布签名，并另行安装这份正式APK进行离线首启和系统文件选择器导入验收。二者验证结果分开记录，不发布长期证书签名的测试注入包。

```sh
cd android
./gradlew -Pindependent=true :app:assembleRelease :app:lintRelease
```

## 原包兼容说明

应用名称：知序云教材。包名：`app.zhixu.textbook`。当前源码构建目标：1.5.0（versionCode 8）；正式发布状态以 Releases 为准。适用 Android 8.0 及以上、具有较新 Android System WebView 的设备；请通过应用商店更新网页组件。

## 1.5.0 源码与待签名构建

当前1.5.0源码包含30节起步入口，原78道三档题仍覆盖26节。知识图、原创SVG与交互实验由 `bundle_android.py` 自动打入离线资源，仍不需要网络权限。课文与入口数量见 [`content-stats.json`](site/assets/content-stats.json)；`python tools/test-offline-learning.py` 检查运行资源与网站源码字节一致。

资源打包、安装包编译、模拟器测试和正式签名发布是分别验证的阶段。1.5.0 / versionCode 8 已设置为源码构建目标，但未签名构建不表示正式APK已发布；已安装版本不会自动获得新版内容。正式发布还需完成对应提交的检查，并使用原签名密钥签名，不能以debug包或另一签名冒充可覆盖升级的正式版。

## 安装与使用

正式签名 APK 会放在本仓库的 [Releases](https://github.com/patatohek-boop/zhixu-cloud-textbook/releases) 中。下载后在安卓手机打开 APK，按照系统提示允许本次安装。安装包未经应用商店审核，不应关闭系统安全保护来强行安装；如设备有拦截，可先核对来源与公布的 SHA-256。

- 安装包内置其对应版本的课文、公式字体、示意图、交互实验和逐章修订对照，首次打开也无需联网。已发布APK的实际内容以 Releases 所列版本为准，与当前源码构建目标分开核对。
- 顶部“应用菜单”提供返回书架、备份导入/导出、打印、打开网页版、查看新版安装包与版本说明。
- 学习记录只保存在这个 App 内，与浏览器中的网站记录不自动同步。迁移时先从原位置导出 JSON，再在目标位置导入；不同笔记合并保留。
- 导出和导入使用系统文件选择器，不需要授予整个手机存储的访问权限。
- 打开参考链接或在线新版时使用系统浏览器。App 本身没有联网权限，网页中的外链不能在 App 内执行。
- 升级请覆盖安装相同签名的新版本，不要先卸载。卸载或清除 App 数据会删除本地记录，操作前请导出备份。

## 持续更新

网站更新后立即在网址生效；App 内置的离线课文会在安装新版 APK 后更新，二者不会暗中同步。每次发布新版需增加 `android/app/build.gradle` 中的 `versionCode`，并更新 `versionName`。

GitHub 工作流 `Build Android textbook` 自动构建未经签名的 release 安装包并进行检查。它不包含发布私钥，构建产物中的 debug APK 仅用于模拟器测试，不作为正式下载包。正式发布前，在本机使用原签名密钥完成签名并校验，然后将签名 APK 和 SHA-256 文件上传 Releases。

原包签名应使用原有密钥；独立版签名密钥与口令保存在明确排除版本控制的私有文件夹。务必整体保管，不要公开上传，也不要随 APK 分享。丢失密钥会使原 App 无法用相同身份覆盖升级。

## 构建

使用 JDK 17、Android SDK Platform 37.0 和 Build Tools 36.0.0。已固定 AGP 9.2.1、Gradle 9.4.1（含下载 SHA-256）及 AndroidX WebKit 1.17.0。

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

1.1.0 已发布版本曾运行 Android 15 模拟器的七项核心测试，新增内容版本、修订页面、先修与节内导航检查。运行测试抽查代表性课文，全部正文与公式另有网站构建校验。系统文件选择器与打印面板尚未在各品牌实机上逐一验证。构建和模拟器结果可在对应版本的 GitHub Actions 与发布说明查看；只有全部通过后才提供正式签名包。

1.2.0 新增第八项概念目录跳转与手机整页宽度检查，第九项检查科研路线、47 节机器学习内容和六个新实验的离线打开、参数响应、重置及手机宽度，并保存概念段落和研究实验截图。新增测试代码不等于已经运行通过；本轮结果应另行查看构建报告。

正式发布前检查权限数为 0、调试标记关闭，全部实际离线资源与发布源码逐项一致（网站专用 `.nojekyll` 不进入 APK）。新版本继续使用原有 RSA 3072 位签名密钥，核对 APK v2/v3 签名及证书 SHA-256 后，才发布安装包和公开校验文件；私钥及口令不在仓库中。

原包历史签名证书 SHA-256：`3da7385ede7d60fd7135df028aff3814b8b3b42f0f10576b576ada77dad5ca20`。升级前先导出备份，然后覆盖安装，不要卸载旧版。原有 182 个课文编号与学习记录存储键均保留。
