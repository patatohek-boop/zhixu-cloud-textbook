---json
{
  "id": "fluid-mechanics-34",
  "title": "重力波与毛细波：自由表面的色散关系",
  "group": "07 · 可压缩与自由液面",
  "summary": "小振幅波，把条件、定义和推导连成可复查的学习链。",
  "objectives": [
    "准确区分并说明本章各概念",
    "在明确假设下复现推导并解释条件失效的情形"
  ],
  "prerequisites": [
    "fluid-mechanics-19",
    "fluid-mechanics-24"
  ],
  "tags": [
    "小振幅波",
    "色散关系",
    "相速度与群速度",
    "深水浅水及张力尺度"
  ],
  "minutes": 50,
  "level": "进阶",
  "quiz": {
    "question": "深水纯重力小振幅波中，群速度与相速度的关系是？",
    "options": [
      "群速度是相速度的一半",
      "二者总相等",
      "群速度是相速度的两倍"
    ],
    "answer": 0,
    "explanation": "ω=√(gk)，对k求导得cg=cp/2。"
  },
  "lab": null,
  "revision": "2026-09 · 缺漏补章"
}
---

## 严谨定义：波形速度与波包速度

考虑均匀密度液体，静止自由面 $z=0$、平底 $z=-h$，自由面位移 $\eta(x,t)$ 很小。波数 $k=2\pi/\lambda$，波长 $\lambda$，角频率 $\omega=2\pi f$。简谐波写作 $\eta=a\cos(kx-\omega t)$，小振幅条件包括 $ak\ll1$ 及 $a\ll h$。

色散关系是 $\omega$ 与 $k$ 的关系。相速度 $c_p=\omega/k$ 追踪固定相位的波峰；群速度 $c_g=d\omega/dk$ 描述窄带波包包络传播的线性近似。以下假定无黏、不可压、无旋、小振幅，气体压力恒定，表面张力 $\sigma$ 均匀。

## 通俗解释：同一片水面，不同波长跑得不一样

长重力波主要受重力和水深控制；很短的波更受表面张力影响。多个接近波长叠加会出现慢慢移动的包络，它不一定和其中的波峰同速。

<figure class="teaching-figure"><img src="assets/diagrams/surface-wave.svg" alt="线性表面波的几何量。波形传播速度与单个流体质点的运动不是同一个概念。" loading="lazy"><figcaption>线性表面波的几何量。波形传播速度与单个流体质点的运动不是同一个概念。</figcaption></figure>

## 推导：逐个写出边界条件

速度势满足 $\phi_{xx}+\phi_{zz}=0$，底部无穿透 $\phi_z(-h)=0$。自由面跟随流体，原条件为 $\eta_t+\phi_x\eta_x=\phi_z$；线性化后在 $z=0$ 得 $\eta_t=\phi_z$。表面压力跳跃的一阶项为 $p-p_{atm}=-\sigma\eta_{xx}$；把它代入非定常伯努利、舍去速度平方小项，得到 $\phi_t+g\eta-(\sigma/\rho)\eta_{xx}=0$。

选与底部条件相容的势 $\phi=B\cosh[k(z+h)]\sin(kx-\omega t)$。运动学条件给 $a\omega=Bk\sinh(kh)$；动力学条件给 $B\omega\cosh(kh)=a(g+\sigma k^2/\rho)$。消去 $a,B$，得到
$$\omega^2=(gk+\sigma k^3/\rho)\tanh(kh).$$
它来自场方程及两个不同的自由面条件，不能只通过量纲分析确定其中的双曲正切函数。

## 极限与群速度的证明

忽略张力，浅水 $kh\ll1$ 时 $\tanh(kh)\approx kh$，得 $\omega\approx k\sqrt{gh}$，故 $c_p=c_g\approx\sqrt{gh}$，与浅水方程一致。深水 $kh\gg1$ 时 $\omega\approx\sqrt{gk}$，故 $c_p=\sqrt{g/k}$、$c_g=c_p/2$。若深水短波由张力主导，$\omega\approx\sqrt{\sigma/\rho}\,k^{3/2}$，所以 $c_g=3c_p/2$。

为何包络速度是导数？叠加 $\cos(k_1x-\omega_1t)$ 与 $\cos(k_2x-\omega_2t)$，用和差化积得到快速载波乘以慢因子 $2\cos[(\Delta kx-\Delta\omega t)/2]$；慢因子固定相位速度为 $\Delta\omega/\Delta k$，窄带极限为 $d\omega/dk$。

## 例题与练习

忽略张力，水深0.5 m、波长20 m，$kh=2\pi\times0.5/20\approx0.157$，接近浅水范围；近似波速 $\sqrt{9.81\times0.5}=2.215$ m/s。若波长改成0.5 m，$kh\approx6.28$，应转向深水表达，不可仍只由水深求速度。

1. 深水重力波的波长增加四倍，相速度和群速度如何变化？
<details><summary>查看解析</summary>

$k$ 降至四分之一，$c_p\propto k^{-1/2}$，所以相速度翻倍；群速度始终为相速度的一半，也翻倍。前提是仍处于深水且张力可忽略。
</details>

2. 为什么破碎浪不能直接套线性解？
<details><summary>查看解析</summary>

大陡度、卷曲和破碎违反小振幅及光滑单值自由面的线性化条件，且存在强烈耗散和混气，已超出本模型。
</details>
