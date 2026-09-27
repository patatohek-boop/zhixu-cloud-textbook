---json
{
  "id": "fluid-mechanics-11",
  "title": "连续方程与 Navier–Stokes 方程",
  "group": "04 · 从守恒到流场",
  "summary": "把控制体守恒局部化，并知道求解还缺哪些条件。",
  "objectives": [
    "准确解释连续方程",
    "在列明条件后复现本章推导，并用例题检验结论"
  ],
  "prerequisites": [
    "fluid-mechanics-29",
    "fluid-mechanics-10",
    "fluid-mechanics-36"
  ],
  "tags": [
    "连续方程与 Navier–Stokes 方程",
    "理解质量与动量微分方程",
    "选择初始条件和边界条件"
  ],
  "minutes": 40,
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
  "lab": null,
  "revision": "2026-09 · 定义与推导修订"
}
---

## 严谨定义：方程中的每种运算

$\nabla\cdot\mathbf u$ 是散度；$\nabla p$ 是压力梯度；$\nabla^2\mathbf u$ 表示分别对三个速度分量取各坐标二阶偏导并求和。密度 $\rho$、动力黏度 $\mu$ 取正常正值。**不可压缩运动**定义为流体质点密度保持不变，即 $D\rho/Dt=0$，它不要求不同质点一定具有相同密度。

质量守恒和牛顿第二定律是物理规律。Navier–Stokes 方程还用了牛顿材料本构，故不是仅靠“守恒”对任何流体都自动成立。以下从光滑场出发推导；不连续场应回到积分式或弱形式。

## 通俗解释：每个小格都遵守同一账本

大控制体告诉我们进出多少、合力多大；让每个可任选的小区域都满足同样的账，就能约束每个位置的变化。方程表达局部规则，边界条件表达这个实验或设备怎样与外界相接。

## 推导一：从任意控制体到连续方程

固定控制体质量式用散度定理改写为 $\int_{CV}[\partial_t\rho+\nabla\cdot(\rho\mathbf u)]dV=0$。若连续的被积函数在某点为正，则足够小邻域也为正，积分不可能为零；负号同理。因此它在每点均为零：
$$\partial_t\rho+\nabla\cdot(\rho\mathbf u)=0.$$
展开乘积得 $D\rho/Dt+\rho\nabla\cdot\mathbf u=0$。在 $\rho>0$ 且不可压运动时，$\nabla\cdot\mathbf u=0$。这个论证明确了为何“任意区域”和“足够光滑”不可省略。

## 推导二：动量方程与本构闭合

对第 $i$ 个动量分量作同样局部化：$\partial_t(\rho u_i)+\partial_j(\rho u_iu_j)=\partial_j\sigma_{ij}+\rho g_i$。重复指标 $j$ 表示从 1 到 3 求和。展开左侧并用连续方程消去 $u_i[\partial_t\rho+\partial_j(\rho u_j)]$，剩下 $\rho Du_i/Dt$，得到 Cauchy 方程。

代入不可压牛顿应力 $\sigma_{ij}=-p\delta_{ij}+\mu(\partial_ju_i+\partial_iu_j)$。若 $\mu$ 恒定，$\partial_j\sigma_{ij}=-\partial_ip+\mu\partial_j\partial_ju_i+\mu\partial_i(\nabla\cdot\mathbf u)$，最后项为零。因此
$$\rho\big[\partial_t\mathbf u+(\mathbf u\cdot\nabla)\mathbf u\big]=-\nabla p+\mu\nabla^2\mathbf u+\rho\mathbf g.$$
若黏度随位置变化，不能把 $\mu$ 直接提出导数；若可压缩，还须保留体积变形项、能量方程和状态关系。

## 求解条件与不能推出的结论

指定区域、物性、入口或壁面条件，非稳态另给与不可压约束相容的初始速度。常见固壁为无滑移/无穿透；压力只通过梯度进入时需选择参考值。不能在同一边界任意同时指定全部速度和压力。方程写出来不意味着一定有简单解析解，更不等于证明三维所有初值均存在光滑全局解。

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
