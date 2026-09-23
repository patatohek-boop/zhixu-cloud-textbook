---json
{
  "id": "fluid-mechanics-14",
  "title": "圆管层流与沿程阻力",
  "group": "05 · 管路与外流",
  "summary": "从抛物线速度分布走到工程压降公式。",
  "objectives": [
    "推导平均速度和压降关系",
    "分清 Darcy 与 Fanning 摩擦因子"
  ],
  "prerequisites": [
    "前面各节；导数与积分基础"
  ],
  "tags": [
    "圆管层流与沿程阻力",
    "推导平均速度和压降关系",
    "分清 Darcy 与 Fanning 摩擦因子"
  ],
  "minutes": 25,
  "level": "基础",
  "quiz": {
    "question": "圆管充分发展层流中，最大速度与平均速度之比为？",
    "options": [
      "1",
      "1.5",
      "2",
      "4"
    ],
    "answer": 2,
    "explanation": "用圆形面积元对抛物线分布积分，得到 u最大=2u平均。"
  },
  "lab": null
}
---

## 管中心快，靠壁慢
在圆管充分发展层流中，无滑移使壁面速度为零，中心不受同样强的局部速度约束，因此形成轴对称抛物线。它不是任意管流都能使用的默认速度剖面；入口区域和湍流有不同结构。

对半径 R、长度 L 的水平圆管，稳态不可压牛顿层流有
$$u(r)=\frac{\Delta p}{4\mu L}(R^2-r^2),\qquad \bar u=\frac{\Delta pR^2}{8\mu L}.$$
积分时面积元为 $dA=2\pi r\,dr$，不能把速度对半径直接平均。由此得到 Hagen–Poiseuille 关系 $Q=\pi R^4\Delta p/(8\mu L)$，以及中心速度 $u_{\max}=2\bar u$。

## 工程上统一写成水头损失
Darcy–Weisbach 公式为
$$h_f=f_D\frac LD\frac{\bar u^2}{2g},\qquad \Delta p=\rho gh_f.$$
圆管层流中 $f_D=64/Re$，$Re=\rho\bar uD/\mu$。另一种 Fanning 因子满足 $f_F=f_D/4$；使用图表或文献前必须确认定义。数值差四倍通常不是实验错误，而是约定不同。

## 例题：细管中输送黏性油
油密度 $\rho=850\,\mathrm{kg/m^3}$，动力黏度 $\mu=0.05\,\mathrm{Pa\cdot s}$，圆管直径 D=0.01 m、长 L=2 m，平均速度 0.2 m/s。先算 $Re=850\times0.2\times0.01/0.05=34$，明确处于常规管流层流范围。

层流压降 $\Delta p=32\mu L\bar u/D^2=6400\,\mathrm{Pa}$。Darcy 因子 $f_D=64/34\approx1.882$，大于 1 并不违反物理，因为低 Re 时该因子可以很大。代入统一水头式也得到相同压降。流量 $Q=\bar u\pi D^2/4=1.571\times10^{-5}\,\mathrm{m^3/s}$。

## 模型边界
常规光滑圆管中 Re 低于约 2300 常为层流，2300–4000 常作过渡区，具体转捩受入口扰动等影响。层流入口长度常估 $L_e/D\approx0.05Re$；太短的管道不能完全使用充分发展公式。黏度随温度变化明显时应联立热分析或分段处理。

## 练习
1. 固定 Q、L 与黏度，直径加倍，层流压降如何变化？
<details><summary>查看解析</summary>

$\Delta p\propto Q/D^4$，降为原来的 1/16。前提是改变后仍满足充分发展层流等假设。
</details>

2. Darcy 摩擦因子为 0.04 时，Fanning 因子是多少？
<details><summary>查看解析</summary>

$f_F=0.01$。不要把这个值直接代入使用 Darcy 定义的公式。
</details>
