# 数学两科独立教学审读与修订记录

审读日期：2026-09-28。定位均指本轮修改前的正文行号，路径均相对于项目根目录。这是一轮教材教学质量审读，不表示外部教师认证。先保存基线，再实施用户要求的概念分段与有把握的修正。

## 已记录的基线问题

1. **P1，先修顺序／教学设计**。[content/calculus/calculus-25.md:46-61](https://github.com/patatohek-boop/zhixu-cloud-textbook/blob/a1847cd253133caeee745411f6e86444395fac6a/content/calculus/calculus-25.md#L46)，本课在目录中排第二，原文已使用“数列 $a_n$”“柯西条件”“$K\subseteq\mathbb R^n$”“连续函数”等概念，但数列收敛正式定义到第11课、连续定义到第02课。初学者必须同时消化未定义对象与证明。修订方向：在本课明确补充数列、子列、柯西条件和欧氏空间的定义，连续性相关证明安排在读过第02课后回读，给出具体阅读路径。
2. **P2，数学／物理概念错误**。[content/calculus/calculus-03.md:43](https://github.com/patatohek-boop/zhixu-cloud-textbook/blob/a1847cd253133caeee745411f6e86444395fac6a/content/calculus/calculus-03.md#L43)：“平均速度是‘这段路程除以这段时间’。”平均速度应为位移除以时间；路程除以时间为平均速率。修订方向：分别定义，给往返运动例子。
3. **P1，先修顺序／教学设计**。[content/calculus/calculus-06.md:49-58](https://github.com/patatohek-boop/zhixu-cloud-textbook/blob/a1847cd253133caeee745411f6e86444395fac6a/content/calculus/calculus-06.md#L49) 在积分和泰勒定理前给出积分余项及牛顿法误差证明；[content/calculus/calculus-30.md:48-50](https://github.com/patatohek-boop/zhixu-cloud-textbook/blob/a1847cd253133caeee745411f6e86444395fac6a/content/calculus/calculus-30.md#L48) 将“对基本定理连续积分四次并交换有限连续积分次序”写入“完整推导”，但泰勒和二重积分尚在后面。读者无法独立复现。修订方向：先讲可执行方法与算例，标明误差证明的先修条件，并调整第30课位置、改用分部积分证明积分余项。
4. **P2，证明缺口**。[content/calculus/calculus-12.md:59](https://github.com/patatohek-boop/zhixu-cloud-textbook/blob/a1847cd253133caeee745411f6e86444395fac6a/content/calculus/calculus-12.md#L59)：“反复求导得到‘1/x 的多项式乘…’；指数衰减快于任意幂，所以每阶导数在零都为零。”非零点的导数表达式及其极限不足以直接断言零点的高阶导数值；应以零点差商归纳补足。修订方向：写明归纳假设、差商和连续延拓三个环节。
5. **P2，概念分段／认知负担**。[content/calculus/calculus-16.md:38](https://github.com/patatohek-boop/zhixu-cloud-textbook/blob/a1847cd253133caeee745411f6e86444395fac6a/content/calculus/calculus-16.md#L38) 在一段引入单位方向、方向导数、梯度、Hessian及三种定性；[content/calculus/calculus-13.md:38](https://github.com/patatohek-boop/zhixu-cloud-textbook/blob/a1847cd253133caeee745411f6e86444395fac6a/content/calculus/calculus-13.md#L38) 在一段引入参数曲线、像集、正则性、重参数、定向和极坐标。初次阅读无法区分对象、条件、用途。修订方向：按概念依赖拆成有明确标题的段落，并将定义、几何解释与使用条件分开；同样逐篇检查两科。
6. **P2，例题／操作目标缺口**。[content/calculus/calculus-16.md:51](https://github.com/patatohek-boop/zhixu-cloud-textbook/blob/a1847cd253133caeee745411f6e86444395fac6a/content/calculus/calculus-16.md#L51)：“直接导出行列式判别”，没有列出二维二阶判别的各条件和不能判定的情形。知道矩阵定义不等于会判极值。修订方向：从配方明确推导 $D=AC-B^2$ 的分支规则，并给一个完整计算例子。

7. **P2，先修顺序／教学设计**。[content/linear-algebra/linear-algebra-08.md:51-54](https://github.com/patatohek-boop/zhixu-cloud-textbook/blob/a1847cd253133caeee745411f6e86444395fac6a/content/linear-algebra/linear-algebra-08.md#L51) 在特征值、特征空间、代数重数第13课才定义之前证明相似不变量；迹也直接使用而未先定义。修订方向：保留换基主线，将谱不变量的证明移到第13课已定义术语之后，第08课保留明确链接和秩不变的当前结论。
8. **P2，概念与证明过密／例题缺口**。[content/linear-algebra/linear-algebra-23.md:37](https://github.com/patatohek-boop/zhixu-cloud-textbook/blob/a1847cd253133caeee745411f6e86444395fac6a/content/linear-algebra/linear-algebra-23.md#L37) 一段同时给矩阵多项式、湮灭、最小多项式、广义空间、幂零、Jordan链及无关证明；`62-64` 把商空间解释、归纳、提升与补基挤在两段。已有算例只从核维数辨认块，未示范从普通坐标构造链基。修订方向：分清定义与证明，拆出归纳的四个任务，并新增非标准基下的三阶链构造和回乘核对。Jordan存在性论证本身经检查成立，不把行文压缩误报为定理错误。
9. **P2，例题与目标不匹配**。[content/linear-algebra/linear-algebra-11.md:61-67](https://github.com/patatohek-boop/zhixu-cloud-textbook/blob/a1847cd253133caeee745411f6e86444395fac6a/content/linear-algebra/linear-algebra-11.md#L61) 唯一完整算例是常数拟合；“拟合直线与设计矩阵”只描述如何排一与输入，没有实际列出矩阵、解两参数、核对残差。修订方向：补三点直线拟合的完整过程及变式练习，使一般正规方程有可复现任务。
10. **P2，定理范围／符号精度**。[content/linear-algebra/linear-algebra-20.md:40,54-60](https://github.com/patatohek-boop/zhixu-cloud-textbook/blob/a1847cd253133caeee745411f6e86444395fac6a/content/linear-algebra/linear-algebra-20.md#L40) 条件数先只定义可逆方阵，随后直接对长方形满列秩矩阵使用同一符号；相对扰动界未在本段重申 $b\ne0$。[content/linear-algebra/linear-algebra-22.md:48-51](https://github.com/patatohek-boop/zhixu-cloud-textbook/blob/a1847cd253133caeee745411f6e86444395fac6a/content/linear-algebra/linear-algebra-22.md#L48) 使用 $v_{k+1}$、$\sigma_{k+1}$，未规定 $k$ 范围，满秩截断端点会使下标越界。修订方向：明确矩形二范数条件数扩展、非零右端条件，以及低秩近似非平凡范围与精确重构端点。

## 本轮实施结果

已逐篇查看微积分31节、线性代数24节的正文、目录、例题和练习；全部55个旧ID保留。每篇都按数学对象和推理用途拆段，最终两科共有359个三级小节。拆分点包括“定义什么”“条件是什么”“这一步为何成立”，并把原本串在一段的例题步骤各自呈现，没有按句号机械切段。

| 基线问题 | 处理结果 |
|---|---|
| 1：完备性章先修不明 | 补数列、子列、柯西条件、向量收敛和连续的明确定义；保留存在性证明并提供首次学习及回读路线。 |
| 2：平均速度概念错误 | 已更正为位移除以时间，另定义平均速率并给往返运动反例。 |
| 3：牛顿、辛普森先修错位 | 牛顿算法和迭代实例先于收敛证明；回读证明链接积分与泰勒；辛普森补充移到泰勒之后，四次分部积分替代隐藏的Fubini依赖。 |
| 4：平坦函数证明缺步 | 增补非零点求导形式、零点差商归纳、各阶连续性三步。 |
| 5：多个新概念堆叠 | 全55节均已分段；梯度、方向导数、Hessian与定性，参数曲线、正则性、换参和极坐标分别可定位。 |
| 6：二维极值判据不可操作 | 明列行列式符号与首项符号分支、零行列式不能判定；补完整驻点计算及配方核对全局性。 |
| 7：相似证明提前用术语 | 相似的谱、迹不变量移到第13课，先定义后证明；第08课保留换基主线与秩不变。 |
| 8：Jordan链过密且缺构造 | 按链定义、无关、降维、提升、补基拆开；补幂零核非零的理由和非标准三阶链构造，另加链顶变式。补充章移到核心SVD及数值应用之后、动力系统之前。 |
| 9：一般拟合缺算例 | 新增三点两参数直线拟合：设计矩阵、正规方程、参数、残差正交、平方误差及精确拟合变式。 |
| 10：条件数与截断范围 | 说明矩形条件数的伪逆扩展，重申相对误差的非零右端；低秩近似分清非平凡范围与精确重构端点。 |

另修正和明确了：参数二阶导数的C2条件；标量与向量值极限的不同距离记号；保守场等价定理的开且路径连通条件；多元换元统一导数界L；洛必达无穷下界估计的余量；正交投影证明的有限维范围；零矩阵的最大奇异值表述；动力系统的实矩阵实初值范围。指数压过幂的证明改为积分归纳，不再预先借用后续泰勒展开。

## 专门复核的三条证明

- **calculus-31多元换元**：复核了紧致邻域、局部凸小盒上的导数界、收缩填满内盒、像边界零体积、一般零体积边界的立方网格覆盖、单射下分片可加及统一黎曼和误差。当前证明没有用“点移动小”代替“体积误差小”；本轮补明确L并拆出每一环节。它仍是所陈述的连续函数、紧致Jordan区域、单射非退化C1映射版本。
- **linear-algebra-15实对称谱定理**：极大方向给特征向量；其正交补不变；选正交基后限制矩阵仍对称；对低一维矩阵归纳并拼基。没有把“特征向量两两正交”误作完整基存在证明。本轮将这四项拆开，没有无根据地宣布原定理错误。
- **linear-algebra-23Jordan链基**：最高链向量模去N(W)后的独立性、提升向量的独立性、N(U)=W及V=U+ker N这条论证成立。本轮补充非零幂零算子像空间严格降维的理由；商空间只在本章给出所需的最小定义，完整商空间理论仍是后续主题。

## 本轮实际核对的公开主源

1. [MIT 18.06 Lecture 28: Similar Matrices and Jordan Form](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/6e1f793f6c25fd39e002c100e278bf1b_MIT18_06SCF11_Ses3.4sum.pdf)，阅读5页PDF正文。用于核对相似保特征结构、重复特征值与块大小的区别，并判断Jordan专题的课程定位。该讲义并未给本教材的整套链基归纳证明，本报告不把它说成该证明的外部认证。
2. [MIT 18.06 Lecture 25: Symmetric Matrices and Positive Definiteness](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/804ab1e53134741d2044d241b50a285e_MIT18_06SCF11_Ses3.1sum.pdf)，阅读4页PDF正文。核对实对称谱定理、正交模态与正定判据的准确结论；逐步归纳论证另外依照本教材前面已证明的紧致和正交理论审查。
3. [MIT 18.01SC Syllabus](https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/pages/syllabus/)，仅用来比较本科初学路线与先修安排，不将目录当成证明来源。

以上均为本轮实查来源；未复制讲义长段。例题、分段与修订论证均独立书写。

## 验证与实际边界

- 数学源文件检查通过：55节、419项检查，其中391项元数据／覆盖映射／链接检查与28项既有数学验证；3771个公式通过KaTeX解析。
- 对本轮新增内容另做13项精确符号核查，覆盖二维极值配方、最小二乘系数与残差、Jordan相似及替代链、四次分部积分余项恒等式。另核对全部55节的JSON头部与359个h3均位于数学公式外。
- 两科逐章审计和coverage_map已同步：所有55节仍有覆盖映射，记录标题与课文标题一致。数学检查不构成定理的形式化验证。

这一轮没有以“进阶主题没有穷尽”作为缺陷。仍明确保留的范围限制包括：一般Lebesgue积分与粗糙区域上的积分定理；复多项式分裂所依赖的代数基本定理证明；连续Fourier级数的完整点态及均方收敛理论；Schur、Krylov与一般浮点稳定性分析。这些不属于本轮必须补成完整专著的目标。

教学上仍需后续工作：完备性与一般Jordan证明即使拆段后仍较难，应该按标明的阅读路线分次学习；现有练习可检验基础操作与部分条件辨析，但还不是覆盖每个高阶证明目标的完整习题库。页面学习分钟数未经过真实初学者试学校准。本报告没有声称外部教师审校、教师认证或实际课堂验证。
