---json
{
  "id": "fluid-mechanics-36",
  "title": "应力、变形率与牛顿流体：从受力面到方程",
  "group": "04 · 从守恒到流场",
  "summary": "定义每一个应力分量，证明牵引和对称关系，再区分变形、旋转与材料本构。",
  "objectives": [
    "按面方向和力方向解释张量指标并执行一次牵引计算",
    "区分由守恒推出的应力性质与实验本构，验证变形、旋转和耗散"
  ],
  "prerequisites": [
    "fluid-mechanics-06",
    "fluid-mechanics-10"
  ],
  "tags": [
    "面力与应力张量",
    "Cauchy牵引定理",
    "角动量与应力对称",
    "变形率与刚体旋转",
    "剪切黏度和体积黏度"
  ],
  "minutes": 70,
  "level": "基础",
  "quiz": {
    "question": "纯刚体转动的牛顿黏性应力如何？",
    "options": [
      "速度梯度非零所以必非零",
      "变形率为零，所以黏性应力为零",
      "压力也必为零"
    ],
    "answer": 1,
    "explanation": "牛顿黏性应力由对称变形率决定，不能把单个速度梯度直接当一般剪切率。"
  },
  "lab": null,
  "revision": "2026-09-28 · 概念分段与教学审读"
}
---

## 严谨定义：应力需要说明两个方向

### 牵引、法向与切向分量

在流体内想象切出一个小面。外侧流体作用于所选一侧的单位面积力称为**牵引向量** $\mathbf t(\mathbf n)$，其中单位法线 $\mathbf n$ 指向所选体积外侧，单位为 Pa。$\mathbf t\cdot\mathbf n$ 是法向应力，$\mathbf t-(\mathbf t\cdot\mathbf n)\mathbf n$ 是切向牵引。压力取压缩为正，所以静止简单流体有 $\mathbf t=-p\mathbf n$。

### 应力分量的两个指标

在直角坐标中，定义 $\sigma_{ij}$ 为“法线沿第 $j$ 轴的面上，牵引沿第 $i$ 轴的分量”。例如 $\sigma_{12}$ 是 $y$ 法向面上的 $x$ 向力密度。

### 张量与坐标表示

把九个分量组成矩阵 $\boldsymbol\sigma$，就得到二阶应力张量；**张量**在这里是把面法线线性映射为牵引的物理对象，换坐标时矩阵分量会相应变化，不是九个任意互不相关的数。

### 偏导与重复指标求和

记 $\partial_j u_i=\partial u_i/\partial x_j$；重复指标意味着从1到3求和，例如 $\sigma_{ij}n_j=\sum_{j=1}^3\sigma_{ij}n_j$。

### 单位矩阵与 Kronecker 符号

$\delta_{ij}$ 为 Kronecker 符号，同指标时为1，否则为0；矩阵形式就是单位矩阵 $\mathbf I$。

### 矩阵的迹

**迹** $\operatorname{tr}\mathbf A$ 是方阵对角线元素之和。

## 通俗解释：先说明在哪个面上，再说明往哪边推

同一点的不同朝向截面会受到不同方向的力。只说“这里应力是10 Pa”往往信息不够，就像只说一个盒子受力而没有说推哪一面。压力是很特殊的情形：无论切面朝哪里，力都垂直向内；流动中的黏性作用还会沿面拖动，也可能改变法向受力。

## 证明一：为什么任意面的牵引等于应力矩阵乘法线

### 第一步：列清局部假设并证明反向牵引

采用经典连续介质假设：面力由该处状态和面法线决定，考察点邻域内的应力、体积力与加速度连续且有界，内部没有额外的表面质量，且不跨越应力跳跃界面。

先用极薄的小柱跨过同一点的两侧面。两大面面积为 $A$，侧面面积和体积随厚度趋零；动量平衡除以 $A$ 后取极限，得到 $\mathbf t(-\mathbf n)=-\mathbf t(\mathbf n)$。

### 第二步：对小四面体写动量平衡

再取三面与坐标面平行、第四面法线为 $\mathbf n$ 的小四面体。先令三个 $n_j>0$。斜面面积为 $A$，三个坐标面的投影面积分别为 $A n_j$，其外法线为 $-\mathbf e_j$。

特征边长为 $\epsilon$ 时，面力是 $O(\epsilon^2)$，体积力和惯性是 $O(\epsilon^3)$。动量方程除以 $A$ 并令 $\epsilon\to0$，得到
$$\mathbf t(\mathbf n)-\sum_{j=1}^3 n_j\mathbf t(\mathbf e_j)=0.$$

### 第三步：从分量式回到矩阵式

取第 $i$ 分量即 $t_i=\sigma_{ij}n_j$。其他法线象限可用对应正负坐标面并结合反向牵引关系处理；零分量由连续极限得到。因此 $\mathbf t=\boldsymbol\sigma\mathbf n$。这是一条由局部动量平衡推出的结论，尚未使用牛顿黏性本构。

## 证明二：应力对称来自角动量守恒

考虑以中心为原点、各边长为 $\epsilon$ 的小立方体，忽略独立体偶矩与偶应力。两 $y$ 面上的 $x$ 向剪切形成绕 $z$ 轴的力矩 $-\sigma_{12}\epsilon^3$，两 $x$ 面上的 $y$ 向剪切给 $+\sigma_{21}\epsilon^3$。光滑场的应力变化给更高阶项；有界体积力和惯性关于中心的总力矩也高于这一阶。角动量平衡因此给 $(\sigma_{21}-\sigma_{12})\epsilon^3=o(\epsilon^3)$，除以体积取极限，得 $\sigma_{12}=\sigma_{21}$。另两对坐标同理。

