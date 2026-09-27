---json
{
  "id": "fluid-mechanics-04",
  "title": "液面受力、浮力与稳定性",
  "group": "02 · 静止流体",
  "summary": "不仅计算总压力，还寻找它的作用位置。",
  "objectives": [
    "准确解释面积形心与压力中心",
    "在列明条件后复现本章推导，并用例题检验结论"
  ],
  "prerequisites": [
    "fluid-mechanics-29",
    "fluid-mechanics-03"
  ],
  "tags": [
    "液面受力、浮力与稳定性",
    "计算平面静水总力",
    "解释浮力和浮体稳定性"
  ],
  "minutes": 40,
  "level": "基础",
  "quiz": {
    "question": "上边缘位于水面的竖直矩形闸门，压力中心在何处？",
    "options": [
      "高度中点",
      "水面下 2H/3",
      "水面下 H/3",
      "底部"
    ],
    "answer": 1,
    "explanation": "压力随深度线性增加，合力位于三角形分布形心，即水面下 2H/3。"
  },
  "lab": null,
  "revision": "2026-09 · 定义与推导修订"
}
---

## 严谨定义：总力与作用点是两个问题

面积形心的深度为 $h_c=A^{-1}\int_Ah\,dA$。压力中心是使集中合力与原压力分布对任一参考点产生相同力矩的作用点。面积二次矩 $I_G=\int_A\eta^2dA$ 中，$\eta$ 是到所选形心轴的距离，单位为 $\mathrm{m^4}$；它不是质量转动惯量。

**浮力**是流体表面压力的合力；**浮心 $B$**是排开流体体积的形心；**重心 $G$**是重力作用点。**稳心 $M$**是浮体轻微倾斜后新浮力作用线与原竖直中心线的交点在倾角趋零时的极限。以下液体静止、密度均匀，外侧大气压一致，故使用表压 $p=\rho gh$。

## 通俗解释：越深的位置贡献越大的力矩

每小块面积受的力都指向板的法线，但深处受力更大。因此，把所有小力合成时，作用点会被深处的“大力”拉下去。漂浮时还要比较力矩：浮力等于重量只说明不上下加速，并不说明船不会翻。

## 证明一：平面合力和压力中心

设平板与水平面夹角为 $\theta$，沿板向下坐标为 $s$，并以它与自由液面的交线为 $s=0$，则 $h=s\sin\theta$。积分得
$$F=\int_A\rho gs\sin\theta\,dA=\rho gA s_c\sin\theta=\rho gAh_c.$$
力矩等价要求 $Fs_p=\int_A s\,p\,dA=\rho g\sin\theta\int_A s^2dA$。写 $s=s_c+\eta$，由形心定义 $\int_A\eta dA=0$，故 $\int_As^2dA=As_c^2+I_G$。因此
$$s_p=s_c+\frac{I_G}{As_c},\qquad h_p=h_c+\frac{I_G\sin^2\theta}{Ah_c}.$$
竖直板 $\theta=90^\circ$ 才退化为常见的 $h_p=h_c+I_G/(Ah_c)$。水平板压力均匀，作用点在形心，应直接用均匀分布处理。

## 证明二：浮力与小倾角稳定性

把排水体积想象成仍被同种液体占据。这团静止液体受到周围相同的压力分布，合力必须平衡其重量。把液体换成物体，表面形状和周围压力不变，所以压力合力仍为 $F_B=\rho gV_{\mathrm{disp}}$，向上并通过该体积形心。也可由 $-\int_Sp\mathbf n\,dA=-\int_V\nabla p\,dV$ 得到同一结论。

对满足左右对称平衡、水线面平滑变化的浮体，绕水线形心轴小转角 $\varphi$ 后，横向坐标 $x$ 处新增或减少的排水薄片近似为 $x\varphi\,dA$。排水体积一阶不变，因为 $\int_Ax\,dA=0$；浮心横向位移满足 $V_{\mathrm{disp}}\Delta x_B=\varphi\int_Ax^2dA=\varphi I_{\mathrm{waterplane}}$。于是 $BM=\lim_{\varphi\to0}\Delta x_B/\varphi=I_{\mathrm{waterplane}}/V_{\mathrm{disp}}$，$GM=KB+BM-KG$。

小倾角恢复力矩为 $-W GM\varphi$，其中 $W$ 是物体重量：$GM>0$ 时与扰动方向相反，$GM<0$ 时同向，$GM=0$ 则一阶分析不能判定。大倾角、舱内自由液面和复杂浮体须进一步分析，不能由初稳性直接担保。

## 例题：一扇竖直矩形闸门
闸门宽 $b=2\,\mathrm m$、高 $H=3\,\mathrm m$，上边缘与水面齐平。形心深度 $h_c=1.5\,\mathrm m$，面积 $A=6\,\mathrm{m^2}$。合力为 $1000\times9.81\times1.5\times6=88290\,\mathrm N$。

$I_G=bH^3/12=4.5\,\mathrm{m^4}$，所以 $h_p=1.5+4.5/(1.5\times6)=2.0\,\mathrm m$。相对上边缘的力矩为 $176580\,\mathrm{N\cdot m}$。这也等于三角形压力分布的形心在底部以上 $H/3$ 处的几何结论。

## 练习
1. 体积为 0.02 m³ 的刚体完全浸在水中，浮力是多少？
<details><summary>查看解析</summary>

$F_B=1000\times9.81\times0.02=196.2\,\mathrm N$。
</details>

2. 将例题闸门高度减半、宽度不变且顶端仍在水面，合力变成多少倍？
<details><summary>查看解析</summary>

$F=\rho gbH^2/2$，因此为原来的四分之一；作用点深度也减半。
</details>
