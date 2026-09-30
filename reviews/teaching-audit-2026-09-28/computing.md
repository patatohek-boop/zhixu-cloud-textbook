# Python 与机器学习教学审读及修订记录

日期：2026-09-28。范围：Python 29节、机器学习35节。采用教学设计与学科正确性检查，不代表外部教师认证。以下为修改前已确认的基线问题；原文行号指本轮改动前版本。后续修订会增加段落，因此最终行号可能移动。

## 已确认基线问题

1. **P1／教学缺陷：字符串例题提前使用列表推导式和解包。** `content/python/python-04.md:65`：`name, value_text, unit = [part.strip() for part in raw.split(",")]`。循环到第6节才讲，推导式到第10节才讲；本例没有先展示简单 split 结果、三个字段或替代逐步写法。初学者能复制但难以独立改写。建议先按 split → 逐字段 strip → float → 格式化四步演示，将压缩写法留为已学推导式后的对照。
2. **P2／教学缺陷：基础语法、概念定义与复杂反例的局部次序倒置。** `content/python/python-07.md:47–66` 先展开可变默认列表的两函数反例，第68–82行才演示普通单参数函数；`content/python/python-06.md:38–58` 在首次解释 for/while（第63行）前先给循环不变量、求和符号和完整证明。数学内容本身可保留，但应先建立可追踪的最小程序和符号，再完成论证，否则新增严谨内容遮住了第一次学习的入口。
3. **P2／教学缺陷：多个独立概念堆叠在同一段。** `content/python/python-02.md:39–41` 同时介绍身份、类型、值、可变性、别名和浅复制；`content/python/python-04.md:39` 同时定义str、码点、bytes、编码、解码与字形差异。建议按概念关系分段/小标题，配一组对象或文本的持续例子，不按句号机械拆散论证。
4. **P2／教学缺陷：学习目标没有对应的生成性练习。** `content/python/python-07.md:125–130` 两道题仅判断返回值和解释默认列表；未要求从零设计函数，也未检验新增参数签名目标。`content/python/python-10.md:85–90` 没有要求编写推导式，而目标包含“编写简单推导式”。建议每个核心能力至少有一道需编写/修改代码且提供边界样例与解析的题。

## 修订状态

已完成两门课全部64篇正文阅读与内容修订，保留全部旧ID、原推导、例题、自测和插图。教学缺陷与技术条件遗漏分别记录；不以缺少元类、任意相关FDR理论等合理进阶范围作为必修缺失。

## 补充确认的问题（同一修改前基线）
5. **P1 技术表述错误：二分查找的候选边界。** `content/python/python-19.md:73` 原文“维护左闭右开区间 [left,right)，答案若存在且尚未确认，就不会被错误丢弃”。在 [1,3,3,7,9] 查 3，right 更新到 1 时首个答案索引 1 已不在 [0,1) 内。算法正确，但不变量直觉表述错误；应区分未决元素区间 [left,right) 与插入位置候选边界 [left,right]。
6. **P1 技术条件遗漏：EM 分解的无穷量。** `content/machine-learning/machine-learning-16.md:44–48` 原文“取任意概率 q(z)”后无条件写 log p=F+KL，随后允许 q>0、r=0 时 KL=∞。此时 F=−∞，等式右侧是未定义的 −∞+∞。应限制正证据、有限联合值及 q 的正支持落在后验正支持内；支持不合时仅保留下界，不能使用该加法恒等式。
7. **P2 教学缺陷：科学库首次使用没有可执行的环境路线。** `content/python/python-20.md:58` 原文“安装环境准备好后，可导入 numpy”；`content/machine-learning/machine-learning-29.md:60` 原文“运行前需准备 NumPy 与 scikit-learn”。Python11 提到虚拟环境和包名占位命令，但未给后续所用库的实际安装与导入核验步骤。零基础读者遇到 ModuleNotFoundError 时难判断解释器与安装对象是否一致。应给同一解释器调用 pip 的具体命令，并从20–22与ML29链接回该入口。
8. **P2 教学缺陷：推导内容多，但练习未检验关键能力。** `content/machine-learning/machine-learning-10.md:87–92` 仅问 sigmoid(0) 和多标签选择，未检验本章梯度；`content/machine-learning/machine-learning-12.md:93–98` 仅问 k=1 风险与分数非概率，未检验间隔/对偶；`content/machine-learning/machine-learning-16.md:99–104` 仅问归一化与非全局最优，未完成一次加权 M 步。应补数值可手算、有中间答案的计算题，避免把能复述名称当成会做算法。
9. **P2 教学缺陷：概率统计桥梁把不同层次压在一个段落。** `content/machine-learning/machine-learning-03.md:63–65` 同段出现正交变换、卡方、独立性、t 分布与区间；`content/machine-learning/machine-learning-31.md:82` 在单段完成 Beta 归一化、分部积分、两式联立与后验均值；`content/machine-learning/machine-learning-35.md:81` 将非退化密度分解、退化坐标处理和零概率解释叠放。内容基本正确但初学者难找到前提与推导入口；应分别标记所用结论、计算步骤、边界条件并保留全部数学内容。

