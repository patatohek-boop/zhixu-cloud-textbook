---json
{
  "id": "heat-transfer-31",
  "title": "熔化与凝固：移动界面和Stefan条件",
  "group": "07 · 补足核心推导",
  "minutes": 40,
  "level": "进阶",
  "tags": [
    "移动相界",
    "潜热",
    "Stefan条件",
    "Stefan数"
  ],
  "objectives": [
    "定义并区分移动相界、潜热、Stefan条件",
    "逐步完成界面能量跳跃、平方根冻结深度及相似解参数方程",
    "核对边界、单位和模型误差"
  ],
  "prerequisites": [
    "heat-transfer-02",
    "heat-transfer-09",
    "thermodynamics-04"
  ],
  "summary": "熔化与凝固：移动界面和Stefan条件：以可复核的步骤补足核心模型。",
  "quiz": {
    "question": "结冰厚度随时间近似按平方根增长的主要原因是？",
    "options": [
      "潜热不守恒",
      "冰层增厚使导热路径热阻增大",
      "冰的密度始终为0",
      "外表面温度不断升高"
    ],
    "answer": 1,
    "explanation": "固定温差时热流约为kΔT/s，界面速度随厚度增加而减慢。"
  },
  "lab": null
}
---

## 严谨定义与记号

移动相界问题的未知量不仅是温度场，还包括相界位置 $s(t)$。取初始液体在熔点 $T_m$，壁面x=0固定为更低温 $T_w$，0<x<s为新生成固体。固体导热系数k、密度ρ、比热c、热扩散率α，凝固潜热 $L_f$用J/kg，不是长度。

Stefan数 $Ste=c(T_m-T_w)/L_f$比较固体显热尺度与相变潜热。这里使用一相模型：液相始终为 $T_m$、没有显著液相导热或对流，忽略密度变化引起的体积运动。

## 通俗解释

冷却不仅要把温度降下来，还要为每一千克新冰带走凝固潜热。冰越厚，热要穿过的路越长，结冰速度便越来越慢。

## 从界面能量平衡推导Stefan条件

在单位面积上，时间dt内新凝固质量为 $\rho\,ds$，释放潜热 $\rho L_f ds$。若液相不供显热，固体侧从界面向冷壁导出的热率大小为 $kT_x(s^-,t)$。因此

$$\rho L_f\frac{ds}{dt}=k\left.\frac{\partial T}{\partial x}\right|_{s^-}.$$

一般两相问题右边为固液两侧按同一方向定义的热流差，不能永远只写固体一项。相界温度还须 $T(s(t),t)=T_m$；仅有热方程而没有界面条件无法求s。

## 小Ste的准稳态推导

若固体显热相对潜热小，近似每一时刻固体温度线性：$T(x,t)\approx T_w+(T_m-T_w)x/s(t)$。代入界面式得 $\rho L_f s\,ds/dt=k(T_m-T_w)$，积分初始s=0：

$$s(t)\approx\sqrt{\frac{2k(T_m-T_w)t}{\rho L_f}}.$$

这不是完整瞬态解，而是忽略固体温度场储能的近似；Ste较大时需恢复热方程。

## 一相相似解与近似极限的核验

令 $s=2\lambda\sqrt{\alpha t}$，在固体内的热方程解可取

$$T=T_w+(T_m-T_w)\frac{\operatorname{erf}[x/(2\sqrt{\alpha t})]}{\operatorname{erf}\lambda}.$$

它满足壁温和界面温度。对x求导，代入Stefan条件，并用 $ds/dt=\lambda\sqrt{\alpha/t}$，消去时间因子得

$$Ste=\sqrt\pi\lambda e^{\lambda^2}\operatorname{erf}\lambda.$$

给定Ste可求正根λ。小λ时 $\operatorname{erf}\lambda\approx2\lambda/\sqrt\pi$，故 $Ste\approx2\lambda^2$；代入s恢复上一条平方根近似，完成两模型一致性检查。

## 一步步算一个例子

教学冰层参数k=2.2 W/(m·K)、ρ=917 kg/m³、c=2100 J/(kg·K)、$L_f=334000$ J/kg，壁温比熔点低10 K，t=3600 s。

1. $Ste=2100\times10/334000\approx0.063$，可先作小Ste估计。
2. $s\approx\sqrt{2\times2.2\times10\times3600/(917\times334000)}\approx0.0227$ m。
3. 一小时约22.7 mm是本理想模型的估计，不包括表面对流、液体流动及实际冰水密度差。

## 动手练习

**练习1**　相同边界下冻结时间变4倍，准稳态厚度变几倍？

<details><summary>查看解析</summary>

2倍，来自 $s\propto\sqrt t$；不是4倍，因为越厚越难向外传热。

</details>

**练习2**　液体最初比熔点更热，能否继续用无液相热流的一相式？

<details><summary>查看解析</summary>

不能直接用。须先移除液体显热，并在界面平衡保留液相侧热流；可采用两相温度场或焓法求解。

</details>

## 范围与继续阅读

本章把相变与非稳态导热连起来，补足仅有沸腾凝结设备式时缺失的移动边界概念。它属于[MIT 2.51导热与相变课程范围](https://ocw.mit.edu/courses/2-51-intermediate-heat-and-mass-transfer-fall-2008/pages/readings/)的进一步工程延伸；枝晶、糊状区、自然对流和材料相图耦合不在这一相模型内。
