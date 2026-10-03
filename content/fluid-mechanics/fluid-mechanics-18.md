---json
{
  "id": "fluid-mechanics-18",
  "title": "阻力、升力与绕流",
  "group": "05 · 管路与外流",
  "summary": "从表面压力和剪切积分，走到工程升阻系数。",
  "objectives": [
    "明确升阻力方向、参考面积和环量正号",
    "列明理想模型条件解释 Kutta–Joukowski 关系及其局限"
  ],
  "prerequisites": [
    "fluid-mechanics-29",
    "fluid-mechanics-17",
    "fluid-mechanics-19"
  ],
  "tags": [
    "阻力、升力与绕流",
    "区分摩擦阻力与压差阻力",
    "解释升力而不使用等时到达误说"
  ],
  "minutes": 40,
  "level": "基础",
  "quiz": {
    "question": "关于机翼上下方的流体，正确说法是？",
    "options": [
      "必须在后缘同时相遇",
      "上方路径更长所以必定更快",
      "无需等时到达条件，需由完整流场与边界条件求解",
      "升力与压力无关"
    ],
    "answer": 2,
    "explanation": "等时到达是误说；速度和压力分布由运动方程、几何、边界与流动状态共同确定。"
  },
  "lab": null,
  "revision": "2026-10-04 · 知识页结构与行文整理"
}
---
## 升阻力与参考面积

### 升阻力的方向约定

设来流沿 $+x$，向上为 $+y$。物体外法线为 $\mathbf n_b$，流体对物体的力为 $\mathbf F=\int_{S_b}(-p\mathbf n_b+\boldsymbol\tau\mathbf n_b)dA$。其 $x$ 分量叫阻力 $D$，$y$ 分量叫升力 $L$。

### 升阻力系数与参考面积

系数定义为 $C_D=D/(\rho U_\infty^2A/2)$、$C_L=L/(\rho U_\infty^2A/2)$，必须指定参考面积 $A$。

### 环量符号与单位翼展升力

二维环量 $\Gamma=\oint\mathbf u\cdot d\mathbf l$ 取逆时针为正。单位翼展升力记为 $L'$，单位 N/m。对于以下理想外流模型，带符号的结论是 $L'=-\rho U_\infty\Gamma$；只讨论大小时才写 $|L'|=\rho U_\infty|\Gamma|$。

## 表面受力与控制体动量

表面压力和剪切产生升阻力；围住整个物体的大控制体则用流体动量变化计算同一股力。不存在“上下两团空气必须同时到达后缘”的约束。环量多少也不能靠伯努利方程单独指定，还需要几何与合适的尾缘、启动过程条件。

## 证明：二维理想升力从远场动量积分得到

假设稳态、不可压、外部无黏无旋、物体有限大小、没有净源流，远处趋于均匀速度 $U_\infty$；忽略体力，压力可用同一伯努利常数。若存在均匀重力，应先扣除静水压，把以下 $L'$ 理解为扣除浮力后的流动附加升力；不能把浮力漏掉后仍称总受力。二维外部调和势的远场由均匀流、环量项和衰减的谐波组成。衰减势的各项为 $r^{-n}\cos n\vartheta$ 或 $r^{-n}\sin n\vartheta$（可代回 Laplace 方程检验），所以相应速度至少为 $O(r^{-2})$；净源流为零排除了径向 $1/r$ 项。

因此在大圆 $r=R$ 上，$u_r=U_\infty\cos\vartheta+O(R^{-2})$，$u_\vartheta=-U_\infty\sin\vartheta+\Gamma/(2\pi R)+O(R^{-2})$。伯努利展开给 $p-p_\infty=\rho U_\infty\Gamma\sin\vartheta/(2\pi R)+O(R^{-2})$；笛卡尔竖直速度为 $u_y=u_r\sin\vartheta+u_\vartheta\cos\vartheta=\Gamma\cos\vartheta/(2\pi R)+O(R^{-2})$。

控制体动量平衡与作用反作用给物体所受竖直力
$$L'=-\lim_{R\to\infty}\int_0^{2\pi}[\rho u_yu_r+(p-p_\infty)\sin\vartheta]R\,d\vartheta.$$
代入前面的首项，动量通量给 $\rho U_\infty\Gamma\int\cos^2\vartheta\,d\vartheta/(2\pi)=\rho U_\infty\Gamma/2$，压力项再给同样的一半；合计得到 $L'=-\rho U_\infty\Gamma$。水平方向的一阶项含 $\sin\vartheta\cos\vartheta$，全周积分为零，故该理想模型阻力为零。这正暴露其不能描述黏性尾迹和真实阻力的边界。

真实有限翼展、分离、失速、可压缩效应会违反上述理想条件。球体的 Stokes 阻力及其低 Reynolds 假设在“低 Reynolds 数与润滑流”补章推导，不把线性阻力当普遍平方阻力系数常数。

## 例题：从系数换算受力
空气密度 1.2 kg/m³，速度 20 m/s，翼参考面积 0.5 m²。某已知工况的升力系数 0.8、阻力系数 0.06，则动压 $q=\rho U^2/2=240\,\mathrm{Pa}$。升力 $F_L=96\,\mathrm N$，阻力 $F_D=7.2\,\mathrm N$，升阻比约 13.3。

如果速度改变而 Reynolds 或 Mach 数明显改变，系数也可能变，不能不加条件地认为受力总严格正比于速度平方。超过失速迎角时升力系数可下降，阻力增大；“迎角越大升力越大”只在一定范围成立。

## 练习
1. 例题中参考面积加倍，保持系数和工况不变，升力是多少？
<details><summary>查看解析</summary>

升力加倍为 192 N。但改变几何后系数未必保持原值，这是假设性比例计算。
</details>

2. 为什么势流绕圆柱可预测零阻力，却与实际不同？
<details><summary>查看解析</summary>

理想稳态不可压无黏无旋模型给出对称压力分布，缺少真实黏性边界层、分离和尾迹，即达朗贝尔佯谬揭示了模型边界。
</details>
