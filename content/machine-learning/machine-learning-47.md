---json
{
  "id": "machine-learning-47",
  "title": "完整研究项目：冷却数据、物理基线与下一次实验",
  "group": "09 · AI、传热与可复现研究",
  "minutes": 110,
  "level": "研究实践",
  "tags": [
    "可复现代码",
    "独立实验划分",
    "物理约束消融",
    "失败分析"
  ],
  "objectives": [
    "独立运行NumPy冷却研究基线并解释每项输出",
    "隔离训练、验证和测试run并完成超参数选择",
    "比较估参模型、纯数据代理和物理约束代理",
    "以预设失败案例与灵敏度规划下一次实验"
  ],
  "prerequisites": [
    "machine-learning-38",
    "machine-learning-39",
    "machine-learning-41",
    "machine-learning-43",
    "machine-learning-46"
  ],
  "summary": "用一个不依赖深度学习框架的小项目走完研究流程：先给诚实基线，再比较物理约束，最后用失败结果决定补什么实验。",
  "quiz": {
    "question": "下面哪一种步骤属于测试集泄漏？",
    "options": [
      "只用训练run估计冷却率",
      "按验证run选择物理项权重",
      "看到测试误差后反复修改多项式阶数并仍称其为最终测试"
    ],
    "answer": 2,
    "explanation": "测试输出一旦用于模型选择就失去独立最终评价作用；要保留新的未见实验才能重新进行确认性测试。"
  },
  "lab": null,
  "revision": "2026-09-30 · AI与传热研究扩展"
}
---

## 研究问题与模型定义

**基线模型** 是首先应当比较的简单方案。**代理模型** 用便宜的映射近似原问题的输入输出。**消融** 在其他设置保持可比时去掉或改变某个组成部分，以判断结果来自哪里。本节使用可解释的多项式代理，完整流程只需Python和NumPy；数据全部由给定的冷却模型合成，代理函数为多项式。

本项目问：对同一块材料、同一冷却机制，多次实验中的温度噪声存在共同偏移时，少量数据是否足以估计冷却率？增加物理约束，能否改善一个简单代理模型？改变换热条件后，原模型怎样失败？三个问题分别涉及参数估计、模型比较与超出训练范围时的失效。

最终交付包括固定随机种子、物理常数、分组清单、候选超参数、选择规则、全部模型的测试指标及预设失败案例。代码不下载数据，不读取私人文件，不需要PyTorch或GPU。

## 物理模型与数据生成假设

设m=0.2 kg、c=900 J/(kg·K)、A=0.01 m²、h=18 W/(m²·K)，热容C=mc=180 J/K。忽略辐射与其他输入，环境温度Ta恒定，物体内部近似均温，则

$$C\frac{dT}{dt}=-hA(T-T_a),\quad
\beta=\frac{hA}{C}=0.001\ {\rm s}^{-1},\quad \tau_c=1/\beta=1000\ {\rm s}.$$

这个集中参数近似通常要先检查Bi=hLc/k足够小；Lc=V/A，k为固体导热系数。代码没有给出完整几何与k，因此只把均温作为合成生成假设，不能据此宣布某个真实试样符合该假设。

参考工况T0=80 ℃、Ta=20 ℃，1000 s时T=20+60/e≈42.0728 ℃。不同run轻微改变已知的T0、Ta，h保持不变。每条曲线叠加一个该run共享的随机偏移和逐点独立噪声，展示“多帧不等于多次独立实验”。本例T0、Ta视为另行准确给定的条件，不用测试曲线的首点或末点估计它们。

## 模型、单位和选择规则

### 一个参数的物理基线

定义固定t*=1000 s、x=t/t*、u=(T−Ta)/(T0−Ta)，理论为u=e⁻γx，其中γ=βt*。只用训练run在事先规定的γ网格上最小化以K²计的温度误差，得到γ̂；再换算β̂=γ̂/t*和ĥ=β̂C/A。网格搜索有离散精度限制，输出应保留合适位数，并说明网格分辨率。

