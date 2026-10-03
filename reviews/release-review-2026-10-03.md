# 1.5.0 · 基础衔接与完整算例修订

本版以 2026 年 10 月 3 日内容复查为依据，集中修复四项已确认的表述/条件问题，并补齐代表性基础操作链。保留七科253个课号，不新增整门课程，不把目录齐全等同于七门独立教材的完整训练强度。

## 先修正四个会影响结论的条件

1. 微积分25：上确界的逼近表述同时要求候选值已经是上界；有限集合反例说明只从下方逼近并不足够
2. 机器学习36：研究目标为新试件时，训练、验证和测试按试件隔离，同一试件的全部实验与派生样本属于同一集合；原练习和自测条件同步
3. 机器学习47：数据残差先乘初温差与参考温差的比例，再平方平均；等价MSE权重为比例平方，矩阵与右端同缩放；原正确程序和结果表保留
4. 流体39/55：常比热本身不足以忽略焓的压力依赖。保留一般焓差能量账，再声明理想气体或压力项可忽略等简化条件；原空气5 K算例保留

同时澄清：相律的组分/物种/反应计数、正值自然对流关联式的热膨胀系数前提、表压有效载荷与实际湿壁牵引、转子控制体的其他轴矩、壁面相对切向速度、浮点可表示范围，以及正交性之外借用的完备性和收敛结论。

## 起步与续学

- 起步入口由26节增至30节：极限、复合求导、子空间、基与维数增加“具体例子→可操作步骤→独立自检→原文回读”
- 极限入口用同一函数的孔洞和另指定点值作图；四节原有完整正文仍保留
- Python02/05/08/11轻量补最低就绪与后读提示；热学、量纲分析、实验不确定度等在实际使用工具处精确链接先修
- 六组“本科核心续学”列出能独立完成的动作，覆盖全部七科过滤入口，再连接研究和仿真专项；没有固定天数或阅读即掌握的保证
- 跨章代码题区分现在可做的手算判断与学会后续工具后可选运行的部分

## 用完整问题练基本能力

- 数学：渐近线与函数图、由平面/抛物面构造积分区域、部分分式与换元、级数端点、未见矩阵的特征值及非轴对齐SVD；计算后作代回或第二方法核验
- 热学：注明来源和单位的水/制冷剂物性记录、判相与插值、状态图与循环账；增加管束从几何到热负荷、三表面辐射网络、未知壁温迭代；往复式压气机明确为能源动力专业续学
- 流体：移动控制体动量、不等并联支路、浮体初稳性、加速容器静水压力四道独立题，要求画对象、列条件并复核质量/能量或几何
- 统计与分类：从原始样本计算标准误、预设检验、尾概率和区间；由小分数表逐阈值算混淆矩阵、ROC/PR与AP，再在独立测试集上评价冻结的选择
- Python：修改一项项目规格，先写测试，再用边界变异解释失败；原分析器和研究项目程序保留

新增正文编号练习31道：数学14、热学8、流体4、计算5。它们与原78道三档练习分开统计；后者仍集中在原26节。本轮另增加8张原创教学图，修正1张弯管图的力对象说明。未把例题、断言数或代码运行数混算成题量。

## 保留哪些兼容性

- 253个课号、自测答案索引、学习记录/笔记/收藏与备份格式不变
- ML36仅为保持新试件目标一致而修正正确风险选项和解释，其余选项与题干保持，唯一答案仍为原索引
- 原78题仅平均值题prompt补浮点输入范围与返回近似值说明，答案及其他题不变
- 旧正文/原题基线文件不被整批刷新。`report-revision-preservation.json` 只记录精确审阅过的前后哈希；无关改动仍使保留测试失败
- 数值模型函数未因图注文案调整而改变。新增图、公式和代码随网站构建同步打入离线包

## 可复跑检查与发布边界

常规校验见 README。新增回归入口：

```sh
python tools/verify_report_revision.py
python tools/revision/verify_math.py
python tools/revision/verify_fluid.py
python tools/revision/verify_computing.py
python tools/verify_thermal_cases.py
```

数学和计算回归使用 `tools/qa/requirements.txt` 的固定开发依赖；热学常规复算只用标准库。需要重新生成状态模型数据/图时，另用官方 CoolProp 7.2.0，并运行 `tools/reproduce_thermal_properties.py` 和 `tools/render_thermal_case_figures.py`。模型输出与打印物性表、实验数据是不同来源，正文分别标明，不能混称为实测值。

发布检查覆盖源文件哈希、原文/题库保留、全部公式与DOM、六种浏览器宽度、真实双向滚轮、图放大、旧记录保留，以及Android离线包与真实触摸。修订内容的代表性页面另有截图，代码和物理条件有独立回读/复算。检查结果必须对应具体提交的 [Actions记录](https://github.com/patatohek-boop/zhixu-cloud-textbook/actions)，不能用旧版本通过代替新版本验收。

网页部署、Android未签名构建和正式签名APK是不同状态。Android源码目标为1.5.0 / versionCode 8；正式安装包是否可用以 [Releases](https://github.com/patatohek-boop/zhixu-cloud-textbook/releases) 为准。未取得原签名密钥时，不能以新密钥或debug包冒充可覆盖更新的正式版。

上述检查不能证明所有定理和任意输入下的全正确性，也不代替外部专业教师审校、真实学习者试学或每一种手机的实测。一般测度论、完整泛函分析、工业湍流实现和大型生成模型仍不是本轮统一扩写门槛。

## 主要公开依据

- [NIST 水与蒸汽物性表](https://www.nist.gov/publications/thermodynamic-properties-water-tabulation-iapws-formulation-1995-thermodynamic)及正文标明的具体表页
- [MIT 热方程讲义](https://ocw.mit.edu/courses/18-303-linear-partial-differential-equations-fall-2006/d11b374a85c3fde55ec971fe587f8a50_heateqni.pdf)：展开定理和初始/正时间边界
- [IUPAC 相律](https://goldbook.iupac.org/terms/view/P04533)：独立组分与相数
- [MIT 焓的全微分](https://ocw.mit.edu/courses/3-020-thermodynamics-of-materials-spring-2021/mit3_020s21_l11.pdf)：一般焓压力项
- [SciPy 单样本t检验](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_1samp.html)、[scikit-learn分类评价](https://scikit-learn.org/stable/modules/model_evaluation.html#classification-metrics)、[分组交叉验证](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data)

来源支持原理、物性或工具约定；新数据情景、教学组织、独立变式和原创图不冒充上述机构的官方教材。
