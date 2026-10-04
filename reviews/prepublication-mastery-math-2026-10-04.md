# 发布前数学分级练习逐题复核 · 2026-10-04

对象为 [mastery-exercises-math.json](../content/mastery-exercises-math.json) 中全部24题：微积分12题、线性代数12题，共8个课程锚点，每个锚点包含基础理解、常规应用、综合提高各1题。本轮逐题读取完整题干、solution全部步骤、checkpoints、pitfall、知识点、方法、核验说明及显式先修要求，并重新推演关键计算与推理；没有以脚本通过代替审读。

这一补审补齐了[数学55节复核报告](prepublication-math-2026-10-04.md)中明确留下的“未逐字重读独立JSON练习库”范围。该旧报告描述的是上一轮实际范围，不回写成当时已经做过。

## 结论与精确修改

未发现题目数值答案、单位、推理方向或证明的实质错误。所有24题ID、题干、所属课程与难度保持不变，仅修订两个字段：

1. `mastery-calculus-01-01.verification`：原先写不存在的 `verify_math_exercises.py`，改为实际文件 `tools/mastery/verify_math.py`，case名称保持 `calculus-01-01`。
2. `mastery-linear-algebra-02-03.solution`：在退化相容分支的参数族后补明 `t∈R`。这是把原来默认的实数参数范围写全，没有更改解集、数值或分类条件。

其余字段逐一比较相同。未修改任何课文quiz、测试阈值或数学验证脚本；未生成data.js，未冻结总审校清单。精确字段差异另存本地 `work/prepublication-mastery-math-changes.json`。

## 逐题记录

下表每行均以该题完整JSON对象为审读范围，索引链接到修订后源文件的ID行；“核对记录”覆盖题干要求、解答步骤与适用边界，不只是最终数字。