所以普通非极性连续介质中 $\boldsymbol\sigma$ 对称。若研究带独立微旋转、体偶矩或偶应力的介质，必须扩展角动量方程，不能不加说明照搬这个结论。应力对称也不意味着三个主应力相同。

## 证明三：速度梯度怎样分成变形和旋转

相邻两个质点的间隔 $\mathbf r$ 足够小时，其相对速度一阶为 $\dot{\mathbf r}=\mathbf A\mathbf r$，$A_{ij}=\partial_j u_i$。把矩阵唯一拆成
$$\mathbf D=\frac{\mathbf A+\mathbf A^T}{2},\qquad \mathbf W=\frac{\mathbf A-\mathbf A^T}{2},\qquad\mathbf A=\mathbf D+\mathbf W.$$

### 检验：哪一部分改变质点间距离

因为反对称矩阵满足 $\mathbf r^T\mathbf W\mathbf r=0$，有 $d|\mathbf r|^2/dt=2\mathbf r^T\mathbf D\mathbf r$。因此 $\mathbf D$ 决定局部长度和夹角的变化率，称**变形率张量**；$\mathbf W$ 只对应瞬时刚体旋转。逐分量比较可得 $\mathbf W\mathbf r=(\boldsymbol\omega/2)\times\mathbf r$，局部刚体角速度等于涡量的一半。

### 反例比较：剪切与纯转动

例如简单剪切 $\mathbf u=(ay,0,0)$ 中，$D_{12}=D_{21}=a/2$，$\omega_z=-a$，既有变形也有旋转。纯刚体转动 $\mathbf u=(-\Omega y,\Omega x,0)$ 则 $\mathbf D=0$、$\omega_z=2\Omega$；速度梯度非零并不必然产生牛顿黏性应力。

## 材料模型：牛顿本构及可压缩时多出来的一项

对简单各向同性牛顿流体，采用瞬时线性本构
$$\boldsymbol\sigma=-p\mathbf I+2\mu\mathbf D+\lambda(\nabla\cdot\mathbf u)\mathbf I.$$
$p$ 是局部热力学压力，$\mu$ 是剪切动力黏度，$\lambda$ 是第二黏度系数。材料各向同性、响应线性和无记忆是模型假设；材料是否符合、系数多少要由实验判断，不能靠数学把它们证明成所有流体的规律。

定义体积膨胀率 $\theta=\operatorname{tr}\mathbf D=\nabla\cdot\mathbf u$，无迹部分 $\mathbf D'=\mathbf D-\theta\mathbf I/3$，以及体积黏度 $\zeta=\lambda+2\mu/3$，则黏性应力 $\boldsymbol\tau=2\mu\mathbf D'+\zeta\theta\mathbf I$。把 $\tau_{ij}\partial_j u_i$ 展开，利用对称与反对称正交、$\operatorname{tr}\mathbf D'=0$，得到
$$\Phi=\boldsymbol\tau:\mathbf D=2\mu\sum_{i,j}(D'_{ij})^2+\zeta\theta^2.$$
冒号表示逐元素乘积再求和。对被动耗散的该模型，$\mu\ge0,\zeta\ge0$ 使 $\Phi\ge0$。这给条件下的耗散结论；$\lambda$ 本身可以为负。Stokes 假设 $\lambda=-2\mu/3$ 等价于令 $\zeta=0$，是额外近似，不等于“牛顿流体”的定义。

不可压时 $\theta=0$，便回到 $\boldsymbol\sigma=-p\mathbf I+2\mu\mathbf D$。在这个约束模型里压力承担维持无散条件的作用；有界区域只给速度边界时，往往还需指定压力参考值。

## 例题：从速度场算真正的面力

流场 $u=3y,v=w=0$，$y$ 单位m，系数3单位s⁻¹；$\mu=0.2$ Pa·s，$p=100$ Pa。先求 $D_{12}=D_{21}=1.5$ s⁻¹，故 $\tau_{12}=\tau_{21}=0.6$ Pa。对 $\mathbf n=(0,1,0)$ 的面，有 $\mathbf t=(0.6,-100,0)$ Pa：压力向内，黏性力沿 $x$ 方向。若面积0.01 m²且各量均匀，合力为 $(0.006,-1,0)$ N。

1. 把法线反向，同一切面另一侧的牵引是什么？
<details><summary>查看解析</summary>

$\mathbf t(-\mathbf n)=-\boldsymbol\sigma\mathbf n=(-0.6,100,0)$ Pa。不要只反转压力而忘记切向分量。
</details>

2. 对纯刚体转动，能否直接用 $\tau_{xy}=\mu\partial_yu$ 求剪切应力？
<details><summary>查看解析</summary>

不能。一般式为 $\tau_{xy}=\mu(\partial_yu+\partial_xv)$；两项 $-\Omega$ 和 $+\Omega$ 相消。只有 $v_x=0$ 等额外条件满足时，才退化为平行剪切的简式。
</details>

## 讲义对照与后续阅读

本章用于补足“受力描述→材料关系→场方程”的先修链。可对照 [MIT 2.20 Lecture 3：应力与守恒](https://ocw.mit.edu/courses/2-20-marine-hydrodynamics-13-021-spring-2005/resources/lecture3/) 和 [Lecture 4：牛顿流体与边界](https://ocw.mit.edu/courses/2-20-marine-hydrodynamics-13-021-spring-2005/resources/lecture4/) 的主题；此处符号、算例与叙述独立编写。
