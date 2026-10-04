# 发布前数学逐节教学复核 · 2026-10-04

复核对象：1.6.0 待发布源码 `content/calculus` 31 节、`content/linear-algebra` 24 节，共 55 节。复核者为独立于上一轮数学编辑者的任务代理。本轮按 `course.json` 顺序读取每节完整文本，包含 JSON 中的测验、每个证明、例题与答案折叠内容；没有用标题搜索或摘要替代全文审读。

先读了 [上一轮逐课记录](buaa-math-2026-10-04.md) 和 [内容保全方法](reader-revision-method-2026-10-04.md)，但下列结论来自重新阅读与推演。知识清单/哈希只用于确定审查对象，不能证明数学正确。

## 结论与修复范围

现有 55 道课尾选择题未发现错误答案，未修改任何 quiz、课程顺序、课号或其他 front matter。未发现需要更改原例题数值答案的错误。发现的是定义条件、证明衔接及主干知识覆盖的具体缺口，已修复以下 7 节；其余 48 节原文未动。

| 课号 | 发现的具体缺口 | 本轮处理与核对依据 |
| --- | --- | --- |
| calculus-07 | 基本定理处理负 h 时已使用反向积分，但先前没有正式给出方向约定 | 在原函数定义后给出反向积分与同端点积分；不更改原黎曼定义或FTC证明 |
| calculus-10 | 反常积分没有区分绝对收敛与条件收敛；级数中的定义不能自动代替积分定义 | 补定义、绝对值可积依据、正负部分证明；sin(x)/x 分部积分证明收敛，互不相交区间加分组下界证明绝对值积分发散 |
| calculus-14 | 第25课承诺此处有欧氏三角不等式代数证明，实际止于柯西不等式；空间直线及常见二次曲面多停留于外链 | 补平方展开与反三角不等式；明示非零法向；补直线/平面交点三种情况、点线距离、六类曲面截痕和柱面；数值交点独立回代 |
| calculus-16 | 已证明梯度垂直等值集，但没有把结论明确写成初学者可计算的切平面方程 | 补非零梯度和隐函数前提、图形切平面及精确二次余项例；零梯度孤立点反例说明边界 |
| calculus-22 | 单次覆盖条件后文才出现，最初的正则面片定义仅有叉积非零 | 前置内部单射及零面积接缝约定，明确局部正则不排除重复覆盖 |
| linear-algebra-20 | 上一章已进入复数，Frobenius 定义却直接平方且未写实数范围 | 保留原实公式，补复数模平方与一阶矩阵 (i) 的范数反例，避免得到虚“长度” |
| linear-algebra-24 | 明确定义了普通稳定，后文仅完整陈述渐近稳定谱判据 | 补普通稳定的连续/离散 Jordan 边界充要条件，先证稳定等价于演化矩阵一致有界；同一幂零矩阵给连续与离散对照 |

## 逐课记录

“未发现需修改项”表示本次审读未发现实质问题，不是形式化验证承诺。每行的检查均包括先定义后使用的衔接、定理假设和证明、例题与所有答案、课尾 quiz；下列说明列出便于独立核对的具体对象。行号对应本轮修复后的源码。

