---json
{
  "id": "fluid-mechanics-31",
  "title": "低 Reynolds 数流动与润滑近似",
  "group": "04 · 从守恒到流场",
  "summary": "Stokes方程，把条件、定义和推导连成可复查的学习链。",
  "objectives": [
    "分别检查小 Reynolds 数、薄隙几何和非稳态时间条件",
    "沿边界条件理解球体 Stokes 解与润滑近似，说明远场局限"
  ],
  "prerequisites": [
    "fluid-mechanics-12",
    "fluid-mechanics-19"
  ],
  "tags": [
    "Stokes方程",
    "可逆性与边界条件",
    "球体阻力",
    "薄隙润滑与Reynolds方程"
  ],
  "minutes": 50,
  "level": "进阶",
  "quiz": {
    "question": "薄隙润滑模型除间隙很小，还需检查什么？",
    "options": [
      "合适缩放下惯性可忽略及边界条件",
      "只要流体颜色一样",
      "只看总质量"
    ],
    "answer": 0,
    "explanation": "几何小参数与惯性小参数是不同的条件，均需核验。"
  },
  "lab": null,
  "revision": "2026-10-04 · 知识页结构与行文整理"
}
---
## Stokes 近似与润滑近似

本节采用不可压、常密度、常黏度牛顿流体，并忽略体力；若保守体力在常密度条件下已并入修正压力，也可使用相同形式。非牛顿或显著变黏度流动需重新建立相应的应力和薄隙方程。

### Stokes 流与惯性尺度

Reynolds 数 $Re=\rho UL/\mu$ 比较惯性与黏性。稳态 $Re\ll1$ 且不存在放大惯性的特殊远场时，动量方程可近似为 $-\nabla p+\mu\nabla^2\mathbf u=0$、$\nabla\cdot\mathbf u=0$，称 Stokes 流。低 $Re$ 不自动允许忽略快速非稳态惯性。

### 润滑流的几何条件

润滑近似另用几何小参数 $\epsilon=h/L\ll1$，$h$ 为间隙、$L$ 为沿程尺度。以代表性速度 $U_*$ 定义 $Re_h=\rho U_*h/\mu$，对流惯性可忽略还要求 $Re_h\epsilon\ll1$。

### 非稳态时需要另查时间尺度

若间隙或边界速度随时间变化，以下准稳态速度剖面另需 $h^2/(\nu T)\ll1$，其中 $T$ 是边界变化时标；否则非稳态惯性仍可能重要。薄隙流不等于整个装置所有尺度的 Reynolds 数都小。

## 低速流动与薄隙流动的区别

缓慢搅动黏液时，黏性比惯性更重要；狭缝中的速度即使不极小，法向梯度也会非常大，仍可由黏性主导。它们都能简化方程，但依据不同，不能只凭“看起来很慢”混为一个模型。

## 推导一：孤立球体的 Stokes 阻力

球半径为 $a$，远处流速沿 $+z$ 为 $U$，用球坐标 $r,\vartheta$，$\vartheta$ 从 $+z$ 轴量起。轴对称且无周向速度（不等于无涡量）的速度场可用流函数 $\psi=f(r)\sin^2\vartheta$ 表示，$u_r=2f\cos\vartheta/r^2,u_\vartheta=-f'\sin\vartheta/r$，自动满足连续性。

将此式代入 Stokes 方程，取旋度消去压力后径向方程为 $f^{(4)}-4f''/r^2+8f'/r^3-8f/r^4=0$。试 $f=r^m$ 得根 $m=4,2,1,-1$；远处均匀速度排除 $r^4$ 项，保留 $f=Ur^2/2+Br+C/r$。球面无滑移要求 $f(a)=f'(a)=0$，解得 $B=-3Ua/4,C=Ua^3/4$。于是
$$u_r=U\cos\vartheta\left(1-\frac{3a}{2r}+\frac{a^3}{2r^3}\right),\quad u_\vartheta=-U\sin\vartheta\left(1-\frac{3a}{4r}-\frac{a^3}{4r^3}\right).$$
由径向 Stokes 动量式积分并取 $p\to p_\infty$ 得 $p-p_\infty=-3\mu Ua\cos\vartheta/(2r^2)$。在球面 $u_r=u_\vartheta=0$，$\partial_ru_r=0$，故压力造成的 $z$ 向牵引为 $3\mu U\cos^2\vartheta/(2a)$；切向黏性应力为 $\sigma_{r\vartheta}=-3\mu U\sin\vartheta/(2a)$，其 $z$ 向贡献为 $3\mu U\sin^2\vartheta/(2a)$。均匀背景压力的合力为零。

两者相加是常数 $3\mu U/(2a)$，乘球面积 $4\pi a^2$ 得 $F_D=6\pi\mu aU=3\pi\mu DU$。以 $A=\pi D^2/4$ 定义阻力系数便得 $C_D=24/Re_D$。壁面邻近、多颗粒、较大惯性或非牛顿流体均会破坏这一孤立球模型。

## 推导二：薄隙流量与润滑方程

间隙为 $h(x,t)$，下板固定、上板沿 $x$ 速度 $U$。薄隙近似使 $p_y\approx0$，流向平衡为 $\mu u_{yy}=p_x$。积分并使用 $u(0)=0,u(h)=U$，得 $u=Uy/h+p_x(y^2-hy)/(2\mu)$。单位宽流量为
$$q=\int_0^hu\,dy=\frac{Uh}{2}-\frac{h^3}{12\mu}p_x.$$
无渗漏质量守恒给 $h_t+q_x=0$，故 $\partial_x(h^3p_x)=6\mu\partial_x(Uh)+12\mu h_t$。这是这里一维薄隙模型的 Reynolds 润滑方程；不应与 Reynolds 平均湍流方程混淆。

## 例题与练习

半径 $a=0.1$ mm 的球以 $U=0.001$ m/s 在 $\mu=0.1$ Pa·s、$\rho=1000$ kg/m³ 的流体中运动，$Re_D=0.002$。阻力为 $6\pi\mu aU\approx1.885\times10^{-7}$ N，低 $Re$ 条件自洽。

1. 固定压力梯度、静止两板，间隙减半时流量变为几倍？
<details><summary>查看解析</summary>

$q=-h^3p_x/(12\mu)$，所以为八分之一；此结论还要求常黏度与薄隙模型继续有效。
</details>

2. 为什么不能把球体 Stokes 阻力直接用于无限长圆柱的同一无界二维问题？
<details><summary>查看解析</summary>

几何与远场边界不同；二维无界稳态 Stokes 绕圆柱不能同时满足非零均匀远流与无滑移，出现 Stokes 佯谬。不能从三维球解无条件外推。
</details>
