---json
{
  "id": "fluid-mechanics-40",
  "title": "控制方程与热流耦合",
  "group": "09 · 仿真问题与前处理",
  "summary": "围绕连续性、动量、能量、Boussinesq近似，逐步建立定义、适用条件、推导与可核对的实践。",
  "objectives": [
    "区分并解释连续性、动量、能量、Boussinesq近似",
    "在给定假设下复现由内能方程约化温度方程",
    "完成例题、检查单位与适用范围"
  ],
  "prerequisites": [
    "fluid-mechanics-39"
  ],
  "tags": [
    "连续性",
    "动量",
    "能量",
    "Boussinesq近似"
  ],
  "minutes": 55,
  "level": "专项进阶",
  "quiz": {
    "question": "低 Mach 数是否自动意味着密度处处相同？",
    "options": [
      "只由网格决定",
      "不是，还需检查温度和组分变化",
      "一定相同"
    ],
    "answer": 1,
    "explanation": "低 Mach 数限制声学压缩效应，不排除热致密度变化。"
  },
  "lab": null,
  "revision": "2026-10-04 · 知识页结构与行文整理"
}
---
## 流动与传热的控制方程

### 场变量与符号

速度 $\mathbf u$ 的单位是 m/s，压力 $p$ 是 Pa，密度 $\rho$ 是 kg/m³，动力黏度 $\mu$ 是 Pa·s，温度 $T$ 用 K，导热系数记为 $\lambda$，避免与湍动能 $k$ 混淆。材料导数 $D/Dt=\partial_t+\mathbf u\cdot\nabla$ 描述跟随流体质点的变化。

### 质量、动量与热能

一般质量方程是

$$\partial_t\rho+\nabla\cdot(\rho\mathbf u)=0.$$

对常密度不可压 Newton 流体，$\nabla\cdot\mathbf u=0$。动量方程为

$$\rho\frac{D\mathbf u}{Dt}=-\nabla p+\nabla\cdot(2\mu\mathbf S)+\rho\mathbf g,\qquad
\mathbf S=\tfrac12[\nabla\mathbf u+(\nabla\mathbf u)^T].$$

若 $\mu$ 也恒定，黏性项才能简化为 $\mu\nabla^2\mathbf u$。忽略黏性耗散、压缩功和其他能量耦合，常物性温度方程为

$$\rho c_p\frac{DT}{Dt}=\nabla\cdot(\lambda\nabla T)+q_v.$$

$q_v$ 是 W/m³ 的体积热源，不是 W/m² 的表面热流。固体区域取零流速，得到 $\rho_s c_s\partial_tT_s=\nabla\cdot(\lambda_s\nabla T_s)+q_{v,s}$。

## 流动与温度的双向耦合

对流项不是新的热源，而是热随质量流动进入与离开。温差如果改变密度，就可能产生自然对流；温差如果改变黏度，就会改变阻力。因此先求流场再单向计算温度，只有在温度反馈可忽略时才合理。

## 推导：温度方程如何从内能方程得到

对简单可压缩流体，局部内能平衡可写为

$$\rho\frac{De}{Dt}=-p\nabla\cdot\mathbf u+\boldsymbol\tau:\nabla\mathbf u-\nabla\cdot\mathbf q+q_v.$$

这里 $e$ 是单位质量内能，冒号表示对应分量乘积之和，$\mathbf q=-\lambda\nabla T$。在不可压、热膨胀能量修正可忽略且 $de\simeq c_p dT$ 的液体近似中，压缩功为零；再忽略黏性耗散，便得到前式。若高速气体、强压缩、强剪切黏性加热或大物性变化不可忽略，应使用相容的焓或总能量方程，不能把这个温度式直接照搬。

### Boussinesq 浮力近似

取 $\rho(T)\simeq\rho_0[1-\beta(T-T_0)]$，仅在重力项保留密度变化，其余项用 $\rho_0$。将静水部分吸收进修正压力后，温度相关体积力是

$$\mathbf f_b=-\rho_0\beta(T-T_0)\mathbf g.$$

若重力向下，热流体对应的该力向上。它要求 $|\beta\Delta T|\ll1$ 等小密度变化条件；低 Mach 数并不自动保证这个条件。大温差气体可保持低 Mach 数但仍需变密度模型。

## 例题：判断单向耦合是否可信

空气近似 $\beta=1/300\ \mathrm{K^{-1}}$，温差 3 K 时 $\beta\Delta T=0.01$，密度线性化的尺度较小；温差 150 K 时为 0.5，不再是小量。即使前一工况可用 Boussinesq，也还应比较浮力与惯性：小密度变化仍可能驱动整个低速流场。

## 实际建模时逐项核对

先列方程，再列每个系数来自哪里。物性曲线需要温度有效区间；固体可各向异性，此时 $\lambda$ 要换成导热张量；接触界面可能有温度跳跃；黏性耗散若保留，应在流体能量平衡中一致处理。商业软件中的“不可压理想气体”之类名称并不等于恒密度，必须阅读它的实际状态方程。

<details><summary>练习 1：2 cm³ 固体内部均匀发热 4 W，体积热源是多少？</summary>

$2\ \mathrm{cm^3}=2\times10^{-6}\ \mathrm{m^3}$，所以 $q_v=2\times10^6\ \mathrm{W/m^3}$。如果把 4 当作 W/m³ 输入，实际功率仅为 $8\times10^{-6}\ \mathrm W$，比 4 W 小五十万倍；应积分检查 $\int q_vdV=4\ \mathrm W$。

</details>

<details><summary>练习 2：为什么变黏度时不能直接用 μ∇²u？</summary>

乘积求导产生黏度梯度项。以分量表示，$\partial_j[\mu(\partial_j u_i+\partial_i u_j)]$ 包含 $\partial_j\mu$ 与速度梯度的乘积。忽略这些项是额外近似，不能由不可压条件自动推出。

</details>

## 参考

[CFD Direct：CFD 基本原理讲义](https://doc.cfd.direct/notes/cfd-general-principles/)用于方程与数值概念对照。本节方程的删项条件也是后续每个工程案例必须重新核对的条件。
