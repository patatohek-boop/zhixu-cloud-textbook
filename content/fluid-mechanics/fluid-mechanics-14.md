---json
{
  "id": "fluid-mechanics-14",
  "title": "圆管层流与沿程阻力",
  "group": "05 · 管路与外流",
  "summary": "从抛物线速度分布走到工程压降公式。",
  "objectives": [
    "从圆管动量平衡推导抛物线速度、流量与压降",
    "证明 Darcy 与 Fanning 因子的换算，并核对层流假设"
  ],
  "prerequisites": [
    "fluid-mechanics-29",
    "fluid-mechanics-13"
  ],
  "tags": [
    "圆管层流与沿程阻力",
    "推导平均速度和压降关系",
    "分清 Darcy 与 Fanning 摩擦因子"
  ],
  "minutes": 40,
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
  "lab": null,
  "revision": "2026-10-04 · 知识页结构与行文整理"
}
---
## 圆管层流的条件与摩擦因子

### 圆管几何与截面平均

圆管半径 $R$、直径 $D=2R$、测量长度 $L$，取轴向速度 $u(r)$。$r$ 是离轴距离；半径 $r$ 到 $r+dr$ 的薄环面积为 $dA=2\pi r\,dr$。$\Delta p=p_{in}-p_{out}$，平均速度 $\bar u=Q/(\pi R^2)$。

### 层流解的假设

假定水平、稳态、不可压、常黏度牛顿流体、轴对称充分发展层流、壁面无滑移。

### 两种摩擦因子的定义

Darcy 因子由 $\Delta p=f_D(L/D)\rho\bar u^2/2$ 定义；Fanning 因子由 $f_F=\tau_w/(\rho\bar u^2/2)$ 定义，$\tau_w$ 为壁面剪应力大小。两者的定义不同，不能直接比较数值。

## 速度的面积加权

中心附近速度高但面积小，靠近壁面的很多圆环各有更大面积。因此截面平均必须按面积加权，不能简单取“各半径速度的平均”。

## 推导一：轴向动量方程的精确解

轴向方程简化为 $0=-dp/dx+\mu r^{-1}d(r u')/dr$。令 $G=\Delta p/L=-dp/dx$，乘 $r$ 并积分：$ru'=-Gr^2/(2\mu)+C_1$。中心 $r=0$ 速度和梯度应有限，故 $C_1=0$；再积分得 $u=-Gr^2/(4\mu)+C_2$。壁面 $u(R)=0$ 给
$$u(r)=\frac{G}{4\mu}(R^2-r^2).$$
面积积分得 $Q=\int_0^Ru(r)2\pi r\,dr=\pi GR^4/(8\mu)$，故 $\bar u=GR^2/(8\mu)$，$u_{max}=GR^2/(4\mu)=2\bar u$。这同时推导出 $\Delta p=8\mu LQ/(\pi R^4)=32\mu L\bar u/D^2$。

## 推导二：两个摩擦因子的关系

取长度 $L$ 的整管流体，稳态充分发展使进出轴向动量相等，所以 $\Delta p\pi R^2=\tau_w2\pi RL$，即 $\Delta p=4\tau_w L/D$。与两个因子的定义比较，得到 $f_D=4f_F$。

再把层流压降代入 Darcy 定义：
$$f_D=\frac{32\mu L\bar u/D^2}{(L/D)\rho\bar u^2/2}=\frac{64\mu}{\rho\bar uD}=\frac{64}{Re}.$$
推导只对上述层流解成立；湍流即使仍在圆管中，也不能保留这一结果。对称性、壁面条件、压降符号和 $\mu>0$ 共同保证该剖面有正确方向。

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
