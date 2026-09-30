# 热学教材教学审读与修订记录

日期：2026-09-28。审读角色是教材教学内容校核，不是外部教师认证。范围是工程热力学29章、传热学31章的目录、学习目标、概念定义、正文推导、例题和练习。下表记录修改前的基线位置；后续内容行号会改变。P1为明确概念/物理错误，P2为条件缺口或会阻碍初学者完成目标的教学问题。

## 修改前的具体问题

### T01 · P1

- 基线文件：[thermodynamics-01.md](https://github.com/patatohek-boop/zhixu-cloud-textbook/blob/a1847cd253133caeee745411f6e86444395fac6a/content/thermodynamics/thermodynamics-01.md#L84)，第84—88行。
- 短原文证据：剩余或取出气体均为 1 kg，体积 0.30 m³，因此比体积仍为 0.30 m³/kg。
- 初学者影响：原题从 0.60 m³ 刚性罐取出一半质量，剩余气体仍占原罐 0.60 m³。将两部分体积都写成 0.30 m³，混淆了几何等分与实际抽气，误教比性质的含义。
- 可实施改法：改为分别计算新罐与原罐的比体积，说明温度保持并不意味着状态全部保持。

### T02 · P1

- 基线文件：[thermodynamics-25.md](https://github.com/patatohek-boop/zhixu-cloud-textbook/blob/a1847cd253133caeee745411f6e86444395fac6a/content/thermodynamics/thermodynamics-25.md#L39)，第39—39行。
- 短原文证据：热容 C=dU/dT 在指定约束下用 J/K
- 初学者影响：用内能温度导数统称热容，会把定压热容也教成内能导数，与第06节自身定义冲突。
- 可实施改法：明确 C_V=(∂U/∂T)_V、C_p=(∂H/∂T)_p；本节测量模型的 C 仅在膨胀功可忽略等条件下作为有效热容。

### T03 · P2

- 基线文件：[thermodynamics-06.md](https://github.com/patatohek-boop/zhixu-cloud-textbook/blob/a1847cd253133caeee745411f6e86444395fac6a/content/thermodynamics/thermodynamics-06.md#L97)，第97—101行。
- 短原文证据：上述气体若等温膨胀至两倍体积，T=300 K，做功多少？
- 初学者影响：等温与两端体积不足以确定路径功。答案代入可逆/准平衡积分而题干没有给出对应边界条件，学生易把任意等温过程当同一功。
- 可实施改法：题干显式给准平衡、边界机械平衡、只有体积功；解析对照理想气体自由膨胀的零功。

### T04 · P2

- 基线文件：[thermodynamics-21.md](https://github.com/patatohek-boop/zhixu-cloud-textbook/blob/a1847cd253133caeee745411f6e86444395fac6a/content/thermodynamics/thermodynamics-21.md#L65)，第65—65行。
- 短原文证据：超过露点则必须同时算潜热和凝水
- 初学者影响：冷却问题中“超过”没有方向，容易被理解为高于露点就凝结。
- 可实施改法：明确冷却至露点以下才发生凝结，并在同压假设下区分到露点与露点以下。

### H01 · P2

- 基线文件：[heat-transfer-21.md](https://github.com/patatohek-boop/zhixu-cloud-textbook/blob/a1847cd253133caeee745411f6e86444395fac6a/content/heat-transfer/heat-transfer-21.md#L39)，第39—51行。
- 短原文证据：对漫射表面，角系数 F_ij 是表面i离开的总辐射中直接到达表面j的份额
- 初学者影响：把整面功率分数视为仅几何量，还需要所分面离开辐射度均匀。现有积分把 I_i 提到积分号外，没有明确空间均匀条件。非等温热点会使学习者错误套用一个整面平均温度。
- 可实施改法：定义中加入面内均匀离开辐射度；推导解释为何可提出 I_i；不均匀时细分面元或保留 I_i(x) 权重。第22节同步补离散面假设。

### T05 · P2

- 基线文件：[thermodynamics-04.md](https://github.com/patatohek-boop/zhixu-cloud-textbook/blob/a1847cd253133caeee745411f6e86444395fac6a/content/thermodynamics/thermodynamics-04.md#L59)，第59—97行。
- 短原文证据：邻近表格点 z_a,z_b 的线性插值来自假定局部 y(z)=a+bz
- 初学者影响：目标包含物性表读法与插值，但正文只有抽象插值式，唯一算例已直接给 h_f、h_fg，两个练习也没有表格。初学者不能实际练到选行、选列、插值、检查相区。
- 可实施改法：补一个明确教学数据表与逐步插值任务，给同压与单位，区分插值误差和真实物性数据精度；与第15节状态构造练习衔接。

### T06 · P2

- 基线文件：[thermodynamics-13.md](https://github.com/patatohek-boop/zhixu-cloud-textbook/blob/a1847cd253133caeee745411f6e86444395fac6a/content/thermodynamics/thermodynamics-13.md#L73)，第73—76行。
- 短原文证据：这两个数字若来自不同子过程不能随意相减
- 初学者影响：例题同时给不同子过程的热量火用与火用毁灭，并正确提醒不能乱减，但没有完整同一边界的能量—熵—火用闭合算例。学生学会两个乘法，尚未练到本节目标的整账。
- 可实施改法：保留原反例，补同一个循环装置的闭合数据例：热输入、排热、功和熵产均明确，由三条账独立得到相容结果。

### H02 · P2

- 基线文件：[heat-transfer-08.md](https://github.com/patatohek-boop/zhixu-cloud-textbook/blob/a1847cd253133caeee745411f6e86444395fac6a/content/heat-transfer/heat-transfer-08.md#L49)，第49—55行。
- 短原文证据：边界项因相同对称与Robin条件消失
- 初学者影响：分离变量、特征值、正交性和投影在相邻两大段中连续跳跃，例题又直接给第一根和系数；数学初学者缺少实际计算入口。
- 可实施改法：按分离、边界筛根、正交与投影分段；解释Robin边界含义；补一次用区间求根、代入 A_1 的练习，说明多项检查。

### T07 · P2

- 基线文件：[thermodynamics-28.md](https://github.com/patatohek-boop/zhixu-cloud-textbook/blob/a1847cd253133caeee745411f6e86444395fac6a/content/thermodynamics/thermodynamics-28.md#L42)，第42—42行。
- 短原文证据：滞止温度 T0由 h(T0)=h0定义
- 初学者影响：定义写成单变量 h(T)，必须限定固定组成理想气体或相应热性质模型；真实气体焓一般也依赖压力。后文理想气体计算正确，但第一定义未收紧适用域。
- 可实施改法：先给一般停滞焓定义，再明确本章固定组成理想气体下才由 h(T0)唯一反求温度。

### H03 · P2

- 基线文件：[heat-transfer-01.md](https://github.com/patatohek-boop/zhixu-cloud-textbook/blob/a1847cd253133caeee745411f6e86444395fac6a/content/heat-transfer/heat-transfer-01.md#L41)，第41—45行。
- 短原文证据：温度场…热量…热流率…热流密度…体积热源；对流换热…热辐射
- 初学者影响：入门定义把状态描述、四种不同量纲、三种机制及两类系数堆在三个长段中；热容/流率等近名概念也在其他章同段连续出现。会妨碍初学者停下来检查每个符号与适用条件。
- 可实施改法：全60章按具体概念分段/命名小节，不机械按句号切分；物理定律、定义、模型、经验式分别交代；保持公式推导与例题条件完整。

## 事实核对来源

- 热容的约束与内能/焓区别，核对 [MIT Unified Thermodynamics T5 教学释疑](https://ocw.mit.edu/ans7870/16/16.unified/thermoF03/mud/T5mud03.html) 和 [MIT 8.21 Lecture 4](https://ocw.mit.edu/courses/8-21-the-physics-of-energy-fall-2009/c53354320a738e2b43ce891740f1c79a_MIT8_21s09_lec04.pdf)。这里采用其定义层面的核对，不复制讲义内容。
- 辐射角系数的漫射及面内均匀条件，核对 [MIT 2.997 Lecture 8 逐字稿中的角系数推导](https://ocw.mit.edu/courses/2-997-direct-solar-thermal-to-electrical-energy-conversion-technologies-fall-2009/1AOL4OEVBcePRrLqikulQwNYWbUcsXTyh_transcript.pdf)。
- Carnot→Clausius→熵路径独立链另核对正文已有的 MIT 5.60 Lecture 9 具体讲义链接；本轮未发现该链循环论证，保留其论证顺序。

## 逐章覆盖

逐篇审读过以下60章。合理专业边界（完整湍流闭合、多组分非理想扩散、复杂两相设备等）不作为缺陷；未声称穷尽所有工程应用。

### thermodynamics

- thermodynamics-01：从一杯热水开始：系统、状态与平衡。已读定义、推导、例题和练习。
- thermodynamics-02：温度、压力与测量基准。已读定义、推导、例题和练习。
- thermodynamics-03：状态方程、理想气体与真实气体。已读定义、推导、例题和练习。
- thermodynamics-04：相变、干度与物性表的读法。已读定义、推导、例题和练习。
- thermodynamics-05：热、功与闭口系统第一定律。已读定义、推导、例题和练习。
- thermodynamics-06：比热、理想气体过程与多变关系。已读定义、推导、例题和练习。
- thermodynamics-07：控制体：质量守恒与稳流能量方程。已读定义、推导、例题和练习。
- thermodynamics-08：常见流动设备与非稳态充气。已读定义、推导、例题和练习。
- thermodynamics-09：第二定律、热机与可逆性。已读定义、推导、例题和练习。
- thermodynamics-10：Carnot 循环与热泵极限。已读定义、推导、例题和练习。
- thermodynamics-11：熵：状态量、传递与产生。已读定义、推导、例题和练习。
- thermodynamics-12：控制体熵平衡与等熵效率。已读定义、推导、例题和练习。
- thermodynamics-13：火用：能量的利用价值与损失定位。已读定义、推导、例题和练习。
- thermodynamics-14：基本热力学关系、势函数与 Maxwell 关系。已读定义、推导、例题和练习。
- thermodynamics-15：Rankine 蒸汽动力循环。已读定义、推导、例题和练习。
- thermodynamics-16：再热、回热与联合循环。已读定义、推导、例题和练习。
- thermodynamics-17：Brayton 循环与燃气轮机再生。已读定义、推导、例题和练习。
- thermodynamics-18：Otto 与 Diesel：内燃机的空气标准模型。已读定义、推导、例题和练习。
- thermodynamics-19：蒸气压缩制冷、热泵与工质选择。已读定义、推导、例题和练习。
- thermodynamics-20：理想混合气体与混合熵。已读定义、推导、例题和练习。
- thermodynamics-21：湿空气、相对湿度与空气处理。已读定义、推导、例题和练习。
- thermodynamics-22：燃烧计量、生成焓与绝热火焰温度。已读定义、推导、例题和练习。
- thermodynamics-23：化学势、反应平衡与平衡常数。已读定义、推导、例题和练习。
- thermodynamics-24：相平衡、Clapeyron 关系与稳定性边界。已读定义、推导、例题和练习。
- thermodynamics-25：量热实验、传感器与不确定度。已读定义、推导、例题和练习。
- thermodynamics-26：综合项目：从第一律到能量审计。已读定义、推导、例题和练习。
- thermodynamics-27：真实气体性质：可测导数与节流温变。已读定义、推导、例题和练习。
- thermodynamics-28：滞止性质、喷管堵塞与推进效率。已读定义、推导、例题和练习。
- thermodynamics-29：熵的微观桥梁：计数、概率与宏观极限。已读定义、推导、例题和练习。

### heat-transfer

- heat-transfer-01：传热三方式与第一张能量流图。已读定义、推导、例题和练习。
- heat-transfer-02：导热方程、初始条件与边界条件。已读定义、推导、例题和练习。
- heat-transfer-03：平壁热阻、复合墙与接触热阻。已读定义、推导、例题和练习。
- heat-transfer-04：圆柱与球壳：面积变化后的导热。已读定义、推导、例题和练习。
- heat-transfer-05：内热源与变导热系数。已读定义、推导、例题和练习。
- heat-transfer-06：肋片效率与临界保温半径。已读定义、推导、例题和练习。
- heat-transfer-07：集总热容：小物体如何随时间冷却。已读定义、推导、例题和练习。
- heat-transfer-08：一维非稳态导热、特征值与图表。已读定义、推导、例题和练习。
- heat-transfer-09：半无限体、热穿透与叠加原理。已读定义、推导、例题和练习。
- heat-transfer-10：数值导热：差分、稳定性与网格检查。已读定义、推导、例题和练习。
- heat-transfer-11：对流边界层与质量、动量、能量守恒。已读定义、推导、例题和练习。
- heat-transfer-12：Re、Pr、Nu、Gr、Ra：无量纲数的地图。已读定义、推导、例题和练习。
- heat-transfer-13：外部强迫对流：平板、圆柱与局部系数。已读定义、推导、例题和练习。
- heat-transfer-14：内部层流、入口段与主体温度。已读定义、推导、例题和练习。
- heat-transfer-15：内部湍流、摩擦与泵功折中。已读定义、推导、例题和练习。
- heat-transfer-16：自然对流、稳定分层与混合对流。已读定义、推导、例题和练习。
- heat-transfer-17：沸腾、临界热流与沸腾曲线。已读定义、推导、例题和练习。
- heat-transfer-18：凝结、液膜与相变换热器。已读定义、推导、例题和练习。
- heat-transfer-19：黑体辐射、光谱与太阳能。已读定义、推导、例题和练习。
- heat-transfer-20：表面辐射性质与 Kirchhoff 定律。已读定义、推导、例题和练习。
- heat-transfer-21：角系数、几何遮挡与黑体交换。已读定义、推导、例题和练习。
- heat-transfer-22：灰体辐射网络与参与介质。已读定义、推导、例题和练习。
- heat-transfer-23：换热器与对数平均温差法。已读定义、推导、例题和练习。
- heat-transfer-24：效能–NTU 法：出口未知时如何计算。已读定义、推导、例题和练习。
- heat-transfer-25：传热传质类比与蒸发耦合。已读定义、推导、例题和练习。
- heat-transfer-26：综合设计：散热器、保温与可信验证。已读定义、推导、例题和练习。
- heat-transfer-27：多维导热：矩形解析解、乘积解与唯一性。已读定义、推导、例题和练习。
- heat-transfer-28：边界层积分法：从方程到可计算近似。已读定义、推导、例题和练习。
- heat-transfer-29：扩散的两种边界：等摩尔逆扩散与Stefan流。已读定义、推导、例题和练习。
- heat-transfer-30：圆柱横掠、管束与非圆通道的关联式选择。已读定义、推导、例题和练习。
- heat-transfer-31：熔化与凝固：移动界面和Stefan条件。已读定义、推导、例题和练习。

## 修订与验证状态

本轮已完成60章正文修订及两门课审计记录更新，全部原课文ID与标题保留。概念按含义拆成238个 h3 小节，定义、符号、模型条件与通俗解释有各自位置。分段阶段逐篇检查了“移除新增标题并忽略空白后原文字不变”，随后才单独修正错误和补例题，避免用删减内容换取短段落。

实际修复：

- T01、T02：修正刚性罐抽气后的剩余体积/比体积，以及定容、定压热容的性质定义。
- T03、T04、T07：补等温做功的路径条件，明确露点以下凝结的冷却方向，限定由单变量焓求滞止温度的理想气体前提。
- H01：补整面角系数所需的均匀离开辐射度，区分总离开辐射 $J=\pi I$ 与自身发射 $E=\pi I_e$；第22章同步补离散面的模型条件。
- T05、T06、H02：加入同压教学物性表的插值与反插、Rankine 出口判相及实际涡轮练习、同一个循环的能量/熵/火用闭合例、特征根二分求解与早期截断反例。
- H03：全60章作语义分段。另展开第14章势函数的乘积微分和一般比热差推导，给第12章使用性质恒等式时的就地先修说明，在 Brayton 章首次使用空气标准模型时明确假设。

验证结果：

- 既有热学内容、覆盖和数值核查：337项通过；两门课共60条审计与课文对应。
- 新增抽气、等温功、插值、循环三账、Rankine出口及特征根：27项数值与一致性检查通过。
- 60章正文共1905条公式通过 KaTeX；没有公式解析错误。
- 60章结构检查通过：无空h3、控制字符、失配折叠解析/代码围栏或断开的内部课文链接。
- 未修改共享UI、构建脚本、版本、发布内容或git；网站和APK由主任务统一处理。

仍存限制：

- 新增物性查表和循环练习采用明确标注的假想/取整教学数据，用来练选区、插值和状态构造；没有将未核验数值冒充精确水蒸气数据。真实工质数据库、测量数据与设备选型需要另作实际工况任务。
- 特征函数、偏导与概率桥梁等扩展章节依赖相应数学基础；已补关键衔接和步骤，并不替代完整微积分、常微分方程或数值分析课程。
- 沸腾、凝结、湍流与辐射均保留所列物理假设和经验适用范围。完整工业模型和全部研究生专题未纳入；这些既定边界不作为本轮缺陷。
- 检查证明所执行范围内的结构、算例与公式一致性，不代表外部教师认证，也不能证明教材不存在其他遗漏。


## 修订后抽查入口

- [thermodynamics-01：**练习 1**](https://github.com/patatohek-boop/zhixu-cloud-textbook/blob/a1847cd253133caeee745411f6e86444395fac6a/content/thermodynamics/thermodynamics-01.md#L93)。
- [thermodynamics-04：把“查表与插值”](https://github.com/patatohek-boop/zhixu-cloud-textbook/blob/a1847cd253133caeee745411f6e86444395fac6a/content/thermodynamics/thermodynamics-04.md#L86)。
- [thermodynamics-06：**练习 1**](https://github.com/patatohek-boop/zhixu-cloud-textbook/blob/a1847cd253133caeee745411f6e86444395fac6a/content/thermodynamics/thermodynamics-06.md#L113)。
- [thermodynamics-13：一台循环装置](https://github.com/patatohek-boop/zhixu-cloud-textbook/blob/a1847cd253133caeee745411f6e86444395fac6a/content/thermodynamics/thermodynamics-13.md#L86)。
- [thermodynamics-14：第一步：把两种比热](https://github.com/patatohek-boop/zhixu-cloud-textbook/blob/a1847cd253133caeee745411f6e86444395fac6a/content/thermodynamics/thermodynamics-14.md#L81)。
- [thermodynamics-15：从物性记录](https://github.com/patatohek-boop/zhixu-cloud-textbook/blob/a1847cd253133caeee745411f6e86444395fac6a/content/thermodynamics/thermodynamics-15.md#L86)。
- [thermodynamics-21：$h_l$ 是凝水](https://github.com/patatohek-boop/zhixu-cloud-textbook/blob/a1847cd253133caeee745411f6e86444395fac6a/content/thermodynamics/thermodynamics-21.md#L73)。
- [thermodynamics-25：对固定组成的简单可压缩系统](https://github.com/patatohek-boop/zhixu-cloud-textbook/blob/a1847cd253133caeee745411f6e86444395fac6a/content/thermodynamics/thermodynamics-25.md#L41)。
- [thermodynamics-28：本章以下取固定组成理想气体](https://github.com/patatohek-boop/zhixu-cloud-textbook/blob/a1847cd253133caeee745411f6e86444395fac6a/content/thermodynamics/thermodynamics-28.md#L46)。
- [heat-transfer-08：从边界条件实际求](https://github.com/patatohek-boop/zhixu-cloud-textbook/blob/a1847cd253133caeee745411f6e86444395fac6a/content/heat-transfer/heat-transfer-08.md#L120)。
- [heat-transfer-21：对漫射且所分面内](https://github.com/patatohek-boop/zhixu-cloud-textbook/blob/a1847cd253133caeee745411f6e86444395fac6a/content/heat-transfer/heat-transfer-21.md#L41)。
