---json
{
  "id": "heat-transfer-08",
  "title": "一维非稳态导热、特征值与图表",
  "group": "03 · 非稳态与数值",
  "minutes": 35,
  "level": "基础",
  "tags": [
    "Fourier",
    "特征值",
    "平板"
  ],
  "objectives": [
    "严谨定义并区分无量纲温度、Fourier数、平板半厚度",
    "逐步完成平板模态ODE、Robin特征方程与初值投影积分",
    "从边界和单位检查模型并解原算例"
  ],
  "prerequisites": [
    "集总热容：小物体如何随时间冷却"
  ],
  "summary": "厚面包放进烤箱，表面已经热了，中心还可能很冷。",
  "quiz": {
    "question": "Fourier 数主要比较什么？",
    "options": [
      "压力与速度",
      "扩散作用经历的时间与尺寸尺度",
      "质量与体积",
      "辐射与颜色"
    ],
    "answer": 1,
    "explanation": "Fo=αt/L² 表示温度扰动扩散相对于物体尺度的进展。"
  },
  "lab": null
}
---

## 严谨定义与记号

半厚度 $L$ 的无限平板初温均匀 $T_i$，两侧突然与相同恒温流体 $T_\infty$ 对流。定义无量纲温差 $\theta=(T-T_\infty)/(T_i-T_\infty)$、坐标 $X=x/L$、Fourier数 $Fo=\alpha t/L^2$、$Bi=hL/k$。本节长度为**半厚度**，不是任意采用集总模型的 $V/A_s$。

**模态**是一种空间形状乘以时间衰减；**特征值**是满足全部边界条件而允许存在的模态参数。初值需要叠加多个模态，系数由正交投影确定，而非随意设为1。

## 通俗解释

初始温度形状像由多个“音符”叠加成的声音，细小起伏衰减快，最慢的宽缓模式最后占主导。早期只留一个音符通常还拼不出正确形状。

## 逐步证明：平板级数从何而来

方程 $\theta_{Fo}=\theta_{XX}$；中心对称 $\theta_X(0)=0$，表面对流 $-\theta_X(1)=Bi\theta(1)$。设 $\theta=F(X)G(Fo)$，分离得 $F''/F=G'/G=-\lambda^2$。于是 $G=e^{-\lambda^2Fo}$，$F=A\cos\lambda X+B\sin\lambda X$。中心条件消去 $B$，表面条件给

$$\lambda\sin\lambda=Bi\cos\lambda\quad\Rightarrow\quad\lambda\tan\lambda=Bi.$$

不同特征根 $\lambda_m,\lambda_n$ 的方程相乘相减后积分，边界项因相同对称与Robin条件消失，得 $(\lambda_n^2-\lambda_m^2)\int_0^1F_mF_n dX=0$。故不同模态正交，可以将初值1投影：

$$A_n=\frac{\int_0^1\cos(\lambda_nX)dX}{\int_0^1\cos^2(\lambda_nX)dX}=\frac{4\sin\lambda_n}{2\lambda_n+\sin2\lambda_n}.$$

最后

$$\theta(X,Fo)=\sum_{n=1}^{\infty}A_n e^{-\lambda_n^2Fo}\cos(\lambda_nX).$$

对 $Bi>0$ 各根正；$Bi=0$ 的完全绝热情况另有零模态，初温不变，不能误删它。

## 输出量与近似精度

中心取 $X=0$，表面取 $X=1$；体平均温差还需积分，得 $\bar\theta=\sum_nA_ne^{-\lambda_n^2Fo}\sin\lambda_n/\lambda_n$，储能用平均温度。第一项近似常在 $Fo\gtrsim0.2$ 时有用，精度应通过增加项数检查，不能把经验门槛当证明。

模型要求常物性、一维、均匀初温、恒定 $h,T_\infty$、无内热源。圆柱和球体因径向面积变化有不同特征方程，不能套平板根；新增多维章说明适当边界下的乘积解。



## 补足圆柱和球体：几何如何改变特征方程

