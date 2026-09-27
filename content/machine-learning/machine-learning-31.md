---json
{
  "id": "machine-learning-31",
  "title": "参数估计：似然、最大似然与最大后验",
  "group": "01 · 数据与统计基础",
  "minutes": 55,
  "level": "进阶",
  "tags": [
    "似然与概率的区别",
    "Bernoulli 和高斯 MLE",
    "Bayes 后验、MAP 与正则化"
  ],
  "objectives": [
    "似然与概率的区别",
    "Bernoulli 和高斯 MLE",
    "Bayes 后验、MAP 与正则化",
    "证明 Bernoulli MLE 一致性并区分无偏和低均方误差"
  ],
  "prerequisites": [
    "machine-learning-03",
    "machine-learning-04"
  ],
  "summary": "似然固定观测、比较参数；后验还需要先验和归一化。",
  "quiz": {
    "question": "似然作为参数的函数有什么性质？",
    "options": [
      "一定对参数积分为一",
      "一般不是参数的概率分布",
      "就是后验概率",
      "不允许超过一"
    ],
    "answer": 1,
    "explanation": "似然固定观测、比较参数；后验还需要先验和归一化。"
  },
  "lab": null,
  "revision": "2026-09-27 · 官方讲义交叉复核与先修补全"
}
---

## 严格定义：先把观测和参数的角色分开
**参数化模型**是一组由参数 θ 索引的分布 $\{p_\theta:\theta\in\Theta\}$，Θ 是允许参数集合。观察数据 D 后，把数据固定，把分布对该数据给出的质量或密度作为参数的函数，叫**似然**：
$$L(\theta;D)=p_\theta(D).$$
似然一般不对 θ 积分为一，因此**不是参数概率分布**；连续观测用的是密度，不能把一个点的密度误称该点的概率。

若 $X_1,\ldots,X_n$ 在模型下独立，则联合密度/质量相乘；取自然对数得对数似然 $\ell(\theta)=\sum_i\log p_\theta(x_i)$。最大似然估计（MLE）选择 $\hat\theta\in\arg\max_{\theta\in\Theta}\ell(\theta)$；最大值可能不存在，也可能不唯一，必须检查边界。

通俗地说，先拿到一份成绩单，再比较不同参数“对这份成绩单解释得多好”。这不等于在说各参数本身有多少概率。

## Bernoulli MLE 的完整推导
设 n≥1，独立标签 $y_i\in\{0,1\}$，共同成功概率 θ∈[0,1]。记成功数 $s=\sum_i y_i$，
$$L(\theta)=\theta^s(1-\theta)^{n-s}.$$
当 0<s<n，在 (0,1) 内
$$\ell'(\theta)=\frac s\theta-\frac{n-s}{1-\theta}=0
\iff\hat\theta=\frac sn.$$
二阶导为 $-s/\theta^2-(n-s)/(1-\theta)^2<0$，边界似然为零，所以它是唯一全局最大。若 s=0，似然 $(1-\theta)^n$ 随 θ 下降，最大在 θ=0；若 s=n，最大在 θ=1。不能只给内点求导而漏掉这两种情形。

例：十次成功三次，MLE=0.3。若只有一次试验且成功，MLE=1，这是对当前有限样本的拟合结果，不是证明下一次绝不失败。

这里还可证明具体估计量的性质：$E\hat\theta=\theta$、$\operatorname{Var}(\hat\theta)=\theta(1-\theta)/n$，因为它是伯努利样本均值。由 Chebyshev 不等式，任意 ε>0 时 $P(|\hat\theta-\theta|\ge\epsilon)\le\theta(1-\theta)/(n\epsilon^2)\to0$，故它**依概率一致**。无偏描述每个 n 的平均位置，一致描述 n 趋无穷时集中到真值，两者不同。任何二阶矩有限的估计量还满足 $E[(\hat\theta-\theta)^2]=\operatorname{Var}(\hat\theta)+(E\hat\theta-\theta)^2$，由中心化展开证明；有偏方法也可能因方差更小而有更低均方误差。

这些是当前模型可直接证明的性质，不能推广为“所有 MLE 都无偏、一致或渐近正态”。一般结论另需可识别性（不同参数对应不同分布）、正则性和抽样条件；边界、混合模型奇异性、模型设错都需要分别分析。

