---json
{
  "id": "fluid-mechanics-30",
  "title": "涡量输运与 Kelvin 环量定理",
  "group": "06 · 进阶流动模型",
  "summary": "物质闭曲线，把条件、定义和推导连成可复查的学习链。",
  "objectives": [
    "准确区分并说明本章各概念",
    "在明确假设下复现推导并解释条件失效的情形"
  ],
  "prerequisites": [
    "fluid-mechanics-19",
    "fluid-mechanics-11"
  ],
  "tags": [
    "物质闭曲线",
    "正压流体与保守体力",
    "涡量伸长与扩散",
    "Kelvin与涡管"
  ],
  "minutes": 50,
  "level": "进阶",
  "quiz": {
    "question": "Kelvin定理中的闭曲线应是什么？",
    "options": [
      "任意固定圆圈",
      "随同一群流体质点移动的闭曲线",
      "必须始终保持圆形的曲线"
    ],
    "answer": 1,
    "explanation": "环量守恒证明使用物质曲线速度与流体速度相同这一条件。"
  },
  "lab": null,
  "revision": "2026-09 · 缺漏补章"
}
---

## 严谨定义与定理条件

物质闭曲线 $C(t)$ 由同一组流体质点构成，随速度场移动；其环量为 $\Gamma(t)=\oint_{C(t)}\mathbf u\cdot d\mathbf l$。正压流体（barotropic）满足局部状态关系 $\rho=\rho(p)$，使 $dp/\rho$ 可以写成某个标量 $H(p)$ 的全微分。保守体力每单位质量为 $-\nabla\Phi$，例如重力势 $\Phi=gz$。

**Kelvin 环量定理。**若流体无黏，场与物质曲线足够光滑，流体正压，体力保守，且曲线不穿过激波或奇点，则 $d\Gamma/dt=0$。这里的曲线必须随同一群质点运动，固定空间圆圈不满足同一命题。

## 通俗解释：给流体圈一条会变形的橡皮圈

橡皮圈可以拉长、扭曲，局部速度可以改变，但在上述理想条件下沿圈累积的切向速度保持同一个值。黏性、非正压的密度压力错位、激波或非保守作用都可能改变环量。

## 完整证明：对移动曲线求导

用周期参数 $s$ 表示曲线 $\mathbf X(s,t)$，满足 $\mathbf X_t=\mathbf u(\mathbf X,t)$。于是
$$\Gamma=\int\mathbf u(\mathbf X,t)\cdot\mathbf X_s\,ds.$$
对时间求导并用链式法则，得到 $d\Gamma/dt=\int[D\mathbf u/Dt\cdot\mathbf X_s+\mathbf u\cdot\partial_s\mathbf u]ds$。第二项为闭曲线上 $\int\partial_s(|\mathbf u|^2/2)ds=0$；故 $d\Gamma/dt=\oint(D\mathbf u/Dt)\cdot d\mathbf l$。

Euler 方程给 $D\mathbf u/Dt=-\nabla p/\rho-\nabla\Phi$。定义 $H(p)=\int^p dq/\rho(q)$，便有 $\nabla H=\nabla p/\rho$。因此 $d\Gamma/dt=-\oint\nabla(H+\Phi)\cdot d\mathbf l=0$，因为闭合曲线上的单值势函数增量为零，证毕。若不正压，$\nabla p/\rho$ 未必是梯度，证明在这一步失效。

## 推导：局部涡量会如何变化

对常密度、常黏度不可压 Navier–Stokes 取旋度，压力梯度和保守体力旋度为零。利用 $\nabla\times[(\mathbf u\cdot\nabla)\mathbf u]=(\mathbf u\cdot\nabla)\boldsymbol\omega-(\boldsymbol\omega\cdot\nabla)\mathbf u$，得
$$\frac{D\boldsymbol\omega}{Dt}=(\boldsymbol\omega\cdot\nabla)\mathbf u+\nu\nabla^2\boldsymbol\omega.$$
第一项拉伸和转向涡量，第二项扩散涡量。一般可压缩无黏流还会出现 $-\boldsymbol\omega\nabla\cdot\mathbf u$ 与斜压项 $(\nabla\rho\times\nabla p)/\rho^2$；可通过展开 $\nabla\times(-\nabla p/\rho)$ 得到后者的正号。

无黏不可压时，一个随流线元 $\boldsymbol\ell$ 满足 $D\boldsymbol\ell/Dt=(\boldsymbol\ell\cdot\nabla)\mathbf u$，和涡量具有同一线性演化式。因此初始与涡量平行的线元会继续保持这种方向对应，这是涡线随流体运动的基础。涡管截面通量由 Stokes 定理等于边界物质环量，故在这些条件下守恒；管子变细时涡量可变强，并不违背环量守恒。

## 例题与练习

在局部拉伸 $\mathbf u=(-ax/2,-ay/2,az)$ 中，散度为零。若局部已有沿 $z$ 的涡量、忽略扩散，其涡量方程给 $D\omega_z/Dt=a\omega_z$，所以 $\omega_z(t)=\omega_z(0)e^{at}$。这描述给定拉伸背景对涡量的作用，不声称此线性背景本身带有非零涡量。

1. 上述例题中 $a=1\,\mathrm{s^{-1}}$，一秒后局部涡量放大几倍？
<details><summary>查看解析</summary>

放大 $e$ 倍。若物质涡管相应截面积按 $e^{-t}$ 缩小，涡量通量保持不变，两个结论相容。
</details>

2. 为什么粘性边界层里不能直接用 Kelvin 定理证明环量恒定？
<details><summary>查看解析</summary>

动量式含黏性力，其闭合线积分未必为零，已不满足无黏条件。真实启动过程和壁面可以生成、扩散涡量。
</details>