径向热方程为 $T_t=\alpha r^{-m}\partial_r(r^mT_r)$，无限长圆柱m=1、球体m=2。令 $X=r/R,Fo=\alpha t/R^2,Bi=hR/k$，分离后的空间方程为 $(X^mF')'+\lambda^2X^mF=0$，中心要求有界，表面 $-F'(1)=BiF(1)$。

圆柱的正则解为 $F=J_0(\lambda X)$。这里 $J_0$是满足 $z^2J_0''+zJ_0'+z^2J_0=0$且在零点有限、$J_0(0)=1$的Bessel函数，$J_1=-J_0'$。代入表面条件得到 $\lambda J_1(\lambda)=BiJ_0(\lambda)$。球体可令 $Y=XF$，方程变为 $Y''+\lambda^2Y=0$，中心有界选 $F=\sin(\lambda X)/(\lambda X)$；表面条件整理为 $1-\lambda\cot\lambda=Bi$。

两种情况下，时间项都是 $e^{-\lambda_n^2Fo}$，但投影内积须带体积权重 $X^m$。均匀初值给

$$A_n=\frac{\int_0^1X^mF_n(X)dX}{\int_0^1X^mF_n^2(X)dX}.$$

这是由不同模态方程相乘相减、按同一边界消去积分端项得到的加权正交投影。球体积分可得 $A_n=4(\sin\lambda_n-\lambda_n\cos\lambda_n)/(2\lambda_n-\sin2\lambda_n)$；圆柱则为 $A_n=2J_1(\lambda_n)/\{\lambda_n[J_0^2(\lambda_n)+J_1^2(\lambda_n)]\}$。温差场为各 $A_nF_n(X)e^{-\lambda_n^2Fo}$相加。这样便明确了平板、圆柱、球体何处相同、何处必须更换，使用表格时仍要核对它采用的F归一化和长度R。

## 一步步算一个例子

给定平板 Bi=1，第一特征值 λ₁≈0.8603、A₁≈1.119，取 Fo=0.5。
1. 中心 X=0，cos0=1。
2. 中心温差比 θ₀≈1.119exp(−0.8603²×0.5)≈0.773。
3. 初温 100 ℃、环境 20 ℃，中心温度约 20+80×0.773=81.84 ℃。
4. 表面 X=1 的温差比还要乘 cos0.8603≈0.652，约为 0.504，对应 60.3 ℃。中心与表面明显不同，单温模型不适合。

## 再深一层：把知识连接起来

平板、无限圆柱和球体的级数解具有相似时间结构，但空间函数和特征方程不同。平板用余弦函数，圆柱通常涉及 Bessel 函数，球体则涉及正弦与半径组合。初学者不必一开始推导所有特殊函数，先准确识别形状、特征长度与边界条件，再使用可靠系数或数值计算。

## 常见误区

把平均温度当中心温度；早期 Fo 很小时仅保留第一项；查图时用错半径或半厚度；忘记系数 A₁ 不总是 1。

## 动手练习

**练习 1**　若 α=10⁻⁵ m²/s、L=0.02 m，Fo=0.5 对应多长时间？

<details><summary>查看解析</summary>

t=Fo L²/α=0.5×0.0004/10⁻⁵=20 s。尺寸平方控制内部扩散时间。

</details>

**练习 2**　同一冷却时刻，中心还是表面更热？

<details><summary>查看解析</summary>

在均匀初温且两侧冷环境冷却的设定中，中心通常更热，表面先响应。若内部有热源或边界不同，则需重新判断。

</details>

## 建立自己的解题习惯

非稳态分析先问三件事：物体初始温度是否均匀，边界随时间怎样改变，内部温差能否忽略。随后计算相关无量纲数并检查所用长度定义，才选择集总、有限体或半无限体模型。结果应在初始时刻恢复初值，在很长时间后趋向相应稳态；纯冷却且无热源时不能无故出现低于所有冷边界的温度。解析近似、数值模型和实验曲线可用这些共同极限互相校验。

## 继续阅读

本章为原创中文讲解与教学例题；课程范围与模型条件参考[MIT 2.51 Intermediate Heat and Mass Transfer — syllabus](https://ocw.mit.edu/courses/2-51-intermediate-heat-and-mass-transfer-fall-2008/pages/syllabus/)。课程资料页列出进一步阅读入口，原课程的高级内容需要另外系统学习。
