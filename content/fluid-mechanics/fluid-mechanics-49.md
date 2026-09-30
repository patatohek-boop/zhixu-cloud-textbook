---json
{
  "id": "fluid-mechanics-49",
  "title": "k–ω、SST 与 SA 选型",
  "group": "11 · 湍流与近壁传热",
  "summary": "围绕比耗散率、混合函数、剪切应力限制、SA，逐步建立定义、适用条件、推导与可核对的实践。",
  "objectives": [
    "区分并解释比耗散率、混合函数、剪切应力限制、SA",
    "在给定假设下复现SST涡黏限制不等式",
    "完成例题、检查单位与适用范围"
  ],
  "prerequisites": [
    "fluid-mechanics-48"
  ],
  "tags": [
    "比耗散率",
    "混合函数",
    "剪切应力限制",
    "SA"
  ],
  "minutes": 55,
  "level": "专项进阶",
  "quiz": {
    "question": "不同 SST 变体可否只看名称就视为完全一样？",
    "options": [
      "只看结果颜色",
      "不能，应核对方程、限制器与版本",
      "可以"
    ],
    "answer": 1,
    "explanation": "SST 有不同定义和实现，模型版本属于可复现信息。"
  },
  "lab": null,
  "revision": "2026-09-30 · 流动换热仿真专项"
}
---

## 严谨定义：ω、混合函数与剪切应力限制

### k–ω 的尺度

$\omega$ 是单位 s⁻¹ 的比耗散率模型变量，提供逆时间尺度。常见关系为 $\varepsilon\approx\beta^*k\omega$，不是定义所有变体的普遍恒等式。基本涡黏尺度为 $\nu_t\sim k/\omega$。相较高 Re k–ε，部分 k–ω 实现便于积分到壁面，但自由流 $\omega$ 和近壁条件会影响解。

### SST 模型是什么

Menter SST 以混合函数连接近壁与外区方程，并限制涡黏度。这里说明常密度不可压  **SST-2003**  的结构；原始 1994 版、2003 版与各软件修正并非完全相同。

$$\rho D_tk=\widetilde P_k-\beta^*\rho k\omega+
\nabla\cdot[(\mu+\sigma_k\mu_t)\nabla k],$$

$$\rho D_t\omega=\gamma\frac{\widetilde P_k}{\nu_t}-\beta\rho\omega^2+
\nabla\cdot[(\mu+\sigma_\omega\mu_t)\nabla\omega]
+2(1-F_1)\frac{\rho\sigma_{\omega2}}{\omega}\nabla k\cdot\nabla\omega.$$

其中 $S=\sqrt{2S_{ij}S_{ij}}$，$\widetilde P_k=\min(P_k,10\beta^*\rho k\omega)$，

$$\nu_t=\frac{a_1k}{\max(a_1\omega,SF_2)},\qquad
\phi=F_1\phi_1+(1-F_1)\phi_2.$$

$\phi$ 代表被混合的系数，$F_1,F_2\in[0,1]$ 由壁距、局部 $k,\omega,\nu$ 等构成，不是用户随便调的区域开关。$a_1=0.31,\beta^*=0.09$；2003 版使用应变率 $S$，原始版的相应限制器使用涡量大小。上式中 $\widetilde P_k/\nu_t$ 的零值极限、正性保护、壁面边界和混合函数须按具体实现处理，不应照此概览自行省略保护编写工业求解器。

## 通俗解释：同样叫 SST，设置不一定相同

SST 不是“遇到分离一定算准”的按钮。模型试图改善不利压梯度等情况，但真实入口边界层、转捩、粗糙度和三维效应仍会改变换热。报告“用了 SST”还不够，需写明版本、变体、壁面解析策略与湍流热流模型。

## 推导：限制器到底限制了什么

当 $k\ge0,\omega>0$ 时，分母不小于 $a_1\omega$，因此

$$0\le\nu_t\le\frac{k}{\omega}.$$

当 $SF_2>a_1\omega$ 时，涡黏度取更小值。生产限制器则满足 $\widetilde P_k\le10\beta^*\rho k\omega$，避免某些高应变区域产生过强生产。上述不等式是给定模型后的代数性质，不是湍流真实应力的严格上界。

### 完整算例

给定 $k=0.1\ \mathrm{m^2/s^2}$、$\omega=100\ \mathrm{s^{-1}}$、$S=200\ \mathrm{s^{-1}}$、$F_2=1$，则分母 $\max(31,200)=200$，$\nu_t=0.031/200=1.55\times10^{-4}\ \mathrm{m^2/s}$，小于 $k/\omega=10^{-3}$。这展示局部限制机制，不代表任何实际设备的预测值。

## SA 与模型选择的另一条路线

Spalart–Allmaras（SA）模型输运一个修正运动黏度变量 $\widetilde\nu$，通过阻尼函数得到涡黏度；它不直接求解 k 和 ε。SA 在附着气动边界层等问题中常见，但仍须另选热通量闭合。SA、SA-neg、旋转修正和转捩处理需要分别注明，不能给 SA 输入 k–ε 的变量然后以为模型相同。

完整混合函数、所有系数、生产项变体和壁面建议直接对照 [TMR 的 SST 定义](https://tmbwg.github.io/turbmodels/sst.html)；[SA 定义与变体](https://tmbwg.github.io/turbmodels/spalart.html)用于进一步实现核对。本课给出可用于选型和检查的结构，完整源代码级闭合实现属于延伸阅读，不以省略函数冒充完整算法。

<details><summary>练习 1：S=0 时上述涡黏度限制器回到什么形式？</summary>

若 $k\ge0,\omega>0$，分母为 $a_1\omega$，所以 $\nu_t=k/\omega$。该极限检查可以帮助识别公式单位或括号错误。

</details>

<details><summary>练习 2：换成 SST 后热流更接近实验，是否能证明 SST 更正确？</summary>

单个结果接近可能来自误差抵消。还需核对网格、入口、热损失和实验误差，比较速度、压力、温度剖面及多个工况。模型优劣应针对目标问题和证据陈述。

</details>
