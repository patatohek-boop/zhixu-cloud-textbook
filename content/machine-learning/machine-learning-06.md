---json
{
  "id": "machine-learning-06",
  "title": "评估指标、偏差方差与交叉验证",
  "group": "02 · 可靠评估与线性模型",
  "minutes": 45,
  "level": "基础",
  "tags": [
    "指标",
    "偏差方差",
    "交叉验证"
  ],
  "objectives": [
    "解读混淆矩阵",
    "区分选择与最终评估",
    "定义回归与分类指标及分母"
  ],
  "prerequisites": [
    "machine-learning-05"
  ],
  "summary": "让指标回答实际问题，用重采样估计方案稳定性。",
  "quiz": {
    "question": "TP=8、FP=2 时精确率是多少？",
    "options": [
      "20%",
      "40%",
      "80%",
      "无法计算"
    ],
    "answer": 2,
    "explanation": "精确率为 TP/(TP+FP)=8/10。"
  },
  "lab": null,
  "revision": "2026-09-28 · 概念分段、教学先修与练习复核"
}
---

## 先把“误差小”写成明确公式
对 n 个测试目标 $y_i$、预测 $\hat y_i$，$\mathrm{MAE}=n^{-1}\sum_i|y_i-\hat y_i|$，$\mathrm{MSE}=n^{-1}\sum_i(y_i-\hat y_i)^2$，$\mathrm{RMSE}=\sqrt{\mathrm{MSE}}$。

### R² 的参照对象

残差平方和 SSE 为上式求和部分；$\mathrm{SST}=\sum_i(y_i-\bar y)^2$，$\bar y$ 是此评估集目标均值。仅当 SST>0，$R^2=1-\mathrm{SSE}/\mathrm{SST}$ 按通常公式定义。

二分类中“阳性”是事先指定的目标类别；TP/FP/TN/FN 分别是真阳、假阳、真阴、假阴。

### 精确率、召回率与未定义情形

精确率分母是预测阳性数，召回率分母是真实阳性数，分母为零时必须报告未定义或所选软件处理规则。$F_1=2TP/(2TP+FP+FN)$，不能用来反映所有成本。

## 定理：经典偏差—方差分解
固定输入 x。设未来 $Y=f^*(x)+\varepsilon$，其中 $E[\varepsilon|x]=0$、噪声方差为 σ²，且未来噪声独立于训练数据 D。模型 $\hat f_D(x)$ 会随训练集变化，令 $m(x)=E_D[\hat f_D(x)]$，所有二阶矩有限。

将误差写成
$$Y-\hat f_D(x)=\varepsilon+[f^*(x)-m(x)]+[m(x)-\hat f_D(x)].$$


### 第二步：逐项检查交叉项

展开平方取期望：噪声均值零且与训练独立，涉及噪声的交叉项为零；最后一项均值零，剩余交叉项也为零。因此
$$E[(Y-\hat f_D(x))^2]=\sigma^2+[m(x)-f^*(x)]^2+\operatorname{Var}_D(\hat f_D(x)).$$


### 第三步：解释三个来源

分别是噪声、偏差平方、训练集引起的方差。通俗地说，有“新观测本来随机”“方法平均就偏了”“换套训练数据就变了”三种来源。一次训练的一个分数不能独自识别这三项；该恒等式也不证明模型复杂度增加时验证曲线必定呈 U 形。

## 反例：R² 不是正确率
测试目标为 [0,2]，其均值 1、SST=2；预测都是 3，则 SSE=9+1=10，$R^2=1-10/2=-4$。它只说明在该测试集上比“使用此测试集均值作常数”的参考更差，不表示负的概率。

交叉验证用训练的子集选择方案，最小验证误差本身经过挑选，不能自动当独立最终性能。嵌套交叉验证把“挑参数”整体放到内层，外层评估完整选择程序，而不只是评估一个固定参数。

## 一个分数装不下所有错误
回归常用 MAE、MSE、RMSE。MAE 与目标同单位，MSE 更惩罚大误差，RMSE 恢复目标单位。$R^2=1-\mathrm{SSE}/\mathrm{SST}$ 比较模型与评估集均值基准，在某些测试情形下可以为负；它不是“预测正确百分比”。常数目标时还需注意定义与软件处理。

