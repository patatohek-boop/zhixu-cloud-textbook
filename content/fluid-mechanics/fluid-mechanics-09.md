---json
{
  "id": "fluid-mechanics-09",
  "title": "角动量与透平机械入门",
  "group": "03 · 描述与守恒",
  "summary": "从旋转喷头到叶轮，用力矩控制角动量。",
  "objectives": [
    "准确解释关于固定点的角动量",
    "在列明条件后复现本章推导，并用例题检验结论"
  ],
  "prerequisites": [
    "fluid-mechanics-29",
    "fluid-mechanics-08"
  ],
  "tags": [
    "角动量与透平机械入门",
    "使用角动量方程",
    "理解欧拉透平方程的符号"
  ],
  "minutes": 40,
  "level": "基础",
  "quiz": {
    "question": "计算轴向力矩时需要哪一种速度分量？",
    "options": [
      "径向绝对速度",
      "轴向速度",
      "绝对周向速度",
      "只需要叶片相对速度大小"
    ],
    "answer": 2,
    "explanation": "绕轴的单位质量角动量为 rVθ，Vθ 是绝对速度的周向分量。"
  },
  "lab": null,
  "revision": "2026-09 · 定义与推导修订"
}
---

## 严谨定义：相对于哪根轴

相对于固定惯性原点的位置为 $\mathbf r$，单位质量角动量为 $\mathbf r\times\mathbf V$。叉积的方向按右手规则，绕 $z$ 轴分量为 $rV_\theta$；这里 $r$ 是到轴的垂直距离，$V_\theta$ 是**绝对速度**的周向分量。力矩为 $\mathbf r\times\mathbf F$，单位 N·m。

叶片线速度为 $\mathbf U$，流体相对叶片速度为 $\mathbf W$，有 $\mathbf V=\mathbf U+\mathbf W$；刚体叶轮 $U=\Omega r$。本章约定 $M_z$ 和功率 $P$ 为转子**输入流体**的量，正方向与 $\Omega$ 一致。单位质量输入功 $w=P/\dot m$，单位 J/kg；泵的理想扬程为 $w/g$。

## 通俗解释：叶轮给流体增加或取走旋转动量

叶轮既可能把流体向周向“拨快”，也可能从原有旋流取出功。只看水是否朝径向流动还不够：力矩看的是绝对周向分量。速度三角形是三向量相加的图，不是三种独立的速度。

## 推导：从力矩到欧拉透平方程

对固定原点，质点角动量求导：$d(\mathbf r\times m\mathbf V)/dt=\mathbf V\times m\mathbf V+\mathbf r\times m\mathbf a=\mathbf r\times\mathbf F$，第一项为零。对系统求和，成对内力矩在经典无偶应力模型中抵消，得总外力矩等于系统角动量变化率。

把 $b=\mathbf r\times\mathbf V$ 代入输运定理：
$$\sum\mathbf M=\frac{d}{dt}\int_{CV}\rho(\mathbf r\times\mathbf V)dV+\int_{CS}\rho(\mathbf r\times\mathbf V)(\mathbf V\cdot\mathbf n)dA.$$
对稳态或周期平均稳态叶轮取轴向分量，在一进一出、截面以代表性 $rV_\theta$ 描述时，$M_z=\dot m(r_2V_{\theta2}-r_1V_{\theta1})$。若分布明显不均匀，应保留积分，不能拿任意测点作截面代表。

微小转角 $d\vartheta$ 中，转子做功为 $dW=M_zd\vartheta$，故 $P=M_z\Omega$。除以 $\dot m$ 并使用 $U_i=\Omega r_i$，得到
$$w=U_2V_{\theta2}-U_1V_{\theta1}.$$
这就是欧拉透平方程的守恒推导。泵对流体输入功常为正；涡轮按同一约定为负，涡轮对外输出功则取其相反数。该式决定能量交换的骨架，不独自确定叶片滑移、损失或效率。

## 例题：叶轮的力矩和功率
某叶轮角速度为 $100\,\mathrm{rad/s}$，流量 $\dot m=2\,\mathrm{kg/s}$。入口 $r_1=0.10\,\mathrm m$、$V_{\theta1}=0$；出口 $r_2=0.20\,\mathrm m$、$V_{\theta2}=15\,\mathrm{m/s}$。

角动量方程给出 $M_z=2(0.20\times15)=6\,\mathrm{N\cdot m}$。流体所得功率 $P=\Omega M=600\,\mathrm W$。单位质量功为 300 J/kg；对水若全部作为理想机械能增加，等价扬程 $H=w/g\approx30.6\,\mathrm m$。实际可用水头还要扣除内部损失。

注意角速度的单位：若给 3000 r/min，应先换成 $2\pi\times3000/60\,\mathrm{rad/s}$。转速和角速度不是数值相同的量。

## 练习与边界
本节只建立守恒骨架。叶片角度、滑移系数、空化、相似律和效率特性需要结合专门透平机械教材与实测性能曲线，不能由单条欧拉方程全部确定。

1. 例题中质量流量减半，速度三角形不变，理论力矩如何变化？
<details><summary>查看解析</summary>

力矩减半至 3 N·m，理论单位质量功不变。真实装置变流量时速度三角形往往也会改变。
</details>

2. 纯径向绝对流入且流出也无周向速度，理想轴力矩是多少？
<details><summary>查看解析</summary>

两端 $rV_\theta$ 均为零，净轴力矩为零。径向压力和径向力仍可存在。
</details>
