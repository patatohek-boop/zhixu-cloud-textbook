---json
{
  "id": "fluid-mechanics-07",
  "title": "控制体、输运定理与质量守恒",
  "group": "03 · 描述与守恒",
  "summary": "用清晰的边界，把“流进、流出、积累”写成方程。",
  "objectives": [
    "区分固定质点的物质系统与可移动控制体",
    "推导输运定理并用相对边界速度计算有向质量通量"
  ],
  "prerequisites": [
    "fluid-mechanics-29",
    "fluid-mechanics-06"
  ],
  "tags": [
    "控制体、输运定理与质量守恒",
    "解释雷诺输运定理",
    "计算质量流量与体积流量"
  ],
  "minutes": 40,
  "level": "基础",
  "quiz": {
    "question": "对固定控制体，出口通量为正是因为？",
    "options": [
      "出口压力总为正",
      "使用指向外侧的法线",
      "出口流速总较大",
      "质量在出口被创造"
    ],
    "answer": 1,
    "explanation": "通量符号由 u·n 决定；入口速度与外法线相反，所以为负。"
  },
  "lab": null,
  "revision": "2026-10-04 · 知识页结构与行文整理"
}
---
## 物质系统、控制体与通量

### 系统：固定一组质点

**物质系统**由一组确定的流体质点组成，边界随这些质点移动。

### 控制体：人为选定的区域

**控制体 $CV$**是为计算选定的空间区域，边界称控制面 $CS$，可以固定、平移或变形。取控制面外法线 $\mathbf n$，边界速度 $\mathbf v_b$。流体穿越边界的相对法向速度是 $(\mathbf u-\mathbf v_b)\cdot\mathbf n$。

### 广延量与单位质量量

**广延量 $B$**可对不重叠部分相加，例如质量、动量和能量。其局部单位质量量记为 $b$，故 $B=\int\rho b\,dV$；只有系统内 $b$ 均匀时，才可以写成单个常数 $b=B/m$。

### 通量：每单位面积每秒流过多少

向外质量通量为 $\rho(\mathbf u-\mathbf v_b)\cdot\mathbf n$，单位为 $\mathrm{kg/(m^2s)}$。

## 控制体的积累与边界输运

水箱是控制体，水箱里今天和明天的水不是同一群质点。箱内质量增加可能只是流入比流出多，并不意味着创造了质量。输运定理把“同一批物质怎样变化”转换为“边界内积累多少、穿过边界多少”。

<figure class="teaching-figure"><img src="assets/diagrams/control-volume-flux.svg" alt="固定控制体的通量符号。图中“流入量”按正数计；守恒积分统一用外法线，所以入口通量取负。" loading="lazy"><figcaption>固定控制体的通量符号。图中“流入量”按正数计；守恒积分统一用外法线，所以入口通量取负。</figcaption></figure>

## 质量、体积流量与质量流量

本段和下面的截面流量简式先采用固定控制体。移动或变形控制面的流率必须使用相对边界速度，不能直接使用流体的绝对法向速度；其一般表达在后面的输运定理中保留。

$m_{CV}$（kg）是此刻控制体内的质量；$Q$（m³/s）是体积流量；$\dot m$（kg/s）是质量流量。截面密度均匀时 $\dot m=\rho Q$。热力学常用 $Q$ 表示热量，而本流体课用它表示体积流量，不能跨课程直接照搬字母含义。

在控制面每一点，取垂直于表面、指向控制体外的单位向量 $\mathbf n$，称为外法线方向。$\mathbf u$ 是当地流速向量，$\mathbf u\cdot\mathbf n$ 是向外的法向速度。出口 $\mathbf u\cdot\mathbf n>0$，入口 $\mathbf u\cdot\mathbf n<0$。若另把 $\dot m_{in},\dot m_{out}$ 定义为各自**正的大小**，质量守恒式为

$$\frac{dm_{CV}}{dt}=\sum\dot m_{in}-\sum\dot m_{out}.$$

用外法线统一积分时入口已经带负号，不能再人为减去一次。符号形式可以不同，含义必须一致。

<figure class="teaching-figure"><a href="assets/diagrams/learn-fluid-mechanics-07.svg" target="_blank" rel="noopener" aria-label="打开大图：水箱进水6升每分钟、出水2升每分钟，存量每分钟增加4升，水位每分钟升高2厘米"><img src="assets/diagrams/learn-fluid-mechanics-07.svg" alt="水箱进水6升每分钟、出水2升每分钟，存量每分钟增加4升，水位每分钟升高2厘米" loading="lazy"></a><figcaption>本例进出口流量为给定常数；若出流受水位控制，必须重新建立随水位变化的流量关系。 · 点按图形可放大</figcaption></figure>

## 截面流量的几何推导

均匀法向速度为 $\bar u$，截面积为 $A$。经过 $dt$，流体走过距离 $\bar u\,dt$，扫过体积 $dV=A\bar u\,dt$；乘密度得到 $dm=\rho A\bar u\,dt$。所以 $Q=A\bar u$，$\dot m=\rho A\bar u$。若速度不均匀，要先对截面积分求 $Q=\int_Au_n\,dA$，不能用中心最大速度代替平均速度。

