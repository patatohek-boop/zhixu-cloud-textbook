---json
{
  "id": "machine-learning-29",
  "title": "完整实验：可复现的回归流程",
  "group": "07 · 综合实践与高级导读",
  "minutes": 45,
  "level": "进阶",
  "tags": [
    "项目",
    "Pipeline",
    "回归"
  ],
  "objectives": [
    "运行完整 Pipeline",
    "解释合成实验的证据边界",
    "定义合成机制、训练协议和实验结论范围"
  ],
  "prerequisites": [
    "machine-learning-28"
  ],
  "summary": "用合成数据完成基线、划分、交叉验证、最终评估与结果解释。",
  "quiz": {
    "question": "这段实验的测试集用于什么？",
    "options": [
      "选择每个 alpha",
      "最终比较固定方案与基线",
      "拟合标准化均值",
      "生成训练标签"
    ],
    "answer": 1,
    "explanation": "超参数选择在训练内部完成，测试集保留给最终评估。"
  },
  "lab": null,
  "revision": "2026-09-28 · 概念分段、教学先修与练习复核"
}
---

## 数据生成机制与样本划分
本节生成 X 为 240×2 矩阵，每行是一条独立合成样本，两特征为标准正态抽样。目标为
$$Y=3X_1-2X_2+\varepsilon,\qquad \varepsilon\sim N(0,0.5^2),$$
噪声与特征及其他样本独立。真实条件均值已知为 f*(x)=3x₁−2x₂，因此这是检验学习流程的可控实验，不是真实设备数据。随机种子规定一次伪随机过程，不把该次样本变成总体。

25% 测试比例产生 60 个测试、180 个训练样本；训练内部五折每折 144 个训练、36 个验证。

### 每折重新拟合与最终重拟合

每折标准化只拟合该折 144 个样本，选定 alpha 后再用全部 180 个训练样本重新拟合，最后才读取 60 个测试标签计算指标。

## 不可约误差与有限测试集波动
对任意由独立训练数据得到的模型 f，固定输入 x：
$$E[(Y-f(x))^2|x,f]
=E[(f^*(x)-f(x)+\varepsilon)^2]
=(f^*(x)-f(x))^2+0.25.$$
噪声均值零使交叉项消失。

### 总体下界与有限测试误差

再对输入求期望，总体 MSE≥0.25；若恰好知道 f*，等号成立。总体 RMSE 下界对应 0.5，但**有限测试集的经验 RMSE 可以低于或高于 0.5**，不能把总体界当成每次随机样本都满足的界。

即使条件均值完全已知，新的观测仍含随机噪声；有限的 60 个测试点可能恰好具有较小或较大的噪声。岭回归还需从有限样本估计系数，惩罚也可能引入偏差，所以一次约 0.57 的结果并不矛盾。

## 数据与评估条件
先确认 X 的两列未包含目标、X 与 y 行序未错位、噪声生成独立；再确认搜索只传入训练数据。打印最优 alpha 是选参结果，不是物理真值。

### Pipeline 能保证的边界

将全部训练与评估放在相同 Pipeline 内能防止一类泄露，但无法代替时间或设备粒度的设计。

下文代码可独立运行，其比较结论针对这里给定的数据生成机制。更换真实任务后，独立同分布假设、单位、标签延迟和划分都必须重新审查。

## 运行入口

先完成[科学计算环境与版本核验](#/course/python/python-11)，确认 `numpy`、`sklearn` 可以从同一个解释器导入。把本节完整代码保存为 `regression_experiment.py`，在该环境运行；例如 Windows 使用 `.\.venv\Scripts\python.exe regression_experiment.py`。本节不需要下载数据。先记录实际库版本，再比较文中的示例指标。

## 实验代码
代码比较均值基线与岭回归，并在训练集内用五折交叉验证选择正则化参数。固定随机种子便于复现，不同库版本仍可能产生细微数值差异。

```python
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, KFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error

rng = np.random.default_rng(42)
X = rng.normal(size=(240, 2))
y = 3 * X[:, 0] - 2 * X[:, 1] + rng.normal(scale=0.5, size=240)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)
baseline = DummyRegressor(strategy="mean").fit(X_train, y_train)
pipeline = make_pipeline(StandardScaler(), Ridge())
search = GridSearchCV(
    pipeline,
    {"ridge__alpha": [0.01, 0.1, 1.0, 10.0]},
    cv=KFold(n_splits=5, shuffle=True, random_state=7),
    scoring="neg_mean_squared_error"
)
search.fit(X_train, y_train)
for name, model in [("baseline", baseline), ("ridge", search.best_estimator_)]:
    prediction = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, prediction))
    mae = mean_absolute_error(y_test, prediction)
    print(name, "RMSE:", round(rmse, 3), "MAE:", round(mae, 3))
print("selected:", search.best_params_)
```

## Pipeline 与交叉验证的执行顺序
首先生成数据，再划分训练与测试。标准化放入 Pipeline，所以交叉验证每一折都只用该折训练部分计算均值与尺度。

### 选参、重拟合与测试的顺序

GridSearchCV 根据训练内部验证选择 alpha，最后使用整个训练集重新拟合最佳方案。测试集只在最后比较一次，保持相对独立的评估角色。

scikit-learn 的打分接口常把损失取负数，以统一成“越大越好”。neg_mean_squared_error 越接近零越好，不能把负号误读成数学上的负均方误差。最终报告时使用原始 RMSE 与 MAE，便于按目标尺度理解。

## 指标解释与残差检查
目标确实由线性关系加噪声生成，所以岭回归应明显优于只预测均值的基线。噪声标准差为 0.5，合理模型的测试 RMSE 通常在这一量级附近，但有限样本与随机划分会带来波动，不能要求每次恰好等于 0.5。

若结果异常，检查 X 与 y 是否对齐、是否错误把目标作为特征、是否在全数据上拟合变换。再画残差图，检查误差是否随预测值变化。这里没有组与时间依赖，因此普通随机划分合理；换成真实设备数据时必须重新设计协议。

## 扩展与限制
可加入无关特征比较正则化，加入二次项比较特征工程，改变噪声观察不可约误差，或构造分布变化检验泛化。每次只改变一个因素，并记录配置。合成数据能验证程序逻辑和已知机制下的行为，不能证明真实任务数据质量、因果关系或部署安全。

最终保存代码、依赖、随机种子、指标与任务说明。若继续在同一测试集上反复挑选新方案，应承认它已参与开发，并准备新的独立最终评估数据。

## 结果示例与外推范围
本次已验证运行中，均值基线测试均方根误差约为三点三四，岭回归约为零点五七；具体数值会受环境与版本影响。这个差距符合数据由线性关系生成的设定，说明模型利用了输入信息，而不是只猜平均值。
但一次划分不足以证明所有抽样下都同样好。可在保持最终测试独立的前提下，用训练内部重复验证观察选择稳定性，并报告变化范围。不要在看到结果后删掉误差较大的样本来提高分数，除非先有可辩护的数据质量规则。
如果更换为真实温度任务，还需补充时间划分、传感器分组、单位检查与观测延迟。代码流程可以复用，科学假设与评估设计必须重新确认。

## 练习
1. 为什么标准化必须放在 Pipeline 内？
<details><summary>查看解析</summary>这样每折只从训练部分拟合变换，避免验证数据参与均值和尺度估计。</details>

2. 为什么 RMSE 不会随着模型复杂度无限降低到零？
<details><summary>查看解析</summary>未来目标包含不可预测随机噪声，且过度复杂模型可能增加估计方差。训练误差为零不代表测试误差为零。</details>
