---json
{
  "id": "linear-algebra-13",
  "title": "特征值与特征向量",
  "group": "05 · 特征与能量",
  "minutes": 60,
  "level": "进阶",
  "tags": [
    "特征值",
    "特征空间",
    "特征多项式"
  ],
  "objectives": [
    "准确区分特征值、特征空间、特征多项式并写清适用条件",
    "逐步复现特征方程与不同特征值无关",
    "独立完成例题与练习，并用反例检验条件"
  ],
  "prerequisites": [
    "linear-algebra-12"
  ],
  "summary": "寻找变换中方向不变的向量，把混合运动拆成自然模式。",
  "quiz": {
    "question": "零是方阵的特征值意味着什么？",
    "options": [
      "矩阵不可逆",
      "矩阵所有元素为零",
      "矩阵一定对称",
      "矩阵只有零特征值"
    ],
    "answer": 0,
    "explanation": "存在非零向量被映成零，说明零空间非平凡。"
  },
  "lab": null
}
---

## 严谨定义：特征对、特征空间与重数

### 特征值和非零特征向量

对标量域 $\mathbb F$ 上方阵 $A\in\mathbb F^{n\times n}$，若存在 $v\ne0$ 使 $Av=\lambda v$，称 $\lambda\in\mathbb F$ 为特征值，$v$ 为特征向量。

### 特征空间包含零向量

特征空间 $E_\lambda=\ker(A-\lambda I)$ 包括零向量，但零向量不是特征向量。

### 特征多项式与两种重数

特征多项式本节约定 $p_A(t)=\det(tI-A)$。根 $\lambda$ 的代数重数是多项式因子 $(t-\lambda)$ 的次数；几何重数是 $\dim E_\lambda$。

## 通俗解释：特殊方向只改变倍数
一般矩阵会把一个方向混到其他方向；特征方向经过作用仍在同一直线上，负特征值表示反向，零特征值表示被压掉。复特征向量是复坐标方向，不一定是实平面中可画的一条固定线。

