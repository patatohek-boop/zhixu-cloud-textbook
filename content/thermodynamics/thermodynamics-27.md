---json
{
  "id": "thermodynamics-27",
  "title": "真实气体性质：可测导数与节流温变",
  "group": "07 · 真实气体、推进与统计熵",
  "minutes": 38,
  "level": "进阶",
  "tags": [
    "真实气体",
    "热性质一致性",
    "Joule–Thomson系数",
    "反转温度"
  ],
  "objectives": [
    "定义并区分真实气体、热性质一致性、Joule–Thomson系数",
    "逐步完成从基本关系推导du与dh及节流温度导数",
    "核对假设、极限与数值例题"
  ],
  "prerequisites": [
    "thermodynamics-14",
    "thermodynamics-08"
  ],
  "summary": "真实气体性质：可测导数与节流温变：从定义到推导，再检验模型边界。",
  "quiz": {
    "question": "真实气体绝热节流且动位能可忽略时，温度一定下降吗？",
    "options": [
      "一定下降",
      "一定不变",
      "由Joule–Thomson系数符号决定",
      "一定上升"
    ],
    "answer": 2,
    "explanation": "节流保持焓，dT=μ_JT dp；降压dp<0，μ_JT的正负决定降温或升温。"
  },
  "lab": null
}
---
## 真实气体的性质导数

### 真实气体状态与热性质

真实气体在给定区域用平衡状态方程 $p=p(T,v)$ 描述；比内能 $u$、比焓 $h=u+pv$ 不一定只依赖温度。定容比热 $c_v=(\partial u/\partial T)_v$，定压比热 $c_p=(\partial h/\partial T)_p$。

### 等焓温度响应与反转曲线

Joule–Thomson系数 $\mu_{JT}=(\partial T/\partial p)_h$，单位K/Pa，描述等焓小压降的温度响应，不是流体黏度。

反转曲线是 $\mu_{JT}=0$ 的状态集合；它不是“某种气体永远冷却或永远升温”的分界温度常数，通常也随压力改变。

### 体膨胀系数

$\alpha_v=(1/v)(\partial v/\partial T)_p$ 描述定压下比体积随温度的相对变化，单位K⁻¹。下标 $v$ 用于区别传热学中的热扩散率。

## 等焓过程中的温度变化

理想气体的内能只依赖温度；真实气体的分子相互作用还会使内能随比体积变化。节流过程在相应条件下保持焓，因此真实气体可能降温，也可能升温，方向由该状态的Joule–Thomson系数决定。

## 推导一：状态方程怎样约束内能

从 $du=Tds-pdv$ 出发，将熵视为 $s(T,v)$：$ds=(c_v/T)dT+(\partial s/\partial v)_Tdv$。Maxwell关系给 $(\partial s/\partial v)_T=(\partial p/\partial T)_v$，于是

$$du=c_vdT+\left[T\left(\frac{\partial p}{\partial T}\right)_v-p\right]dv.$$

理想状态式 $p=RT/v$ 使方括号为0，因此 $u$在定温时不随体积变，即 $u=u(T)$。这补上了前面“理想气体内能仅依赖温度”的依据；它依赖热力学基本关系及理想机械状态模型。

取 van der Waals 教学模型 $p=RT/(v-b)-a/v^2$，其中b是排除比体积参数（m³/kg），a的单位为Pa·m⁶/kg²。代入得 $(\partial u/\partial v)_T=a/v^2$，因此定温从 $v_1$ 到 $v_2$ 的内能差为 $a(1/v_1-1/v_2)$。这只是该模型内的结果，不能当精确物性数据库。

## 推导二：等焓节流温变

写 $s=s(T,p)$，由第14节Maxwell关系得 $ds=(c_p/T)dT-(\partial v/\partial T)_pdp$。代入 $dh=Tds+vdp$：

$$dh=c_p dT+\left[v-T\left(\frac{\partial v}{\partial T}\right)_p\right]dp.$$

令 $dh=0$，解出

$$\mu_{JT}=\frac{T(\partial v/\partial T)_p-v}{c_p}=\frac{v(T\alpha_v-1)}{c_p}.$$

理想气体 $\alpha_v=1/T$故系数0。真实气体降压时 $dp<0$，若 $\mu_{JT}>0$ 则降温；若负则升温。大压降应沿等焓路径积分或查出口焓，不能把入口系数视为全程常数。

## 例题1

某状态 $T=300$ K、$v=0.020$ m³/kg、$\alpha_v=0.0040$ K⁻¹、$c_p=1000$ J/(kg·K)。

1. $T\alpha_v-1=0.20$。
2. $\mu_{JT}=0.020\times0.20/1000=4.0\times10^{-6}$ K/Pa，即0.0040 K/kPa。
3. 小降压 $\Delta p=-100$ kPa时，线性估计 $\Delta T\approx-0.40$ K。
4. 这是局部斜率近似；若压力下降很多，应重新评价物性并积分。

## 练习

**练习1**　理想气体等焓节流为何不变温？

<details><summary>查看解析</summary>

由推导 $dh=c_pdT$，正比热时 $dh=0$推出 $dT=0$。原因是热性质，不是任何绝热过程都不升温。

</details>

**练习2**　上述同一状态若测得 $\alpha_v=0.0020$ K⁻¹，降压100 kPa时局部温变符号及数值？

<details><summary>查看解析</summary>

$T\alpha_v-1=-0.40$，$\mu_{JT}=-8.0\times10^{-6}$ K/Pa，乘负压差得到约+0.80 K，反而升温。

</details>

## 范围与继续阅读

本节讨论性质导数与节流机制，不包括临界区高精度状态方程拟合。课程范围参照[MIT热力学讲义](https://web.mit.edu/16.unified/www/FALL/thermodynamics/notes/notes.html)及[MIT 2.43课程说明](https://ocw.mit.edu/courses/2-43-advanced-thermodynamics-spring-2024/pages/syllabus/)，推导和数值题为原创。
