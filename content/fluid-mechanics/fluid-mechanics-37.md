---json
{
  "id": "fluid-mechanics-37",
  "title": "基本势流、镜像法与附加质量",
  "group": "06 · 进阶流动模型",
  "summary": "从源与偶极子逐步构造圆柱解，验证镜像边界，并用流体动能推导附加质量。",
  "objectives": [
    "说明极坐标速度势的定义、条件与物理意义",
    "说明源汇与偶极子的定义、条件与物理意义",
    "说明圆柱绕流与压力系数的定义、条件与物理意义"
  ],
  "prerequisites": [
    "fluid-mechanics-19"
  ],
  "tags": [
    "极坐标速度势",
    "源汇与偶极子",
    "圆柱绕流与压力系数",
    "镜像边界",
    "球体非定常附加质量"
  ],
  "minutes": 65,
  "level": "进阶",
  "quiz": {
    "question": "半平面中点源的固壁镜像，应使用什么？",
    "options": [
      "同强度同号源",
      "同强度反号源",
      "任意强度都可以"
    ],
    "answer": 0,
    "explanation": "同号镜像源的法向速度在壁面相消；点涡则需反号镜像，二者不能混用。"
  },
  "lab": null,
  "revision": "2026-09 · 讲义对照补充"
}
---

## 严谨定义：先选定义域与边界条件

本章使用无黏、不可压、无旋模型。速度为 $\mathbf u=\nabla\phi$，流体内部满足 $\nabla^2\phi=0$；固壁只要求法向速度与壁面相同，并不满足黏性无滑移。**奇点解**在某个点失去光滑性，所以该点必须被排除出普通流体区域，或被解释为理想化流量入口。

二维极坐标 $x=r\cos\vartheta,y=r\sin\vartheta$ 中，径向位移为 $dr$，角向弧长为 $r\,d\vartheta$，于是 $u_r=\phi_r$、$u_\vartheta=\phi_\vartheta/r$。环绕一周的体积流率按单位轴向长度计，单位为 m²/s；三维点源的流率单位才是 m³/s。不能把两种源强混为一个量。

## 通俗解释：用几块能算清楚的积木拼出边界

势流的优势是已知解可以相加。关键不是“叠加之后图好看”，而是叠加后的法向速度恰好满足物体表面条件。压力含速度平方，不能把各个积木的压力也线性相加；想象出来的源或涡通常放在物体内部或流体域外。

## 从流量定义推导源、汇与涡

二维各方向均匀向外的源强为 $q$。包围原点的半径 $r$ 圆周上，$q=\int_0^{2\pi}u_r r\,d\vartheta=2\pi r u_r$，所以 $u_r=q/(2\pi r)$。对 $r$ 积分，得到 $\phi=q\ln(r/r_0)/(2\pi)$，参考长度 $r_0$ 只改变势常数。$q<0$ 为汇。

同理，环量定义给点涡 $u_\vartheta=\Gamma/(2\pi r)$，因此 $\phi=\Gamma\vartheta/(2\pi)$。绕原点角度增加 $2\pi$ 时势增加 $\Gamma$，说明它一般多值；速度却在去掉原点的区域单值。三维径向点源用球面积 $4\pi r^2$ 代替圆周长度，得 $u_r=Q/(4\pi r^2)$、$\phi=-Q/(4\pi r)$。

现在把强度 $+q$ 的源放在 $x=-\epsilon/2$，强度 $-q$ 的汇放在 $x=+\epsilon/2$。两势相加，令 $\epsilon\to0$、$q\epsilon=m$ 保持不变。对位移作一阶展开，$\ln|\mathbf x+\epsilon\mathbf e_x/2|-\ln|\mathbf x-\epsilon\mathbf e_x/2|\approx\epsilon\partial_x\ln r=\epsilon\cos\vartheta/r$，于是**二维偶极子**的势为 $m\cos\vartheta/(2\pi r)$，$m$ 的单位是 m³/s。其净源强为零，但速度场并不为零。

## 分步构造：圆柱外的速度与压力

均匀流势为 $Ur\cos\vartheta$，加上偶极子，取 $m=2\pi Ua^2$，得到
$$\phi=U\left(r+\frac{a^2}{r}\right)\cos\vartheta,\quad
u_r=U\left(1-\frac{a^2}{r^2}\right)\cos\vartheta,\quad
u_\vartheta=-U\left(1+\frac{a^2}{r^2}\right)\sin\vartheta.$$
逐项可检查 $\nabla^2\phi=0$，$r=a$ 时 $u_r=0$，远处趋于均匀来流。因此 $r=a$ 可以成为半径 $a$ 的理想不可穿透圆柱表面。表面仍有切向滑动，这是模型假设的直接后果。

