---json
{
  "id": "heat-transfer-12",
  "title": "对流传热的无量纲分析",
  "group": "04 · 对流、沸腾与凝结",
  "minutes": 38,
  "level": "基础",
  "tags": [
    "无量纲",
    "相似",
    "量纲分析"
  ],
  "objectives": [
    "严谨定义并区分Re、Pr、Pe",
    "逐步说明无量纲化动量能量式及浮升惯性黏性比",
    "区分解析推导、模型假设和经验数据范围"
  ],
  "prerequisites": [
    "heat-transfer-11"
  ],
  "summary": "从守恒方程比较惯性、黏性、热扩散和浮力，说明Re、Pr、Nu、Gr与Ra的含义。",
  "quiz": {
    "question": "Nu 与 Bi 的关键区别之一是？",
    "options": [
      "Nu 有单位而 Bi 无单位",
      "Nu 用流体 k，Bi 用固体 k",
      "两者永远相等",
      "Bi 只用于辐射"
    ],
    "answer": 1,
    "explanation": "相似外观掩盖了不同的物理比较对象与导热系数基准。"
  },
  "lab": null
}
---
## 对流中的无量纲数

### 速度、长度与扩散尺度

取速度尺度 $U$、长度 $L$、流体导热系数 $k_f$、运动黏度 $\nu$、热扩散率 $\alpha$。定义 $Re=UL/\nu$、$Pr=\nu/\alpha$、$Pe=UL/\alpha=RePr$。

### Nusselt数与Biot数的不同物性

Nusselt数 $Nu=hL/k_f$ 用流体 $k_f$，Biot数 $Bi=hL_c/k_s$ 用固体 $k_s$，二者不能互换。

### 浮升参数与物性评价

浮升热膨胀系数 $\beta=-(1/\rho)(\partial\rho/\partial T)_p$（K⁻¹）；$Gr=g\beta|\Delta T|L^3/\nu^2$，$Ra=GrPr$，$Ri=Gr/Re^2$。所有这些比值无量纲，特征长度和物性取值必须与所用关联式的定义一致。

### 本节正值Gr/Ra的前提

本节“热而轻”及 $g\beta|\Delta T|$ 作为非负强弱量级，默认所用温区 $\beta>0$ 且可近似常数。若 $\beta<0$，必须保留浮力项 $g\beta(T-T_0)$ 的符号，按实际密度随高度的分布判断稳定性；若只比较驱动大小，可另定义含 $|\beta\Delta T|$ 的模量，但不能因此自动使用本节正Ra经验式。常压水约0—4 ℃受热反而变密，跨密度极大值时常 $\beta$ 模型也可能失效。低速、近不可压缩且无其他密度因素时，重液在下、轻液在上才是通常的稳定排序；具体临界条件还依几何与边界。参见[OpenStax水的反常热膨胀](https://openstax.org/books/university-physics-volume-2/pages/1-3-thermal-expansion)。

## 尺度与相对作用强弱

无量纲数比较方程中不同作用的相对大小。例如同一流体在相同速度下，流道尺寸改变就会改变惯性与黏性的相对作用。比较实验或模型时，必须同时核对长度、速度和边界条件的定义。

## 推导：从方程读出这些比值

在动量方程中惯性量级 $U^2/L$、黏性量级 $\nu U/L^2$，二者比为 $Re$。用 $x=Lx^*,u=Uu^*,p=\rho U^2p^*$ 无量纲化，得到惯性项等于无量纲压梯加 $(1/Re)\nabla^{*2}\mathbf u^*$，这说明 $Re$ 真正控制相对项强弱。

能量方程携热量级 $U\Delta T/L$ 与扩散 $\alpha\Delta T/L^2$ 比为 $Pe$，而 $Pr=\nu/\alpha$ 比较两种扩散速度。壁面条件 $q''=h\Delta T=-k_fT_y$ 用 $L,\Delta T$缩放后，$Nu$ 等于相应无量纲壁面温度梯度。

浮升加速度量级 $g\beta|\Delta T|$ 与惯性 $U^2/L$ 的比为 $Ri=g\beta|\Delta T|L/U^2$。代入 $Re$可得 $Ri=Gr/Re^2$。若用黏性速度尺度 $\nu/L$，浮升对应 $Gr$；把热扩散一起纳入得到 $Ra=g\beta|\Delta T|L^3/(\nu\alpha)$。

## 相似不是只对一个数字

几何、无量纲边界条件、粗糙度、物性变化和所有主导无量纲数都要相容，才能声称相似。相同Nu在不同尺寸设备上给 $h=Nu k_f/L$，数值可不同。平板 $L$ 常取流向长度，圆管取直径，非圆管需明确水力直径；自然对流水平板可能用面积/周长，不能统一偷换最大边长。

## 例题1

空气沿长 0.50 m 平板流动，U=3 m/s、ν=1.5×10⁻⁵ m²/s、α=2.1×10⁻⁵ m²/s，测得 h=10 W/(m²·K)、k_f=0.026 W/(m·K)。

1. Re=3×0.5/(1.5×10⁻⁵)=100000。
2. Pr=1.5/2.1≈0.714。
3. Nu=10×0.5/0.026≈192.3。
4. Re 给出流动尺度，Pr 说明热与动量扩散相近，Nu 则总结测得换热强度；三个数角色不同。

## 从无量纲结果恢复实际热流

Pr 较大不直接表示换热系数一定大，因为 h 还受几何、流速、导热系数与边界控制。无量纲数适合比较机制，实际性能仍需恢复有量纲结果。同一个 Nu 放在尺寸不同的设备上，h=Nu k/L 可以不同；同一个 h 配上不同面积，总换热量也可能差很多。

## 常见误区

不同关联式使用不同 L 却直接比较 Nu；把经验临界 Re 当绝对自然常数；把 Nu 的 k 取成固体 k。

## 练习

**练习 1**　在同一流体与长度下，速度加倍，Re 如何变化？

<details><summary>查看解析</summary>

Re 加倍。换热系数不一定加倍，因为关联式通常对 Re 是非线性幂律，且可能跨越流态范围。

</details>

**练习 2**　若热扩散率比动量扩散率大十倍，Pr 多少，热边界层通常更厚还是更薄？

<details><summary>查看解析</summary>

Pr=0.1。层流常物性边界层中热扩散更快，热边界层通常比速度边界层厚；具体厚度比依模型确定。

</details>

## 继续阅读

课程内容与模型条件可参阅[MIT 2.51 Intermediate Heat and Mass Transfer — syllabus](https://ocw.mit.edu/courses/2-51-intermediate-heat-and-mass-transfer-fall-2008/pages/syllabus/)。