10. **P2／教学缺陷：测试框架先于类与继承。** `content/python/python-15.md:61` 为 `class MeanTests(unittest.TestCase)`；类、继承和 self 到第16节才系统定义。应在本节先给仅使用已学函数、assert、try/except的完整可运行检查，再把 unittest 保留为有明确回读路径的扩展。


## 修订结果与教学判断

两门课均已逐篇按实际意义划分概念段落和三级标题，没有按字数或句号机械分段。定义、符号与条件、直观解释、推导步骤以及代码状态各有阅读入口；证明内容保留，不把程序运行通过写成定理证明。共301个 h3，其中 Python104个、机器学习197个；以实际逐章统计为准。

已修复上述10项基线问题。Python重点补齐早期语法与环境路线、基本测试路径以及二分不变量；机器学习重点补齐先修链接、EM有限性条件、SVM证书与完整M步、梯度更新与数值核验、样本量和预测区间计算。另修正Python26仍把已讲装饰器列作纯导读的旧范围表述，补ML14等相关方差公式的正方差与成员数条件，统一ML24成本阈值的概率前提。

这套内容更适合作为有明确先修的本科自学讲义或课程配套教材。机器学习的概率证明、GLM、泛化界和GP仍不是仅凭四则运算即可通读的零基础路线；已增加具体数学入口及回读安排。练习现在能检验更多实际计算与编程能力，但尚未形成足够覆盖整学期考核的分层作业库、评分量规和综合实验集。这些限制不应被“代码全部通过”掩盖。

## 验证

- `tools/verify_computing.py`：64篇、57个独立可运行代码块、795个KaTeX公式、34项联合数值/契约检查全部通过。
- 运行环境：Python3.10.10、NumPy1.26.4、pandas2.3.3、Matplotlib3.9.2、scikit-learn1.7.2。此次未测试所有操作系统或新解释器版本；环境章节以实际解释器、导入和版本核验为准。
- 新手算独立核算：逻辑损失0.5876561461；GMM方差152/75；同时更新网络损失0.73156608；样本量门槛415/1659；GP两个区间分别约[0.723,2.477]与[0.285,2.915]。核算时纠正了新增代码输出注释的末位舍入，正文为0.5877。
- 检查新增小标题未插入代码围栏或展示公式内部；两门课自有审计记录追加修订，未删除旧记录，覆盖与标题仍一致。
- 本任务只修改两门课内容、对应审计与本报告；未编辑共享UI、构建器或验证工具，未执行git提交或变更分支，未负责网站/APK发布。

## 本轮实际核对的主源

