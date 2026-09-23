---json
{
  "id": "fluid-mechanics-11",
  "title": "连续方程与 Navier–Stokes 方程",
  "group": "04 · 从守恒到流场",
  "summary": "把控制体守恒局部化，并知道求解还缺哪些条件。",
  "objectives": [
    "理解质量与动量微分方程",
    "选择初始条件和边界条件"
  ],
  "prerequisites": [
    "前面各节；导数与积分基础"
  ],
  "tags": [
    "连续方程与 Navier–Stokes 方程",
    "理解质量与动量微分方程",
    "选择初始条件和边界条件"
  ],
  "minutes": 25,
  "level": "基础",
  "quiz": {
    "question": "不可压缩条件 ∇·u=0 表示？",
    "options": [
      "速度处处为零",
      "流体没有黏度",
      "微团没有净体积膨胀",
      "流场必定无旋"
    ],
    "answer": 2,
    "explanation": "散度描述体积膨胀率；涡量描述局部旋转，两者不同。"
  },
  "lab": null
}
---

## 为什么需要微分方程
控制体方法可以求流量和设备总受力，却不一定告诉我们管内每一点的速度。把控制体缩小，守恒定律在每个位置成立，就得到场方程。它们不是新物理定律，而是相同守恒关系的局部形式。

质量守恒为
$$\frac{\partial\rho}{\partial t}+\nabla\cdot(\rho\mathbf u)=0.$$
若密度沿流体运动保持不变，即 $D\rho/Dt=0$，则 $\nabla\cdot\mathbf u=0$。这不是说速度为零，而是微小体积元没有净体积膨胀。

对常密度、常黏度的不可压缩牛顿流体，动量方程为
$$\rho\left(\frac{\partial\mathbf u}{\partial t}+\mathbf u\cdot\nabla\mathbf u\right)=-\nabla p+\mu\nabla^2\mathbf u+\rho\mathbf g.$$
左边是惯性，右边分别是压力梯度、黏性扩散与重力。压力本身的绝对大小不会直接推动不可压流，驱动局部运动的是压力梯度。

## 方程之外还必须有什么
要求解速度与压力，需要区域形状、物性、适当的边界条件；非稳态还需初始速度场。固壁常用无滑移和无穿透；入口可给速度分布；出口常给压力参考配合适当开放条件。不能在所有边界同时任意指定压力与全部速度分量，否则常会过约束。

当问题涉及温度变化、可压缩性、化学反应或非牛顿性质时，还要加入能量方程、状态方程和相应本构关系。本节显示的简式不能直接覆盖所有这些情况。无黏近似将黏性项略去得到 Euler 方程，但固体壁面附近即使总体黏度很小，黏性仍可能重要。

## 例题：检查一个速度场是否守恒
二维流场 $u=ax,v=-ay$，$a$ 为常数。计算散度：$\partial u/\partial x+\partial v/\partial y=a-a=0$，因此满足不可压质量守恒。它在 x 方向拉伸，同时在 y 方向压缩，体积不变但形状改变。

再看 $u=ax,v=ay$，散度为 $2a$，若 $a\ne0$ 就不能代表二维、无源、不可压的流场。不能只因两式看起来对称就认为它们同样合理。满足质量守恒也还不等于满足动量和边界条件。

## 练习
1. 静止流体代入动量方程会得到什么？
<details><summary>查看解析</summary>

速度为零，惯性与黏性项均为零，得到 $\nabla p=\rho\mathbf g$。取 z 向上，即 $dp/dz=-\rho g$。
</details>

2. 若 $u=ay,v=0$，散度与二维涡量分别是什么？
<details><summary>查看解析</summary>

散度为零，$\omega_z=\partial v/\partial x-\partial u/\partial y=-a$。无散不代表无旋。
</details>
