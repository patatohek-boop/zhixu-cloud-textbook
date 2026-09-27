---json
{
  "id": "fluid-mechanics-19",
  "title": "势流、流函数、环量与涡量",
  "group": "06 · 进阶流动模型",
  "summary": "把漂亮的数学解与真实的物理边界区分开。",
  "objectives": [
    "准确解释势函数",
    "在列明条件后复现本章推导，并用例题检验结论"
  ],
  "prerequisites": [
    "fluid-mechanics-29",
    "fluid-mechanics-18"
  ],
  "tags": [
    "势流、流函数、环量与涡量",
    "使用速度势和流函数",
    "辨别无旋与无环量的差别"
  ],
  "minutes": 40,
  "level": "进阶",
  "quiz": {
    "question": "二维流函数定义 u=ψᵧ、v=−ψₓ 自动保证什么？",
    "options": [
      "所有动量方程",
      "不可压连续方程",
      "所有固壁无滑移条件",
      "流体无黏"
    ],
    "answer": 1,
    "explanation": "混合偏导相等时 uₓ+vᵧ=ψᵧₓ−ψₓᵧ=0。"
  },
  "lab": "",
  "revision": "2026-09 · 定义与推导修订"
}
---

## 严谨定义：势与流函数承担不同约束

速度势 $\phi$ 满足 $\mathbf u=\nabla\phi$。二维流函数 $\psi$ 定义为 $u=\psi_y,v=-\psi_x$。涡量 $\boldsymbol\omega=\nabla\times\mathbf u$，环量 $\Gamma=\oint_C\mathbf u\cdot d\mathbf l$。**简单连通**在本节指闭曲线可在定义域内连续收缩到一点，没有被排除的洞或涡核阻挡。

势函数的全局单值存在性，需要速度足够光滑、无旋和适当的区域拓扑条件。流函数主要编码二维质量守恒，不自动满足动量方程。这里所有偏导交换均假设所涉函数有连续二阶偏导。

## 通俗解释：一个记“沿路累积”，一个记“横穿流量”

沿速度方向积分可构造势；跨越流线累积的流量可用流函数记录。两者是帮助表示速度的数学工具，不能凭存在一个函数就认为固壁无滑移、压力或力都已经求出。

## 证明：各个结论的条件从哪里来

在无旋、简单连通的光滑区域，以固定点 $P_0$ 定义 $\phi(P)=\int_{P_0}^P\mathbf u\cdot d\mathbf l$。两条路径之差是一条闭曲线；由 Stokes 定理，其积分为所围曲面上旋度通量，等于零。因此路径无关。沿各坐标微移求导得 $\partial_i\phi=u_i$。若再不可压缩，$\nabla\cdot\mathbf u=\nabla^2\phi=0$。

由流函数定义，$u_x+v_y=\psi_{yx}-\psi_{xy}=0$，故它自动满足二维不可压连续方程。沿流线 $dx/ds=u,dy/ds=v$，有 $d\psi/ds=\psi_xu+\psi_yv=(-v)u+uv=0$，所以规则等值线是流线。对于从 $P$ 到 $Q$ 的有向曲线，取法向为路径顺时针转90度，则单位厚度流量为 $\int(u\,dy-v\,dx)=\int d\psi=\psi(Q)-\psi(P)$。

若势和流函数都存在，$\nabla\phi\cdot\nabla\psi=(u,v)\cdot(-v,u)=0$；在梯度非零处，其等值线正交。停滞点不能由零向量谈唯一的交角。

**反例。**在排除原点的平面，$u_\vartheta=\Gamma/(2\pi r)$ 的局部旋度为零，但绕原点积分仍为 $\Gamma$。绕洞的曲线无法在该区域内围出避开洞的完整曲面，不能违反 Stokes 的定义域条件来制造矛盾；角度势可以多值。

## 非定常势流伯努利的推导

常密度无黏势流代入 Euler 方程：$\partial_t\nabla\phi+\nabla(|\nabla\phi|^2/2)=-\nabla(p/\rho+gz)$，因此连通域中 $\partial_t\phi+|\nabla\phi|^2/2+p/\rho+gz=C(t)$。空间梯度为零只说明它可随时间变化；非稳态时不能随意删去 $\partial_t\phi$。Laplace 方程的线性允许势叠加，但构造出的速度必须重新检查边界条件，伯努利求压力时仍有速度平方的非线性。

## 例题：均匀流的两种表示
二维均匀流 $u=U,v=0$。可以选 $\phi=Ux$、$\psi=Uy$。取偏导后得到原速度。速度势等值线为 x=常数的竖直线，流函数等值线为 y=常数的水平线，彼此正交。

若 U=2 m/s，两条水平流线相距 0.3 m，则 $\Delta\psi=U\Delta y=0.6\,\mathrm{m^2/s}$。乘上垂直纸面的实际宽度才得到 m³/s 的体积流量。

## 练习
1. $\psi=axy$ 对应的二维速度是什么？
<details><summary>查看解析</summary>

$u=ax$，$v=-ay$；散度为 a−a=0。这是拉伸与压缩组合的局部流场。
</details>

2. 零涡量是否必定意味着任何闭合回路环量都为零？
<details><summary>查看解析</summary>

要检查定义域和奇点。简单连通且速度光滑的无旋区域可以；排除涡核的多连通区域则不必然。
</details>