- [Python官方虚拟环境教程](https://docs.python.org/3/tutorial/venv.html)：核对项目环境、同一解释器的pip调用与依赖记录。
- [Python官方unittest基本例](https://docs.python.org/3/library/unittest.html#basic-example)：核对TestCase继承、测试方法与异常断言的所需语法。
- [Python官方bisect_left](https://docs.python.org/3/library/bisect.html#bisect.bisect_left)：核对插入位置将左右元素划分为小于目标和大于等于目标；本报告的半开区间反例为独立构造。
- [Stanford CS229 EM正文](https://cs229.stanford.edu/notes2020spring/cs229-notes8.pdf)：实际阅读第2节与2.1节的下界、后验E步及KL形式，并独立补齐教材加法恒等式的有限性边界。没有把外部讲义的省略当成教材可省略条件的理由。

## 逐章覆盖范围

以下列出全部64篇，均阅读了正文、定义条件、例题、练习与先修衔接；“分段重点”指本轮实际修改的部分，不表示本章其他内容未阅读。

### Python：29篇

|课文|标题|分段或实质修订重点|
|---|---|---|
|[python-01](../../content/python/python-01.md)|第一段程序：环境、交互式与脚本|增加退出 REPL、切换文件夹和使用同一解释器运行脚本的步骤。|
|[python-02](../../content/python/python-02.md)|变量、对象与基本类型|可变性与名字的类型；浅复制只分离外层；先求右侧再解包。|
|[python-03](../../content/python/python-03.md)|数值计算、浮点误差与单位|有限表示的证明；按数值规则选择类型；单位换算为什么要平方。|
|[python-04](../../content/python/python-04.md)|字符串、编码与格式化|把超前的列表推导式与解包改为逐字段索引，补 split、strip、float、显示四步及 CSV 范围。|
|[python-05](../../content/python/python-05.md)|条件分支与逻辑判断|布尔值与一般对象的真值；有限性是分类前提；短路运算的返回值。|
|[python-06](../../content/python/python-06.md)|循环、不变量与终止|把 for/while/range 机制与一次状态跟踪移到完整循环证明之前，保留原不变量、终止和浮点边界。|
|[python-07](../../content/python/python-07.md)|函数、参数与作用域|普通函数调用先于共享默认列表反例；新增关键字参数函数的编写练习和三种调用核查。|
|[python-08](../../content/python/python-08.md)|列表、元组与序列|列表与元组的修改范围；单元素元组的逗号；返回副本与原地排序。|
|[python-09](../../content/python/python-09.md)|字典、集合与数据建模|哪些对象能作为键；不可变不一定可哈希。|
|[python-10](../../content/python/python-10.md)|推导式、迭代器与生成器|增加普通循环、列表推导式与生成器状态的对照编写练习，含独立可运行答案。|
|[python-28](../../content/python/python-28.md)|函数对象、闭包与装饰器|自由变量与闭包；外层调用结束后仍可访问；绑定与当时数值的区别。|
|[python-11](../../content/python/python-11.md)|模块、包与虚拟环境|补 Windows/macOS/Linux 虚拟环境解释器安装四种科学库、版本核查与导入故障定位。|
|[python-12](../../content/python/python-12.md)|文件、路径与持久化|文件对象与读取模式；自动清理保证的边界。|
|[python-13](../../content/python/python-13.md)|CSV、JSON 与数据交换|键与日期的表示约定；格式版本和迁移；把数据含义与文件一起保存。|
|[python-14](../../content/python/python-14.md)|异常处理与输入契约|finally 的执行范围；检查与使用之间仍可能变化；业务异常与退出信号。|
|[python-15](../../content/python/python-15.md)|测试、调试与最小复现|先给只用已学语法的三类测试，保留 unittest 类作为带第16节回读链接的扩展。|
|[python-16](../../content/python/python-16.md)|类、对象与组合|方法如何接收当前实例；共享类属性的不同结果；super 与方法查找。|
|[python-17](../../content/python/python-17.md)|数据类、类型注解与接口|注解不会自动执行检查；为每个实例创建字段；构造后的运行时校验。|
|[python-29](../../content/python/python-29.md)|对象协议、上下文管理与结构匹配|进入与退出的配对规则；退出返回值控制异常传播。|
|[python-18](../../content/python/python-18.md)|标准库工具箱与可靠随机性|统计与计时是不同任务；数值统计与有效样本数；测量经过多久。|
|[python-19](../../content/python/python-19.md)|算法、递归与计算复杂度|纠正半开未决元素区间与闭合插入位置边界的混淆，补 [1,3,3,7,9] 的反例追踪。|
|[python-27](../../content/python/python-27.md)|递归与分治：阶乘、插入排序和归并排序|正确性与终止分开论证；为何一定回到基本情况；合并的逐项选择。|
|[python-20](../../content/python/python-20.md)|NumPy 数组、形状与广播|在第一次 NumPy 代码前给出环境准备入口。|
|[python-21](../../content/python/python-21.md)|pandas 表格、缺失与连接|在第一次 pandas 代码前给出环境准备入口，分开计数分母与写入语义。|
|[python-22](../../content/python/python-22.md)|Matplotlib 科学绘图|给出绘图库准备入口及无图窗环境的图片保存方法。|
|[python-23](../../content/python/python-23.md)|数值方法：求根、积分与微分方程|反例：残差小而解仍不准；梯形公式的误差条件；时间推进的稳定条件。|
|[python-24](../../content/python/python-24.md)|性能、并发与异步导读|协程对象与执行资源；为何一行更新仍需同步；解释器实现的条件。|
|[python-25](../../content/python/python-25.md)|完整项目：实验记录分析器|成功与失败的输出；逻辑记录与物理行；逐条校验与分组。|
|[python-26](../../content/python/python-26.md)|复现、版本管理与持续学习|修正装饰器仍只属未讲路线的旧说法，与已有第28节一致。|

### 机器学习：35篇

|课文|标题|分段或实质修订重点|
|---|---|---|
|[machine-learning-01](../../content/machine-learning/machine-learning-01.md)|从真实问题到学习任务与基线|增加具体数学与 Python 先修入口，区分手算章节和代码环境。|
|[machine-learning-02](../../content/machine-learning/machine-learning-02.md)|概率桥梁：条件概率、贝叶斯与分布|符号与一次观测；方差、标准差与协方差；各恒等式分别需要什么。|
|[machine-learning-03](../../content/machine-learning/machine-learning-03.md)|统计桥梁：估计、不确定性与检验|把正态均值区间证明拆为四步，并明确正交变换、卡方与联合高斯的回读路线。|
|[machine-learning-04](../../content/machine-learning/machine-learning-04.md)|数学桥梁：向量、矩阵与梯度|明确矩阵、求导、积分三项先修检查及对应课文，分开优化与联合高斯阅读路线。|
|[machine-learning-31](../../content/machine-learning/machine-learning-31.md)|参数估计：似然、最大似然与最大后验|把一致性、Beta 分部积分、后验均值与众数拆成可逐步核对的小节。|
|[machine-learning-05](../../content/machine-learning/machine-learning-05.md)|数据划分、预处理与信息泄露|拟合与使用变换；独立测试结论的边界；对照：泄露如何改变训练表示。|
|[machine-learning-06](../../content/machine-learning/machine-learning-06.md)|评估指标、偏差方差与交叉验证|R² 的参照对象；精确率、召回率与未定义情形；第二步：逐项检查交叉项。|
|[machine-learning-34](../../content/machine-learning/machine-learning-34.md)|有限样本为何能学习：集中不等式与泛化界|拆开重加权方差、指数矩、一致界与 ERM 界，新增由误差门槛反解样本量的练习。|
|[machine-learning-07](../../content/machine-learning/machine-learning-07.md)|线性回归与最小二乘|残差与可识别性；第三步：求斜率并检查最小性；参数不唯一而预测唯一。|
|[machine-learning-08](../../content/machine-learning/machine-learning-08.md)|梯度下降、学习率与数值检查|光滑性约束坡度变化；第二步：代入负梯度方向；第三步：选择保证下降的步长。|
|[machine-learning-09](../../content/machine-learning/machine-learning-09.md)|正则化、特征工程与非线性扩展|截距与中心化约定；零点为何可以直接成为最优点。|
|[machine-learning-10](../../content/machine-learning/machine-learning-10.md)|逻辑回归、多分类与交叉熵|增加四点逻辑回归一次平均交叉熵更新、稳定损失代码与损失总和缩放练习。|
|[machine-learning-32](../../content/machine-learning/machine-learning-32.md)|感知机：线性分类与错误次数界|范数界与间隔的尺度；合并不等式得到次数界；如何报告算法停止。|
|[machine-learning-33](../../content/machine-learning/machine-learning-33.md)|广义线性模型：指数族、连接函数与计数回归|将泊松截距例题移到引用它的 IRLS 数值步之前，分开工作响应、正规方程与重加权。|
|[machine-learning-11](../../content/machine-learning/machine-learning-11.md)|朴素贝叶斯与生成式分类|从后验到行动；离散特征的两种机制；第一步：展开类别对数得分。|
|[machine-learning-12](../../content/machine-learning/machine-learning-12.md)|近邻、距离与支持向量机|增加两点 SVM 原对偶可行性与零间隙的完整手算证书。|
|[machine-learning-35](../../content/machine-learning/machine-learning-35.md)|概率预测：贝叶斯线性回归与高斯过程|分开非退化与退化条件高斯证明，增加潜在函数区间和未来观测区间的数值对照。|
|[machine-learning-13](../../content/machine-learning/machine-learning-13.md)|决策树、划分与剪枝|局部选择与整树最优；Gini 的极值；回归划分的平方和分解。|
|[machine-learning-14](../../content/machine-learning/machine-learning-14.md)|随机森林、提升与集成学习|在等相关方差证明前明确 m≥2、公共方差正的条件。|
|[machine-learning-15](../../content/machine-learning/machine-learning-15.md)|聚类：k-means、层次与密度|几何假设的含义；第二步：更新非空簇的均值；第三步：说明收敛的是目标值。|
|[machine-learning-16](../../content/machine-learning/machine-learning-16.md)|高斯混合与 EM 算法|补 EM 分解正证据和支持条件，排除 −∞+∞；加入软计数、均值、方差的一次完整 M 步。|
|[machine-learning-17](../../content/machine-learning/machine-learning-17.md)|PCA、降维与流形可视化|投影方差；把方向展开到特征向量基；最优方向的非唯一性。|
|[machine-learning-18](../../content/machine-learning/machine-learning-18.md)|神经网络与反向传播|增加两参数中心差分核验与同时更新后的损失计算。|
|[machine-learning-19](../../content/machine-learning/machine-learning-19.md)|深度网络优化与泛化|偏差修正与更新；二阶矩的含义；推导的平稳假设。|
|[machine-learning-20](../../content/machine-learning/machine-learning-20.md)|卷积网络与图像学习|位置之间共享什么；第一步：约束核的放置位置；第二步：数合法整数起点。|
|[machine-learning-21](../../content/machine-learning/machine-learning-21.md)|序列、RNN 与时间预测|模型状态与物理状态；历史输入的影响；梯度消失的一组充分条件。|
|[machine-learning-22](../../content/machine-learning/machine-learning-22.md)|注意力与 Transformer|自注意力与交叉注意力；缩放推导的适用范围；凸组合性质的边界。|
|[machine-learning-23](../../content/machine-learning/machine-learning-23.md)|自监督、迁移与生成模型导读|迁移与生成不是同一维度；条件生成；截断历史才增加模型假设。|
|[machine-learning-24](../../content/machine-learning/machine-learning-24.md)|不平衡、阈值与概率校准|统一成本阈值例题的条件概率前提，避免把粗分箱校准直接等同于真实后验。|
|[machine-learning-25](../../content/machine-learning/machine-learning-25.md)|解释、稳健性与公平性|置换重要性测量模型；条件于真实阳性的比较；同时约束两类错误率。|
|[machine-learning-26](../../content/machine-learning/machine-learning-26.md)|部署、漂移与 MLOps|标签漂移的保持条件；协变量迁移的保持条件；支持缺失不能靠重加权弥补。|
|[machine-learning-27](../../content/machine-learning/machine-learning-27.md)|强化学习：状态、行动与长期回报|策略与马尔可夫性；价值是回报的条件期望；第二步：极限存在且为固定点。|
|[machine-learning-28](../../content/machine-learning/machine-learning-28.md)|因果推断：关联之外的边界|一致性把观测与潜在结果连接；比较组必须在目标区域存在；识别公式逐步使用的假设。|
|[machine-learning-29](../../content/machine-learning/machine-learning-29.md)|完整实验：可复现的回归流程|给完整回归项目补同一虚拟环境的安装核查及运行命令入口。|
|[machine-learning-30](../../content/machine-learning/machine-learning-30.md)|高级主题地图与继续学习|风险率不同于生存概率；第二步：相乘得到生存曲线；为什么未来分数的秩均匀。|
