---json
{
  "id": "machine-learning-32",
  "title": "感知机：线性分类与错误次数界",
  "group": "03 · 经典监督学习",
  "minutes": 50,
  "level": "进阶",
  "tags": [
    "感知机更新规则",
    "线性可分与几何间隔",
    "有限错误界与不可分边界"
  ],
  "objectives": [
    "感知机更新规则",
    "线性可分与几何间隔",
    "有限错误界与不可分边界"
  ],
  "prerequisites": [
    "machine-learning-10"
  ],
  "summary": "感知机有限错误保证依赖可分间隔和有界输入，不能迁移到任意标签数据。",
  "quiz": {
    "question": "有限错误界必须有哪个关键条件？",
    "options": [
      "任意不可分数据",
      "存在统一正间隔的分离方向",
      "只需特征数量多",
      "初值必须随机"
    ],
    "answer": 1,
    "explanation": "感知机有限错误保证依赖可分间隔和有界输入，不能迁移到任意标签数据。"
  },
  "lab": null,
  "revision": "2026-09-28 · 概念分段、教学先修与练习复核"
}
---

## 从分类规则开始定义
把偏置并入增广向量 $\tilde x=(1,x_1,\ldots,x_p)$，权重 $\tilde w=(b,w_1,\ldots,w_p)$，分数为 $\tilde w^\top\tilde x$。标签 y∈{−1,+1}。感知机遇到 $y\tilde w^\top\tilde x\le0$ 的错误或边界点，就更新
$$\tilde w\leftarrow\tilde w+y\tilde x.$$
本节学习率取一、初态权重为零。它使用硬分类纠错，不输出概率，也不同于逻辑回归的平滑似然目标。

**严格线性可分**指存在单位向量 u 和 γ>0，使全部样本 $yu^\top\tilde x\ge\gamma$。

### 范数界与间隔的尺度

再要求输入有界 $\|\tilde x\|\le R$。γ 是在所选增广空间与单位范数下的间隔，R 是样本最大长度。通俗地说，不仅有一条线分开两类，还在两边留出正宽度安全带。

## 定理：错误更新次数有上界
在上述条件下，感知机最多作 $(R/\gamma)^2$ 次错误更新。这里计数每一次发生更新，不是遍历轮数。

**证明第一步：沿正确方向稳定前进。** 令 w_m 为第 m 次更新后的权重。每次更新的 $yu^\top\tilde x\ge\gamma$，故归纳有
$$u^\top w_m\ge m\gamma.$$

**第二步：权重长度不会增长得太快。** 更新前满足 $yw^\top\tilde x\le0$，所以
$$\|w+y\tilde x\|^2=\|w\|^2+2yw^\top\tilde x+\|\tilde x\|^2
\le\|w\|^2+R^2.$$
从零出发，m 次后 $\|w_m\|^2\le mR^2$。

**第三步：合并。** 由柯西–施瓦茨且 ||u||=1，
$m\gamma\le u^\top w_m\le\|w_m\|\le R\sqrt m$。

### 合并不等式得到次数界

m>0 时除以 √m，再平方得 $m\le(R/\gamma)^2$。证毕。

这证明可分、有界条件下反复遍历最终能达到零训练分类错误，不证明最大间隔、最好泛化或不可分数据也会停。它还说明尺度会影响界和轨迹。

## 可独立运行的实现
```python
def perceptron(points, labels, max_epochs=100):
    if not points or len(points) != len(labels):
        raise ValueError("需要非空且长度匹配的数据")
    dimension = len(points[0])
    if any(len(x) != dimension for x in points):
        raise ValueError("特征维度必须一致")
    if any(y not in (-1, 1) for y in labels):
        raise ValueError("标签必须为 -1 或 1")
    w = [0.0] * (dimension + 1)
    updates = 0
    for epoch in range(max_epochs):
        mistakes = 0
        for x, y in zip(points, labels):
            augmented = [1.0] + list(x)
            score = sum(a * b for a, b in zip(w, augmented))
            if y * score <= 0:
                w = [a + y * b for a, b in zip(w, augmented)]
                updates += 1
                mistakes += 1
        if mistakes == 0:
            return w, updates, True
    return w, updates, False

points = [[-1.0], [-2.0], [1.0], [2.0]]
labels = [-1, -1, 1, 1]
weights, count, converged = perceptron(points, labels)
assert converged
assert all(y * (weights[0] + weights[1] * x[0]) > 0
           for x, y in zip(points, labels))
```
输入契约还要求特征为有限实数；该教学实现不承担所有外来格式解析。

### 如何报告算法停止

完成一个**没有更新的完整轮次**才返回收敛，达到轮数上限仅返回未收敛状态，不能静默声称成功。

## 手算第一步与不可分反例
初始 w=(0,0)，先看 x=−1、y=−1，增广向量 (1,−1)，分数为零，更新得到 w=(−1,1)。此时原样本分数 −2，乘标签得 2，已正确；但其他样本仍需逐个检查。

如果同一 x=1 同时被标成 +1 和 −1，不可能有任何确定性线性分类器同时严格正确。感知机可反复更新；有限错误定理的可分前提已失效，而不是证明出了矛盾。

## 练习与解析
1. R=2、γ=0.5 时定理上界是多少？
<details><summary>查看解析</summary>(2/0.5)²=16 次错误更新。这是最坏上界，不保证恰更新16次。</details>

2. 感知机找到零训练错误边界是否就是最大间隔 SVM？
<details><summary>查看解析</summary>不是。感知机只按错误更新并依赖样本次序，不优化 SVM 的最大间隔目标。</details>
