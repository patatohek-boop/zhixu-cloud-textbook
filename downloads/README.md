# 知序 1.6.0

> 网站和应用源码的 1.6.1 五项勘误已准备；正式签名的 1.6.1 升级包尚未发布。本页当前可下载安装的仍为 1.6.0，未包含本次勘误；下列旧包链接与校验信息保持有效。

应用名：**知序**；包名：`app.zhixu.textbook.reader`；版本：1.6.0 / versionCode 9。新版使用新的长期发布证书，与“知序·独立版 1.5.0”并存，不能覆盖它，也不会自动读取或更改旧版记录。

**正式版本：知序 1.6.0，适用于 Android 8.0 及以上。** 1.6.0 发布时网站与 App 使用同一版教材；本页校验信息仅对应下方的正式安装包。

**[下载知序 1.6.0 APK](https://raw.githubusercontent.com/patatohek-boop/zhixu-cloud-textbook/main/downloads/Zhixu-1.6.0.apk)**

下载后打开文件，按 Android 提示安装。新版名称为“知序”，与旧版分别保存学习记录；迁移步骤见下方。

七科 253 节继续保留；主入口整理为“知识树、知识联系、关于”。主干定义、解释、证明和推导组成连续正文，练习解析可展开。原有交互实验、图解、AI × 传热与实验、流动换热仿真内容保留。

## 安装和迁移

1. 保留 1.5.0 或更早的旧应用，在旧应用“应用菜单 → 导出学习备份”保存 JSON。
2. 下载上方 1.6.0 APK，打开文件，按 Android 提示允许该来源安装应用。
3. 打开名称为“知序”的新应用，选择“应用菜单 → 导入备份”，导入刚才的 JSON。
4. 核对完成状态、收藏、笔记和答题记录；不同笔记合并保留，主题、字号及最后阅读位置不随导入替换。
5. 核对前不要卸载或清除旧版。保留 JSON，之后两个应用各自存储，需再次手动导入/导出才能同步。

JSON 未加密，不要上传公开仓库。1.6.0 今后的升级需使用同一包名与发布证书；维护者的签名保管说明见 [ANDROID.md](../ANDROID.md)。

## 校验与验收记录

- 安装包：`Zhixu-1.6.0.apk`（3123445 字节）。
- 应用：知序 1.6.0；包名 `app.zhixu.textbook.reader`；versionCode 9。
- APK SHA-256：`ed7ff3bad991e391c1552c62ca6bc3670fd2ac50e905192eb257c981ea626963`。
- 发布证书 SHA-256：`f1b7e619da6c7b2dbbef27fe3c9f61f6d574352b3d83fed3e70df769879e12fe`。
- [本次正式签名包验收](https://github.com/patatohek-boop/zhixu-cloud-textbook/actions/runs/37166324383)。
- 对应源码提交：`c085ea46ee39d7a85c5dd977ba1fd0ad15bb54b6`。

本次正式包已核对零权限、debug 标记关闭、v2/v3 签名及内置资源一致性。安装、离线首启、与旧版并存、JSON 迁移和持久化等实际测试范围见上方验收记录。模拟器通过不代表全部手机品牌实测，也不保证任意强杀或断电时序。

## 历史：知序·独立版 1.5.0

- [历史 1.5.0 APK](./Zhixu-Independent-1.5.0.apk?raw=true)，Android 8.0+。
- [历史 Android 15 完整验收](https://github.com/patatohek-boop/zhixu-cloud-textbook/actions/runs/37123439458)。
- 应用名“知序·独立版”，包名 `app.zhixu.textbook.independent`，versionCode 8；与原包 `app.zhixu.textbook` 并存。
- 历史 APK SHA-256：`b4f92a1342ac5029e2a8a6c599e676ed414246c76d48c80b5dd50a37705734a0`。
- 历史独立版证书 SHA-256：`eac09dcca7192a3a7c99bc67de80d9616c9afa9b986fb107d5ef233e7368f376`。

1.5.0 的记录显示：正式签名 APK 的离线首启、独立 UID、初始空记录、零权限、153 项资源一致性，以及经系统文件选择器的合成 JSON 迁移、取消/坏 JSON 后原记录不变、重启和同证书覆盖后的持久化检查通过。临时测试签名的非 debug release 另有 14 项正文/UI/安全检查。这些是隔离模拟器中的合成数据结果，没有操作用户设备或真实记录。

上述记录仅对应 1.5.0，不能作为 1.6.0 的验收依据，也不保证任意强杀、断电或所有品牌设备。当前版本的安装与迁移说明见 [ANDROID.md](../ANDROID.md)。