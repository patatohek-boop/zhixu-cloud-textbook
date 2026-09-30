---json
{
  "id": "fluid-mechanics-41",
  "title": "无量纲尺度与模型判断",
  "group": "09 · 仿真问题与前处理",
  "summary": "围绕Re、Pr、Pe、Ra、Ri、Br，逐步建立定义、适用条件、推导与可核对的实践。",
  "objectives": [
    "区分并解释Re、Pr、Pe、Ra、Ri、Br",
    "在给定假设下复现对流扩散方程无量纲化",
    "完成例题、检查单位与适用范围"
  ],
  "prerequisites": [
    "fluid-mechanics-40"
  ],
  "tags": [
    "Re",
    "Pr",
    "Pe",
    "Ra",
    "Ri",
    "Br"
  ],
  "minutes": 55,
  "level": "专项进阶",
  "quiz": {
    "question": "Ri 比较哪两种作用？",
    "options": [
      "辐射与导热",
      "时间与长度",
      "浮力与惯性"
    ],
    "answer": 2,
    "explanation": "Ri=Gr/Re²，表示浮力相对惯性的重要程度。"
  },
  "lab": null,
  "revision": "2026-09-30 · 流动换热仿真专项"
}
---

## 严谨定义：无量纲数是项的相对大小

### 尺度与参数

选特征长度 $L$、速度 $U$、温差 $\Delta T$ 和运动黏度 $\nu=\mu/\rho$。热扩散率为 $\alpha=\lambda/(\rho c_p)$。定义

$$Re=\frac{UL}{\nu},\quad Pr=\frac{\nu}{\alpha},\quad Pe=RePr=\frac{UL}{\alpha}.$$

$Re$ 衡量惯性与黏性，$Pr$ 比较动量与热扩散，$Pe$ 比较热对流与热扩散。 **物理 Peclet 数** 使用物理尺度 $L$；数值格式中的 **网格 Peclet 数** 使用单元尺度，不能混用。

### 浮力、压缩性与耗散

$$Gr=\frac{g\beta\Delta T L^3}{\nu^2},\quad Ra=GrPr,\quad Ri=\frac{Gr}{Re^2}=\frac{g\beta\Delta T L}{U^2}.$$

$Ri$ 是浮力与惯性的尺度比，$Ra$ 用于自然对流。Mach 数 $Ma=U/a$ 比较速度与声速；Brinkman 数 $Br=\mu U^2/(\lambda\Delta T)$ 比较黏性耗散与导热。正负温差、重力与温度梯度方向还会影响浮力稳定性，不能只看绝对值。

## 通俗解释：同样的网格，不一定能同时看清速度和温度

高 $Pr$ 流体的热扩散慢，温度边界层可能比速度边界层薄；低 $Pr$ 液态金属的热扩散快。由此，满足速度场分辨率的网格不一定满足壁面热流精度。湍流热输运也不只是把黏度改成某个更大的值。

## 推导：尺度怎样进入方程

取 $\mathbf x=L\mathbf x^*$、$t=(L/U)t^*$、$\mathbf u=U\mathbf u^*$、$\theta=(T-T_0)/\Delta T$。将常物性温度方程除以 $\rho c_pU\Delta T/L$，无热源时得

$$\partial_{t^*}\theta+\mathbf u^*\cdot\nabla^*\theta=\frac1{RePr}\nabla^{*2}\theta.$$

动量方程除以 $\rho U^2/L$ 后，黏性项系数为 $1/Re$，Boussinesq 浮力项大小系数为 $Ri$。因此尺度分析给出“可能重要的项”，但不会自动给出真实分离位置、转捩点或湍流强度。

### 完整算例：缓慢空气冷却

取 $L=0.1\ \mathrm m$、$U=0.2\ \mathrm{m/s}$、$\nu=1.5\times10^{-5}\ \mathrm{m^2/s}$、$Pr=0.7$、$\beta=1/300\ \mathrm{K^{-1}}$、$\Delta T=20\ \mathrm K$。得到 $Re\approx1333$、$Pe\approx933$、$Ri\approx1.64$。尽管入口是风扇驱动，浮力不宜直接忽略。改为 $U=2\ \mathrm{m/s}$ 时 $Ri\approx0.0164$，浮力相对惯性弱得多。

## 从尺度到建模决策

圆管流的典型转捩 Reynolds 数不能直接搬到平板、喷流或自然对流腔体。需说明特征长度与速度定义，并检查入口扰动、粗糙度、曲率、加热与稳定性。低 $Ma$ 是忽略声学压缩效应的常用起点，不是恒密度或无浮力的证明。微尺度通道还要检查连续介质与无滑移假设，而不只看 Re。

<details><summary>练习 1：物理 Pe=1000，把一个方向网格加密一倍会发生什么？</summary>

物理 Pe 不变，因为设备与流速没变；若单元长度减半，局部网格 Pe 约减半。后者影响离散格式的数值振荡和扩散，前者描述原来的物理问题。

</details>

<details><summary>练习 2：只把速度扩大两倍，Re、Ri 和 Br 各变多少？</summary>

固定其他量时，Re 变为 2 倍，Ri 变为 1/4，Br 变为 4 倍。强迫对流相对更重要，但黏性耗散也相对增强。是否可以删项还需用实际数值而非倍率判断。

</details>

## 参考

[NASA 验证与确认概述](https://www.grc.nasa.gov/www/wind/valid/tutorial/overview.html)强调先识别流动特征。无量纲分析是建模依据，不能替代针对几何和工况的验证。
