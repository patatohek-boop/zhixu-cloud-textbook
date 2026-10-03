---json
{
  "id": "calculus-19",
  "title": "三重积分与坐标变换",
  "group": "07 · 积分与场",
  "minutes": 55,
  "level": "进阶",
  "tags": [
    "三重积分",
    "Jacobian",
    "柱坐标与球坐标"
  ],
  "objectives": [
    "准确区分三重积分、Jacobian、柱坐标与球坐标并写清适用条件",
    "逐步复现线性换元证明与一般定理的证明入口",
    "独立完成例题与练习，并用反例检验条件"
  ],
  "prerequisites": [
    "calculus-18"
  ],
  "summary": "换坐标要同时改变区域、函数和体积微元。",
  "quiz": {
    "question": "坐标换元后为什么要乘 Jacobian 的绝对值？",
    "options": [
      "消除所有积分限",
      "保证结果为整数",
      "补偿局部体积缩放",
      "使函数一定为正"
    ],
    "answer": 2,
    "explanation": "坐标格子映到实际空间后体积会变化，雅可比给出局部缩放。"
  },
  "lab": null
}
---

## 严谨定义：体积积分与雅可比

### 体积积分

三重黎曼积分 $\iiint_Df\,dV$ 是“取点函数值乘小体积”的共同极限，本节区域有界、边界零体积、函数连续。

### 雅可比矩阵与行列式

坐标变换 $T:U\to V$ 的雅可比矩阵 $DT$ 由 $\partial T_i/\partial u_j$ 组成，雅可比行列式 $J_T=\det DT$。

### 换元定理的单次覆盖条件

$C^1$ 微分同胚指 $T$ 是双射，$T$ 及其逆都连续可导。常用换元定理要求这种单次、非退化的覆盖：
$$\int_{T(D)} f(x)\,dx=\int_D f(T(u))\,|\det DT(u)|\,du.$$
这里 $dx,du$ 分别表示相应维数的面积或体积元，而非单独一个坐标差。

## 通俗解释：新坐标格子的真实大小不同
角度增加同样一小格，在离原点较远处对应更长的弧，因此面积要多乘半径。雅可比把“参数空间的一格”换算成真实空间的一格；负行列式表示方向翻转，面积体积仍用绝对值。