忽略体力，用伯努利 $p+\rho|\mathbf u|^2/2=p_\infty+\rho U^2/2$。定义压力系数 $C_p=(p-p_\infty)/(\rho U^2/2)$，在圆柱面有 $C_p=1-4\sin^2\vartheta$。上、下、前、后对称使合升力、合阻力均为零。若另加环量，表面速度变为 $-2U\sin\vartheta+\Gamma/(2\pi a)$，上下压力不再对称，积分得到 $L'=-\rho U\Gamma$；这里仍采用逆时针环量为正的约定。

圆柱势流不是黏性流的可靠阻力模型。边界层与分离破坏其前后对称压力分布；“算出来零阻力”说明理想假设的边界，不是流体不会阻碍物体。

## 镜像法：把固壁条件逐项验算

在 $y>0$ 半平面，点源位于 $(0,b)$，壁面为 $y=0$。在区域外 $(0,-b)$ 放置同强度镜像源。合势
$$\phi=\frac{q}{4\pi}\ln\frac{x^2+(y-b)^2}{r_0^2}+\frac{q}{4\pi}\ln\frac{x^2+(y+b)^2}{r_0^2}.$$
这里 $r_0>0$ 是参考长度，使对数自变量无量纲；改变它只改变势常数。
对 $y$ 求导，在 $y=0$ 两项分别正比 $-b/(x^2+b^2)$ 和 $b/(x^2+b^2)$，相消，所以壁面无穿透；它没有保证无滑移。若原奇点是点涡，壁下需放**反向**涡才能消去法向速度。源与涡的镜像符号不同，应求导检查，而非靠记忆图像。

## 非定常并不等于有阻力：附加质量的完整球例

半径 $a$ 的球以速度 $U(t)\mathbf e_z$ 在无限大、远处静止的理想流体中平移。以瞬时球心为球坐标原点，候选势为 $\phi=-Ua^3\cos\vartheta/(2r^2)$。它在 $r>a$ 调和，远处衰减，且 $\phi_r(a)=U\cos\vartheta$ 满足运动壁面的法向速度。球外速度为 $u_r=Ua^3\cos\vartheta/r^3$、$u_\vartheta=Ua^3\sin\vartheta/(2r^3)$。

直接积分流体动能，避免把移动坐标中的时间导数误当固定空间导数：
$$K_f=\frac{\rho}{2}\int_a^\infty\int_0^{2\pi}\int_0^\pi
\frac{U^2a^6}{r^6}\left(\cos^2\vartheta+\frac14\sin^2\vartheta\right)r^2\sin\vartheta\,d\vartheta\,d\varphi\,dr.$$
径向积分为 $1/(3a^3)$；角积分为 $2\pi[2/3+(1/4)(4/3)]=2\pi$。故 $K_f=\rho\pi a^3U^2/3=\tfrac12m_aU^2$，其中
$$m_a=\frac{2}{3}\pi\rho a^3=\frac12\rho\left(\frac43\pi a^3\right).$$
无黏、无辐射、无远场能流的这个模型中，球对流体做功率 $-F_zU=dK_f/dt=m_aU\dot U$，故流体对球的力为 $F_z=-m_a\dot U$（$U=0$ 处由连续延拓）。外力驱动质量为 $m_b$ 的球时，$(m_b+m_a)\dot U=F_{ext}$。**附加质量**描述需要同时加速的周围流体动能，并不表示球真的吸收了这部分液体。邻近壁面、自由面、可压缩波或其他形状都会改变它。

## 例题与练习

半径0.1 m的球在密度1000 kg/m³的理想水体中平移，附加质量 $m_a=2\pi/3\approx2.094$ kg。球自身质量0.5 kg，若期望加速度0.4 m/s²，则此模型所需净外力为 $(0.5+2.094)\times0.4=1.038$ N；这里只算加速方向上的净力，重力与浮力若有关要另入账。

1. 无环量圆柱面在迎流停滞点和顶部的 $C_p$ 分别是多少？
<details><summary>查看解析</summary>

停滞点 $\sin\vartheta=0$，得1；顶部 $\sin^2\vartheta=1$，得−3。负的压力系数只是低于来流静压，不等于绝对压力为负。若实际压力降到蒸气压附近，还须检查空化。
</details>

2. 理想球匀速运动时该附加质量力为零，是否意味着启动它也不需额外力？
<details><summary>查看解析</summary>

否。匀速时 $\dot U=0$，启动时 $\dot U\ne0$，必须建立周围流体的动能。实际黏性流还会产生阻力，不能把附加质量替代所有水动力。
</details>

## 讲义对照与后续阅读

主题对照 [MIT 2.20 Lecture 10：基本势流](https://ocw.mit.edu/courses/2-20-marine-hydrodynamics-13-021-spring-2005/resources/lecture10/)、[Lecture 11：镜像与受力](https://ocw.mit.edu/courses/2-20-marine-hydrodynamics-13-021-spring-2005/resources/lecture11/)、[Lecture 13：附加质量](https://ocw.mit.edu/courses/2-20-marine-hydrodynamics-13-021-spring-2005/resources/lecture13/)。一般六自由度附加质量矩阵与船舶波浪辐射属于后续海洋工程专题，本章完整推导的是无界球体平移模型。
