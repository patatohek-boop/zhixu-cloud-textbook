# 目录重排后的正文课次引用复核

日期：2026-10-04。本次是有界的课次连贯性修复，不重新扩大教学审查范围。

## 依据与结论

扫描`content`中的中文“第…课/节”（包括范围、中文数字和空格形式）及英文`lesson`加数字的引用，并阅读匹配上下文，区分本教材引用、外部文献章节号和解题步骤。构建器`tools/build.py`按各课程`course.json.lessons`顺序生成`chapters`；正文界面`site/assets/app.js`用`c.chapters.indexOf(l)+1`显示“第几节”。章节树按同一数组中的章组归类，因此不能把稳定ID的数字后缀当成当前目录序号。

确认13个文件有14处不匹配：最初13处单课引用，以及补充发现的机器学习“第31—35节”范围引用。修订前已分两次报告给主任务；收到修订确认后才编辑。范围引用指向的5个专题现位于第5、13、14、8、17节，确实不再是连续目录序号。

全部修复均去除错误目录数字，改为准确主题链接。稳定ID、旧链接的目标、章节顺序、课程分组、数学内容及题目保持；原先没有链接的引用补上对应稳定ID链接。没有为统一风格改写仍正确的课次引用。

## 逐处前后对照

下表行号对应此次修复后的Markdown；替换不增加或删除换行。