## 线性换元证明与一般定理的证明入口
对可逆线性变换 $x=Au$，线性代数的[行列式体积定理](#/course/linear-algebra/linear-algebra-09)给每个小平行六面体的体积为 $|\det A|$ 乘原小盒体积。把区域分割、取点，相应两侧有限和逐项相等；边界小块误差由有界函数乘边界覆盖体积控制而趋零，取极限即得换元公式。平移不改变体积，所以仿射变换也成立。

一般 $C^1$ 换元还需要证明小盒像的体积误差相对于原盒体积一致趋零。完整的紧致误差控制、收缩映射体积夹逼和黎曼和极限证明见紧接本节的[换元与曲面面积证明](#/course/calculus/calculus-31)。该补充章给出连续函数、有界 Jordan 区域、单射非退化 $C^1$ 变换下的完整证明；本节先对常用极、柱、球坐标直接推导微元，便于计算时理解每个因子。

## 极、柱、球坐标微元的直接证明

### 极坐标：先求小环扇形精确面积

极坐标小格 $r_1\le r\le r_2,\theta_1\le\theta\le\theta_2$ 的真实面积由圆环扇形公式精确等于
$\tfrac12(r_2^2-r_1^2)(\theta_2-\theta_1)$。
中值定理将它写成 $r_*\Delta r\Delta\theta$，$r_*$ 位于两半径之间。分格后连续函数的取点差由一致连续性控制，极限即 $dA=r\,dr\,d\theta$；柱坐标再乘高度 $\Delta z$，得 $dV=r\,dr\,d\theta\,dz$。

### 球坐标：先固定两个角的含义

球坐标取 $\rho\ge0$、极角 $0\le\phi\le\pi$（从正 $z$ 轴量起）、方位角 $\theta$：
$x=\rho\sin\phi\cos\theta,y=\rho\sin\phi\sin\theta,z=\rho\cos\phi$。
可以从已证柱坐标 $(r,z,\theta)$ 出发，在子午平面用二维极坐标 $r=\rho\sin\phi,z=\rho\cos\phi$；其平面面积元为 $\rho\,d\rho\,d\phi$，原柱坐标权重 $r$ 变为 $\rho\sin\phi$，所以总体积元为 $\rho^2\sin\phi\,d\rho\,d\phi\,d\theta$。这直接给出本节全部球积分的依据。

**条件失效。** 极轴或原点 $J=0$，不属于微分同胚点；可把半径、角度端点先截去，再令截去区域体积趋零处理。角度取两整周则重复覆盖，公式会算两次。

## 配图：把定义与几何对应起来

<figure class="teaching-figure"><a href="assets/diagrams/jacobian-area.svg" target="_blank" rel="noopener" aria-label="打开大图：变换 x=2u+v、y=v 将单位正方形变为面积为 2 的平行四边形；Jacobian 行列式为 2。"><img src="assets/diagrams/jacobian-area.svg" alt="变换 x=2u+v、y=v 将单位正方形变为面积为 2 的平行四边形；Jacobian 行列式为 2。" loading="lazy"></a><figcaption>变换 x=2u+v、y=v 将单位正方形变为面积为 2 的平行四边形；Jacobian 行列式为 2。<br><small>两个坐标系使用相同单位尺度。变换为可逆线性映射，J=[[2,1],[0,1]]，dA=|det J| du dv=2 du dv。 · 点按图形可放大。</small></figcaption></figure>

## 逐步例题：计算半径为二的球体积
第一步利用球对称性选球坐标。半径从零到二，极角从零到 $\pi$，方位角从零到 $2\pi$。

第二步写被积函数为一，但体积微元不能忘记平方半径与正弦因子。

第三步分离三个积分：半径部分为 $8/3$，极角部分为二，方位角部分为 $2\pi$。相乘得到 $32\pi/3$。

第四步与球体积公式核对，二者一致。

若忘记雅可比而只把三个参数范围相乘，就会得到带错误长度次方的结果。这说明雅可比不是形式上的修正，而是把参数格子换算成真实空间小体积的必要步骤。

## 易错点与应用
三重积分不总表示体积，密度积分给质量，位置加权积分可给质心，到转轴距离平方乘质量密度的积分给转动惯量。写惯量时应使用到指定轴的距离，不是到原点的距离。选择坐标后先列范围，再写微元，最后代入被积函数，这个固定顺序能减少遗漏。积分完成后检查量纲以及半径增大时的尺度律：均匀体积应随长度三次方增长，惯量还多出距离平方。

<!-- math-revision-20261003:mixed-solid-bounds:start -->
## 完整案例：抛物面与平面之间的立体

接续[截痕与投影](#/course/calculus/calculus-14)，求 $D=\{x^2+y^2\le z\le4\}$ 的体积。先把表面、投影和积分次序分开。

1. **交线给投影。** 两边界相交于 $x^2+y^2=4,z=4$；向 $xy$ 平面投影为半径 $2$ 的圆盘
2. **选择坐标。** 柱坐标 $x=r\cos\theta,y=r\sin\theta$ 把下面写成 $z=r^2$，上面仍是 $z=4$
3. **固定外层再读内层。** 当 $0\le\theta\le2\pi,0\le r\le2$，竖线上的 $z$ 从 $r^2$ 到 $4$。体积元为 $r\,dz\,dr\,d\theta$，不能把 Jacobian 的 $r$ 漏掉。轴线和角度接缝处的重复是零体积边界，不影响积分

<figure class="teaching-figure"><a href="assets/diagrams/math-paraboloid-bounds.svg" target="_blank" rel="noopener" aria-label="打开大图：柱坐标的 r–z 截面：0≤r≤2，r²≤z≤4；在 r=1 处竖直线段从 z=1 到 z=4。灰色区域是截面，绕 z 轴转一周才得到立体。"><img src="assets/diagrams/math-paraboloid-bounds.svg" alt="柱坐标的 r–z 截面：0≤r≤2，r²≤z≤4；在 r=1 处竖直线段从 z=1 到 z=4。灰色区域是截面，绕 z 轴转一周才得到立体。" loading="lazy"></a><figcaption>柱坐标的 r–z 截面：0≤r≤2，r²≤z≤4；在 r=1 处竖直线段从 z=1 到 z=4。灰色区域是截面，绕 z 轴转一周才得到立体。 · 点按图形可放大。</figcaption></figure>

$$V=\int_0^{2\pi}\int_0^2\int_{r^2}^4r\,dz\,dr\,d\theta
=2\pi\int_0^2(4-r^2)r\,dr=8\pi.$$

**独立换序检查。** 固定高度 $0\le z\le4$ 时，横截面圆盘半径为 $\sqrt z$、面积为 $\pi z$，所以 $V=\int_0^4\pi z\,dz=8\pi$。不是先背上下限，而是每次都回答“固定外层变量后，内层从哪儿走到哪儿”。

### 练习 M10：改变高度并加入密度

全部坐标取无量纲值。对 $D_3=\{x^2+y^2\le z\le3\}$，先计算体积，再对密度函数 $\rho(x,y,z)=z$ 计算质量 $M=\iiint_{D_3}\rho\,dV$。用竖直线与水平圆盘两种切法分别列式并复算质量。

<details><summary>查看完整解析与检查</summary>

交线给 $r=\sqrt3$，故 $0\le\theta\le2\pi,0\le r\le\sqrt3,r^2\le z\le3$。体积为
$$V=2\pi\int_0^{\sqrt3}(3-r^2)r\,dr=\frac{9\pi}{2}.$$
质量须再乘 $z$，不是把密度当成恒定顶面值：
$$M=2\pi\int_0^{\sqrt3}\int_{r^2}^3zr\,dz\,dr
=\pi\int_0^{\sqrt3}(9-r^4)r\,dr=9\pi.$$
独立按高度切片：$z\in[0,3]$，每片面积 $\pi z$，密度在该片恒为 $z$，故 $M=\int_0^3z(\pi z)\,dz=9\pi$。平均密度 $M/V=2$ 位于最小 $0$ 与最大 $3$ 之间，提供额外量级检查。

</details>
<!-- math-revision-20261003:mixed-solid-bounds:end -->

## 练习
1. 用极坐标计算单位圆盘面积。
<details><summary>查看解析</summary>

积分为 $\int_0^{2\pi}\int_0^1r\,dr\,d\theta=\pi$，额外的半径因子不可省略。
</details>

2. 变换 $x=2u,y=3v$ 的面积缩放因子是多少？
<details><summary>查看解析</summary>

雅可比矩阵为对角矩阵，对角元素二和三，行列式绝对值为六，因此面积微元变为六倍。
</details>