## 高斯均值与方差的最大似然
假设独立实数观测来自 $N(\mu,\sigma^2)$，σ²>0。负对数似然为
$$-\ell(\mu,\sigma^2)=\frac n2\log(2\pi\sigma^2)
+\frac1{2\sigma^2}\sum_i(x_i-\mu)^2.$$
固定 σ²，最小化平方和给 $\hat\mu=\bar x$，已由均值定理证明。令 $Q=\sum_i(x_i-\bar x)^2$，若 Q>0，对 v=σ² 求导：
$$\frac{d(-\ell)}{dv}=\frac n{2v}-\frac Q{2v^2}
=\frac{nv-Q}{2v^2}.$$
在 v<Q/n 为负、之后为正，故唯一最小在 $\hat\sigma^2=Q/n$。它与第3节无偏方差的 Q/(n−1) 不同：一个优化似然，一个优化无偏性，标准不同。若 Q=0，令 v趋零可使似然无界，没有合法 σ²>0 的有限最大值。

## 贝叶斯后验、MAP 和完整不确定性
给参数先验密度 p(θ)，且证据 $p(D)=\int L(\theta;D)p(\theta)d\theta$ 为正且有限，则
$$p(\theta|D)=\frac{L(\theta;D)p(\theta)}{p(D)}.$$
先验是观察当前数据前对参数的分布描述，后验结合了模型、先验和观测。最大后验（MAP）取后验密度众数：
$$\hat\theta_{\mathrm{MAP}}\in\arg\min_\theta[-\ell(\theta)-\log p(\theta)].$$
分母与 θ 无关，取负对数给等式。MAP 只保留一个点，不等于完整后验，也一般不等于后验均值。对参数作非线性变换时密度含雅可比，MAP 还可能改变，所以“最可能参数”需说明参数化。

## 平滑来自怎样的先验
Bernoulli 成功概率的 Beta(a,b) 先验在 (0,1) 的密度正比于 $\theta^{a-1}(1-\theta)^{b-1}$，a,b>0。与似然相乘，幂相加得到
$$\theta|D\sim\operatorname{Beta}(a+s,b+n-s).$$
定义 Beta 积分 $B(a,b)=\int_0^1t^{a-1}(1-t)^{b-1}dt$，它是密度归一化常数。由 $t+(1-t)=1$，有 $B(a,b)=B(a+1,b)+B(a,b+1)$；对 $B(a+1,b)$ 分部积分、端点项为零，得 $B(a+1,b)=aB(a,b+1)/b$。联立得到 $B(a+1,b)/B(a,b)=a/(a+b)$，这正是 Beta 分布均值的积分。因此后验均值为 $(a+s)/(a+b+n)$。若 a=b=1，则均值 $(s+1)/(n+2)$，对应二元结果各加一的平滑。
后验两参数均>1 时 MAP 为 $(a+s-1)/(a+b+n-2)$，不是同一个数；有边界时需单独分析。例 n=10、s=1，均匀先验后的均值为 2/12，而 MAP 仍为 1/10。

## 正则化对应的概率条件
高斯回归噪声方差为 σ²，给每个权重独立 $N(0,\tau^2)$ 先验，固定两个方差。负对数后验忽略常数为
$$\frac{\mathrm{SSE}}{2\sigma^2}+\frac{\|w\|^2}{2\tau^2}.$$
乘正数 σ²/n 得 $\mathrm{SSE}/(2n)+\lambda\|w\|^2/2$，其中 $\lambda=\sigma^2/(n\tau^2)$。这与本教材岭回归缩放一致。拉普拉斯先验 $p(w_j)\propto e^{-|w_j|/b}$ 则导出 L1，系数为 $\sigma^2/(nb)$。先验越集中，收缩越强；这并不证明先验适合真实问题。

## 练习与解析
1. 似然在某参数处为 2，就违反概率不能超过 1 吗？
<details><summary>查看解析</summary>连续观测的似然可来自密度，密度可大于一；参数方向的似然也不是归一化参数概率。</details>

2. 三次成功、两次失败，均匀 Beta 先验的后验均值是什么？
<details><summary>查看解析</summary>后验为 Beta(4,3)，均值 4/7；MLE 与此时的 MAP 都为 3/5。不同估计准则不能混写。</details>

3. 为什么高斯方差 MLE 除 n，样本无偏方差却除 n−1？
<details><summary>查看解析</summary>MLE 来自似然导数；无偏修正来自平方离差和期望为 (n−1)σ²。两者解决不同优化要求，不矛盾。</details>
