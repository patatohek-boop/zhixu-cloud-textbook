# 发布前 Android 并存与迁移验收边界 · 2026-10-04

本轮检查与修改限于测试脚本、CI 工作流和公开历史证书指纹，没有修改 App 源码、包名或签名工具，没有读取私钥或口令，没有创建密钥，没有改写历史 APK，也没有操作用户手机。**实际 Android 模拟器中的两场景验收尚未执行**；本报告不能作为 1.6.0 安装成功的证据。

## 核实的版本身份

| 对象 | 包名 | 版本 | 本轮核实方式 |
| --- | --- | --- | --- |
| 新版知序 | `app.zhixu.textbook.reader` | 1.6.0 / code 9 | `android/app/build.gradle` 的 `-Pindependent=true` 分支、应用名资源及最终 APK 校验器；正式 APK 尚待生成与验收 |
| 历史知序·独立版 | `app.zhixu.textbook.independent` | 1.5.0 / code 8 | 对仓库现有历史 APK 实际运行 `aapt dump badging` 及 `apksigner verify --verbose --print-certs` |
| 原包测试样本 | `app.zhixu.textbook` | 本次源码构建的 1.6.0 / code 9 | CI 不带 `independent` 参数编译；这是旧包身份的兼容性样本，不能冒称历史 1.5.0 APK |

历史 APK 的实际 SHA-256 为 `b4f92a1342ac5029e2a8a6c599e676ed414246c76d48c80b5dd50a37705734a0`，与原有 `.apk.sha256` 文件一致。实际验证 v2、v3 签名均有效，单一签名者的公开证书 SHA-256 为 `eac09dcca7192a3a7c99bc67de80d9616c9afa9b986fb107d5ef233e7368f376`。上述检查使用本地 JDK 17；机器默认 Java 9 不适用于本轮签名工具。

新版与两个源包的安装身份均不同；Manifest 未声明共享 UID。包名区分提供并存的设计条件，仍需实际安装和独立 UID 检查证实。1.5.0 到 1.6.0 是两个应用间的显式 JSON 迁移，不是覆盖升级；测试中的覆盖行为仅为**同一个 1.6.0 APK、同一个证书重新安装**。

## 原验收的缺口与本轮修改

此前 CI 的所谓 legacy APK 来自本次源码的原包分支；正式 UI 脚本也只在原包 `app.zhixu.textbook` 与新版之间搬运合成数据。它没有安装真实 1.5.0 独立版，脚本结果中的 `legacy_1_5_independent_coexistence_tested` 因而一直为 `false`。本轮保留这组原包检查，另加真实旧独立版场景。

修改范围：

- [正式 APK 公有界面测试](../tools/test-signed-android-ui.py)：加入 `--source-package`、`--source-apk`、`--out-dir` 和 Android 工具路径参数。原包场景仍为默认值。1.5.0 场景先验证固定历史 APK 摘要、sidecar、包名、版本、非 debug、独立历史证书及 v2/v3，再普通安装该历史文件；不能用重打包 APK 代替。旧源应用不卸载、不清数据；测试只在确认 `emulator-…` 且 `ro.kernel.qemu=1` 后操作隔离模拟器。只允许卸载新版 reader 及其测试包，并先检查是否已安装，避免第二组场景因测试包已不存在而失败。
- [工作流](../.github/workflows/android-independent.yml)：原来的 14 项临时签名非 debug UI/安全检查、合成记录 instrumentation 检查全部保留。正式签名 APK 校验之后，依次执行原包与真实 1.5.0 两组公有界面测试，并分别保存证据。CI 权限保持 `contents: read`。
- [历史证书指纹](../downloads/1.5.0-certificate-sha256.txt)：新增版本固定的公开指纹，避免发布新版时改写 `downloads/certificate-sha256.txt` 后混用历史签名身份。工作流另检查新版公开指纹与历史指纹不同；实际签名有效性仍由 `apksigner` 核验。

两组场景均保留以下检查：源应用通过原生菜单导入合成记录，正常返回并重开后导出；新版离线首次启动及空记录；各自独立 UID；通过系统文件选择器导入源应用实际导出的 JSON；完成状态、收藏、笔记与答题记录；取消及坏 JSON 不改变原记录；新增笔记、重开及同 APK 重装后的持久化；再次打开源应用确认记录未被新版改动。

两组设备端文件分别使用 `original-package-` 与 `independent-1.5.0-` 前缀，避免系统文件选择器重名保存后误读前次结果；每次导出前还拒绝已存在的同名文件。复跑应使用新的隔离模拟器，不应清除用户数据来迁就测试。`verification.json` 仅在整组检查结束后写出；真实 1.5.0 场景才将 `legacy_1_5_independent_coexistence_tested` 记为 `true`，同时记录历史 APK、证书、版本和双方 UID。

## 发布阶段不能静默跳过

首次构建尚无正式 APK 时，普通 CI 仍允许跳过正式签名包测试，以便取得未签名产物。**只要待验收代码树已包含 `downloads/Zhixu-1.6.0.apk`，PR 和推送触发的同一工作流就自动强制检查两组正式包迁移结果**，不依赖手动启动或本机 GitHub CLI 登录。也可手动启动并把 `require_production` 设为 `true`；该选项即使 APK 缺失也会要求验收并报错。例如：

```sh
gh workflow run android-independent.yml --ref RELEASE_VALIDATION_BRANCH -f require_production=true
```

`RELEASE_VALIDATION_BRANCH` 应替换为实际待验收分支；本轮没有运行这条远程命令。

