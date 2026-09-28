---json
{
  "id": "calculus-02",
  "title": "极限、连续与存在性",
  "group": "01 · 变化之前",
  "minutes": 45,
  "level": "基础",
  "tags": [
    "极限",
    "连续",
    "介值定理"
  ],
  "objectives": [
    "准确区分极限、连续、介值定理并写清适用条件",
    "逐步复现极限定理与证明",
    "独立完成例题与练习，并用反例检验条件"
  ],
  "prerequisites": [
    "calculus-01"
  ],
  "summary": "极限描述靠近时的趋势，连续把趋势与点值接起来。",
  "quiz": {
    "question": "函数在 a 连续必须满足？",
    "options": [
      "只需 f(a) 存在",
      "只需左右极限存在",
      "函数必须可导",
      "极限等于 f(a)"
    ],
    "answer": 3,
    "explanation": "连续要求点值存在且与该点极限一致，可导是更强条件。"
  },
  "lab": null
}
---

## 严谨定义：函数极限与连续

### 聚点：允许怎样接近

设 $D\subseteq\mathbb R$，$a$ 是 $D$ 的聚点，即每个去掉中心的区间 $(a-\delta,a+\delta)\setminus\{a\}$ 都含有 $D$ 中的点。

### 极限的误差定义

极限 $\lim_{x\to a}f(x)=L$ 指
$\forall\varepsilon>0,\ \exists\delta>0,\ \forall x\in D:\quad 0<|x-a|<\delta\Rightarrow|f(x)-L|<\varepsilon.$
$\varepsilon$ 是允许的输出误差，$\delta$ 是保证它的输入范围。

### 连续：极限与点值接上

连续则要求 $a\in D$，且上式允许 $x=a$、把 $L$ 换成 $f(a)$。端点用定义域内的单侧接近。

### 无穷处极限与无穷极限

$\lim_{x\to\infty}f(x)=L$ 把输入条件改为 $x>M$；$\lim_{x\to a}f(x)=+\infty$ 指对任意实数 $K$，充分接近时都有 $f(x)>K$。

## 通俗解释：误差承诺的先后顺序
先由读者任意提出精度，作者再给出一个对所有合法输入都有效的范围。选择 $\delta$ 时不能偷看最后会选哪个 $x$。数值表只能检查有限个输入，因此不能替代“所有”。

## 极限定理与证明
**唯一性。** 若 $L_1\ne L_2$ 都是极限，取 $\varepsilon=|L_1-L_2|/3$。在两个保证范围的交集中选合法 $x$，则三角不等式给 $|L_1-L_2|\le|L_1-f(x)|+|f(x)-L_2|<2|L_1-L_2|/3$，矛盾。

**和与积法则。** 若 $f\to A,g\to B$，分别把两个误差控制在 $\varepsilon/2$ 内，即得和的法则。对积，先限制 $|f-A|<1$，从而 $|f|\le|A|+1$；再使 $|g-B|<\varepsilon/[2(|A|+1)]$、$|f-A|<\varepsilon/[2(|B|+1)]$。由 $fg-AB=f(g-B)+B(f-A)$ 得误差小于 $\varepsilon$。若 $B\ne0$，充分接近时 $|g|\ge|B|/2$，而 $|1/g-1/B|\le2|g-B|/|B|^2$，故倒数及商法则成立。

**夹逼定理。** 若附近 $u\le f\le v$ 且 $u,v\to L$，选择同时使 $L-\varepsilon<u$、$v<L+\varepsilon$ 的范围，就有 $|f-L|<\varepsilon$。这一步直接验证定义。

## 连续函数的存在性定理与证明
以下用到[实数完备性与紧致](#/course/calculus/calculus-25)中的上确界、子列和极值定理。

**介值定理。** 若 $f$ 在 $[a,b]$ 连续，$f(a)<c<f(b)$，则存在 $s\in(a,b)$ 使 $f(s)=c$。令 $S=\{x\in[a,b]:f(x)<c\}$，$s=\sup S$。端点连续性保证 $a<s<b$。若 $f(s)<c$，连续性使某个 $s$ 右侧点也在 $S$，违反上界；若 $f(s)>c$，连续性使 $s$ 左侧一小段没有 $S$ 中的点，违反最小上界的定义。故只能等于 $c$。端值次序相反时对 $-f$ 使用同一论证。

**闭区间极值定理。** 连续函数在 $[a,b]$ 取得最大、最小值，完整的子列证明见上述先修章。闭、有界、连续三个前提各不可省：$1/x$ 在 $(0,1]$ 无最大值；$x$ 在 $\mathbb R$ 无最大值；在 $[0,1]$ 上令 $f(0)=0,f(x)=1/x$（$x>0$）也无最大值。

## 配图：把定义与几何对应起来

<figure class="teaching-figure"><a href="assets/diagrams/epsilon-delta.svg" target="_blank" rel="noopener" aria-label="打开大图：对 f(x)=2x+1，在 a=2、L=5 处，δ=0.5 将函数值限制在 5±1 的输出带内。"><img src="assets/diagrams/epsilon-delta.svg" alt="对 f(x)=2x+1，在 a=2、L=5 处，δ=0.5 将函数值限制在 5±1 的输出带内。" loading="lazy"></a><figcaption>对 f(x)=2x+1，在 a=2、L=5 处，δ=0.5 将函数值限制在 5±1 的输出带内。<br><small>线性函数示例；严格误差采用开区间。a 点本身可不参与极限定义。 · 点按图形可放大。</small></figcaption></figure>

## 逐步例题：孔洞与连续补全
设 $f(x)=(x^2-4)/(x-2)$，$x\ne2$。直接代入得到的 $0/0$ 是未定形式，不是零，也不是无穷。

第一步分解分子：$x^2-4=(x-2)(x+2)$。

第二步，只在 $x\ne2$ 的条件下约去因子，得到 $f(x)=x+2$。

第三步利用连续多项式，极限为 $4$。若定义 $f(2)=4$，新函数在此连续；若定义为 $7$，极限仍是 $4$，但函数不连续。这说明点值和附近行为是两份不同的信息。

## 练习
1. 求 $\lim_{x\to0}x\sin(1/x)$。
<details><summary>查看解析</summary>

由 $-|x|\le x\sin(1/x)\le |x|$，两边都趋于零，夹逼定理给出极限零。振荡本身没有消失，但振幅消失了。
</details>

2. 为什么 $x^3+x-1=0$ 在 $(0,1)$ 有且仅有一个根？
<details><summary>查看解析</summary>

多项式连续，两端值为 $-1$ 与 $1$，故有根。若 $x_2>x_1$，则 $x_2^3+x_2>x_1^3+x_1$，函数严格递增，故根至多一个。
</details>