## 特征方程与不同特征值无关：证明
存在非零 $v$ 解 $(A-\lambda I)v=0$，当且仅当该方阵不可逆，由[行列式定理](#/course/linear-algebra/linear-algebra-09)等价于 $\det(\lambda I-A)=0$。它证明求根的依据，而不是把“行列式零”另立为不解释的口诀。

### 不同特征值的向量为什么无关

设 $\lambda_1,\ldots,\lambda_k$ 两两不同，$v_i$ 为对应非零特征向量。对 $k$ 归纳，$k=1$ 显然。若 $\sum_{i=1}^kc_iv_i=0$，对两边用 $A-\lambda_kI$，得 $\sum_{i<k}c_i(\lambda_i-\lambda_k)v_i=0$。归纳假设使每个 $c_i=0$（$i<k$），再回原式得 $c_k=0$。所以无关。

## 几何重数不超过代数重数：证明
设 $E_\lambda$ 有基 $v_1,\ldots,v_r$，扩充为整个空间基。新基中的矩阵前 $r$ 列为 $\lambda e_j$，因此是分块上三角
$\begin{pmatrix}\lambda I_r&B\\0&C\end{pmatrix}$。
其特征多项式为 $(t-\lambda)^r\det(tI-C)$（按下方零块展开），故根的代数重数至少为 $r$。这证明几何重数至多代数重数；也说明重复根未必提供相同数量的独立方向。

## 迹与行列式为何对应特征值和积

迹定义为对角元素的和 $\operatorname{tr}A=\sum_i a_{ii}$。
展开 $\det(tI-A)$，$t^{n-1}$ 系数只能来自选择一个 $-a_{ii}$、其余取 $t$，所以为 $-\operatorname{tr}A$；常数项为 $(-1)^n\det A$。

### 和积公式需要根在数域中完全分裂

若在所取数域多项式分解为 $\prod_i(t-\lambda_i)$，比较这些系数得到 $\sum_i\lambda_i=\operatorname{tr}A$、$\prod_i\lambda_i=\det A$，按代数重数计。复数域的“每个非恒定多项式有根”是代数基本定理，这里明确作为复数理论先修使用，其复分析证明不属于本线性代数课。

**反例。** 实矩阵 $\begin{pmatrix}0&-1\\1&0\end{pmatrix}$ 的 $p_A(t)=t^2+1$ 没有实根，不能宣称每个实矩阵都有实特征方向。相反，实对称矩阵不需要借助这个复数结果就能证明有完整实谱，见第 15 节。

## 相似不变量：现在可以使用特征值语言
设 $B=S^{-1}AS$，$S$ 可逆。

$Bv=\lambda v$ 当且仅当 $A(Sv)=\lambda(Sv)$，且可逆 $S$ 将非零向量保持非零，所以特征值与特征空间维数不变。左右乘可逆矩阵不改变像空间维数，所以秩不变。由[行列式乘法](#/course/linear-algebra/linear-algebra-09)，
$\det(tI-B)=\det(S^{-1}(tI-A)S)=\det(tI-A)$，故特征多项式及代数重数也不变。迹满足 $\operatorname{tr}(XY)=\sum_{i,j}x_{ij}y_{ji}=\operatorname{tr}(YX)$，于是 $\operatorname{tr}(S^{-1}AS)=\operatorname{tr}A$。

若只是行等价，特征值未必相同：$\operatorname{diag}(1,2)$ 消元后为 $I$，两者特征值不同。非正交基中的坐标长度也不应直接按平方和计算：$x=Sc$ 时真实欧氏长度平方是 $c^\mathsf TS^\mathsf TSc$，只有 $S^\mathsf TS=I$ 才简化为 $c^\mathsf Tc$。

## 逐步例题：对称混合的自然方向
<figure class="teaching-figure"><a href="assets/diagrams/eigen-directions.svg" target="_blank" rel="noopener" aria-label="打开大图：A=[[2,1],[1,2]] 的两个特征方向为 (1,1) 与 (1,−1)，伸缩倍数分别为 3 和 1。"><img src="assets/diagrams/eigen-directions.svg" alt="A=[[2,1],[1,2]] 的两个特征方向为 (1,1) 与 (1,−1)，伸缩倍数分别为 3 和 1。" loading="lazy"></a><figcaption>A=[[2,1],[1,2]] 的两个特征方向为 (1,1) 与 (1,−1)，伸缩倍数分别为 3 和 1。<br><small>两个特征值均为正，因此同向伸缩；一般负特征值会反向，图中不代表所有矩阵特征值都为正。箭头坐标按同一比例准确绘制。 · 点按图形可放大。</small></figcaption></figure>

设 $A=\begin{pmatrix}2&1\\1&2\end{pmatrix}$。

第一步构造特征多项式，得到 $(2-\lambda)^2-1$。

第二步令其为零，解得特征值三与一。

第三步对三解齐次系统，两个坐标必须相等，可取向量 $(1,1)$。

第四步对一求解，两个坐标互为相反数，可取 $(1,-1)$。代回原矩阵，分别得到三倍和一倍，验证成立。

这两个方向分别代表同向变化和反向变化。对称混合会放大共同部分，却保持差异部分的幅度。相同的结构会出现在两个耦合系统的模态分析中。

## 特征向量为何不唯一
同一个特征向量乘任何非零数仍是特征向量，因此求解时通常选简单整数或单位长度表示。对于高维特征空间，甚至可以选不同的基，所以不同软件返回的向量不必逐元素相同。比较结果时应看方向或张成空间，而不是要求符号完全一致。若两个向量只差一个负号，它们代表同一条特征直线。

## 练习
1. 对角矩阵对角元素为二和负一，特征值与标准特征方向是什么？
<details><summary>查看解析</summary>

特征值是二和负一，对应两个标准坐标方向。第二方向被反向而长度不变。
</details>

2. 零向量可以称为特征向量吗？
<details><summary>查看解析</summary>

不可以。必须排除零向量，否则特征方程对任意标量都成立，无法识别特殊方向。
</details>

<!-- math-revision-20261003:eigenproblem-practice:start -->
## 练习 M12：未见过的矩阵与重复根

分别对实矩阵
$$A=\begin{pmatrix}4&2\\1&3\end{pmatrix},\qquad
B=\begin{pmatrix}2&1\\0&2\end{pmatrix}$$
求特征多项式、每个特征空间的一组基、代数与几何重数，并判断能否选出两个独立的特征方向。每个方向都必须代回原矩阵检查。

<details><summary>查看完整解析与检查</summary>

对 $A$，$p_A(t)=(t-4)(t-3)-2=t^2-7t+10=(t-5)(t-2)$。$\lambda=5$ 时解 $-x+2y=0$，故 $E_5=\operatorname{span}\{(2,1)\}$；$\lambda=2$ 时解 $x+y=0$，故 $E_2=\operatorname{span}\{(1,-1)\}$。两根各代数重数 $1$、几何重数 $1$，方向独立，因为以这两列组成的矩阵行列式为 $-3\ne0$。代回 $A(2,1)=(10,5)=5(2,1)$、$A(1,-1)=(2,-2)=2(1,-1)$；迹 $7=5+2$ 与行列式 $10=5\cdot2$ 是额外检查。

对 $B$，$p_B(t)=(t-2)^2$，唯一根 $2$ 的代数重数为 $2$。但 $(B-2I)(x,y)=(y,0)$，核要求 $y=0$，所以 $E_2=\operatorname{span}\{(1,0)\}$，几何重数只有 $1$。代回 $B(1,0)=2(1,0)$；任意该特征值的向量都沿此直线，不能选出两个独立特征方向。两个代数根按重数计数，不等于自动得到两个独立向量；对应的对角化问题见[第14课](#/course/linear-algebra/linear-algebra-14)。

</details>
<!-- math-revision-20261003:eigenproblem-practice:end -->
