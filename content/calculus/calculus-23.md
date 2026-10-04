---json
{
  "id": "calculus-23",
  "title": "Stokes 定理与向量微积分统一",
  "group": "07 · 多重积分与向量微积分",
  "minutes": 55,
  "level": "进阶",
  "tags": [
    "Stokes 定理",
    "旋度",
    "边界方向"
  ],
  "objectives": [
    "准确区分Stokes 定理、旋度、边界方向并写清适用条件",
    "逐步复现严谨定义与定理",
    "独立完成例题与练习，并用反例检验条件"
  ],
  "prerequisites": [
    "calculus-22"
  ],
  "summary": "沿边界的环量，由曲面上穿过的旋度汇总决定。",
  "quiz": {
    "question": "Stokes 定理把边界环量转成什么？",
    "options": [
      "曲线的长度",
      "任意函数的平均值",
      "曲面上的旋度通量",
      "体积上的函数值"
    ],
    "answer": 2,
    "explanation": "边界线积分等于旋度穿过一致定向跨越曲面的通量。"
  },
  "lab": null
}
---

## 旋度、定向和边界

### 旋度的分量定义

对 $\mathbf F=(P,Q,R)\in C^1$，定义
$$\nabla\times\mathbf F=(R_y-Q_z,\ P_z-R_x,\ Q_x-P_y).$$

### 曲面法向与边界方向

曲面可定向指能够连续选择单位法向；边界正向与法向服从右手规则。

### Stokes 定理的适用范围

本课证明以下范围：$S$ 可由有限个 $C^2$ 正则面片拼接，面片参数域满足[Green 定理](#/course/calculus/calculus-21)的条件，拼接处方向一致；$\mathbf F$ 在曲面邻域 $C^1$。则
$$\oint_{\partial S}\mathbf F\cdot d\mathbf r=\int_S(\nabla\times\mathbf F)\cdot n\,dS.$$

### 平面定理经参数化搬到曲面
在曲面上走一小步，可以由参数平面中的一小步控制。先把沿曲面做功写成参数平面的两个分量，再用已证明的 Green 定理，就能严格得到曲面结论。

## Stokes 定理的完整面片证明

### 第一步：将边界积分拉回参数平面

设 $\mathbf r(u,v)=(x,y,z)$，定义
$A(u,v)=\mathbf F(\mathbf r)\cdot\mathbf r_u$，
$B(u,v)=\mathbf F(\mathbf r)\cdot\mathbf r_v$。
参数边界上的 $A\,du+B\,dv$ 正是曲面边界的 $\mathbf F\cdot d\mathbf r$。Green 定理给其积分等于 $\iint(B_u-A_v)\,du\,dv$。

### 第二步：辨认旋度与叉积

乘积与链式法则展开：
$$B_u-A_v
=(D\mathbf F\,\mathbf r_u)\cdot\mathbf r_v-(D\mathbf F\,\mathbf r_v)\cdot\mathbf r_u,$$
因为 $\mathbf F\cdot(\mathbf r_{vu}-\mathbf r_{uv})=0$，这里用到 $C^2$ 的混合偏导相等。按分量收集，该式成为
$$(R_y-Q_z)(y_uz_v-z_uy_v)
 +(P_z-R_x)(z_ux_v-x_uz_v)
 +(Q_x-P_y)(x_uy_v-y_ux_v),$$
恰是 $(\nabla\times\mathbf F)\cdot(\mathbf r_u\times\mathbf r_v)$。按通量定义积分，得到单面片结论。

### 第三步：共享边相消

有限片相加时，相邻片共享边方向相反，线积分相消，仅剩 $\partial S$；面积积分相加得到全部曲面，证明完成。

## 两个向量恒等式的逐项证明
对 $\phi\in C^2$，$\nabla\times\nabla\phi$ 的第一分量为 $\phi_{zy}-\phi_{yz}=0$，另外两分量同理，所以为零。对 $C^2$ 场，
$$\nabla\cdot(\nabla\times\mathbf F)
=R_{yx}-Q_{zx}+P_{zy}-R_{xy}+Q_{xz}-P_{yz}=0,$$
因为每对混合偏导相等而成对抵消。这里必须区分“一个场的旋度为零”与“它一定有全局势函数”；后者仍受定义域孔洞限制，反例见[线积分与保守场中的有孔区域](#/course/calculus/calculus-20)。

**条件失效。** Möbius 带没有全局一致的单位法向，不能在未选可定向面片与处理边界的情况下写本定理的单一通量。把曲面法向反向也必须同时反转边界正向。

## 例：选最简单的跨越曲面
场为 $\mathbf F=(-y/2,x/2,0)$，边界是单位圆，按从上方看逆时针行进。

第一步计算旋度为 $(0,0,1)$。

第二步选择单位圆盘作跨越曲面，法向取向上，与边界方向匹配。

第三步旋度与法向的点积恒为一，曲面积分就是圆盘面积，所以环量为 $\pi$。

第四步也可选上半球面并使用一致法向，结果仍相同，但计算通常更麻烦；定理允许我们主动选择方便的几何表面。

若边界方向改成顺时针，法向应改为向下，结果变为负 $\pi$。方向匹配是数学关系的一部分，不是答案出来后再随意决定的符号。

## 旋度、环量与曲面的选择
旋度非零反映局部环量倾向，不要求粒子轨迹一定是一个圆；实际运动还受场随时间变化及其他因素影响。无旋场也可能在复杂区域拥有非零闭路环量。计算时先列曲面与边界、画法向，再写积分式；如果算式极其复杂，可以考虑更换跨越曲面或直接沿边界参数化。参数化边界和更换跨越曲面均可用于简化计算，使用积分定理时仍须满足场的光滑性与定向条件。

## 练习
1. 场 $(x,y,z)$ 的旋度是多少？其任意合适闭路环量呢？
<details><summary>查看解析</summary>

旋度为零，而且场是 $(x^2+y^2+z^2)/2$ 的梯度，所以闭路环量为零。
</details>

2. 曲面法向反向而边界方向保持不变，Stokes 等式是否仍按原式成立？
<details><summary>查看解析</summary>

不成立。旋度通量改变符号，必须同时反转边界方向以保持定理要求的方向匹配。
</details>