显式 `require_production=true` 会先要求新版和历史 APK、摘要及两个公开证书指纹文件存在；自动和显式两种正式验收都会在末尾检查两份结果是否对应本次新版 APK 的 SHA-256，源包是否正确，以及全部迁移/持久化标志。正式验收中只有原包结果、历史场景未证实或结果对应另一 APK 时都会失败；显式要求正式验收但 APK 缺失也会失败。发布者必须同时核对整个作业成功与 `ZHIXU_PRODUCTION_RELEASE_ACCEPTANCE_SUCCESS`，不能只看普通构建作业为绿色。

两组证据同属 `production-signed-ui` artifact，按目录明确分开：

- `work/signed-release-ui/original-package/`：原包身份样本；
- `work/signed-release-ui/independent-1.5.0/`：真实历史 APK，并包含其 metadata、签名验证和运行包信息；
- 两组各自的 `verification.json`、截图、界面树、合成 JSON，及 `work/production-ui-original.txt` / `work/production-ui-independent-1.5.0.txt` 日志。

## 本轮实际执行的验证

1. Python 编译及 CLI 帮助解析通过；工作流 YAML 可以正常解析。工作流内最终发布门槛的 Python 代码已单独编译。未运行 GitHub Actions 或把 YAML 解析等同于远程 CI 成功。
2. 在本机调用新增 `verify_historical_source`，只读核验仓库历史 1.5.0 APK；包名、版本、标签、非 debug、固定摘要及独立证书、v2/v3 全部通过。
3. 本地隔离测试架执行 25 项脚本与工作流门槛检查，通过：参数错误拒绝、三包 UID 正确筛选、相同 UID/缺失源包拒绝、模拟器确认前拒绝卸载、禁止卸载两个源包、测试包缺失时不重复卸载、两组文件名分离、已存在导出拒绝，以及发布结果缺包/缺组/错误历史标志/不同 APK 摘要拒绝。最终门槛使用明确标为测试样本的普通文件和合成结果验证，不是可安装 APK，也不冒称 UI 验收。可复核本地结果 `work/android-boundary-static/checks.json`；该文件不属于公开教材资源。

**尚需主发布任务完成：** 生成并签名当前 1.6.0 APK，归档历史 1.5.0 验收记录，写入新版摘要和公开证书，通过含正式 APK 的 PR/推送或 `require_production=true` 启动工作流，在 Android 15 隔离模拟器上真正执行两组迁移与原有全部 UI 检查，再据其结果更新发布状态。即使模拟器通过，也不代表所有手机品牌、文件管理器、任意断电或强杀时序已被覆盖。

## 独立交叉复核补记

复核依据是归档提交 `da07805e018e32e091476d13a94b19c64c4b3a9b` 的源码压缩包（SHA-256 `009d23921d10e971c8df62df064d46db334d5b7ba51f06956f9708bc5a09f89f`），以及本次对应源码。实际阅读并比对了旧版与新版的 `MainActivity.java`、`strings.xml`、Manifest、Gradle 包名配置、`app.js` 的导出/导入/返回行为和完整 `learning-state.js`。旧版独立应用的启动类仍为 `app.zhixu.textbook.MainActivity`；原生“应用菜单”“导出学习备份”“导入备份（合并记录）”文字相同。旧版标题是“知序·独立版 · 离线教材”，新版标题是“知序 · 离线教材”。首页菜单虽然改名，迁移测试不依赖它，也不依据桌面应用名称决定卸载对象。

四类备份字段 `completed`、`bookmarks`、`notes`、`answers` 及 `zhixu-learning` / version 1 格式兼容；答案的正确性按课文重新计算。已用真实旧版、新版的两套 `LearningState` 代码与课程数据实际执行合成记录导入：253 个课文 ID 顺序一致，迁移样例 calculus-03 的选项和答案不变；原包样本已有笔记会合并，真实旧独立版从空记录开始。这里只验证 JavaScript 状态处理，不代表系统文件选择器已运行。

独立复核修复了以下实际测试缺口，范围仅为测试与工作流：

1. 单次 Back 可能只关闭页面浮层或退回 WebView 历史，不能证明源应用已正常退出。现按系统报告的前台包名最多按 12 次；仅目标源包当前在前台时发送 Back，切到其他应用立即停止，不能识别前台时拒绝输入。
2. 两场景共用 Downloads，第二场景文件可能在可见列表之外。文件选择现限于 DocumentsUI 节点、精确文件名，在两个方向各最多检查 12 次；列表不变即停止，拒绝在教材或其他应用里滚动找文件。两组文件前缀及同名导出拒绝逻辑保持。
3. 启动后同时核对可见原生菜单所属包及旧/新原生标题，避免将其他应用或未返回的文件选择器当成教材已启动。
4. 新版首次导入后增加四类学习记录的完整相等比较，能发现少量关键样例仍在、其他笔记或答案时间却丢失的情况。源记录最终完整对比仍保留。
5. 正式签名与 UI 检查步骤启用 `set -euo pipefail`，避免管道日志命令掩盖上游失败；含正式 APK 的自动 PR/推送也必须通过两组结果门槛。未增大 CI 权限，未改原 14 项 instrumentation 检查。

本地实际执行了 **33 项模拟输入/静态检查**，覆盖旧新标题、包身份、前台报告解析、Back 有界退出及不得操作其他前台应用、文件列表上下查找与停止、源包卸载拒绝、已不存在测试包、精确包名匹配、UID 隔离、完整记录比较、Python 编译及工作流解析；另执行 **10 项真实旧/新 JavaScript 状态处理检查**，全部通过。脚本与详细结果保存在工作区 `work/android-boundary-crosscheck/`，未通过 adb 连接设备，未将这些检查计作 Android 模拟器或手机验收。**两场景真实公有界面执行仍待 CI。**