### 两种共享表示的代理

取u(x)=1+Σj=1ᵈ wj xʲ，初值u(0)=1自动成立。纯数据模型只拟合无量纲观测；物理约束模型再惩罚

$$r(x)=u'(x)+\widehat\gamma u(x)
=\widehat\gamma+\sum_{j=1}^d w_j[jx^{j-1}+\widehat\gamma x^j].$$

损失是数据误差项、λ倍配点残差均方和η∥w∥²之和。先把每个无量纲数据残差乘以该run的已知初温差与固定60 K参考温差之比，再平方平均；等价地，每个平方误差的权重是该比值的平方。

具体地，令 $e_i=u(x_i)-y_i$，其中 $y_i$ 是无量纲观测，$s_i=\Delta T_i/(60\,\mathrm K)$，$\Delta T_i=T_{0,i}-T_{a,i}>0$。则
$$L_d=\frac1N\sum_{i=1}^N(s_ie_i)^2
=\frac1N\sum_{i=1}^Ns_i^2e_i^2
=\frac{\mathrm{MSE}_{T}}{(60\,\mathrm K)^2}.$$
温度残差是 $\Delta T_i e_i$，因此该数据项与基线的温度误差权重一致。比如两项 $e=[1,1]$、$s=[0.5,2]$，正确均方为 $(0.25+4)/2=2.125$；若只给平方误差乘一次s，会错成1.25。

η为预设的微小岭项。所有损失项均无量纲，γ̂仅来自训练run，这样“物理参数”不会暗中包含测试信息。

令 $\Phi_{ij}=x_i^j$，$R_{ij}=jz_i^{j-1}+\widehat\gamma z_i^j$，z为固定配点，N为训练观测数、M为配点数，$D_s=\operatorname{diag}(s_1,\ldots,s_N)$。矩阵与右端必须一起作相同的行缩放：
$$A_{\rm stack}=\begin{bmatrix}D_s\Phi/\sqrt N\\ \sqrt{\lambda/M}R\\ \sqrt\eta I\end{bmatrix},\qquad
b_{\rm stack}=\begin{bmatrix}D_s(y-\mathbf1)/\sqrt N\\ -\widehat\gamma\sqrt{\lambda/M}\mathbf1\\ \mathbf0\end{bmatrix}.$$
因此 $\|A_{\rm stack}w-b_{\rm stack}\|^2=L_d+(\lambda/M)\sum_{i=1}^M r(z_i)^2+\eta\|w\|^2$。