| 课号 | 实际读取范围 | 数学与教学核对记录 | 处理 |
| --- | --- | --- | --- |
| [calculus-01](../content/calculus/calculus-01.md#L37) | 全文1—130行，含JSON quiz与全部答案折叠 | 核对集合/量词、定义域与陪域、双射逆的双向证明；温度模型的输入单位和合法时段；定义域 (1,2)、反函数与倒数的练习。未发现实质错误。 | 未发现需修改项 |
| [calculus-25](../content/calculus/calculus-25.md#L36) | 全文1—117行，含JSON quiz与全部答案折叠 | 核对上确界的两个条件、完备性作为公理、单调收敛/嵌套区间/BW/柯西准则和有限维紧致；极值及一致连续证明的子列选择合法。发现所指向第14课的三角不等式证明缺口，已在14补齐。 | 交叉引用缺口已在14修复 |
| [calculus-02](../content/calculus/calculus-02.md#L37) | 全文1—130行，含JSON quiz与全部答案折叠 | 核对聚点、去心极限、连续与单侧端点；逐项检查和积商的局部界、夹逼、上确界介值证明；M01 的分母下界和 δ=min(1,2ε) 正确，quiz 正确。 | 未发现需修改项 |
| [calculus-03](../content/calculus/calculus-03.md#L37) | 全文1—126行，含JSON quiz与全部答案折叠 | 核对有限双侧导数与 o(h)、唯一线性化和可导蕴含连续证明；位移0.41与差商4.1区分正确；核算 s(2.05) 和 3.02² 的余项及单位。 | 未发现需修改项 |
| [calculus-04](../content/calculus/calculus-04.md#L37) | 全文1—125行，含JSON quiz与全部答案折叠 | 核对乘积、商、链式及逆函数条件；链式证明包含内层增量为零的情况；复算54、0.4π、M02的12 V/s、球体1.6π及圆切线 -3/4。 | 未发现需修改项 |
| [calculus-05](../content/calculus/calculus-05.md#L37) | 全文1—127行，含JSON quiz与全部答案折叠 | 核对费马/罗尔/中值定理的内点与端点条件、凸性证明；三次曲线极值和拐点、x²/(x−1) 两支与渐近线、M05 孔洞/渐近线区分正确。 | 未发现需修改项 |
| [calculus-28](../content/calculus/calculus-28.md#L36) | 全文1—87行，含JSON quiz与全部答案折叠 | 核对柯西中值定理交叉相乘形式、g′非零后可除；零比零端点补值、无穷分母版有限及无限极限证明；导数比无极限的反例不能误作逆判据。 | 未发现需修改项 |
| [calculus-06](../content/calculus/calculus-06.md#L37) | 全文1—111行，含JSON quiz与全部答案折叠 | 核对全局最优定义、闭区间候选穷尽、二阶充分条件；围栏25、牛顿前两步、二次误差界和局部不离域证明；前引积分/泰勒均有明确先修链接。 | 未发现需修改项 |
| [calculus-07](../content/calculus/calculus-07.md#L37) | 全文1—154行，含JSON quiz与全部答案折叠 | 核对任意取点黎曼和、达布等价和连续可积、FTC两部分；750 J、510 J、位移3/路程5及变量上下限求导正确。修复：补上反向与同端点积分的定义，支撑证明中 h<0 的处理。 | 已补齐，原答案不变 |
| [calculus-29](../content/calculus/calculus-29.md#L36) | 全文1—95行，含JSON quiz与全部答案折叠 | 核对对数积分构造→指数逆的非循环关系、幂函数正输入、三角几何极限和反三角分支；指数压过固定幂的归纳成立。阶乘符号为初等代数记号，正式定义见12。 | 未发现需修改项 |
| [calculus-08](../content/calculus/calculus-08.md#L37) | 全文1—190行，含JSON quiz与全部答案折叠 | 核对正向换元无需单调与反向参数化的覆盖条件；分部、重复因子分式、三角幂/根式分支/二次式递推；M06通分与M07原函数求导和 π/3+√3/2 全部一致。 | 未发现需修改项 |
| [calculus-09](../content/calculus/calculus-09.md#L37) | 全文1—97行，含JSON quiz与全部答案折叠 | 核对非负密度、正质量、期望绝对可积条件；弧长上确界双向估计；圆盘/壳法均8π/3，面积1/6及均匀概率1/4正确。曲面面积严格依据另链31。 | 未发现需修改项 |
| [calculus-10](../content/calculus/calculus-10.md#L37) | 全文1—108行，含JSON quiz与全部答案折叠 | 核对反常截断、奇点两侧分别收敛、主值不同、p积分及梯形误差1/12推导；原练习正确。补齐绝对/条件收敛定义、正负部分证明和 sin(x)/x 的条件收敛完整例证。 | 已补齐，原答案不变 |
| [calculus-11](../content/calculus/calculus-11.md#L37) | 全文1—95行，含JSON quiz与全部答案折叠 | 核对级数以部分和定义、项趋零仅必要、比较与绝对收敛、重排尾部界、交错上下部分和和误差；望远镜和1、等比和3/2及比值为1无结论正确。 | 未发现需修改项 |
| [calculus-26](../content/calculus/calculus-26.md#L36) | 全文1—101行，含JSON quiz与全部答案折叠 | 核对点态/一致定义量词、比值/上极限根值/积分判别和尾界；M判别、连续极限、逐项积分/求导附加条件；x^n、sin(nx)/n反例成立。 | 未发现需修改项 |
| [calculus-12](../content/calculus/calculus-12.md#L39) | 全文1—168行，含JSON quiz与全部答案折叠 | 核对反复罗尔导出Lagrange余项、小闭区间一致收敛与幂级数求导；平坦函数各阶零点差商非循环；端点有限余项、二项式系数递推、M08区间[-1,5)、M09偏小及1/110592界正确。 | 未发现需修改项 |
| [calculus-30](../content/calculus/calculus-30.md#L37) | 全文1—99行，含JSON quiz与全部答案折叠 | 逐项复核辛普森误差核 K、偶对称和非正性、核绝对积分1/90、复合缩放1/180；x³精确、x⁴误差1/120；跨|x|尖点的条件拒绝正确。 | 未发现需修改项 |
| [calculus-13](../content/calculus/calculus-13.md#L37) | 全文1—119行，含JSON quiz与全部答案折叠 | 核对正则、单次重参数化、二阶参数求导、极坐标面积覆盖次数；圆锥曲线焦点准线分支条件、圆弧长π、r=2cosθ面积π及练习斜率3/2正确。 | 未发现需修改项 |
| [calculus-14](../content/calculus/calculus-14.md#L37) | 全文1—147行，含JSON quiz与全部答案折叠 | 核对点积/叉积、柯西、曲率和切法加速度、距离2/3与抛物面投影。补齐三角/反三角不等式证明、非零法向、空间直线/交点/点线距离、六类二次曲面及柱面截痕；新交点(5/2,3,−1/2)复算。 | 已补齐，原答案不变 |
| [calculus-15](../content/calculus/calculus-15.md#L37) | 全文1—161行，含JSON quiz与全部答案折叠 | 核对偏导与统一全可微区别、逐坐标中值定理、链式的余项控制、连续混合偏导交换；移动探头5 K/s、温差−0.0793与反例路径1/2正确。 | 未发现需修改项 |
| [calculus-27](../content/calculus/calculus-27.md#L36) | 全文1—122行，含JSON quiz与全部答案折叠 | 核对标量隐函数的介值/唯一/连续/可微四步、向量收缩自映闭球与Lipschitz控制；逆导数在原像处求矩阵逆，局部条件不推出全局；两个退化反例及答案正确。 | 未发现需修改项 |
| [calculus-16](../content/calculus/calculus-16.md#L37) | 全文1—115行，含JSON quiz与全部答案折叠 | 核对单位方向导数、梯度最大性和等值面正交；多元Taylor、正定最小球面界与二维判别，22/5、全局最小−4正确。补齐等值面/图形切平面的准确方程、梯度非零条件及二次余项例。 | 已补齐，原答案不变 |
| [calculus-17](../content/calculus/calculus-17.md#L37) | 全文1—123行，含JSON quiz与全部答案折叠 | 核对单/多等式约束满秩、隐函数证明、乘子唯一、切空间上Lagrange Hessian与必要/充分区分；圆上极值、灵敏度分支条件、直线距离最小18及四驻点答案正确。 | 未发现需修改项 |
| [calculus-18](../content/calculus/calculus-18.md#L37) | 全文1—144行，含JSON quiz与全部答案折叠 | 核对Jordan边界条件、矩形Fubini统一误差、简单域换序；奇异换序 ±π/4 反例；质量4、质心(7/6,1/2)、惯量8与14/9及三角积分1/3正确。 | 未发现需修改项 |
| [calculus-19](../content/calculus/calculus-19.md#L37) | 全文1—134行，含JSON quiz与全部答案折叠 | 核对三维积分和单次微分同胚、行列式绝对值；极/柱/球微元及轴线截除；球32π/3、抛物体8π、M10体积9π/2与质量9π两种切片一致。 | 未发现需修改项 |
| [calculus-31](../content/calculus/calculus-31.md#L38) | 全文1—171行，含JSON quiz与全部答案折叠 | 逐步核对非凸紧邻域只在小凸盒积分、DS近恒等的内外盒收缩夹逼、Jordan边界像零测、黎曼和误差；规则形状三角片而非任意瘦网格；换参绝对值/方向及例7/6、√6正确。 | 未发现需修改项 |
| [calculus-20](../content/calculus/calculus-20.md#L37) | 全文1—105行，含JSON quiz与全部答案折叠 | 核对开且路径连通、两种线积分、势/路径无关/闭路零的双向证明；星形无旋势构造注明范围，孔洞2π反例有效；端点差3、常力6及长度答案正确。 | 未发现需修改项 |
| [calculus-21](../content/calculus/calculus-21.md#L37) | 全文1—109行，含JSON quiz与全部答案折叠 | 核对有限简单域分割范围、Pdx/Qdy分量推导、内边界顺时针；外法向通量符号和面积场；圆环量2π、半径2外通量8π正确。 | 未发现需修改项 |
| [calculus-22](../content/calculus/calculus-22.md#L37) | 全文1—137行，含JSON quiz与全部答案折叠 | 核对标量面元与有向通量不重复乘面积、散度定理有限分割条件和奇点；球通量32π、抛物面−π/2、M11 5π/2、面积π(5√5−1)/6正确。修复：把单面片的单次覆盖条件前置到正式定义。 | 已补齐，原答案不变 |
| [calculus-23](../content/calculus/calculus-23.md#L37) | 全文1—115行，含JSON quiz与全部答案折叠 | 核对可定向有限C²面片、参数拉回Green、B_u−A_v展开、共享边相消；旋度梯度/散度旋度的混合导数条件；单位圆π、反向边界和Möbius边界说明正确。 | 未发现需修改项 |
| [calculus-24](../content/calculus/calculus-24.md#L37) | 全文1—140行，含JSON quiz与全部答案折叠 | 核对Picard短区间自映、收缩/一致极限/唯一性；积分因子、分离时常值解、连续非唯一与有限时爆破；二阶根型及初值完备；Logistic分支、最大区间(−ln2,∞)和Euler1.8均正确。 | 未发现需修改项 |
| [linear-algebra-01](../content/linear-algebra/linear-algebra-01.md#L37) | 全文1—150行，含JSON quiz与全部答案折叠 | 核对实数向量/矩阵尺寸、三种解数证明与非负/整数附加约束；两组线性组合及quiz零解正确。 | 未发现需修改项 |
| [linear-algebra-02](../content/linear-algebra/linear-algebra-02.md#L37) | 全文1—156行，含JSON quiz与全部答案折叠 | 核对全部行操作含右端及可逆、阶梯主元/自由变量、矛盾行先判、参数基和RREF唯一证明；二维消元(2,3)与三元解(2−t,t,1)正确。 | 未发现需修改项 |
| [linear-algebra-03](../content/linear-algebra/linear-algebra-03.md#L37) | 全文1—159行，含JSON quiz与全部答案折叠 | 核对相乘尺寸、左右逆、结合/转置/乘积逆证明、从唯一可解构造双侧逆；AB及(12,5,2)、Schur补顺序、非零零乘积反例正确。 | 未发现需修改项 |
| [linear-algebra-04](../content/linear-algebra/linear-algebra-04.md#L37) | 全文1—103行，含JSON quiz与全部答案折叠 | 核对非零主元的LU存在、可逆前提下单位对角唯一性、置换同步调整倍数、前后代；A=LU与解(2,1)、n²/n³阶估计正确。 | 未发现需修改项 |
| [linear-algebra-05](../content/linear-algebra/linear-algebra-05.md#L37) | 全文1—137行，含JSON quiz与全部答案折叠 | 核对实向量空间公理与0数乘、非空子空间判据、张成最小性、交和并区别、直和唯一分解；M03可达/非负权重反例及多项式次数条件正确。 | 未发现需修改项 |
| [linear-algebra-06](../content/linear-algebra/linear-algebra-06.md#L37) | 全文1—139行，含JSON quiz与全部答案折叠 | 核对交换引理的可替换系数、维数良定义、基扩缩/坐标唯一、和交维数证明；M04所有系数(3−t,2−t,t)及新多项式基(0,4,−1)正确。 | 未发现需修改项 |
| [linear-algebra-07](../content/linear-algebra/linear-algebra-07.md#L37) | 全文1—111行，含JSON quiz与全部答案折叠 | 核对四空间所在维数、核基扩充秩零度、行列秩与原主元列、正交补依赖10；例的四组基、满行/列区别和输出(2,5)不可达正确。 | 未发现需修改项 |
| [linear-algebra-08](../content/linear-algebra/linear-algebra-08.md#L37) | 全文1—106行，含JSON quiz与全部答案折叠 | 核对映射核像、矩阵列按基的像定义、输入输出分别换基R⁻¹AS与相似S⁻¹AS；基长度的Gram权重；多项式求导矩阵正确。 | 未发现需修改项 |
| [linear-algebra-09](../content/linear-algebra/linear-algebra-09.md#L37) | 全文1—113行，含JSON quiz与全部答案折叠 | 核对排列符号/余子式、交错多线性唯一性、乘法/转置/伴随/Cramer；体积论证只依赖切片不循环援引非线性换元；例行列式5、−24、9正确。 | 未发现需修改项 |
| [linear-algebra-10](../content/linear-algebra/linear-algebra-10.md#L37) | 全文1—162行，含JSON quiz与全部答案折叠 | 核对有限维投影存在的正定Gram系统、唯一分解、最优性、对称幂等充要条件；三读数均值4与误差8、斜投影反例、直线投影(2,2)正确。 | 未发现需修改项 |
| [linear-algebra-11](../content/linear-algebra/linear-algebra-11.md#L37) | 全文1—135行，含JSON quiz与全部答案折叠 | 核对正规方程必要充分的下降方向、预测总唯一与参数满列秩唯一、加权W正定；常数误差14、直线参数(7/6,1/2)与误差1/6、变式(1,1)正确。 | 未发现需修改项 |
| [linear-algebra-12](../content/linear-algebra/linear-algebra-12.md#L37) | 全文1—120行，含JSON quiz与全部答案折叠 | 核对薄/完整QR尺寸、GS无零分母与张成保持、QR最小二乘；Householder sign(0)=1、正对角D补正；手算 q2=(1,−1,2)/√6 和矩形投影区别正确。 | 未发现需修改项 |
| [linear-algebra-13](../content/linear-algebra/linear-algebra-13.md#L37) | 全文1—129行，含JSON quiz与全部答案折叠 | 核对非零特征向量与含零特征空间、数域、不同根无关、几何≤代数重数、分裂后和积及相似不变；M12根5/2与缺陷重根2复算正确。 | 未发现需修改项 |
| [linear-algebra-14](../content/linear-algebra/linear-algebra-14.md#L37) | 全文1—92行，含JSON quiz与全部答案折叠 | 核对基条件/重数判据需完全分裂、Jordan幂截断范围、临界块增长与初值系数；重复根非必要/缺陷反例正确，长期主导不忽略零系数。 | 未发现需修改项 |
| [linear-algebra-15](../content/linear-algebra/linear-algebra-15.md#L37) | 全文1—117行，含JSON quiz与全部答案折叠 | 核对方阵正交定义、谱定理紧致极大→正交补不变→限制对称→归纳完整性；Rayleigh权重和、非对称反例、二次型交叉系数和椭圆方向正确。 | 未发现需修改项 |
| [linear-algebra-16](../content/linear-algebra/linear-algebra-16.md#L37) | 全文1—147行，含JSON quiz与全部答案折叠 | 核对Cholesky Schur补正定/唯一、Sylvester充分必要、PSD必须全部主子式、ε扰动证明；合同惯性维数论证、二次目标全局性和Hessian处处条件；例与练习正确。 | 未发现需修改项 |
| [linear-algebra-17](../content/linear-algebra/linear-algebra-17.md#L37) | 全文1—157行，含JSON quiz与全部答案折叠 | 核对共轭在线性变量的约定、Hermitian极值归纳、正规分解B+iC及交换性、DFT有限几何和/Parseval/FFT蝶形；Fourier只证明有限投影，未冒称完整无穷维收敛；复例均正确。 | 未发现需修改项 |
| [linear-algebra-18](../content/linear-algebra/linear-algebra-18.md#L37) | 全文1—147行，含JSON quiz与全部答案折叠 | 核对任意矩形SVD构造、零奇异值不可相除、完整/薄/紧致/截断尺寸；四空间与零矩阵边界；M13两个3×2矩阵的UΣVᵀ、秩1核与左核均正确。 | 未发现需修改项 |
| [linear-algebra-19](../content/linear-algebra/linear-algebra-19.md#L37) | 全文1—131行，含JSON quiz与全部答案折叠 | 核对四条件伪逆存在唯一及最短最小二乘、满行/列单侧逆的全族、岭与伪逆不同目标及λ→0；欠定最短(1,1)、列(1,2)全部左逆和无右逆正确。 | 未发现需修改项 |
| [linear-algebra-20](../content/linear-algebra/linear-algebra-20.md#L37) | 全文1—117行，含JSON quiz与全部答案折叠 | 核对诱导范数、相容性、残差相对界需b≠0、Neumann扰动分母、正规方程条件数平方；例百万放大正确。修复：明确实Frobenius平方与复Frobenius模平方，新增(i)范数1反例。 | 已补齐，原答案不变 |
| [linear-algebra-21](../content/linear-algebra/linear-algebra-21.md#L37) | 全文1—144行，含JSON quiz与全部答案折叠 | 核对无自环有限图的B符号、L核连通分量、生成森林与环流m−n+c、正权和逐分量相容性；Cesàro存在与正幂收缩唯一收敛；网络(1/3,−1/3,0)和π=(2/3,1/3)正确。 | 未发现需修改项 |
| [linear-algebra-23](../content/linear-algebra/linear-algebra-23.md#L36) | 全文1—185行，含JSON quiz与全部答案折叠 | 核对Cayley–Hamilton逐系数、最小多项式整除、Bezout直和、幂零像空间归纳提升链基、核维数差与块唯一；六维3/2/1块及三阶显式链S正确。 | 未发现需修改项 |
| [linear-algebra-24](../content/linear-algebra/linear-algebra-24.md#L38) | 全文1—118行，含JSON quiz与全部答案折叠 | 核对矩阵指数局部一致收敛、微分/逆/ODE唯一、连续实部与离散模的渐近判据、零幂约定、非周期回路整数拼接。补齐普通稳定的边界块充要条件和有界演化证明；连续幂零不稳定/离散两步归零反例正确。 | 已补齐，原答案不变 |
| [linear-algebra-22](../content/linear-algebra/linear-algebra-22.md#L37) | 全文1—127行，含JSON quiz与全部答案折叠 | 核对样本m>1、中心化方差、多个正交方向权重界；谱范数核向量下界及Frobenius完整n向量补零证明；PCA协方差10/3、主值20/3和训练数据隔离正确。 | 未发现需修改项 |

## 与官方课程的覆盖对照

本轮实际打开并核对下列官方页面。使用它们界定主干范围和核对知识点，不直接复制教材段落。

- [MIT 18.01SC 大纲](https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/pages/syllabus/)：函数极限、微分、图像与优化、相关变化率、定积分及几何/功/概率、积分方法、反常和数值积分、泰勒级数，分别落实在 01—13 与 25、26、28—30。二阶方程入门和严格存在性证明是额外内容，并不等于完整微分方程课。
- [MIT 18.02SC 大纲](https://ocw.mit.edu/courses/18-02sc-multivariable-calculus-fall-2010/pages/syllabus/)及[向量与矩阵单元](https://ocw.mit.edu/courses/18-02sc-multivariable-calculus-fall-2010/pages/1.-vectors-and-matrices/)：空间几何、参数曲线、多元导数、优化、多重积分和 Green/Gauss/Stokes 已在 13—23、27、31 中展开；矩阵方程基础由线代 01—09 承接。此次把空间直线、切平面补为实际正文，不把一条外链视为已经讲授。
- [OpenStax 官方《Calculus Volume 3》§2.6](https://openstax.org/books/calculus-volume-3/pages/2-6-quadric-surfaces)：作为空间几何覆盖交叉检查，补齐椭球、单双叶双曲面、椭圆锥面、椭圆/双曲抛物面以及非圆柱面的截痕。表内判断由固定坐标后的非负平方式重新推导。
- [MIT 18.06SC 大纲](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/pages/syllabus/)：线性方程/四空间/矩阵分块、正交/最小二乘、行列式、特征结构、正定、SVD、换基和伪逆均有正文定义、证明与例题；网络、复数/FFT、Jordan、矩阵指数均已展开。对照并未发现仍只能依赖标题或外链的这些课程主干。
- [MIT 6.241J 官方讲义第13章](https://ocw.mit.edu/courses/6-241j-dynamic-systems-and-control-spring-2011/996025f6db0d90b00f11c44fc49b85f9_MIT6_241JS11_textbook.pdf)（PDF第122—124页）：核对普通稳定的边界 Jordan 块条件。新文字先从本课已定义的稳定量词证明一致有界，再用已证明的块公式推导，未把一般非线性系统稳定判据混入。

## 验证结果和仍需完成的验收

1. `python -X utf8 tools/verify_math.py`：55节，488项通过，其中413项元数据/结构/引用检查、75项独立符号或算例检查；直接从编辑源码渲染4834个公式全部通过。该脚本没有把旧模板标题作为数学条件，也不需要弱化或迁移检测。
2. `python -X utf8 tools/mastery/verify_math.py`：既有24道分级训练的独立精确算术/符号检查全部通过。这是测试回归覆盖；本轮逐字人工审查的对象是55节内的练习和quiz，未重新逐字审阅独立JSON练习库的全部教学叙述。
3. 新增补齐内容另做22项独立算式/反例检查：积分方向、sin(x)/x分部恒等式及两层下界、线面交点、点线距离恒等式、切平面余项、曲面截痕、复范数、连续/离散幂零及纯旋转。全部通过；本地可复跑 `python -X utf8 work/prepublication_math_cases.py`，结果在 `work/prepublication-math-cases.json`。这些本地验证文件不属于待公开教材包。
4. `python -X utf8 tools/revision/verify_math.py --output work/prepublication-math-revision.json`：在旧审校快照的 `reviewed source unchanged calculus-14` 断言处停止。此前符号计算执行未报错，但不能据此声称整套2336项已通过；源文变动本来就应触发这个保护。未修改、跳过该断言，也未更新总保全清单。需主代理审阅本轮7节差异后统一重新冻结，再跑完整保全和此脚本。
5. 对全部55节重新计算规范化元数据摘要，与修复前已审快照逐项一致。这里的哈希只核对元数据与quiz没有漂移，不承担数学正确性结论。

## 覆盖边界

本轮审查达到“逐节全文复核、主干对照、关键算例独立复算”，没有宣称绝对无错或覆盖所有大学数学。无穷维泛函分析、Lebesgue积分、完整Fourier收敛/采样理论、全套常微分方程及PDE、商空间/对偶/张量的系统课程、Krylov/稀疏/随机化数值线代仍属于明确后续专题。当前课程可作为本科微积分和工程线性代数主干，但各章练习量明显少于MIT整套作业和考试，不能把知识点出现等同于学生已经熟练掌握。

本轮阅读了所有图注与数学描述。`tools/revision/verify_math.py` 的3张SVG坐标检查位于源快照检查之后，本轮在源快照处停止，因此不能把这些SVG检查报为新通过。没有逐张重新渲染所有数学插图或操作全部交互实验；视觉/交互验收由发布主任务单独进行。未改生成的 `data.js`、站点构建文件、APP资源、远程仓库或总审校清单。

## 本轮修改文件的审校摘要

下列修复前摘要来自上一轮已审快照，修复后摘要对应本报告源码；可供主代理再次逐文件比对。摘要识别文件，不能替代上述证明审查。

```json
[
  {
    "id": "calculus-07",
    "path": "content/calculus/calculus-07.md",
    "before_reviewed_sha256": "99adae75014a022a69ee2b80e870461ddd25144432fb9ebc972b9b7ab362a0bd",
    "after_sha256": "4ff5df96b5dccc411e8574487f86521c9e96dfb97de304a839bab071150dcd81",
    "metadata_sha256_unchanged": true,
    "quiz_changed": false
  },
  {
    "id": "calculus-10",
    "path": "content/calculus/calculus-10.md",
    "before_reviewed_sha256": "b3d0bdf9a32ef747fbddaccac41d39279eb54611494eed9b157a60aceb14d716",
    "after_sha256": "5a8559a847092fe5aa8255efe2da4e53604187eca5c3fe1516fef45a0ba522d7",
    "metadata_sha256_unchanged": true,
    "quiz_changed": false
  },
  {
    "id": "calculus-14",
    "path": "content/calculus/calculus-14.md",
    "before_reviewed_sha256": "5529cec5e8cdf9cf2e10ee2f0bb39bd6ae73f1c698992ca46550ba27b896866b",
    "after_sha256": "4e731e2ca5ae2bffb8dab331e03a13c5ca1a58206ad47031d0ad773bc5a189eb",
    "metadata_sha256_unchanged": true,
    "quiz_changed": false
  },
  {
    "id": "calculus-16",
    "path": "content/calculus/calculus-16.md",
    "before_reviewed_sha256": "f4ae86663901d791f1144bb945d76057a78c4e410b9cb555465d008661143563",
    "after_sha256": "13dae6f9d8e868ad3fc032e03635c1869eb65dc034650910b98173e7ff1809db",
    "metadata_sha256_unchanged": true,
    "quiz_changed": false
  },
  {
    "id": "calculus-22",
    "path": "content/calculus/calculus-22.md",
    "before_reviewed_sha256": "12b67e42817b993c404744918c683c8600ec2d22d44e940b59b11a1423bd0b87",
    "after_sha256": "b0d9901c8e65945c2480eaf4907cdda5922e0cba80171ef17c3951ffa4049d95",
    "metadata_sha256_unchanged": true,
    "quiz_changed": false
  },
  {
    "id": "linear-algebra-20",
    "path": "content/linear-algebra/linear-algebra-20.md",
    "before_reviewed_sha256": "ee85266dbe816fa16b19ff08a34f91094d894fba14f0c9987afbb213488c8ab7",
    "after_sha256": "476f9088ea7898a95c1ae8e9d0413146f43a8cdee8ab458673757f312f0c42bc",
    "metadata_sha256_unchanged": true,
    "quiz_changed": false
  },
  {
    "id": "linear-algebra-24",
    "path": "content/linear-algebra/linear-algebra-24.md",
    "before_reviewed_sha256": "c8b8915c51229c3700f30db52328d7835fde398a1c952a18276312a8cea72b58",
    "after_sha256": "ae217b2cdbfb9cf5d327c2f6102ba3a9fa1fa99b9b3daca6e826c2042d20dd5c",
    "metadata_sha256_unchanged": true,
    "quiz_changed": false
  }
]
```

## 交叉复核补记

另一名审阅者重新核对上述7节新增部分及22项算式，发现两处小缺口，主代理已修复：calculus-14将含锥面的表改称“常见标准类型”，不再笼统称非退化；linear-algebra-24的稳定性必要性直接对任意单位向量取初值δu/2并取算子上确界，不再暗用未声明的欧氏坐标界。以下历史修改摘要是交叉复核之前的记录；最终哈希以中央reader-revision-1.6.0.json为准。
