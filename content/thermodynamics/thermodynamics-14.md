---json
{
  "id": "thermodynamics-14",
  "title": "基本热力学关系、势函数与 Maxwell 关系",
  "group": "04 · 性质与循环",
  "minutes": 38,
  "level": "进阶",
  "tags": [
    "热力学势",
    "Maxwell",
    "偏导数"
  ],
  "objectives": [
    "严谨定义并区分简单可压缩基本关系、Legendre变换、自然变量",
    "逐步完成基本关系、混合偏导证明四个Maxwell关系及一般比热差",
    "检查定理前提、物理条件与单位并完成算例"
  ],
  "prerequisites": [
    "火用：能量的利用价值与损失定位"
  ],
  "summary": "热力学公式很多，但它们不是互不相关的经验口号。",
  "quiz": {
    "question": "从 dg=−s dT+v dp 可读出？",
    "options": [
      "(∂g/∂T)p=−s",
      "(∂g/∂T)p=v",
      "(∂g/∂p)T=−s",
      "g 恒为零"
    ],
    "answer": 0,
    "explanation": "Gibbs 比自由能的自然变量是 T 和 p，对 T 的偏导在固定 p 下等于负比熵。"
  },
  "lab": null
}
---

## 严谨定义与记号

这里研究固定组成、局部平衡、只考虑体积功的简单可压缩物质。用质量比性质：$u,h,a,g$ 分别为内能、焓、Helmholtz 自由能、Gibbs 自由能，均为 J/kg，定义 $h=u+pv$、$a=u-Ts$、$g=u+pv-Ts$。$s$ 为 J/(kg·K)，$v$ 为 m³/kg。

函数的**自然变量**是其完整微分直接使用的独立变量，例如 $u(s,v)$。将 $u$ 换成 $h=u+pv$，是用与 $v$ 共轭的变量 $p$ 替换 $v$，称 Legendre 变换；并非只给同一函数换个名字。偏导下标表示保持不变的量，不能省略。

## 通俗解释

同一座山，可以按经纬度画等高线，也可以按坡度来组织数据。势函数把难测的熵变化，变成可测的热膨胀和压缩响应。先看实验固定的是温度、压力还是体积，再选最顺手的势。

## 推导一：四个完整微分

用可逆参照过程连接相邻平衡态，第一律 $du=\delta q_{rev}-p\,dv$，熵定义 $\delta q_{rev}=Tds$，因此 $du=Tds-pdv$。两边都是状态函数微分，所得关系适用于这些平衡性质，与真实过程是否可逆无关。

分别对定义做乘积微分并消去项：

$$dh=Tds+vdp,\qquad da=-sdT-pdv,\qquad dg=-sdT+vdp.$$

电、磁、弹性、表面或组成变化均会带来额外共轭项，不能继续只留两项。

## 证明二：Maxwell 关系不是四条孤立口诀

若势函数在所考察单相区域有连续二阶偏导，混合偏导可交换。例如由 $g_T|_p=-s$、$g_p|_T=v$，得 $-s_p|_T=g_{Tp}=g_{pT}=v_T|_p$。同样对其余三个势操作，得到

$$\left(\frac{\partial T}{\partial v}\right)_s=-\left(\frac{\partial p}{\partial s}\right)_v,\qquad
\left(\frac{\partial T}{\partial p}\right)_s=\left(\frac{\partial v}{\partial s}\right)_p,$$

$$\left(\frac{\partial s}{\partial v}\right)_T=\left(\frac{\partial p}{\partial T}\right)_v,\qquad
\left(\frac{\partial s}{\partial p}\right)_T=-\left(\frac{\partial v}{\partial T}\right)_p.$$

负号分别来自 $-p\,dv$ 与 $-s\,dT$。跨越不可微的相变点时，不可直接交换该点不存在的偏导。

## 推导三：一般物质的比热差

由 $du=Tds-pdv$，固定 $v$ 得 $s_T|_v=c_v/T$；链式法则在固定 $p$ 下给 $s_T|_p=c_v/T+(s_v|_T)(v_T|_p)$，而左边为 $c_p/T$。代入 Maxwell 关系，再由 $dv=v_T|_p\,dT+v_p|_T\,dp=0$ 得 $p_T|_v=-v_T|_p/v_p|_T$，所以

$$c_p-c_v=-T\frac{[(\partial v/\partial T)_p]^2}{(\partial v/\partial p)_T}=\frac{Tv\alpha_v^2}{\kappa_T}.$$

这里体膨胀系数 $\alpha_v=(1/v)(\partial v/\partial T)_p$，等温压缩系数 $\kappa_T=-(1/v)(\partial v/\partial p)_T$；稳定可压缩物质通常 $\kappa_T>0$。理想气体代入 $\alpha_v=1/T,\kappa_T=1/p$ 恢复 $c_p-c_v=R$。



## 一步步算一个例子

理想气体 v=RT/p，在固定压力下 (∂v/∂T)_p=R/p。
1. Maxwell 关系给出 (∂s/∂p)_T=−R/p。
2. 沿等温过程积分，Δs=−R ln(p₂/p₁)。
3. 空气 R=0.287 kJ/(kg·K)，压力加倍时 Δs=−0.287 ln2=−0.1989 kJ/(kg·K)。
4. 结果与理想气体熵公式一致。这说明性质关系可互相校验，也展示等温压缩使气体熵减小，但环境熵必须纳入整体判断。

## 再深一层：把知识连接起来

还可由基本关系推出一般物质的焓微分：dh=c_p dT+[v−T(∂v/∂T)_p]dp。对理想气体，方括号恰好为零，恢复焓只随温度变化；对真实气体该项通常不为零，因此等焓节流时温度可能变化。这个结果把抽象偏导关系与实际阀门现象连接起来。

## 常见误区

遗漏偏导的固定变量；认为基本关系只适于真实可逆过程；把势函数的自然变量随意交换而不做完整微分。

## 动手练习

**练习 1**　由 dh=Tds+vdp，写出 h 对 p 在固定 s 下的偏导。

<details><summary>查看解析</summary>

固定 s 时 ds=0，因此 (∂h/∂p)_s=v。注意这不同于固定温度下的偏导。

</details>

**练习 2**　理想气体 α_v=1/T、κ_T=1/p，代入一般比热差公式得到什么？

<details><summary>查看解析</summary>

Tvα_v²/κ_T=Tv(1/T²)p=pv/T=R，因此恢复 c_p−c_v=R。单位与前面比热关系一致。

</details>

## 建立自己的解题习惯

循环题的第一张图应是设备连接图，第二张才是状态图。为所有流股编号，每个设备分别写能量平衡，最后检查整个循环的净热与净功是否闭合。理想模型用来识别趋势，真实性能还受压降、机械效率、传热温差和物性变化影响。比较方案时一次只改变一个主参数，并记录其他约束；若同时改变最高温度和压比，就不能把效率变化全归因于其中任何一项。

## 继续阅读

本章为原创中文讲解与教学例题；课程范围与模型条件参考[MIT 16.050 Thermal Energy — syllabus](https://ocw.mit.edu/courses/16-050-thermal-energy-fall-2002/pages/syllabus/)。课程资料页列出进一步阅读入口，原课程的高级内容需要另外系统学习。