数据块对应代码的 `sample_scale`，物理块的负号来自残差中的常数 $\widehat\gamma$。代码用 `lstsq` 求解，避免显式形成逆矩阵；其最小化的欧氏残差平方和见[NumPy 官方定义](https://numpy.org/doc/stable/reference/generated/numpy.linalg.lstsq.html)。此例是凸二次问题，不涉及深网络的非凸优化困难。

### 实验分组、验证选参与消融

24次独立合成run随机分成14次训练、5次验证、5次测试。d和λ只按验证温度RMSE选择；测试结果不参与选择。纯数据与物理模型使用相同候选阶数。另设“错误物理”消融：保留已选阶数及λ，只把残差中的γ̂乘1.6，检查强行写错物理的代价。

本例的平方损失没有完整利用run共同偏移的协方差结构，因此不声称是已知相关噪声下的最有效估计；可用广义最小二乘或随机截距模型继续扩展。本例也不按逐帧独立的假设生成置信区间。

测试只有5个独立run，演示流程足够，不能代表真实部署置信度。代码同时打印对带噪观测和无噪真值的误差；后者仅在合成数据中可得，真实实验不能称已知真值，须说明参考仪器的不确定度。

## 完整可运行程序

复制整个代码块到一个Python文件运行。需要已有NumPy，程序只输出文本；相同NumPy版本和种子下可复现数值，不同线性代数实现可能有末位差别。`truth`仅用于最终合成诊断，不用于拟合或选参。

```python
import math
import numpy as np

SEED = 20260930
MASS, CP, AREA, H_TRUE = 0.2, 900.0, 0.01, 18.0
CAPACITY = MASS * CP
T_SCALE = 1000.0
BETA_TRUE = H_TRUE * AREA / CAPACITY
TIME = np.linspace(0.0, 1800.0, 19)
DEGREES = (2, 3, 4, 5)
LAMBDAS = (1e-4, 1e-2, 1.0, 100.0)
RIDGE = 1e-8


def make_runs():
    rng = np.random.default_rng(SEED)
    runs = []
    for run_id in range(24):
        t0 = 80.0 + rng.uniform(-5.0, 5.0)
        ta = 20.0 + rng.uniform(-2.0, 2.0)
        truth = ta + (t0 - ta) * np.exp(-BETA_TRUE * TIME)
        run_bias = rng.normal(0.0, 0.25)
        observed = truth + run_bias + rng.normal(0.0, 0.20, TIME.size)
        runs.append(dict(id=run_id, t0=t0, ta=ta,
                         y=observed, truth=truth))
    return runs


runs = make_runs()  # All data in this program are SYNTHETIC.
order = np.random.default_rng(SEED + 1).permutation(len(runs))
train_ids, val_ids, test_ids = order[:14], order[14:19], order[19:]
assert set(train_ids).isdisjoint(val_ids)
assert set(train_ids).isdisjoint(test_ids)
assert set(val_ids).isdisjoint(test_ids)
train = [runs[int(i)] for i in train_ids]
valid = [runs[int(i)] for i in val_ids]
test = [runs[int(i)] for i in test_ids]


def rmse(predict_u, selected_runs, target="y"):
    # Equal weight per run, then equal weight per time within each run.
    per_run = []
    for run in selected_runs:
        prediction = run["ta"] + (run["t0"] - run["ta"]) * predict_u(TIME)
        per_run.append(np.mean((prediction - run[target]) ** 2))
    return math.sqrt(float(np.mean(per_run)))


# Fit the one-parameter physical baseline using TRAIN only.
gamma_grid = np.linspace(0.4, 1.6, 601)
train_errors = [rmse(lambda t, g=g: np.exp(-g * t / T_SCALE), train)
                for g in gamma_grid]
gamma_hat = float(gamma_grid[int(np.argmin(train_errors))])
beta_hat = gamma_hat / T_SCALE
h_hat = beta_hat * CAPACITY / AREA


def basis(x, degree):
    powers = np.arange(1, degree + 1)
    return x[:, None] ** powers[None, :]


def fit_proxy(degree, lam, gamma):
    x = np.tile(TIME / T_SCALE, len(train))
    y = np.concatenate([(r["y"] - r["ta"]) / (r["t0"] - r["ta"])
                        for r in train])
    phi = basis(x, degree)
    sample_scale = np.repeat([r["t0"] - r["ta"] for r in train], TIME.size) / 60.0
    z = np.linspace(0.0, TIME[-1] / T_SCALE, 81)
    powers = np.arange(1, degree + 1)
    derivative = powers[None, :] * z[:, None] ** (powers[None, :] - 1)
    residual_matrix = derivative + gamma * basis(z, degree)
    matrix = np.vstack([sample_scale[:, None] * phi / math.sqrt(x.size),
                        math.sqrt(lam / z.size) * residual_matrix,
                        math.sqrt(RIDGE) * np.eye(degree)])
    rhs = np.concatenate([sample_scale * (y - 1.0) / math.sqrt(x.size),
                          -gamma * math.sqrt(lam / z.size) * np.ones(z.size),
                          np.zeros(degree)])
    weights = np.linalg.lstsq(matrix, rhs, rcond=None)[0]

    def predict(t):
        return 1.0 + basis(np.asarray(t) / T_SCALE, degree) @ weights

    return predict, weights


# Validation chooses the degree for each family, and lambda for physics.
def select(candidates):
    results = []
    for degree, lam in candidates:
        predict, weights = fit_proxy(degree, lam, gamma_hat)
        results.append((rmse(predict, valid), degree, lam, predict, weights))
    return min(results, key=lambda item: (item[0], item[1], item[2]))


pure = select([(degree, 0.0) for degree in DEGREES])
physical = select([(degree, lam) for degree in DEGREES for lam in LAMBDAS])
wrong_predict, wrong_weights = fit_proxy(physical[1], physical[2], 1.6 * gamma_hat)
models = [
    ("ODE baseline", lambda t: np.exp(-beta_hat * np.asarray(t))),
    ("data proxy", pure[3]),
    ("physics proxy", physical[3]),
    ("wrong physics", wrong_predict),
]

print("SYNTHETIC ONLY; NumPy", np.__version__, "seed", SEED)
print("train / validation / test run IDs:")
print(train_ids.tolist(), val_ids.tolist(), test_ids.tolist())
print("beta_hat [1/s] = %.6f; h_hat [W/(m^2 K)] = %.3f" % (beta_hat, h_hat))
print("data degree =", pure[1])
print("physics degree, lambda =", physical[1], physical[2])
print("model | validation K | test observed K | test latent K")
# These test evaluations occur AFTER selection; do not use them to retune.
for name, predict in models:
    print("%s | %.5f | %.5f | %.5f" %
          (name, rmse(predict, valid), rmse(predict, test),
           rmse(predict, test, target="truth")))

# A prespecified time-extrapolation failure test, using the same physical law.
future_t = np.linspace(2000.0, 4000.0, 21)
future_true = np.exp(-BETA_TRUE * future_t)
# A different h has NOT been supplied as an input to any model.
ood_true = np.exp(-1.6 * BETA_TRUE * TIME)
print("model | future 2000-4000s K | unseen h=28.8 K")
for name, predict in models:
    future_error = 60.0 * np.sqrt(np.mean((predict(future_t) - future_true) ** 2))
    ood_error = 60.0 * np.sqrt(np.mean((predict(TIME) - ood_true) ** 2))
    print("%s | %.5f | %.5f" % (name, future_error, ood_error))

# One measurement in a NEW independent run, equal temperature noise variance.
# This is a local, one-parameter design calculation, not a global optimum.
candidate_t = np.linspace(100.0, 1800.0, 171)
sensitivity = 60.0 * candidate_t * np.exp(-beta_hat * candidate_t)
best_time = float(candidate_t[int(np.argmax(sensitivity ** 2))])
print("next-run single measurement time [s] =", best_time)
print("continuous sensitivity optimum [s] =", 1.0 / beta_hat)
print("reference T(1000s) [C] =", 20.0 + 60.0 / math.e)
```

## 各预设工况下的结果比较

本书用NumPy 1.26.4实际运行上述程序，得到β̂=0.001002 s⁻¹、ĥ=18.036 W/(m²·K)。两种代理均选5阶，物理权重选0.01。以下都是同一次固定种子合成实验的RMSE，不是性能保证：

| 模型 | 测试观测 / K | 测试无噪真值 / K | 时间外推 / K | 未见h=28.8工况 / K |
| --- | --- | --- | --- | --- |
| ODE基线 | 0.27425 | 0.03709 | 0.02024 | 8.26155 |
| 纯数据代理 | 0.27657 | 0.03999 | 1.21029 | 8.26527 |
| 物理代理 | 0.27574 | 0.03823 | 4.50160 | 8.26467 |
| 错误物理 | 0.51370 | 0.46856 | 305.90561 | 7.87857 |

物理代理在本次同分布测试中只略有改善，时间外推反而更差。错误物理在某个OOD列中偶然略小，也不能抵消它在其余工况的明显失败。比较结论应同时包含各项预设评估与失败工况。

训练出的β̂应在0.001 s⁻¹附近，而不是精确等于生成参数；噪声和参数网格都会影响结果。ODE基线只估一个参数，知道正确结构时可能胜过更复杂代理，这是合理结果。物理代理是否改善同分布测试误差，由实际运行输出决定，不预先保证。

“错误物理”与选中的物理代理共享阶数及λ，仅改变残差系数。若它变差，说明物理信息的正确性比名称更重要。无噪真值列与带噪观测列的差异，帮助辨别模型误差和测量误差；不能把拟合每个随机波动当成进步。

时间外推测试把预测延长到训练范围之外。多项式可能弯回去、变负或爆增，尽管在0—1800 s内拟合良好。另一个预设测试把真实h改为28.8 W/(m²·K)，但模型没有h这个输入，也没有见过这种工况；大误差说明任务信息不足，不能通过事后删除该工况来“修复分数”。新增h或流量输入时，也要重新收集覆盖相应范围的独立run。

## 序贯实验设计与真实数据扩展

只估β、T0和Ta已知、单次新测量的温度误差方差不随时间变化时，灵敏度平方在t=1/β处最大。代码用训练β̂在预设候选时间中选一个新run的测量时刻，约1000 s。它是局部设计建议；若同时估Ta或传感器时间常数，就需多个不同时间点使灵敏度方向可区分。

重复同一run的许多时刻仍共享偏移。多点联合设计时应使用含相关性的协方差矩阵，而不是简单累加每点信息；安排新的独立run可帮助分离共同偏差。在“实验设计”互动中采用同一180 J/K热容和1000 s时间常数核对趋势；“冷却”入门互动使用的物性以其界面所列参数为准，比较前需统一时间常数。

换成真实CSV前，先按[实验数据](#/course/machine-learning/machine-learning-46)的字段约定记录run_id、时间、T0、Ta、温度、输入及标定版本。保留原始数据；仅把合成生成器替换为经过校验的读取步骤，继续保留分组隔离和同样的基线。检查是否有辐射、非均温或传感器滞后，再决定是否扩展方程。真实实验需另做重复性、参数区间与预测区间覆盖检查；本段代码没有完成这些验证。

## 练习

### 练习一：参数换算

如果训练得到β̂=0.00102 s⁻¹，其他常数不变，ĥ是多少？

<details><summary>查看解析</summary>

ĥ=β̂C/A=0.00102×180/0.01=18.36 W/(m²·K)。这是条件于C和A准确的估计；若C有误差，应把它传播到h，而不是只报告曲线拟合误差。

</details>

### 练习二：什么才是一次合法消融

看完测试结果后把纯数据模型阶数增到12，却保持物理模型原样，再称物理约束带来提升，问题是什么？

<details><summary>查看解析</summary>

一是测试集参与了选参，二是比较的模型容量和搜索预算变了。应事先定义共同候选范围，只用验证集选择，再用未参与决策的测试run比较。测试结论也应报告失败案例而非只报胜出的模型。

</details>

### 练习三：合成数据的边界

代码中的物理代理在全部测试run上很好，是否证明实际铝板实验也准确？

<details><summary>查看解析</summary>

没有。合成生成器预设了均温、恒h、恒Ta和指定噪声；真实试样可能不满足。需要真实标定、几何与Bi检查、未见run和独立测温参考，才能评价该应用。合成测试的主要价值是确认流程和受控假设下的行为。

</details>

## 资料与范围

按实验分组的原则参照[官方分组交叉验证文档](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data)，物理残差的角色与[PINN原始方法](https://maziarraissi.github.io/PINNs/)对应；上述数据、程序、代理族和失败工况均为原创教学设计。本项目没有训练DeepONet/FNO，没有把合成标签伪称实测，也没有构造带有限样本覆盖保证的置信区间。
