---json
{
  "id": "fluid-mechanics-48",
  "title": "k–ε 模型与入口湍流量",
  "group": "11 · 湍流与近壁传热",
  "summary": "围绕k、耗散率、标准模型、RNG与realizable，逐步建立定义、适用条件、推导与可核对的实践。",
  "objectives": [
    "区分并解释k、耗散率、标准模型、RNG与realizable",
    "在给定假设下复现涡黏量纲与入口估计",
    "完成例题、检查单位与适用范围"
  ],
  "prerequisites": [
    "fluid-mechanics-47"
  ],
  "tags": [
    "k",
    "耗散率",
    "标准模型",
    "RNG与realizable"
  ],
  "minutes": 55,
  "level": "专项进阶",
  "quiz": {
    "question": "湍流积分尺度等于首层网格高度吗？",
    "options": [
      "不等于",
      "始终等于",
      "仅由软件名称决定"
    ],
    "answer": 0,
    "explanation": "前者是流动物理输入，后者是数值解析尺度。"
  },
  "lab": null,
  "revision": "2026-10-04 · 知识页结构与行文整理"
}
---
## 标准 k–ε 模型

### k 与 ε

$k=\overline{u_i'u_i'}/2$ 是单位质量湍动能，单位 m²/s²；$\varepsilon$ 是黏性将湍动能耗散为内能的速率，单位 m²/s³，理想精确定义涉及脉动速度梯度。模型中的耗散方程是闭合近似，不能当作严格解析推导。

在高 Reynolds 数、不可压、无浮力等简化条件下，标准模型常写为

$$\rho\frac{Dk}{Dt}=\nabla\cdot[(\mu+\mu_t/\sigma_k)\nabla k]+P_k-\rho\varepsilon,$$

$$\rho\frac{D\varepsilon}{Dt}=\nabla\cdot[(\mu+\mu_t/\sigma_\varepsilon)\nabla\varepsilon]
+C_{\varepsilon1}\frac{\varepsilon}{k}P_k-C_{\varepsilon2}\rho\frac{\varepsilon^2}{k},$$

$$\mu_t=C_\mu\rho\frac{k^2}{\varepsilon}.$$

这里 $D/Dt$ 跟随平均速度，$P_k$ 用 W/m³ 表示。常用标准系数为 $C_\mu=0.09$、$C_{\varepsilon1}=1.44$、$C_{\varepsilon2}=1.92$、$\sigma_k=1.0$、$\sigma_\varepsilon=1.3$；具体实现仍需查版本。浮力、压缩性和低 Re 修正不是上式自动包含的。

## 湍动能与耗散时间尺度

只知道 $k$ 相当于知道“有多少运动”，还不知道这些运动维持多久。$k/\varepsilon$ 提供时间尺度，两者共同估计湍流搬运动量的能力。把模型量设得极小不等于“更接近真实层流”，还可能造成比值病态与初始计算不稳定。

## 推导：涡黏度与入口长度尺度

由 $k$ 和 $\varepsilon$ 组合运动黏度，量纲要求 $k^a\varepsilon^b$ 具有 m²/s，解得 $a=2,b=-1$，因此 $\nu_t\propto k^2/\varepsilon$。量纲分析确定形式但不确定经验系数。

常用入口关系是在给定湍流尺度定义与近似平衡假设下设

$$k=\frac32(UI)^2,\qquad
\varepsilon=C_\mu^{3/4}\frac{k^{3/2}}{\ell}.$$

$\ell$ 不是网格尺度，通常反映入口湍动的大尺度。某些工程经验用通道尺寸的一定比例估计，但不能作为所有喷嘴、风扇或实验整流段的固定真值。

## 例题：入口长度尺度的敏感性

$U=10\ \mathrm{m/s}$、$I=0.05$、$\ell=0.01\ \mathrm m$，得到 $k=0.375$、$\varepsilon\approx3.773\ \mathrm{m^2/s^3}$、$\nu_t\approx0.00335\ \mathrm{m^2/s}$。长度尺度加倍而强度不变时，$\varepsilon$ 减半、入口 $\nu_t$ 加倍。故“同样 5% 湍流强度”并不意味着同样湍流边界。

## 标准、RNG 与 realizable 不能混写

RNG 形式修改耗散相关项和常数，realizable 形式改变涡黏系数与耗散方程结构，以改善某些应变与旋转条件下的约束。它们不是仅换一个名字的同一组方程。高 Re 标准模型通常与壁面函数搭配；低 Re 模型加入近壁修正并需要相应网格。模型选择记录应包括变体、系数、壁面处理、浮力项、入口值和软件版本。

对于强分离、曲率、各向异性、低 Pr 热流等情形，标准 k–ε 可能存在系统偏差。至少用独立基准或实测评价目标量；不同模型预测接近也可能是共同偏差。

<details><summary>练习 1：I 加倍、U 和 ℓ 不变，入口 k、ε、νₜ 分别如何变？</summary>

$k$ 变为 4 倍，$\varepsilon\propto k^{3/2}$ 变为 8 倍，$\nu_t\propto k^2/\varepsilon$ 变为 2 倍。这依赖本节的入口尺度关系，而非湍流的普适定律。

</details>

<details><summary>练习 2：经验系数能否从量纲分析严格证明为 0.09？</summary>

不能。量纲只能限制单位与幂次，不能给出无量纲经验常数。应区分守恒与代数推导可证明的部分，以及依赖实验、理论约束和标定的模型闭合。

</details>

## 参考

[OpenFOAM 动量输运模型入口](https://doc.cfd.direct/openfoam/user-guide-v13/contents)。运行时应查所选变体的实际模型文档或源代码，不能把这里的标准简化式当作所有 k–ε 实现。
