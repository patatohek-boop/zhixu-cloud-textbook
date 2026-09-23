---json
{
  "id": "fluid-mechanics-13",
  "title": "量纲分析、相似与无量纲数",
  "group": "04 · 从守恒到流场",
  "summary": "用尺度组织实验，但不让无量纲数代替物理判断。",
  "objectives": [
    "构造 Buckingham Π 群",
    "区分 Reynolds、Froude、Mach 与 Weber 数"
  ],
  "prerequisites": [
    "前面各节；导数与积分基础"
  ],
  "tags": [
    "量纲分析、相似与无量纲数",
    "构造 Buckingham Π 群",
    "区分 Reynolds、Froude、Mach 与 Weber 数"
  ],
  "minutes": 25,
  "level": "基础",
  "quiz": {
    "question": "几何缩比为 1/4，同流体保持 Reynolds 相似时模型速度应为？",
    "options": [
      "原型的 1/4",
      "原型的 1/2",
      "原型的 2 倍",
      "原型的 4 倍"
    ],
    "answer": 3,
    "explanation": "Re=UL/ν，相同 ν 下长度缩小四倍，速度需放大四倍。"
  },
  "lab": null
}
---

## 为什么小模型能告诉我们大设备的事
如果两个系统的几何、控制方程、无量纲参数和边界条件相同，它们的无量纲解可能相同。风洞和水槽实验正是利用这种相似性。只把模型做成同样形状，并不能保证流动也相同。

Buckingham $\Pi$ 定理说明：一个由 n 个量构成、涉及 r 个独立基本量纲的关系，可改写为 n−r 个独立无量纲群之间的关系。这里的“独立”是量纲矩阵的秩意义，不是随便数出 M、L、T 字母就一定得到 r。

## 常见参数在比较什么
$Re=\rho UL/\mu=UL/\nu$ 比较惯性与黏性；$Fr=U/\sqrt{gL}$ 比较惯性与重力波尺度；$Ma=U/a$ 比较流速与声速；$We=\rho U^2L/\sigma$ 比较惯性与表面张力。它们不是互相替换的“流动复杂度分数”。

阻力系数 $C_D=F_D/(\rho U^2A/2)$ 常写成 $Re$、$Ma$、粗糙度比和几何参数的函数。量纲分析能给出关系形式，却不能独自给出函数的数值系数；还需要理论、实验或可信的数值计算。

## 例题：水中模型的 Reynolds 相似
原型特征长度 L=1 m，速度 U=2 m/s，模型缩为原来的 1/5，两者使用相同温度的水。要求 Reynolds 数相同，就要 $U_mL_m=U_pL_p$，所以模型速度需为 10 m/s。

若同时要求 Froude 数相同，则必须 $U_m/U_p=\sqrt{L_m/L_p}=1/\sqrt5$，模型速度约 0.894 m/s。两个要求互相冲突，说明用同一种流体的小模型一般不能同时严格匹配所有效应。船模常优先保持自由液面相关的 Froude 相似，再对黏性阻力进行修正。

## 用控制方程检查尺度
把速度写作 $\mathbf u=U\mathbf u^*$、长度写作 $\mathbf x=L\mathbf x^*$，以 $\rho U^2/L$ 除动量方程，黏性项前出现 $1/Re$。这才解释了 Reynolds 数的力学意义。然而在很薄的边界层里法向尺度远小于 L，梯度会放大，不能仅凭 Re 大就处处删掉黏性项。

## 练习
1. 水的运动黏度 $10^{-6}\,\mathrm{m^2/s}$，U=1 m/s、L=0.1 m，Re 是多少？
<details><summary>查看解析</summary>

$Re=UL/\nu=10^5$。是否湍流还取决于几何、扰动和边界条件，不是所有流动共用一个临界值。
</details>

2. 动态黏度的基本量纲是什么？
<details><summary>查看解析</summary>

由 $\tau=\mu du/dy$ 得 $[\mu]=ML^{-1}T^{-1}$，即 kg/(m·s)。
</details>
