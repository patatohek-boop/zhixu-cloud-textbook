---json
{
  "id": "linear-algebra-18",
  "title": "奇异值分解 SVD",
  "group": "06 · 复数与奇异值",
  "minutes": 60,
  "level": "进阶",
  "tags": [
    "奇异值分解",
    "输入输出方向",
    "矩阵秩"
  ],
  "objectives": [
    "准确区分奇异值分解、输入输出方向、矩阵秩并写清适用条件",
    "逐步复现SVD 存在性的完整构造证明",
    "独立完成例题与练习，并用反例检验条件"
  ],
  "prerequisites": [
    "linear-algebra-17"
  ],
  "summary": "任何矩阵都可拆成正交换方向、按轴伸缩、再正交换方向。",
  "quiz": {
    "question": "SVD 中右奇异向量属于哪里？",
    "options": [
      "输出空间总是如此",
      "只属于复数空间",
      "只属于零空间",
      "输入空间"
    ],
    "answer": 3,
    "explanation": "矩阵先作用于右奇异方向，再产生对应的左奇异方向输出。"
  },
  "lab": "matrix"
}
---

## 严谨定义：完整 SVD、奇异值和左右方向

### 完整 SVD 的三种尺寸

对 $A\in\mathbb R^{m\times n}$，完整奇异值分解写 $A=U\Sigma V^\mathsf T$，其中 $U$ 是 $m$ 阶正交矩阵，$V$ 是 $n$ 阶正交矩阵，$\Sigma$ 是 $m\times n$ 非负对角型矩阵。

### 奇异值排序与左右方向

正奇异值记 $\sigma_1\ge\cdots\ge\sigma_r>0$，余下对角为零；右方向 $v_i\in\mathbb R^n$，左方向 $u_i\in\mathbb R^m$，$Av_i=\sigma_i u_i$。这里 $r=\operatorname{rank}A$，要由证明得到。

## 通俗解释：输入和输出各自换一把正交尺子
特征向量试图留在同一个方向，长方形矩阵甚至输入输出维数都不同。SVD 允许一边一套方向，中间只负责按非负长度伸缩，因此适用于任何矩阵。

## SVD 存在性的完整构造证明

### 第一步：对输入侧半正定矩阵用谱定理