稳态只让 $dm_{CV}/dt=0$。单进单出、无泄漏时得到 $\rho_1A_1\bar u_1=\rho_2A_2\bar u_2$；再增加“两端密度相同”条件，才约去 $\rho$ 得 $A_1\bar u_1=A_2\bar u_2$。

## 证明：雷诺输运定理

在时刻 $t$ 选择恰好占据控制体的物质系统。经过短时间 $\Delta t$，物质系统与新控制体在内部绝大部分重合，仅在边界附近相差薄片。面元 $dA$ 附近向外多出的有符号体积为 $(\mathbf u-\mathbf v_b)\cdot\mathbf n\,dA\Delta t$，携带量为 $\rho b$ 乘该体积；入口为负，正好表示该部分不属于原来的物质系统。

因此，物质系统的量在 $t+\Delta t$ 等于新控制体内的量，加上所有有符号薄片携带量，再加高阶误差。减去 $t$ 时两者共同的积分、除以 $\Delta t$，在边界和场足够光滑时取极限，得到
$$\frac{dB_{\mathrm{sys}}}{dt}=\frac{d}{dt}\int_{CV(t)}\rho b\,dV+\int_{CS(t)}\rho b(\mathbf u-\mathbf v_b)\cdot\mathbf n\,dA.$$
固定控制体令 $\mathbf v_b=0$；物质体令边界法向速度与流体相同，则通量为零。两个极限都与定义一致。含激波等不光滑情形应使用积分守恒和分片极限，不应机械套用光滑微分推导。

## 从输运定理得到质量方程

经典流体力学的质量守恒是物理定律：$d m_{\mathrm{sys}}/dt=0$。令 $b=1$，固定控制体有
$$\frac{d}{dt}\int_{CV}\rho\,dV+\int_{CS}\rho\mathbf u\cdot\mathbf n\,dA=0.$$
对单一截面定义体积流量 $Q=\int_Au_n\,dA$、平均法向速度 $\bar u=Q/A$；仅当截面密度均匀时 $\dot m=\rho Q$。稳态无泄漏单流管使入口出口质量流量相等；若两端密度还相同，就有 $A_1\bar u_1=A_2\bar u_2$。这清楚列出了从一般式到简式额外用到的每个条件。

## 例题：水箱水位的上升时间

竖直等截面水箱面积 $A_t=0.20\,\mathrm{m^2}$，进水 $6.0\,\mathrm{L/min}$，出水 $2.0\,\mathrm{L/min}$。假设这段时间流量恒定、无溢流无泄漏，水密度固定为 $1000\,\mathrm{kg/m^3}$。

1. 净体积流入 $4.0\,\mathrm{L/min}=0.0040\,\mathrm{m^3/min}=6.667\times10^{-5}\,\mathrm{m^3/s}$
2. 箱内水质量 $m=\rho A_tH$，故 $dm/dt=\rho A_t\,dH/dt$，其中 $H$ 是水深（m）
3. 代入质量守恒并约去相同密度：$dH/dt=(Q_{in}-Q_{out})/A_t=3.333\times10^{-4}\,\mathrm{m/s}=2.0\,\mathrm{cm/min}$
4. 升高 $10\,\mathrm{cm}$ 需要 $10/2.0=5.0\,\mathrm{min}$，新增体积 $A_t\Delta H=0.020\,\mathrm{m^3}=20\,\mathrm L$，新增质量为 20 kg
5. 反查 $5\times(6-2)=20$ L，与几何体积一致

若出口是靠水位压差自行排水，水位升高会改变出口流量，此时应把 $Q_{out}(H)$ 代回方程，不能把本例直线增长外推到任意时刻。

## 思考题：气体的体积流量与质量流量

<details><summary>从质量式判断，再看答案</summary>

不一定。稳态、无泄漏、单进单出的条件保证质量流量相等；若出口密度只有入口一半，则出口体积流量必须是入口两倍。只有进一步确认两端密度相同，才能说体积流量相等。

</details>

## 例题：水箱是在灌满还是排空
固定水箱横截面积为 $A_t=2\,\mathrm{m^2}$，进水量 $Q_i=0.03\,\mathrm{m^3/s}$，出水量 $Q_o=0.01\,\mathrm{m^3/s}$，密度恒定。质量方程约去密度，得 $A_tdh/dt=Q_i-Q_o$，因此水位上升速率 $dh/dt=0.01\,\mathrm{m/s}$，即每分钟 0.6 m。

这个结果假设流量可在该时间段保持不变，且水箱无溢流。若出口靠重力排水，流量会随水位变化，应联立出口关系形成微分方程，而不能长期线性外推。

## 练习
1. 水以 2 m/s 平均速度通过直径 0.1 m 的圆管，体积流量是多少？
<details><summary>查看解析</summary>

$A=\pi D^2/4=0.007854\,\mathrm{m^2}$，$Q=A\bar u=0.01571\,\mathrm{m^3/s}$。
</details>

2. 稳态气流入口密度为出口的两倍、面积相同，出口速度是入口的多少倍？
<details><summary>查看解析</summary>

由质量守恒可得 $u_2=2u_1$。体积流量加倍，但质量流量不变。
</details>

## 相关知识

[稳流能量方程](#/course/thermodynamics/thermodynamics-07)；[伯努利与损失](#/course/fluid-mechanics/fluid-mechanics-10)。
