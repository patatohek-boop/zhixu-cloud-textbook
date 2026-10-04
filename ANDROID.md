# 安卓 App

## 知序 1.6.0

应用名为 **知序**，包名 `app.zhixu.textbook.reader`，版本 1.6.0 / versionCode 9。它与 **知序·独立版 1.5.0**（`app.zhixu.textbook.independent`）及更早原包（`app.zhixu.textbook`）并存，不能覆盖它们，也不会自动读取旧应用的学习记录。

[下载知序 1.6.0](downloads/README.md)。该页面提供正式签名 APK、SHA-256、证书指纹与[本次验收记录](https://github.com/patatohek-boop/zhixu-cloud-textbook/actions/runs/37166324383)。请使用本次发布的安装包；历史版本的检查结果只对应各自版本。

七科 253 节、课文 ID、原有练习及交互内容保留。网站与离线 App 使用同一份教材源文件，主入口为“知识树、知识联系、关于”，定义与主干证明在连续正文中直接呈现，练习解析可以展开。内容统计见 `site/assets/content-stats.json`，安装包信息见[下载说明](downloads/README.md)。

## 安装与迁移

适用于 Android 8.0 及以上、具备较新 Android System WebView 的设备。

1. 保留旧应用，在其“应用菜单 → 导出学习备份”保存 JSON。
2. 从[下载说明](downloads/README.md)下载 1.6.0 APK，打开文件，按 Android 提示允许该来源安装应用。
3. 打开名称为“知序”的新应用，在“应用菜单 → 导入备份”选择 JSON。
4. 核对笔记、收藏、完成状态及答题记录。不同笔记采用合并规则；主题、字号和最后阅读位置不随备份迁移。
5. 核对之前不要卸载旧版或清除旧版数据。核对后也应保留 JSON；两个应用仍各自保存记录，不会自动同步。

JSON 未加密，不要公开上传。卸载或清除某个应用的数据会删除该应用的本地记录。本次正式签名包的实际检查项目见[验收记录](https://github.com/patatohek-boop/zhixu-cloud-textbook/actions/runs/37166324383)；迁移自己的记录后，仍请按上面的步骤逐项核对。

## 离线阅读与更新

安装包内置课文、公式组件、字体、图示和交互实验，首次打开也不依赖运行时网络。顶部应用菜单提供备份导入/导出、打印、打开网页版和查看新版安装包；外部链接交给系统浏览器。导入与导出使用系统文件选择器，不需要整个手机存储的访问权限。

网站在部署后更新，App 在安装新版 APK 后更新内置教材。新应用今后的覆盖升级须保持 `app.zhixu.textbook.reader` 包名及同一发布证书，并增加 versionCode。不能将另一包名或另一签名的安装包冒称覆盖升级。

## 构建和签名

本轮新应用仍使用显式构建开关 `-Pindependent=true`；其输出包名已由 1.5.0 的 independent 改为 reader。不带该参数构建的是原包身份，不能作为本轮“知序”的正式下载。

使用 JDK 17、Android SDK Platform 37.0、Build Tools 36.0.0；仓库固定 AGP 9.2.1、Gradle 9.4.1 及 AndroidX WebKit 1.17.0。构建示例：

```sh
python tools/build.py
node tools/validate.cjs
node tools/test-learning-state.cjs
python tools/security_check.py
cd android
./gradlew -Pindependent=true :app:assembleRelease :app:lintRelease
```

`tools/bundle_android.py` 将网站资源复制到生成目录，并加入 Android 适配脚本。不要修改 `android/app/build/` 中的生成文件。`python tools/test-offline-learning.py` 用于检查离线资源与网站源码的一致性。

本版本使用独立的长期发布证书，以后更新须复用同一证书。签名材料由维护者在本机受限目录保管，本机备份位于 `outputs/知序签名备份/`，不随公开仓库发布；这不等于已经有设备之外的备份。私钥与口令不上传 GitHub、CI 或 APK。签名工具见 `python tools/sign_android.py --help`：默认缺少密钥时失败，只有明确使用 `--create-key` 才创建密钥。

CI 的未签名 release 或临时测试签名用于构建和测试；正式下载须另行使用长期证书签名、核对签名与证书指纹，并验证实际签名 APK。测试注入包和 debug 包不作为正式下载。

## 安全边界

应用按无账号、广告、埋点及设备权限的离线阅读器设计。本地 HTTPS 虚拟来源加载内置资源，关闭 file/content 页面访问和混合内容，不暴露 JavaScriptInterface。仅允许可信本地页面在用户操作时请求导入、导出或打印；导入文本需通过大小、格式与存储检查。课文仍使用 CSP 与 HTML 净化。

本次正式安装包已核对包名、版本、零权限、debug 标记关闭、APK v2/v3 签名及内置资源与发布源码一致性。结果见[下载校验信息](downloads/README.md)与[本次验收记录](https://github.com/patatohek-boop/zhixu-cloud-textbook/actions/runs/37166324383)。

笔记及 JSON 未作应用层加密。自动云备份/设备迁移禁用，以用户明确操作的 JSON 导出作为迁移方式。系统或 WebView 的漏洞、已被控制的设备不在应用沙箱可以消除的风险范围内。

## 验证范围

网站内容与公式、Android 编译与 Lint、临时测试签名包，以及正式签名 APK 的实际检查分别记录。正式包的安装、离线阅读、迁移和持久化覆盖范围，以[本次验收记录](https://github.com/patatohek-boop/zhixu-cloud-textbook/actions/runs/37166324383)列出的项目为准。模拟器测试不表示已经覆盖所有手机品牌、文件管理器或任意强杀/断电时序。

1.6.0 的安装包、校验摘要与对应构建来源见[下载说明](downloads/README.md)。

## 历史版本

- **1.5.0 独立版**：应用名“知序·独立版”，包名 `app.zhixu.textbook.independent`，versionCode 8；[历史 Android 15 验收](https://github.com/patatohek-boop/zhixu-cloud-textbook/actions/runs/37123439458)。该版本使用独立长期证书，与原包并存。历史 APK 和摘要见[下载说明的历史版本](downloads/README.md)。该验收只对应 1.5.0。
- **原包**：应用名“知序云教材”，包名 `app.zhixu.textbook`，历史发布见 [Releases](https://github.com/patatohek-boop/zhixu-cloud-textbook/releases)。原包历史证书 SHA-256 为 `3da7385ede7d60fd7135df028aff3814b8b3b42f0f10576b576ada77dad5ca20`。
- **1.1.0 / 1.2.0 历史检查**：曾逐步增加内容版本、先修/节内目录、手机宽度、科研路线及交互实验的模拟器检查。其运行范围见对应版本的 Actions 与发布说明，不扩展为 1.6.0 的验收结论。

各次内容变化见 [CHANGELOG.md](CHANGELOG.md)。历史签名不能混用于不同应用的覆盖升级。