$B=A^\mathsf TA$ 对称且 $x^\mathsf TBx=\|Ax\|^2\ge0$。由[谱定理](#/course/linear-algebra/linear-algebra-15)，有标准正交特征基 $v_1,\ldots,v_n$、非负特征值。将正的排前面并写成 $\sigma_i^2$。

### 第二步：构造输出侧的单位方向

对 $i\le r$ 定义 $u_i=Av_i/\sigma_i$。则
$$u_i^\mathsf Tu_j
=\frac{v_i^\mathsf TA^\mathsf TAv_j}{\sigma_i\sigma_j}
=\frac{\sigma_j^2}{\sigma_i\sigma_j}v_i^\mathsf Tv_j
=\delta_{ij}.$$
所以这些输出方向单位正交，特别地 $r\le m$。

### 第三步：处理不能相除的零奇异方向

对零特征值方向，$\|Av_i\|^2=v_i^\mathsf TBv_i=0$，故 $Av_i=0$。任意 $x=\sum_i(v_i^\mathsf Tx)v_i$ 因而满足
$$Ax=\sum_{i=1}^r\sigma_i u_i(v_i^\mathsf Tx).$$
所以列空间恰由 $u_1,\ldots,u_r$ 张成、其维数为 $r$。

### 第四步：补齐输出基并得到完整矩阵

用基扩充后正交化将 $u_i$ 补成 $\mathbb R^m$ 的标准正交基，排成 $U$；$v_i$ 排成 $V$，上式便是 $A=U\Sigma V^\mathsf T$，证明完成。复数版把转置换成共轭转置，使用 Hermitian 谱定理同证。

## 长度、秩与四个空间的推论：证明
若 $A=0$，全部方向输出为零，算子范数为零；下面涉及 $\sigma_1$ 的最大伸缩结论针对 $r\ge1$。由 $\|Ax\|^2=\sum_{i\le r}\sigma_i^2(v_i^\mathsf Tx)^2$，单位 $x$ 的最大输出长度是 $\sigma_1$，在 $v_1$ 取到。$v_{r+1},\ldots,v_n$ 构成零空间基；$v_1,\ldots,v_r$ 构成行空间基；$u_1,\ldots,u_r$ 是列空间基；其余 $u$ 是左零空间基。因为所有输出都与后者正交，这些结论直接还原四空间结构。

若 $A$ 实对称，谱分解使 $A^\mathsf TA=A^2$ 的特征值为 $\lambda_i^2$，所以奇异值为 $|\lambda_i|$。一般矩阵则没有这种简单关系。

**反例。** $A=\begin{pmatrix}0&1\\0&0\end{pmatrix}$ 两个特征值都为零，却有奇异值 $1,0$。特征值零不代表矩阵不伸缩任何向量，SVD 才直接描述长度。

## 配图：把定义与几何对应起来

<figure class="teaching-figure"><a href="assets/diagrams/svd-ellipse.svg" target="_blank" rel="noopener" aria-label="打开大图：单位圆先经 Vᵀ 旋转后仍为圆，再被 Σ=diag(2,1) 变为半轴 2 与 1 的椭圆，最后经 U 旋转 30°。"><img src="assets/diagrams/svd-ellipse.svg" alt="单位圆先经 Vᵀ 旋转后仍为圆，再被 Σ=diag(2,1) 变为半轴 2 与 1 的椭圆，最后经 U 旋转 30°。" loading="lazy"></a><figcaption>单位圆先经 Vᵀ 旋转后仍为圆，再被 Σ=diag(2,1) 变为半轴 2 与 1 的椭圆，最后经 U 旋转 30°。<br><small>二维示例，Vᵀ=R(−30°)、U=R(30°)。三个阶段采用同一尺度 30 像素/单位。完整 SVD 也允许正交反射；本图用旋转便于理解。 · 点按图形可放大。</small></figcaption></figure>

## 逐步例题：一个长方形映射
取三行两列矩阵，其两列分别为 $(3,0,0)$ 与 $(0,1,0)$。

第一步求 $A^TA$，得到对角元素九与一的二阶矩阵。

第二步奇异值为三与一，右奇异方向就是两个标准坐标方向。

第三步把各方向映射后除以对应奇异值，得到输出空间中的第一、第二标准方向。

第四步再补第三个单位方向形成完整输出基。

单位圆经过该映射变成三维空间中位于水平面的椭圆，长短半轴为三与一。第三个输出方向无法由任何输入产生，因此它位于左零空间。这个例子把列空间、左零空间与奇异值几何联系在一起。

## 完整、薄与截断分解
完整 SVD 包含两侧空间的全部正交基；薄 SVD 只保留所需数量的列；秩分解还可以只写非零奇异值部分。不同库返回尺寸可能不同，使用公式前应确认。截断 SVD 则主动只保留最大的若干奇异值，这是近似而不是完全相同的分解。不要把“省去本来为零的项”和“舍去小但非零的项”混为一谈。

矩阵可写成若干奇异值乘左、右奇异向量外积之和，每一项都是一个秩一模式。这种表达适合解释图像压缩、数据结构提取和低秩近似。

## 易错点与解释边界
奇异向量也可能符号不唯一，重复奇异值对应的子空间内部可以换基。比较两次分解时，应关注重构矩阵和子空间，而不是逐元素要求一致。小奇异值可能代表真实但弱的信号，也可能主要是噪声，单靠数学排序不能决定删掉哪部分，需要结合任务、测量误差与验证结果。SVD 给出结构工具，具体取舍还需建模判断。

## 练习
1. 对角矩阵对角元素为负四和二，奇异值是多少？
<details><summary>查看解析</summary>

奇异值是四和二，因为它们描述长度伸缩，不保留特征值的正负号。
</details>

2. 一个矩阵只有三个非零奇异值，秩是多少？
<details><summary>查看解析</summary>

秩为三。其余方向对应零伸缩或额外的零空间结构。
</details>

<!-- math-revision-20261003:non-axis-svd-practice:start -->
## 练习 M13：把混合方向的 SVD 完整算出来

对
$$A=\begin{pmatrix}3&1\\1&3\\0&0\end{pmatrix}$$
求一个完整实 SVD $A=U\Sigma V^\mathsf T$：写 $A^\mathsf TA$、奇异值、两侧单位正交基和矩阵尺寸，最后乘回检查。再将矩阵改为
$$B=\begin{pmatrix}1&1\\1&1\\0&0\end{pmatrix},$$
沿同一方法说明零奇异方向应怎样处理，给出完整分解。

<details><summary>查看完整解析与检查</summary>

$A^\mathsf TA=\begin{pmatrix}10&6\\6&10\end{pmatrix}$。它的特征多项式为 $(t-16)(t-4)$，对应单位向量可取
$$v_1=\frac1{\sqrt2}(1,1),\quad v_2=\frac1{\sqrt2}(1,-1),\qquad\sigma_1=4,\ \sigma_2=2.$$
计算 $u_i=Av_i/\sigma_i$，得到 $u_1=(1,1,0)/\sqrt2$、$u_2=(1,-1,0)/\sqrt2$；再补 $u_3=(0,0,1)$。于是
$$U=\begin{pmatrix}1/\sqrt2&1/\sqrt2&0\\1/\sqrt2&-1/\sqrt2&0\\0&0&1\end{pmatrix},\quad
\Sigma_A=\begin{pmatrix}4&0\\0&2\\0&0\end{pmatrix},\quad
V=\frac1{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}.$$
尺寸分别是 $3\times3,3\times2,2\times2$，相乘得到 $3\times2$。各列直接点乘可查 $U^\mathsf TU=I_3,V^\mathsf TV=I_2$。外积重构给
$$4u_1v_1^\mathsf T+2u_2v_2^\mathsf T
=\begin{pmatrix}2&2\\2&2\\0&0\end{pmatrix}+\begin{pmatrix}1&-1\\-1&1\\0&0\end{pmatrix}=A.$$
这次列向量本来并不正交；输入和输出的主要方向都与标准坐标轴倾斜。

对 $B$，$B^\mathsf TB=\begin{pmatrix}2&2\\2&2\end{pmatrix}$，同一 $v_1,v_2$ 分别对应特征值 $4,0$，奇异值为 $2,0$。有 $Bv_1=2u_1$、$Bv_2=0$。不能用 $Bv_2/0$ 定义 $u_2$；而是把已得到的 $u_1$ 补成输出空间正交基，上面同一 $u_2,u_3$ 恰可使用。因此保留上述 $U,V$，令
$$\Sigma_B=\begin{pmatrix}2&0\\0&0\\0&0\end{pmatrix},\qquad B=2u_1v_1^\mathsf T.$$
秩为 $1$，输入零空间由 $v_2$ 张成；输出左零空间由 $u_2,u_3$ 张成。检查 $B^\mathsf Tu_2=B^\mathsf Tu_3=0$，便能区分“一个被压掉的输入方向”与“两个无法生成的输出方向”。

</details>

延伸阅读：[MIT 18.06SC 的 SVD 课程与独立习题](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/pages/positive-definite-matrices-and-applications/singular-value-decomposition/)。本题的两种矩阵与检查步骤可直接手算。
<!-- math-revision-20261003:non-axis-svd-practice:end -->
