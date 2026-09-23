---json
{
  "id": "machine-learning-29",
  "title": "完整实验：可复现的回归流程",
  "group": "07 · 综合实践与高级导读",
  "minutes": 25,
  "level": "进阶",
  "tags": [
    "项目",
    "Pipeline",
    "回归"
  ],
  "objectives": [
    "运行完整 Pipeline",
    "解释合成实验的证据边界"
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
  "lab": null
}
---

## 实验问题
我们用两个合成特征预测连续目标，目的是验证完整学习流程，而不是宣称解决真实工程问题。数据在本机生成，无需下载、密钥或联网服务。运行前需准备 NumPy 与 scikit-learn。固定种子帮助复现，但不同库版本可能产生细微差异。

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

## 为什么这样组织
首先生成数据，再划分训练与测试。标准化放入 Pipeline，所以交叉验证每一折都只用该折训练部分计算均值与尺度。GridSearchCV 根据训练内部验证选择 alpha，最后使用整个训练集重新拟合最佳方案。测试集只在最后比较一次，保持相对独立的评估角色。

scikit-learn 的打分接口常把损失取负数，以统一成“越大越好”。neg_mean_squared_error 越接近零越好，不能把负号误读成数学上的负均方误差。最终报告时使用原始 RMSE 与 MAE，便于按目标尺度理解。

## 预期与检查
目标确实由线性关系加噪声生成，所以岭回归应明显优于只预测均值的基线。噪声标准差为 0.5，合理模型的测试 RMSE 通常在这一量级附近，但有限样本与随机划分会带来波动，不能要求每次恰好等于 0.5。

若结果异常，检查 X 与 y 是否对齐、是否错误把目标作为特征、是否在全数据上拟合变换。再画残差图，检查误差是否随预测值变化。这里没有组与时间依赖，因此普通随机划分合理；换成真实设备数据时必须重新设计协议。

## 扩展与限制
可加入无关特征比较正则化，加入二次项比较特征工程，改变噪声观察不可约误差，或构造分布变化检验泛化。每次只改变一个因素，并记录配置。合成数据能验证程序逻辑和已知机制下的行为，不能证明真实任务数据质量、因果关系或部署安全。

最终保存代码、依赖、随机种子、指标与任务说明。若继续在同一测试集上反复挑选新方案，应承认它已参与开发，并准备新的独立最终评估数据。

## 给结果写一段完整解释
本次已验证运行中，均值基线测试均方根误差约为三点三四，岭回归约为零点五七；具体数值会受环境与版本影响。这个差距符合数据由线性关系生成的设定，说明模型利用了输入信息，而不是只猜平均值。
但一次划分不足以证明所有抽样下都同样好。可在保持最终测试独立的前提下，用训练内部重复验证观察选择稳定性，并报告变化范围。不要在看到结果后删掉误差较大的样本来提高分数，除非先有可辩护的数据质量规则。
如果更换为真实温度任务，还需补充时间划分、传感器分组、单位检查与观测延迟。代码流程可以复用，科学假设与评估设计必须重新确认，这正是完整项目与仅运行示例之间的差别。

## 练习
1. 为什么标准化必须放在 Pipeline 内？
<details><summary>查看解析</summary>这样每折只从训练部分拟合变换，避免验证数据参与均值和尺度估计。</details>

2. 为什么 RMSE 不会随着模型复杂度无限降低到零？
<details><summary>查看解析</summary>未来目标包含不可预测随机噪声，且过度复杂模型可能增加估计方差。训练误差为零不代表测试误差为零。</details>
