---json
{
  "id": "fluid-mechanics-33",
  "title": "膨胀波、摩擦管流与加热管流",
  "group": "07 · 可压缩与自由液面",
  "summary": "Mach波和膨胀扇，把条件、定义和推导连成可复查的学习链。",
  "objectives": [
    "分别列 Prandtl–Meyer、Fanno 与 Rayleigh 模型的物理条件",
    "沿各模型的守恒路径判断 Mach 数、熵和总状态变化"
  ],
  "prerequisites": [
    "fluid-mechanics-23"
  ],
  "tags": [
    "Mach波和膨胀扇",
    "Fanno流",
    "Rayleigh流",
    "不同机制的壅塞"
  ],
  "minutes": 50,
  "level": "进阶",
  "quiz": {
    "question": "哪种模型同时要求等截面、绝热并允许壁面摩擦？",
    "options": [
      "等熵喷管",
      "Fanno流",
      "无摩擦Rayleigh流"
    ],
    "answer": 1,
    "explanation": "Fanno保持总焓但不等熵；Rayleigh允许热交换并忽略壁面摩擦。"
  },
  "lab": null,
  "revision": "2026-10-04 · 知识页结构与行文整理"
}
---
## 膨胀扇、Fanno 流与 Rayleigh 流

### 共同物性与符号

以下均使用定比热理想气体，$M=Ma$，$\gamma>1$。

### Prandtl–Meyer：等熵转向

Prandtl–Meyer 膨胀扇描述二维超声速、无黏、等熵流绕凸角平滑转向。

### Fanno：绝热摩擦

Fanno 模型描述等截面、稳态、绝热、有壁面摩擦的流动。

### Rayleigh：无摩擦加热或冷却

Rayleigh 模型描述等截面、稳态、忽略壁面摩擦但可加热或冷却的流动。后两者均不可直接沿用喷管的全程等熵关系。

### 声速状态与熵条件

声速状态以下标星号表示。第二定律要求总熵产生非负。绝热 Fanno 流沿程比熵增加；Rayleigh 流允许热交换，流体比熵还会受热量输入或移出影响，不能一概要求沿程增加；守恒式和状态模型决定允许的变化路径。以下结论不是说真实发动机仅有一种机制，而是分别隔离各机制来理解。

## 不同壅塞机制

壅塞不只发生在最窄的喷口。长管中的摩擦或持续加热，也可能让流动趋于声速并限制质量流率。区分模型后，才能判断该用哪组条件，而不是看到 Mach 数就用同一张公式表。

## 推导一：超声速转弯膨胀

在局部流向为 $x$ 的近均匀区域，对小扰动 $\delta u,\delta v$ 线性化无旋、等熵流，连续式为 $(1-M^2)\delta u_x+\delta v_y=0$，无旋式为 $\delta v_x-\delta u_y=0$。设扰动沿波面法向坐标 $\xi=x\cos\beta+y\sin\beta$ 变化，消元得到 $\tan^2\beta=M^2-1$，且 $\delta v/\delta u=\tan\beta$。

对膨胀方向取适当正号，速度转角微变 $d\theta=\delta v/V$，速率增量 $dV=\delta u$，故 $d\theta=\sqrt{M^2-1}\,dV/V$。总焓不变使 $T=T_0/[1+(\gamma-1)M^2/2]$；将 $V=M\sqrt{\gamma RT}$ 对数微分，得 $dV/V=dM/[M(1+(\gamma-1)M^2/2)]$。因此膨胀转角是函数 $\nu(M)$ 的增量，其中
$$\nu(M)=\sqrt{\frac{\gamma+1}{\gamma-1}}\tan^{-1}\sqrt{\frac{\gamma-1}{\gamma+1}(M^2-1)}-\tan^{-1}\sqrt{M^2-1}.$$
对这个表达求导恰得 $\nu'(M)=\sqrt{M^2-1}/[M(1+(\gamma-1)M^2/2)]$，且 $\nu(1)=0$，因此它就是上述积分。转角 $\Delta\theta=\nu(M_2)-\nu(M_1)>0$ 对应 Mach 数增加、静压下降。这里只推导光滑膨胀扇；压缩转角产生激波时熵增，不能反用同一等熵扇公式。

## 推导二：Fanno 摩擦为何使两侧都趋向 M=1

等截面质量通量 $G=\rho V$ 和总温 $T_0$ 均保持不变。令 $b=(\gamma-1)/2$，则 $T=T_0/(1+bM^2)$、$p=G\sqrt{RT}/(\sqrt\gamma M)$。用 $ds=c_p\,d\ln T-R\,d\ln p$ 化简得
$$\frac1R\frac{ds}{dM}=\frac{1-M^2}{M(1+bM^2)}.$$
摩擦产生正熵，因此亚声速支路沿程 $M$ 增大，超声速支路 $M$ 减小；两者都趋向声速，$M=1$ 是该路径上的最大熵状态。

若需计算可用长度，轴向动量为 $dp+\rho VdV+4\tau_wdx/D=0$，Darcy 约定 $\tau_w=f_D\rho V^2/8$。联立质量和能量微分式得到
$$\frac{f_Ddx}{D}=\frac{2(1-M^2)}{\gamma M^3(1+bM^2)}dM.$$
对实际的 $f_D$ 和 Mach 变化积分，就可估计到达声速前的长度；$f_D$ 变化明显时不能硬当常数。这里不把 Fanning 与 Darcy 差四倍的定义混用。

## 推导三：Rayleigh 加热的临界限制

无摩擦等截面流保持 $G=\rho V$ 和动量通量 $K=p+\rho V^2=p(1+\gamma M^2)$。因此 $p=K/(1+\gamma M^2)$，由质量和状态式得到 $T\propto M^2/(1+\gamma M^2)^2$，所以
$$T_0\propto\frac{M^2(1+bM^2)}{(1+\gamma M^2)^2},\quad \frac{d\ln T_0}{dM}=\frac{2(1-M^2)}{M(1+bM^2)(1+\gamma M^2)}.$$
加热增加总焓 $c_pT_0$，故亚声速支路 $M$ 上升、超声速支路 $M$ 下降，到声速达到该路径总温上限。静温本身的极大值却在 $M=1/\sqrt\gamma$，说明静温和总温极值不是同一概念。

## 例题与练习

空气 $\gamma=1.4$，等熵膨胀从 $M_1=2$ 到 $M_2=3$，分别代入得 $\nu(2)\approx26.38^\circ$、$\nu(3)\approx49.76^\circ$，转角约23.38°。计算函数时反正切通常输出弧度，最后再转换为度。

1. 绝热等截面管有摩擦，入口 $M=0.5$，沿程总温和总压如何变化？
<details><summary>查看解析</summary>

无轴功绝热使总温不变；摩擦熵增导致总压下降。Mach 数沿 Fanno 亚声速支路增加，但这不表示总压增加。
</details>

2. Rayleigh 模型中能否用静温最大证明已壅塞？
<details><summary>查看解析</summary>

不能。静温极大在 $M=1/\sqrt\gamma$，声速临界为 $M=1$；应检查总温、质量通量和边界约束。
</details>