| 题目索引 | 层级 | 核对记录 |
| --- | --- | --- |
| [mastery-calculus-01-01](../content/mastery-exercises-math.json#L3) | 基础理解 | 分别复核根号非负、分母非零、对数真数为正及三者交集；定义域 (−2,1)∪(1,6]，−2/1 排除而6合法。题干与边界解答正确。仅把核验说明中的旧脚本名改为实际工具路径。 |
| [mastery-calculus-01-02](../content/mastery-exercises-math.json#L25) | 常规应用 | T(6)=33，正斜率使合法值域为[18,38]；达到35的6.8分钟在域内，40对应8.8分钟超域。明确区分代数外推与模型支持范围；分钟/摄氏度使用一致。 |
| [mastery-calculus-01-03](../content/mastery-exercises-math.json#L47) | 综合提高 | 用±1的相同像否定单射；限制到非负区间后逐一说明唯一原像及满射。平方根分支和输入输出区间正确，反函数值1/2与倒数16未混淆。 |
| [mastery-calculus-03-01](../content/mastery-exercises-math.json#L69) | 基础理解 | 完整展开 s(1+h)=2+4h+3h²；在h≠0时相除后才取极限。差商4+3h，左右数值4.3和3.7，瞬时速度4 m/s；位置与速度的单位正确。 |
| [mastery-calculus-03-02](../content/mastery-exercises-math.json#L91) | 常规应用 | 两个模型均满足s(2)=4、s(3)=7；B的右差商为1+2h，A恒为3。限定区间端点采用右导数，只有明确延伸后才谈双侧；平均速度3与瞬时速度不可确定的结论正确。 |
| [mastery-calculus-03-03](../content/mastery-exercises-math.json#L113) | 综合提高 | h=0.04/0.02，线性值0.92/0.96，真值0.9216/0.9604；误差0.0016/0.0004，仅后者满足0.001。四倍误差比例来自精确二次式，未错误推广至任意可导函数。 |
| [mastery-calculus-07-01](../content/mastery-exercises-math.json#L135) | 基础理解 | 有向位移6−6=0，路程6+6=12；完整5秒上的平均速度0和平均速率12/5。单点速度选择不影响积分，零净位移没有被解释为静止。 |
| [mastery-calculus-07-02](../content/mastery-exercises-math.json#L157) | 常规应用 | 逐一重算左右取点的功率和330/390 J、原函数360 J及端点均值360 J；梯形精确性限于线性功率。热输入与系统储能不同、还需其他能量通道的提醒正确。 |
| [mastery-calculus-07-03](../content/mastery-exercises-math.json#L179) | 综合提高 | 两次求导路线一致：H=x⁴+x²−2，H′=4x³+2x；H(0)=−2源于反向积分，H′(−1)=−6源于上限移动。被积函数正与积分/导数正的逻辑边界正确。 |
| [mastery-calculus-15-01](../content/mastery-exercises-math.json#L204) | 基础理解 | 偏导在出发点为4、9；位移(0.02,−0.01)给df=−0.01。二次余项0.0004，实际变化−0.0096，函数由11变10.9904；下降方向与绝对/有向误差未混淆。 |
| [mastery-calculus-15-02](../content/mastery-exercises-math.json#L226) | 常规应用 | 把向左速度译为−1，链式率3(−1)+4=1 K/s；当下抵消速度−4/3 m/s。保持该速度到t=2时率为4 K/s，并明确下一时刻模型仍有效的假设。 |
| [mastery-calculus-15-03](../content/mastery-exercises-math.json#L248) | 综合提高 | 两轴的差商均零；y=x²且x≠0时函数恒1/2，与两轴极限0不一致。不连续因而不全可微的推理方向正确；反例不要求穷举所有路径。 |
| [mastery-linear-algebra-01-01](../content/mastery-exercises-math.json#L273) | 基础理解 | 逐分量得到x+2y=7、2x−y=4，解(3,2)回代两坐标正确。权重与标准坐标的区别没有混同；两个给定向量独立，解确为唯一。 |
| [mastery-linear-algebra-01-02](../content/mastery-exercises-math.json#L295) | 常规应用 | 无额外限制的解(−1,2)回代为(0,3)；非负条件下2x+y=0强迫两个权重均零，又与第二式冲突。区分代数可解和现实可行，未误称原线性系统无解。 |
| [mastery-linear-algebra-01-03](../content/mastery-exercises-math.json#L317) | 综合提高 | v=2u使全体解为(3−2t,t)，t任意实数；给出的第三组(2,1/2)也成立。输出第二坐标总为第一坐标两倍，故(3,7)不可达；没有把两组样本解称为完整解集。 |
| [mastery-linear-algebra-02-01](../content/mastery-exercises-math.json#L339) | 基础理解 | 逐行核对y−z=−1、2y+3z=13、5z=15，后一步使用已更新的第二行；回代(1,2,3)满足全部原方程。非零主元支持唯一性。 |
| [mastery-linear-algebra-02-02](../content/mastery-exercises-math.json#L361) | 常规应用 | 第一错误确为常数列未变；正确第二行为[0,1|2]，解(1,2)。错误解第二行左端22，乘零后的伪解(5,0)违反原第二行；具体反例证明解集改变。 |
| [mastery-linear-algebra-02-03](../content/mastery-exercises-math.json#L383) | 综合提高 | 消元得(a−2)y=b−4；a≠2时两个分式回代正确，a=2下分别为恒等/矛盾。补出解族(2−t,t)的t∈R，把全部实解的参数范围写全；原答案集合不变。 |
| [mastery-linear-algebra-03-01](../content/mastery-exercises-math.json#L405) | 基础理解 | 先B后A得(8,3)，总矩阵AB=[[2,2],[0,1]]；相反次序得(14,3)，BA=[[2,4],[0,1]]。尺寸合法不蕴含可交换，结合律与交换律区别正确。 |
| [mastery-linear-algebra-03-02](../content/mastery-exercises-math.json#L427) | 常规应用 | 反解x₂=y₂−y₁、x₁=3y₁−2y₂，所得逆与A两侧乘积均为I；输出(7,10)恢复(1,3)。逐元素倒数反例的AC左上角为3，足以否定单位阵。 |
| [mastery-linear-algebra-03-03](../content/mastery-exercises-math.json#L449) | 综合提高 | 两个非零矩阵相乘为零；Au=Av=(1,0)但u≠v。可逆条件下左乘逆并用结合律完成约消证明；结论限于题中方阵，不把非零直接等同可逆。 |
| [mastery-linear-algebra-10-01](../content/mastery-exercises-math.json#L471) | 基础理解 | 标准内积、非零方向的条件完整；系数9/5，投影(18/5,9/5)，残差(2/5,−4/5)，点积零和距离平方4/5。方向倍增使系数9/10而投影不变。 |
| [mastery-linear-algebra-10-02](../content/mastery-exercises-math.json#L493) | 常规应用 | 两组展开和配方逐项一致：3(c−3)²+14与4(c−15/4)²+83/4，正系数保证唯一最小。温差与平方和单位正确，不凭权重解释测量真伪，也不横比不同目标的最小值判准确性。 |
| [mastery-linear-algebra-10-03](../content/mastery-exercises-math.json#L515) | 综合提高 | 两个独立方向张成整个W；正交条件给t=s=2，候选在W中。对任意点的距离平方分解2(t−2)²+(s−2)²+2证明全局唯一，最短距离√2与距离平方2区分正确。 |

## 验证与覆盖边界

完成上述审读和两处文字修订后，仅重跑相关的 `python -X utf8 tools/mastery/verify_math.py`：24题精确算术/符号用例、8个锚点及JSON结构检查全部通过。没有重复运行与本次两字段变化无关的广泛数值测试。此结果与逐题审读相互补充，不构成形式化无错保证。

这24题对应微积分01/03/07/15、线代01/02/03/10。它们不能代表对55节每节都有一套分级训练，也未覆盖全部级数、多重积分、向量积分、谱分解、SVD或Jordan应用题。其他章节正文已有的例题和课尾练习在55节报告中另行审读；本轮没有凭24题测试的通过来声称整套本科习题训练量已经充分。

修订前源文件SHA-256：`31f565c8d125545edfcaf0a2c8524caa4979ac826615253f4828d80197eb3970`。

修订后源文件SHA-256：`2162c474e83342ed01cf71d54f4ece7b8b6b0084460bb6c87a1d12ab5b3e4f82`。文件保持UTF-8/LF。摘要只识别审读版本，不能替代上表的数学论证。主任务需据这次源文件变化重新冻结、构建并验证网站及App资源。