分类的混淆矩阵记录真阳性 TP、假阳性 FP、真阴性 TN、假阴性 FN。精确率为 TP/(TP+FP)，召回率为 TP/(TP+FN)，分别回答“报警中多少是真的”和“真实事件中找到了多少”。准确率在类别极不平衡时可能掩盖完全漏检。

## 逐步例题：故障检测
一百个样本中有十个故障，模型检出八个，误报五个。则 TP=8、FN=2、FP=5、TN=85，准确率为 93%，精确率为 8/13≈61.5%，召回率为 80%。全部预测正常也有 90% 准确率，但召回率为零。因此指标必须联系错误成本解释。

F1 是精确率与召回率的调和平均，不能表达所有成本，也忽略真阴性。

### 跨阈值的排序评价

ROC 曲线比较不同阈值的真正率与假正率，PR 曲线更直接关注阳性预测质量；极不平衡时应特别检查 PR 表现。

### 概率本身的质量

概率预测还应看对数损失或 Brier 分数，而不只看最终类别。

## 操作闭环：先扫阈值，再封存选择，最后独立评价

第一遍先手算下面四条记录，不必已经会训练分类器。程序分两段：第一段只复核评价计算；第二段在学过[逻辑回归](#/course/machine-learning/machine-learning-10)、[Python 环境](#/course/python/python-11)与[NumPy](#/course/python/python-20)后回做，把训练也接上。所有数据都是原创教学数据，没有实际设备或部署含义。

### 一张分数表产生多个分类决定

正类事先规定为y=1，分数s越大越倾向正类；本例分数没有单位。约定**s≥阈值τ时判为1**，等于阈值也算阳性。先给定四条验证记录的分数，用来单独理解评价：

| 记录 | A | B | C | D |
| --- | --- | --- | --- | --- |
| 真实标签y | 1 | 0 | 1 | 0 |
| 分数s | 0.9 | 0.8 | 0.4 | 0.2 |

这里有两个真实阳性、两个真实阴性。每降过一个不同分数，预测阳性集合才会改变；相同分数必须一起跨过阈值，不能为了得到更好的曲线把同分样本拆开。各矩阵统一使用**行是真实0/1，列是预测0/1**：
$$C=\begin{bmatrix}TN&FP\\FN&TP\end{bmatrix},\quad
\mathrm{FPR}=\frac{FP}{FP+TN},\quad
\mathrm{TPR}=\mathrm{Recall}=\frac{TP}{TP+FN},\quad
\mathrm{Precision}=\frac{TP}{TP+FP}.$$

| 阈值τ | 预测为1的记录 | 矩阵[[TN,FP],[FN,TP]] | FPR | TPR/Recall | Precision |
| --- | --- | --- | --- | --- | --- |
| +∞ | 无 | [[2,0],[2,0]] | 0 | 0 | 未定义 |
| 0.9 | A | [[2,0],[1,1]] | 0 | 1/2 | 1 |
| 0.8 | A、B | [[1,1],[1,1]] | 1/2 | 1/2 | 1/2 |
| 0.4 | A、B、C | [[1,1],[0,2]] | 1/2 | 1 | 2/3 |
| 0.2 | A、B、C、D | [[0,2],[0,2]] | 1 | 1 | 1/2 |

比如τ=0.4时，A和C是真阳，B是假阳，D是真阴，所以TP=2、FP=1、TN=1、FN=0；$F_1=4/(4+1+0)=0.8$。表中比例均无量纲。若真实阴性数为零，FPR未定义；若真实阳性数为零，TPR未定义，不能按这张两类都存在的表硬算ROC-AUC。

### ROC、PR与面积分别怎样得到

ROC以FPR为横轴、TPR为纵轴。按表中顺序连接点：$(0,0)\to(0,1/2)\to(1/2,1/2)\to(1/2,1)\to(1,1)$。梯形面积为
$$\mathrm{AUC}_{\rm ROC}=\frac12\times\frac12+\frac12\times1=\frac34.$$
竖直段宽度为零，不贡献面积。还可用另一种算法自查：把两个阳性分数[0.9,0.4]分别与两个阴性[0.8,0.2]比较，四对中三对阳性更高，所以AUC=3/4。有同分时每对计半胜。这是经验排序指标，不是75%的分类准确率，也不证明分数是校准概率。

PR以Recall为横轴、Precision为纵轴。四个有阳性预测的阈值点为 $(1/2,1)$、$(1/2,1/2)$、$(1,2/3)$、$(1,1/2)$。零预测阳性时Precision本来未定义；画图软件常额外放置(Recall=0, Precision=1)作为端点约定，不能把它读成“没有报警也获得100%可信精确率”。

若要把PR汇总为一个数，必须写明定义。本例采用**average precision（AP）**：阈值降低时，用每次Recall的增加量乘该次Precision，再相加，得 $\mathrm{AP}=\frac12\times1+\frac12\times\frac23=5/6\approx0.833333$。它不是梯形PR面积；按软件端点和直线连接作梯形积分，本例得到19/24≈0.791667。不要把两者都笼统标成同一个“PR-AUC”。

改变一个用于报警的硬阈值，只是在固定曲线上换一个工作点；若连续分数和标签没变，整条ROC和其AUC不变。ROC/PR的坐标、端点及AP定义可核对[ROC接口](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_curve.html)、[PR接口](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_curve.html)与[AP接口](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html)。

### 代码一：把手算表与官方库对齐

这是完整可运行代码，使用 NumPy 与 scikit-learn。`labels=[0,1]` 固定矩阵行列顺序；`drop_intermediate=False` 保留每个不同分数的ROC点。scikit-learn 1.3及以后用+∞表示ROC的全阴性起点；PR返回的阈值是升序，且坐标比阈值多一个约定端点。

```python
import numpy as np
from sklearn.metrics import (confusion_matrix, roc_curve, roc_auc_score,
                             precision_recall_curve, average_precision_score, auc)

y = np.array([1, 0, 1, 0])
s = np.array([.9, .8, .4, .2])
manual_fpr, manual_tpr = [], []
for threshold in [np.inf, .9, .8, .4, .2]:
    prediction = (s >= threshold).astype(int)
    matrix = confusion_matrix(y, prediction, labels=[0, 1])
    tn, fp, fn, tp = matrix.ravel()
    fpr = fp / (fp + tn)
    tpr = tp / (tp + fn)
    precision = None if tp + fp == 0 else tp / (tp + fp)
    manual_fpr.append(fpr)
    manual_tpr.append(tpr)
    print(threshold, matrix.tolist(), "FPR/TPR =", fpr, tpr,
          "precision =", "undefined" if precision is None else round(precision, 6))
fpr, tpr, thresholds = roc_curve(y, s, drop_intermediate=False)
np.testing.assert_allclose(fpr, manual_fpr)
np.testing.assert_allclose(tpr, manual_tpr)
precision, recall, pr_thresholds = precision_recall_curve(y, s)
np.testing.assert_allclose(precision, [.5, 2/3, .5, 1., 1.])
np.testing.assert_allclose(recall, [1., 1., .5, .5, 0.])
np.testing.assert_allclose(pr_thresholds, [.2, .4, .8, .9])
print("ROC-AUC = %.6f; AP = %.6f; trapezoid PR area = %.6f" %
      (roc_auc_score(y, s), average_precision_score(y, s), auc(recall, precision)))
```

前五行应逐行重现表中的矩阵与指标；最后一行为 `ROC-AUC = 0.750000; AP = 0.833333; trapezoid PR area = 0.791667`。这段代码只核查给定分数的评价，没有声称这四个分数由下面的模型训练得到。

### 代码二：仅训练侧拟合，验证选阈值，冻结后看测试

现在把完整流程接上。下段用一维、无量纲特征x和0/1标签表示一个小型合成分类任务。事先给定8条训练、4条验证、4条测试，三组记录身份互不重叠；不能把真实同一设备的相关帧冒充独立记录。模型固定为标准化加逻辑回归，C=1；候选阈值预设为0.3、0.5、0.7，按验证F1最大选择，平手取较高阈值。F1只是本教学任务选定的准则，真实错误代价不同可能要换准则。

这个例子**不重训**最终模型，直接冻结训练得到的预处理、分类器及验证选出的阈值。若更换训练数据重训，分数尺度可能变化，不能无说明地把原阈值仍当已验证。测试阶段预先决定报告矩阵、Precision、Recall、FPR、F1、ROC-AUC和二分类Brier分数 $n^{-1}\sum_i(p_i-y_i)^2$；这里Brier在[0,1]范围且越小越好，用于检查概率误差，与排序和硬决策是不同问题。

```python
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, f1_score, roc_auc_score

# Fixed synthetic records. All choices below are specified before test evaluation.
train_ids = set(range(8))
valid_ids = set(range(8, 12))
test_ids = set(range(12, 16))
assert train_ids.isdisjoint(valid_ids | test_ids)
assert valid_ids.isdisjoint(test_ids)
X_train = np.array([-4., -3., -2., -1., 1., 2., 3., 4.]).reshape(-1, 1)
y_train = np.array([0, 0, 0, 1, 0, 1, 1, 1])
X_valid = np.array([3., 2., .25, -2.]).reshape(-1, 1)
y_valid = np.array([1, 0, 1, 0])
candidates = (.3, .5, .7)
model = make_pipeline(StandardScaler(),
                      LogisticRegression(C=1., solver="lbfgs", tol=1e-12, max_iter=1000))
model.fit(X_train, y_train)  # Both scaler and classifier see TRAIN only.
positive_column = int(np.flatnonzero(model.classes_ == 1)[0])
p_valid = model.predict_proba(X_valid)[:, positive_column]
validation_f1 = [f1_score(y_valid, p_valid >= t, zero_division=0) for t in candidates]
best = max(range(len(candidates)), key=lambda i: (validation_f1[i], candidates[i]))
frozen_threshold = candidates[best]
print("validation F1:", np.round(validation_f1, 6).tolist())
print("frozen threshold:", frozen_threshold)
np.testing.assert_allclose(model[0].mean_, [0.])
np.testing.assert_allclose(model[0].scale_, [np.sqrt(7.5)])

# Test values are first used here. Never feed these results back into selection.
X_test = np.array([-3., -.5, .5, 3.]).reshape(-1, 1)
y_test = np.array([0, 1, 0, 1])
p_test = model.predict_proba(X_test)[:, positive_column]
prediction = (p_test >= frozen_threshold).astype(int)
matrix = confusion_matrix(y_test, prediction, labels=[0, 1])
tn, fp, fn, tp = matrix.ravel()
precision, recall = tp / (tp + fp), tp / (tp + fn)  # Denominators positive here.
fpr = fp / (fp + tn)
f1 = 2 * tp / (2 * tp + fp + fn)
brier = float(np.mean((p_test - y_test) ** 2))
print("test probabilities:", np.round(p_test, 6).tolist())
print("test matrix:", matrix.tolist())
print("precision/recall/FPR/F1: %.6f %.6f %.6f %.6f" % (precision, recall, fpr, f1))
print("test ROC-AUC = %.6f; Brier = %.6f" % (roc_auc_score(y_test, p_test), brier))
```

用 NumPy2.3.5、scikit-learn1.8.0 运行的预期输出如下。其他兼容版本的优化末位可能略异，解释时先核对分组和决策，再看小数：

```text
validation F1: [0.666667, 0.8, 0.666667]
frozen threshold: 0.5
test probabilities: [0.2384, 0.451756, 0.548244, 0.7616]
test matrix: [[1, 1], [1, 1]]
precision/recall/FPR/F1: 0.500000 0.500000 0.500000 0.500000
test ROC-AUC = 0.750000; Brier = 0.178703
```

测试F1比被选中的验证F1低，并不意味着要立即用测试重选阈值。四条测试仅演示计算，无法给出可靠部署保证；可以记录失败并预先规划下一轮验证，若据此修改了方案，下一次确认必须使用新的未参与选择的数据。对测试分数计算事先约定的整条ROC作报告是允许的，利用曲线挑阈值后又把同一测试称为独立评价则不允许。[官方阈值调优说明](https://scikit-learn.org/stable/modules/classification_threshold.html)也把估计分数与选择决策阈值区分开。

## 偏差与方差的直觉

<figure class="teaching-figure"><a href="assets/diagrams/ml-bias-variance.svg" target="_blank" rel="noopener" aria-label="打开大图：常见概念图：复杂度提高时训练误差下降，验证误差可能先下降后上升。过简单偏差风险高，过复杂方差风险高。"><img src="assets/diagrams/ml-bias-variance.svg" alt="常见概念图：复杂度提高时训练误差下降，验证误差可能先下降后上升。过简单偏差风险高，过复杂方差风险高。" loading="lazy"></a><figcaption>常见概念图：复杂度提高时训练误差下降，验证误差可能先下降后上升。过简单偏差风险高，过复杂方差风险高。<br><small>概念示意，非实测数据、无定量刻度；曲线并非所有任务的普遍规律。现代模型可能出现双下降等其他形态，需依据真实验证结果。 · 点按图形可放大。</small></figcaption></figure>


过于简单模型可能无法表达真实规律，训练与验证都差，表现为欠拟合。过于灵活模型可能对训练样本扰动非常敏感，训练好而验证差，表现为过拟合。经典平方误差分解在特定条件下写成偏差平方、方差与不可约噪声之和；实际单次训练不能直接精确分离这些项。

学习曲线观察训练样本增加时的训练和验证误差。增加数据可能缓解高方差，但不能修复错误特征、泄露或不适合的任务定义。训练与验证差距小也不意味着模型好，二者可能都很差。

## 交叉验证的正确位置
K 折交叉验证轮流用一折验证、其余训练，汇总指标后选择超参数。分组或时间结构必须在折划分中保留。若同一组交叉验证既用于挑最优参数又用于宣称最终表现，估计可能乐观；可用独立测试集或嵌套交叉验证处理。

报告各折变化、样本量与评估协议，而非只报最高分。不同折通常不是完全独立实验，不能机械把折间标准差当作严格置信区间。比较模型还要考虑训练成本、延迟、可解释性和维护负担。

## 指标必须对应比较单位
若一个设备产生很多相关记录，逐行准确率可能让高频设备主导结果；按设备汇总又回答不同问题。应事先确定样本权重和汇总层级，并在多个相关指标之间保持一致。
指标分母为零时要定义行为，例如模型从不预测阳性，精确率公式分母为零。软件可能按参数返回零、缺失或警告，报告时应说明，不能把默认填充值当成真实证据。

## 练习
1. 全部预测为多数类能否在不平衡数据上获得高准确率？
<details><summary>查看解析</summary>可以，因此必须检查少数类召回、精确率与错误成本，而不能只看准确率。</details>

2. 为什么测试集不能反复用于选择超参数？
<details><summary>查看解析</summary>选择过程会适应测试集偶然性，使它失去独立评估作用，最终分数可能高估未来表现。</details>

### 练习三：同分样本必须一起跨阈值

另有六条验证记录，分数为 `[0.9,0.7,0.7,0.4,0.3,0.1]`，标签为 `[1,1,0,0,1,0]`。所有分数无量纲，正类为1，仍用s≥τ。依次在τ=+∞、0.9、0.7、0.4、0.3、0.1处写矩阵、FPR、TPR和Precision；求ROC-AUC，并用正负样本两两比较复核。为什么不能把两个0.7分数按标签先后拆开？

<details><summary>查看完整解析、易错点与自查</summary>

三正三负，所以FPR与TPR的分母都为3，只有Precision的分母随预测阳性数改变。

| τ | [[TN,FP],[FN,TP]] | FPR | TPR | Precision |
| --- | --- | --- | --- | --- |
| +∞ | [[3,0],[3,0]] | 0 | 0 | 未定义 |
| 0.9 | [[3,0],[2,1]] | 0 | 1/3 | 1 |
| 0.7 | [[2,1],[1,2]] | 1/3 | 2/3 | 2/3 |
| 0.4 | [[1,2],[1,2]] | 2/3 | 2/3 | 1/2 |
| 0.3 | [[1,2],[0,3]] | 2/3 | 1 | 3/5 |
| 0.1 | [[0,3],[0,3]] | 1 | 1 | 1/2 |

PR坐标由最后两列按(Recall, Precision)读出即可。ROC非零宽度段的面积为 $\frac13\frac{1/3+2/3}{2}+\frac13\frac23+\frac13\times1=\frac{13}{18}\approx0.722222$。两两比较时：阳性0.9赢3次；阳性0.7对阴性0.7计半胜、对0.4和0.1各赢一次；阳性0.3只赢0.1。故 $(3+2.5+1)/9=13/18$。

```python
import numpy as np
from sklearn.metrics import confusion_matrix, roc_auc_score, roc_curve, auc
s = np.array([.9, .7, .7, .4, .3, .1])
y = np.array([1, 1, 0, 0, 1, 0])
for t in [np.inf, .9, .7, .4, .3, .1]:
    matrix = confusion_matrix(y, s >= t, labels=[0, 1])
    print(t, matrix.tolist())
fpr, tpr, _ = roc_curve(y, s, drop_intermediate=False)
pos, neg = s[y == 1], s[y == 0]
pair_auc = np.mean((pos[:, None] > neg) + .5 * (pos[:, None] == neg))
np.testing.assert_allclose([roc_auc_score(y, s), auc(fpr, tpr), pair_auc], [13/18] * 3)
print("ROC-AUC = %.6f" % pair_auc)
```

前六行矩阵应与表一致，最后输出 `ROC-AUC = 0.722222`。易错点：两个0.7分数共用同一阈值，按真实标签人为先放阳性会虚构模型没有提供的排序。自查：每个矩阵元素总和为6，两行总数均为3；降低阈值时TP和FP都不会下降；同分对计半胜，而不是全胜或删除。

</details>

### 练习四：验证选出的阈值，到了测试还能改吗

用正文四条验证分数 `[0.9,0.8,0.4,0.2]`、标签 `[1,0,1,0]`，在事先规定候选τ∈{0.4,0.8,0.9}中选择验证F1最高者，平手取较高阈值。模型和阈值都冻结后，独立测试分数为 `[0.85,0.65,0.35,0.10]`、标签 `[0,1,1,0]`。求所选阈值、测试矩阵、Precision、Recall、FPR、F1和测试ROC-AUC。有人看完测试后建议改为0.35，理由是测试F1更高；这能成为同一次独立最终评价吗？

<details><summary>查看完整解析、易错点与自查</summary>

三个候选的验证F1依次为0.8、0.5、2/3，因此选τ=0.4。测试前两条被判1，后两条被判0，所以TN=FP=FN=TP=1，矩阵为 `[[1,1],[1,1]]`。Precision、Recall、FPR、F1均为1/2。测试阳性分数0.65和0.35各只胜过阴性0.10，输给0.85，四对胜两对，ROC-AUC=1/2。

若改成0.35，TP=2、FP=1、FN=0、TN=1，测试F1确实会变成0.8；然而这个选择已经读取测试标签。这只能记录成探索性改动，需要新的独立测试，不能用同一四条数据确认新阈值。原分数没有改变，所以ROC-AUC仍为1/2；提高某一个测试阈值点的F1不会自动提高排序AUC。

```python
import numpy as np
from sklearn.metrics import confusion_matrix, f1_score, roc_auc_score
s_valid = np.array([.9, .8, .4, .2])
y_valid = np.array([1, 0, 1, 0])
candidates = (.4, .8, .9)
chosen = max(candidates, key=lambda t: (f1_score(y_valid, s_valid >= t), t))
s_test = np.array([.85, .65, .35, .10])
y_test = np.array([0, 1, 1, 0])
matrix = confusion_matrix(y_test, s_test >= chosen, labels=[0, 1])
assert chosen == .4
np.testing.assert_array_equal(matrix, [[1, 1], [1, 1]])
np.testing.assert_allclose(roc_auc_score(y_test, s_test), .5)
print("frozen threshold:", chosen, "test matrix:", matrix.tolist())
print("test F1 = %.6f; test ROC-AUC = %.6f" %
      (f1_score(y_test, s_test >= chosen), roc_auc_score(y_test, s_test)))
```

预期为 `frozen threshold: 0.4 test matrix: [[1, 1], [1, 1]]`，以及 `test F1 = 0.500000; test ROC-AUC = 0.500000`。

易错点：不能先找测试最优阈值再补写“预设”；也不能把验证0.8报告为最终性能。自查：把选择函数的输入圈出来，应只有验证分数、验证标签和预设候选，不应含任何测试信息。小测试集只检查流程，不支持实际部署结论。

</details>
