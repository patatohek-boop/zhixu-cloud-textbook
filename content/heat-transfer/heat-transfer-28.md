---json
{
  "id": "heat-transfer-28",
  "title": "边界层积分法：从方程到可计算近似",
  "group": "07 · 传热传质专题",
  "minutes": 40,
  "level": "进阶",
  "tags": [
    "积分守恒",
    "动量厚度",
    "热边界层积分",
    "试探剖面"
  ],
  "objectives": [
    "定义并区分积分守恒、动量厚度、热边界层积分",
    "逐步完成守恒式积分、二次剖面闭合及平方根厚度",
    "核对边界、单位和模型误差"
  ],
  "prerequisites": [
    "heat-transfer-11",
    "heat-transfer-12",
    "heat-transfer-13"
  ],
  "summary": "边界层积分法：从方程到可计算近似：以可复核的步骤补足核心模型。",
  "quiz": {
    "question": "边界层积分法选择试探温度剖面的目的是什么？",
    "options": [
      "使守恒不必满足",
      "把未知函数转化为有限参数以闭合近似",
      "证明经验系数绝对精确",
      "消除边界条件"
    ],
    "answer": 1,
    "explanation": "积分守恒仍须满足；误差来自剖面假设和其他边界层近似。"
  },
  "lab": null
}
---
## 积分守恒与试探剖面

### 积分法与试探剖面

积分法在边界层横向积分局部守恒式，再用满足主要边界条件的**试探剖面**把未知场转化为厚度等参数。

### 几何、温度与坐标

取零压梯、等温平板，来流 $U$、壁温 $T_s$、远场 $T_\infty$，沿板x、离壁y。

### 动量厚度

动量厚度 $\theta_m=\int_0^\infty(u/U)(1-u/U)dy$，单位m，不是温差。

### 同厚度闭合的限制

本例限 $Pr=\nu/\alpha=1$，并假设速度层与热层厚度相同为 $\delta(x)$。这是为了形成一个可完全手算的闭合例，不是说所有流体两层都同厚。

## 剖面近似的作用与误差

积分法保留整个边界层的守恒关系，用少数参数和试探剖面表示空间分布。它减少了求解量，但剖面假设会带来模型误差；积分守恒成立并不意味着每一点都满足原微分方程。

## 从局部能量方程得到积分式

用连续性 $u_x+v_y=0$，将 $uT_x+vT_y=\alpha T_{yy}$重写为

$$\partial_x[u(T-T_\infty)]+\partial_y[v(T-T_\infty)]=\alpha T_{yy}.$$

从壁面到无穷远积分。壁面无穿透 $v=0$，远处温差为0，故第二项边界贡献消失；远处温度梯度为0。得到

$$\frac d{dx}\int_0^\infty u(T-T_\infty)dy=-\alpha T_y|_w=\frac{q_w''}{\rho c_p}.$$

类似对零压梯动量守恒积分得到 $U^2d\theta_m/dx=\tau_w/\rho$。这两条是积分守恒，尚不足以独立决定整个未知函数。

## 选剖面并完整闭合

在 $0\le\eta=y/\delta\le1$ 选 $u/U=2\eta-\eta^2$、$(T-T_\infty)/(T_s-T_\infty)=(1-\eta)^2$；外层取外流值。它们满足壁面无滑移、壁温、外缘值和外缘零梯度。关键积分

$$\int_0^1(2\eta-\eta^2)(1-\eta)^2d\eta=\frac2{15}.$$

壁面温度梯度为 $-2(T_s-T_\infty)/\delta$。代入能量积分式并消去温差：$(2/15)U\delta'=2\alpha/\delta$。积分、前缘取厚度0，得到

$$\delta^2=\frac{30\alpha x}{U},\qquad h_x=\frac{2k_f}{\delta},\qquad Nu_x=\frac2{\sqrt{30}}Re_x^{1/2}\quad(Pr=1).$$

动量积分给同样形式、把α换成ν，因Pr=1而相容。系数约0.365，精确边界层数值解约0.332，差约10%；这明确展示试探剖面不是精确解。

## 例题1

$U=1$ m/s、$x=0.1$ m、$\nu=\alpha=10^{-5}$ m²/s、$k_f=0.03$ W/(m·K)。

1. $Re_x=10^4$，积分近似 $Nu_x\approx36.5$。
2. $h_x=Nu_x k_f/x\approx10.95$ W/(m²·K)。
3. 相似解近似给9.96 W/(m²·K)，差异来自剖面模型；增加数字精度不会去掉这项误差。

## 练习

**练习1**　相同条件x增大4倍，厚度和当地h怎样变？

<details><summary>查看解析</summary>

厚度增2倍，h减半，来自 $\delta\propto\sqrt x$，前提是仍层流并保持模型条件。

</details>

**练习2**　若Pr远大于1，能否直接使用同厚度假设？

<details><summary>查看解析</summary>

不能。热扩散相对慢，热层通常更薄，需设独立热层厚度并按两层重叠区域重新积分。

</details>

## 继续阅读

对应[MIT 2.51 Integral methods主题](https://ocw.mit.edu/courses/2-51-intermediate-heat-and-mass-transfer-fall-2008/pages/readings/)。上述二次剖面为完整教学演示，不应替代高精度关联或处理分离、湍流与强浮升的模型。