| 文件与行 | 修复前 | 修复后 | 目标稳定ID与实际目录节次 |
| --- | --- | --- | --- |
| [calculus-14.md:117](../content/calculus/calculus-14.md#L117) | `[三重积分第19课](#/course/calculus/calculus-19)` | `[三重积分与坐标变换](#/course/calculus/calculus-19)` | calculus-19 → 第25节 |
| [calculus-14.md:117](../content/calculus/calculus-14.md#L117) | `[曲面积分第22课](#/course/calculus/calculus-22)` | `[曲面积分与 Gauss 散度定理](#/course/calculus/calculus-22)` | calculus-22 → 第29节 |
| [calculus-23.md:84](../content/calculus/calculus-23.md#L84) | `反例见第 20 节` | `反例见[线积分与保守场中的有孔区域](#/course/calculus/calculus-20)` | calculus-20 → 第27节 |
| [calculus-24.md:124](../content/calculus/calculus-24.md#L124) | `[Python第23课的显式 Euler](#/course/python/python-23)` | `[Python中的显式 Euler 方法](#/course/python/python-23)` | python-23 → 第26节 |
| [calculus-28.md:80](../content/calculus/calculus-28.md#L80) | `指数基础见第 29 节` | `指数基础见[初等函数的微积分基础](#/course/calculus/calculus-29)` | calculus-29 → 第10节 |
| [calculus-31.md:118](../content/calculus/calculus-31.md#L118) | `本课第 19 节还给了` | `[三重积分与坐标变换](#/course/calculus/calculus-19)还给了` | calculus-19 → 第25节 |
| [fluid-mechanics-47.md:43](../content/fluid-mechanics/fluid-mechanics-47.md#L43) | `这一约定与第 20 节一致` | `这一约定与[湍流平均与雷诺应力](#/course/fluid-mechanics/fluid-mechanics-20)一致` | fluid-mechanics-20 → 第28节 |
| [python-15.md:78](../content/python/python-15.md#L78) | `是第12节所学上下文管理器的另一种用途` | `是[文件与上下文管理](#/course/python/python-12)中所学上下文管理器的另一种用途` | python-12 → 第13节 |
| [python-19.md:59](../content/python/python-19.md#L59) | `第 27 节继续给出递归归纳法和排序证明` | `[递归与分治](#/course/python/python-27)继续给出递归归纳法和排序证明` | python-27 → 第22节 |
| [python-27.md:66](../content/python/python-27.md#L66) | `复杂度沿用第19节的常数时间比较与索引模型` | `复杂度沿用[算法与计算复杂度](#/course/python/python-19)中的常数时间比较与索引模型` | python-19 → 第21节 |
| [machine-learning-07.md:76](../content/machine-learning/machine-learning-07.md#L76) | `似然的完整定义和参数概率的区别见第 31 节` | `似然的完整定义和参数概率的区别见[参数估计](#/course/machine-learning/machine-learning-31)` | machine-learning-31 → 第5节 |
| [machine-learning-09.md:65](../content/machine-learning/machine-learning-09.md#L65) | `精确 MAP 对应在第 31 节推导` | `精确 MAP 对应在[参数估计](#/course/machine-learning/machine-learning-31)中推导` | machine-learning-31 → 第5节 |
| [machine-learning-23.md:74](../content/machine-learning/machine-learning-23.md#L74) | `KL 非负已在第16节证明` | `KL 非负已在[高斯混合与 EM 算法](#/course/machine-learning/machine-learning-16)中证明` | machine-learning-16 → 第21节 |
| [machine-learning-30.md:78](../content/machine-learning/machine-learning-30.md#L78) | `第31—35节分别讨论 MLE/MAP、感知机、广义线性模型、有限模型泛化界、贝叶斯回归与高斯过程。` | `相关推导分别见[最大似然与最大后验](#/course/machine-learning/machine-learning-31)、[感知机](#/course/machine-learning/machine-learning-32)、[广义线性模型](#/course/machine-learning/machine-learning-33)、[有限模型泛化界](#/course/machine-learning/machine-learning-34)和[贝叶斯回归与高斯过程](#/course/machine-learning/machine-learning-35)。` | machine-learning-31 → 第5节；machine-learning-32 → 第13节；machine-learning-33 → 第14节；machine-learning-34 → 第8节；machine-learning-35 → 第17节 |

## 保留不改的引用

- 线性代数中的第14、15、17、21节，以及微积分正文指向线代第17节的链接，实际仍与显示顺序一致，保留。
- 热力学与传热学的课次仍按原序，匹配到的第7/10/11/12/14/20/27节、19—22节等未改。
- 流体第61课、Python第1/10节、ML第2/3/36/38/42节及36—47节范围均仍对应当前顺序，保留。
- OpenStax、Stanford CS229、Volkwein、NIST、Fisher信息、Frazier、FNO、伴随法等外部资料的章/节/页码保留；“第一步”等证明步骤、题目编号没有改动。
- 本次未发现需要修改的英文`lesson`加数字引用。

## 实际检查

1. 修改前后逐对象比较全部253节完整front matter：所有元数据完全一致，包括ID、title、group、先修、quiz题干/选项/答案/解释。
2. 对13个修改文件用现有`verify_reader_revision.features`比较代码围栏、显示公式、行内公式、图片引用及各自出现次数，结果全部相同。这项检查保全原内容，不代替数学正确性证明。
3. 对比现存本教材链接，旧链接目标与出现次数均未减少；新链接的目标课文件存在，主题与目标正文标题/相关小节相符。所有文件以UTF-8/LF写入，未引入CRLF。
4. 实际执行`verify_reader_revision.verify(require_frozen=False)`检查本轮内容特征：253个ID与quiz保持，367条精确变更处置仍通过，原始基线81段代码/807处显示公式/10466处行内公式/65张图片及不可变1.5.0清单核验通过。这里只检查特征处置与基线保全，没有把刚发生文字修改的旧冻结快照误称为仍然一致；验证逻辑和阈值没有改动。

精确替换、修改前全文、修改后摘要及检查结果存于`work/prepublication-order-reference-changes.json`。没有运行新的教学数值测试，因为此次不改任何数学表达、数值、代码或答案。没有修改`data.js`、UI、课程配置或中央manifest；网站构建、重新冻结、完整保全/渲染和应用更新由主任务随后执行。本任务在上述标签修订及检查完成后停止，不宣称已经发布。
