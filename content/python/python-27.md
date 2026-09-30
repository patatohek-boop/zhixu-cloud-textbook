---json
{
  "id": "python-27",
  "title": "递归与分治：阶乘、插入排序和归并排序",
  "group": "04 · 抽象与工程基础",
  "minutes": 45,
  "level": "进阶",
  "tags": [
    "递归与数学归纳法",
    "排序正确性与稳定性",
    "分治和复杂度递推"
  ],
  "objectives": [
    "递归与数学归纳法",
    "排序正确性与稳定性",
    "分治和复杂度递推"
  ],
  "prerequisites": [
    "python-19"
  ],
  "summary": "排序必须同时保证次序正确与元素不丢失；递归还须证明终止。",
  "quiz": {
    "question": "归并排序正确性依赖什么？",
    "options": [
      "两半正确排序且合并保持有序与元素",
      "输入没有重复值",
      "输入全是正数",
      "必须使用全局变量"
    ],
    "answer": 0,
    "explanation": "排序必须同时保证次序正确与元素不丢失；递归还须证明终止。"
  },
  "lab": null,
  "revision": "2026-09-28 · 概念分段、教学先修与练习复核"
}
---

## 递归先有契约，再写自我调用
**递归函数**在计算中直接或间接调用自身。**基本情况**无需进一步递归即可返回；**递归情况**把任务化为更小输入，再组合结果。

### 正确性与终止分开论证

递归正确性通常借助数学归纳法：证明最小输入正确，再假定更小输入正确，推出当前输入正确。

### 为何一定回到基本情况

终止还要求规模确实下降。

阶乘对非负整数 n 定义为 $0!=1$，$n!=1\cdot2\cdots n$（n≥1）。下面明确拒绝负数和非整数，且将布尔值排除：
```python
def factorial(n):
    if type(n) is not int or n < 0:
        raise ValueError("n 必须是非负整数")
    if n == 0:
        return 1
    return n * factorial(n - 1)

assert factorial(0) == 1
assert factorial(5) == 120
```
**证明：** n=0 返回定义中的 1。假设 n−1 的调用返回 $(n-1)!$，则当前返回 $n(n-1)!=n!$。每次参数减一，非负整数不能无限严格下降，所以数学过程终止。实际 Python 调用栈有限，过大 n 可能触发递归限制；数学终止不保证任意输入都适合此实现。

通俗地说，递归是把最后一个乘法留给自己，把前面的工作交给“处理更小任务的同一个方法”，不是凭空相信函数会完成。

## 插入排序：把新牌插进已排好的手牌
排序的契约有两个部分：输出按非降序排列，且元素的多重集合与输入相同（重复次数不能变）。**稳定**还要求关键字相同的记录保留相对次序。
```python
def insertion_sort(values):
    result = list(values)
    for i in range(1, len(result)):
        item = result[i]
        j = i
        while j > 0 and result[j - 1] > item:
            result[j] = result[j - 1]
            j -= 1
        result[j] = item
    return result

assert insertion_sort([3, 1, 2, 1]) == [1, 1, 2, 3]
assert insertion_sort([]) == []
```
外层不变量：每轮开始，前 i 项已排序，且整体元素尚未丢失（被暂存的 item 计入状态）。内层把严格大于 item 的前驱向右移，直到找到不大于它的位置或左端；此时放回 item，前 i+1 项有序，其他元素和重复次数保持。初始单元素前缀有序；退出时整个列表有序。两层索引均沿有限整数区间推进，因此终止。

使用 `>` 而不是 `>=`，相等项不会越过新项，所以稳定。逆序输入第 i 次要移动 i 项，总移动次数 $1+\cdots+(n-1)=n(n-1)/2$，最坏时间 $O(n^2)$；已排序时内层立即停止，时间 $O(n)$。返回副本需要 $O(n)$ 额外空间。

## 归并排序：先分开排好，再合并
**分治**把任务拆为较小的同类任务，分别求解后组合。归并时，两边都已排序，只需不断取两个当前首元素中较小者：
```python
def merge_sort(values):
    if len(values) <= 1:
        return list(values)
    mid = len(values) // 2
    left = merge_sort(values[:mid])
    right = merge_sort(values[mid:])
    out = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out

assert merge_sort([4, -1, 4, 0]) == [-1, 0, 4, 4]
assert merge_sort([2]) == [2]
```
**合并不变量：** out 已排序，包含两边已经消耗的元素，且 out 最后一个元素不大于任何剩余元素。每次取两边最小首元素，性质保持；一边耗尽后另一边已排序，可直接追加。相等时优先左边，保留原顺序。

**递归证明：** 长度零或一正确；假设更短输入排序正确，两半递归得到有序且元素不丢失的结果，已证明的

### 合并的逐项选择

合并过程给出当前正确结果。每次至少把规模减为接近一半，递归终止。

长度为 $n=2^k$ 时，每一层合并和切片的总工作为 $O(n)$，有 $\log_2n$ 层，故总时间 $O(n\log n)$；一般长度用上下相邻的 2 的幂给出同阶界。此列表实现峰值额外空间为 $O(n)$，递归深度为 $O(\log n)$。生产代码通常优先使用内置排序，本实现的目标是理解和证明。

## 练习与解析
1. 为什么仅检查排序结果递增还不够？
<details><summary>查看解析</summary>永远返回空列表也“递增”，但丢掉了全部输入。必须同时验证元素及其重复次数保持。</details>

2. 将归并中的 <= 改成 < 会破坏非降序吗？会影响什么？
<details><summary>查看解析</summary>非降序仍成立，但两边关键字相同时先取右边，可能颠倒原输入中的同键顺序，从而破坏稳定性。</details>

3. 阶乘递归每次改成 n+1，基本情况还会保护程序吗？
<details><summary>查看解析</summary>对于正输入不会接近零，规模不下降；有基本情况不等于能到达它。实际程序会触及调用栈限制。</details>
