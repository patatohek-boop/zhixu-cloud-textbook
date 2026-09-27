---json
{
  "id": "fluid-mechanics-32",
  "title": "启动流与振荡边界层：黏性如何传播",
  "group": "04 · 从守恒到流场",
  "summary": "扩散初边值问题，把条件、定义和推导连成可复查的学习链。",
  "objectives": [
    "准确区分并说明本章各概念",
    "在明确假设下复现推导并解释条件失效的情形"
  ],
  "prerequisites": [
    "fluid-mechanics-31"
  ],
  "tags": [
    "扩散初边值问题",
    "相似变量",
    "误差函数",
    "振荡穿透深度和相位"
  ],
  "minutes": 50,
  "level": "进阶",
  "quiz": {
    "question": "振荡平板周期解中，离壁更远会怎样？",
    "options": [
      "振幅不变且同相",
      "振幅减小并产生相位滞后",
      "必定瞬间静止"
    ],
    "answer": 1,
    "explanation": "指数因子控制振幅衰减，余弦中的空间项体现相位滞后。"
  },
  "lab": null,
  "revision": "2026-09 · 缺漏补章"
}
---

## 严谨定义：时间边界条件也是问题的一部分

半无限流体占据 $y>0$，速度 $\mathbf u=(u(y,t),0,0)$，壁面在 $y=0$。常物性、无压力梯度时，Navier–Stokes 化为 $u_t=\nu u_{yy}$。启动流初始为 $u(y,0)=0$，壁面从 $t=0$ 起取 $u(0,t)=U$，远处 $u(\infty,t)=0$。

相似变量是把多个变量合成一个无量纲变量，使解在不同时间具有同形状；这里定义 $\eta=y/(2\sqrt{\nu t})$。误差函数 $\operatorname{erf}(\eta)=\frac2{\sqrt\pi}\int_0^\eta e^{-s^2}ds$，$\operatorname{erfc}=1-\operatorname{erf}$。

## 通俗解释：壁面运动的影响一层层扩散

墙突然开始运动，近壁流体的速度变化最明显，显著受到黏性影响的厚度按时间平方根增长，并不像刚性板那样各处保持同速。这个扩散模型没有有限速度的传播前锋：对任意有限 $y>0$ 和 $t>0$，解析解都已有非零响应，只是在远处可能小到无法观察；“影响厚度”指显著响应的约定尺度。

<figure class="teaching-figure"><img src="assets/diagrams/viscous-diffusion.svg" alt="由启动流解析式计算的三个速度剖面。时间增大时，相同相对速度对应的位置按时间平方根向外延伸。" loading="lazy"><figcaption>由启动流解析式计算的三个速度剖面。时间增大时，相同相对速度对应的位置按时间平方根向外延伸。</figcaption></figure>

## 完整推导：启动平板的误差函数解

设 $u=UF(\eta)$。链式法则给 $u_t=-U\eta F'/(2t)$、$u_{yy}=UF''/(4\nu t)$，代入方程得 $F''+2\eta F'=0$。令 $G=F'$，解 $G'/G=-2\eta$ 得 $G=Ce^{-\eta^2}$。再积分 $F=C\int_0^\eta e^{-s^2}ds+D$。

壁面 $F(0)=1$ 给 $D=1$；远处 $F(\infty)=0$，利用高斯积分 $\int_0^\infty e^{-s^2}ds=\sqrt\pi/2$ 得 $C=-2/\sqrt\pi$。因此 $u=U\operatorname{erfc}[y/(2\sqrt{\nu t})]$。高斯积分可由二维积分改用极坐标证明：全平面 $e^{-x^2-y^2}$ 积分为 $2\pi\int_0^\infty re^{-r^2}dr=\pi$，故一维全轴积分为 $\sqrt\pi$。

固定 $y>0$ 时 $t\to0^+$ 有 $\eta\to\infty$，返回初始静止；任意 $t>0$ 时壁面满足 $u=U$。壁面应力大小为 $\mu U/\sqrt{\pi\nu t}$，理想瞬时启动在 $t\to0$ 奇异，真实有限加速时间会平滑这个极限，不能把无穷瞬时力当设备预测。

## 振荡平板与相位滞后

设壁面速度为 $U\cos\omega t$，研究启动暂态消失后的周期解。用复数表示 $u=\operatorname{Re}\{Ue^{i\omega t-ky}\}$，代入扩散方程得 $i\omega=\nu k^2$；取向远处衰减的根 $k=(1+i)\sqrt{\omega/(2\nu)}$。定义 $\delta_s=\sqrt{2\nu/\omega}$，取实部得到
$$u(y,t)=Ue^{-y/\delta_s}\cos(\omega t-y/\delta_s).$$
距离壁面越远，振幅按指数减小，相位滞后为 $y/\delta_s$。这个解针对半无限平板，不能直接称为圆管完整 Womersley 解；但它说明了高频时近壁薄层与核心的区别。

## 例题与练习

水的 $\nu=10^{-6}$ m²/s，$f=1$ Hz，$\omega=2\pi$ s⁻¹，则 $\delta_s=0.564$ mm。在 $y=\delta_s$ 处，速度振幅为壁面的 $e^{-1}\approx0.368$，滞后 1 rad。

1. 启动时间由 1 s 变为 4 s，相同 $\eta$ 所在深度变成几倍？
<details><summary>查看解析</summary>

$y=2\eta\sqrt{\nu t}$，所以变为两倍，不是四倍。
</details>

2. 振荡频率增为四倍，穿透深度如何变化？
<details><summary>查看解析</summary>

$\delta_s\propto\omega^{-1/2}$，因此减半，壁面影响集中到更薄区域。
</details>
