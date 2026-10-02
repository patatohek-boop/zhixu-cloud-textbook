# 六项内容与数值复核 · 未发布

日期：2026-10-02。基线提交：`4ac8857db7660fe22391a5da8e644692c562f6dd`（1.3.2）。本次只处理两项已确认问题与四项条件/记号澄清，不代表重新完成全部学科的专业审校。

## 修改范围

1. **流体第 61 节、小 Pe 解析参考解**：原 Python 和网页 JavaScript 都从两个接近 1 的指数数值直接相减，`Pe=1e-17, x=1` 会算成 0，破坏右端边界；`Pe=1e-6` 的误差和观察阶也会失真。现将分子、分母的指数差均交给 `expm1`，在 `0<Pe<1e-8` 时采用一阶 Taylor 极限，避免次正规数相除。同步课文完整代码，保留 Pe=0 的精确线性极限。
2. **线代第 12 节、QR 定义一致性**：Householder 反射先生成对角可带负号的薄分解 `Q0 R0`；补充 `D=diag(sign((R0)ii))`、`Q=Q0 D`、`R=D R0`，证明乘积、正交性和正对角约定一致。
3. **微积分第 27 节、逆函数条件**：重申开邻域内 C1、基点方程和可逆 Jacobian 假设；明确逆函数导数在像点求值，原 Jacobian 在对应原像求值。
4. **线代第 22 节、低秩近似的权重和**：完整右正交基有 n 个方向，宽矩阵的额外奇异值补零；在该完整基上权重和才等于投影秩 r，前 p 个方向的和仅保证不超过 r。各求和上限和端点情形明确区分。
5. **线代第 24 节、Jordan 幂边界**：求和上限取 `min(k,r-1)`，不产生负指数；按多项式约定将零次幂项视为常数 1，覆盖零特征值、k=0 和幂零块有限步归零。
6. **传热第 20 节、辐射总量平均**：说明方向、偏振平均与光谱权重的相容性，区分灰体与漫灰模型，以及同温各向同性黑体入射。这是条件澄清；原文已有光谱相等的前提，不能把它说成 Kirchhoff 理论本身错误。

保留 253 节编号、学习记录存储键和备份格式。未修改阅读器状态逻辑、签名配置、工作流触发条件或依赖清单。现有发布标识仍为 1.3.2 / versionCode 6；本次不是版本发布。

## 回归与独立复算

- Python：以 400 位 Decimal 精度直接计算原始指数比值，核对 135 组位置/Péclet 数，包括 0、最小正次正规数、1e-310、1e-17、1e-12、Taylor 阈值两侧、1e-6 和通常范围至 100；检查边界、有限性、有界性、单调性。
- JavaScript：用独立的积分幂级数比值核对同样 135 组输入，不复用生产函数的分支或指数相减表达式。
- 小 Pe 中心格式：实际运行 Python CLI 网格研究，并测试 JavaScript 对应模型；Pe=1e-6、N=10→20→40→80→160 的 Python 观察阶分别约为 2.000001、1.999994、1.999977、2.000250。保留 Pe=5 的一阶迎风与二阶中心收敛测试。
- 数学：增加带符号薄 QR 归一化、宽矩阵右基权重和、零/非零特征值 Jordan 幂及非线性逆映射 Jacobian 评价点的独立符号算例。
- 热学：增加方向选择性灰表面的半球平均与定向入射反例，以及各向同性、漫灰极限数值积分。
- 独立复核另外用 400 位精度核对 Python/JavaScript 共 1,398 个参考点，最大绝对误差约 2.23e-16，并复核 QR、完整基投影和 Jordan 边界案例；未发现本轮数学或数值阻断问题。

这些有限数值/符号测试支撑算例和边界检查，不能替代每个文字证明的逻辑审阅。

## 本地检查结果

环境：Python 3.12.14、Node.js 24.19.0。以下检查实际执行通过：

- `python tools/build.py`：7 科、253 节、253 条审计记录，课文与完整 Python 示例逐字一致
- `node tools/validate.cjs`：253 节、9,340 条公式、21 个实验
- `node tools/test-learning-state.cjs`：8 组学习状态、备份与路由安全边界
- `node tools/test-research-labs.cjs`：12 组数值检查
- `node tools/test-cfd-labs.cjs`：135 组解析参考值、4 个 CFD 模型和 108 组控制组合
- `python tools/verify_cfd.py`：135 组独立解析值与 CLI 收敛等检查
- `python tools/verify_research_foundations.py`：70 项
- `python tools/verify_fluid.py`：65 项
- `python tools/verify_thermal.py`：342 项
- `python tools/security_check.py`：安全配置、5 个固定工作流组件、68 个第三方文件和 31 幅示意图
- `python tools/verify_math.py`：466 项，其中 75 项数学检查，另核对 3,831 条数学公式
- `python tools/verify_computing.py`：59 段代码、1,291 条公式、34 项数值/约定检查
- `python tools/verify_research_physics.py`：49 项
- `python tools/verify_audit_errata.py`：6 组已有输入场景
- `python tools/bundle_android.py`：生成 114 个 Android 离线资源
- `git diff --check`：通过

上述包含现有 Pages 工作流的完整校验集合。起初 `tools/test-rendering.cjs` 因缺少 jsdom 无法启动；随后仅在临时目录从 npm 官方注册表安装 jsdom 30.1.1（禁用安装生命周期脚本，不修改仓库依赖文件），使用 `ZHIXU_JSDOM_MODULE` 指定该模块，实际重新执行并通过：

- `node tools/test-rendering.cjs`：253 节、9,340 条公式、12 组注入输入；笔记转义、异常路由、实验、自测、事务式备份、Android 适配隔离和返回处理通过
- `node tools/test-research-labs.cjs --dom`：12 组数值检查和 5 组 DOM 检查通过，覆盖控制/预设/重置、唯一 ID、等比例坐标以及暂停、移除和隐藏页面的动画清理

JSDOM 检查不等于 Android WebView 或真机测试。

## Android 与发布边界

逐字节核对生成的 Android 离线资源：112 个普通网站资源完全一致；入口 HTML 只增加预期的 Android 适配脚本，适配脚本本身也与来源逐字一致，总计 114 个文件。该步骤验证内容进入离线资源，不等于 APK 已编译或已在设备运行。

当前云环境没有配置 Android SDK，也没有要求的 JDK 17 工具链（现有 Java 21）。未执行 APK 编译、Android Lint、Instrumentation、签名、真机安装或 APK 发布。没有接触私钥。未合并主分支或部署线上网站。现有 Android 工作流不由普通 PR 触发，草稿 PR 的 Pages 校验不能冒充 Android 构建验证。

正式发布需另行确定版本号与递增 versionCode，完成对应的 Android 构建/设备检查，并按原签名身份覆盖升级；不要以本地资源核对替代这些步骤。
