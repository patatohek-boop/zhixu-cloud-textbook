---json
{
  "id": "fluid-mechanics-06",
  "title": "流场、流线与物质导数",
  "group": "03 · 描述与守恒",
  "summary": "固定位置的变化和随流体运动的变化并不相同。",
  "objectives": [
    "区分欧拉与拉格朗日描述以及流线、迹线、脉线",
    "用链式法则推出物质导数，逐项计算局部和对流加速度"
  ],
  "prerequisites": [
    "fluid-mechanics-29",
    "fluid-mechanics-05"
  ],
  "tags": [
    "流场、流线与物质导数",
    "区分欧拉与拉格朗日描述",
    "计算局部与对流加速度"
  ],
  "minutes": 40,
  "level": "基础",
  "quiz": {
    "question": "稳态流动是否可能存在加速度？",
    "options": [
      "不可能",
      "只有温度变化才可能",
      "可能，因为存在对流加速度",
      "只有黏度为零才可能"
    ],
    "answer": 2,
    "explanation": "流体运动到速度不同的位置时，其速度仍会改变，即使固定位置的流场不随时间变化。"
  },
  "lab": null,
  "revision": "2026-09-28 · 概念分段与教学审读"
}
---

## 严谨定义：谁在观察，谁在变化

### 欧拉描述：在固定位置观察

欧拉速度场 $\mathbf u(\mathbf x,t)$ 给出固定位置 $\mathbf x=(x,y,z)$ 在时刻 $t$ 的速度。

### 拉格朗日描述：跟随同一质点

一个标记质点的位置为 $\mathbf X(t)$，满足 $d\mathbf X/dt=\mathbf u(\mathbf X(t),t)$，这是拉格朗日轨迹方程。$\partial/\partial t$ 表示固定空间位置取导数；$D/Dt$ 表示沿同一质点取导数。

### 空间微分算子

对标量场 $f$，梯度 $\nabla f=(f_x,f_y,f_z)$；散度 $\nabla\cdot\mathbf u=u_x+v_y+w_z$ 表示局部体积膨胀率；涡量 $\boldsymbol\omega=\nabla\times\mathbf u$，二维时 $\omega_z=v_x-u_y$。下标 $x,y,z$ 在这里表示相应偏导数，而非乘法。

### 流线：同一时刻的方向

**流线**是在固定时刻 $t_0$ 满足 $d\mathbf x/ds\parallel\mathbf u(\mathbf x,t_0)$ 的曲线，$s$ 是曲线参数。

### 迹线与脉线：区分追踪对象

**迹线**是同一质点的 $\mathbf X(t)$。**脉线**是在不同释放时刻经过某固定注入点、于同一观察时刻所处位置的集合。停滞点速度为零时，流线方向需要另外讨论，不能简单除以零。

## 通俗解释：摄像头不动，叶子在动

桥上摄像头拍固定位置，是欧拉视角；给一片叶子装跟踪器，是拉格朗日视角。一片叶子从慢流区进入快流区会加速，即便整张流速地图每秒都一样，所以“稳态”不等于“没有加速度”。

## 证明：物质导数来自多元链式法则

沿质点轨迹观察 $f(\mathbf X(t),t)$，逐项求导：
$$\frac{d}{dt}f(\mathbf X(t),t)=\frac{\partial f}{\partial t}+\sum_{i=1}^3\frac{\partial f}{\partial x_i}\frac{dX_i}{dt}=\frac{\partial f}{\partial t}+\mathbf u\cdot\nabla f.$$
以每个速度分量代入 $f$，得到 $\mathbf a=\partial_t\mathbf u+(\mathbf u\cdot\nabla)\mathbf u$，不是把 $D/Dt$ 当成可以随意约分的符号。该链式推导要求所用场和轨迹可微。

稳态时 $\mathbf u$ 不显含时间。流线方程和迹线方程便由同一自治向量场决定；在速度局部光滑、轨迹唯一、非停滞的区域，经过同一点的两条积分曲线相同，因此迹线沿流线行进。持续从固定点放出的质点也沿这条曲线，故脉线与之重合。非稳态时三个方程的时间条件不同，不能沿用这个结论。

局部线性化为 $\delta\mathbf u=\mathbf L\delta\mathbf x$，分解 $\mathbf L=\mathbf D+\mathbf W$，$\mathbf D=(\mathbf L+\mathbf L^T)/2$ 对称，$\mathbf W=(\mathbf L-\mathbf L^T)/2$ 反对称。直接比较叉积各分量可得 $\mathbf W\delta\mathbf x=(\boldsymbol\omega/2)\times\delta\mathbf x$，所以局部刚体旋转率是 $\boldsymbol\omega/2$；$\mathbf D$ 则改变长度和夹角。弯曲流线不等于局部流体微团旋转。

## 例题：稳态收缩流中的加速度
设一维局部速度模型 $u(x)=2x$，其中 $x$ 以米计，系数 2 的单位为 s⁻¹。流场不显含时间，因此局部加速度为零。但 $du/dx=2\,\mathrm{s^{-1}}$，所以 $a_x=u\,du/dx=4x$。在 $x=1\,\mathrm m$ 处，速度为 2 m/s，加速度为 4 m/s²。

这个表达只是局部运动学模型；若它被解释成恒截面、不可压的一维通道流，会违反连续性。实际收缩流道中横向速度或截面积变化提供了质量守恒。一个数学速度场是否符合物理，还必须检查质量、动量和边界条件。

## 练习
1. $u=3t$、空间上均匀，流体加速度是多少？
<details><summary>查看解析</summary>

$\partial u/\partial t=3\,\mathrm{m/s^2}$，空间梯度为零，所以加速度为 3 m/s²。
</details>

2. 二维速度 $u=-\Omega y,v=\Omega x$ 的涡量是多少？
<details><summary>查看解析</summary>

$\omega_z=\partial v/\partial x-\partial u/\partial y=2\Omega$，正是角速度的两倍。这是刚体旋转，变形率为零。
</details>
