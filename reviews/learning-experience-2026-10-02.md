# 本科基础薄弱者的学习体验增强（待审核）

## 范围与边界

- 基于审核修复提交 `04b715def31b838b93201da521b633d8dcddf10f`，独立功能分支，不修改该修复的草稿 PR。
- 全部 253 节接入分层知识框架、单节关系定位与改进的阅读界面。不是把 253 节全部重写。
- 首轮实质增强 26 节：具体问题、概念图、符号和单位、中间推导步骤、数值例题、理解检查；完整原文与原有练习保留在“深入”展开层。
- “起步主线”是本科基础的连接路线，不是固定天数速成承诺，也不替代课程考试大纲、严格证明训练或专业审校。主线之外的必备概念仍明确链接。
- 原有课号、标题、课文元数据、学习记录键、备份格式及已有答题数据保持不变。

## 首轮 26 节

| 课程 | 实质增强的稳定课号 |
|---|---|
| 微积分 | calculus-01、03、07、15 |
| 线性代数 | linear-algebra-01、02、03、10 |
| 工程热力学 | thermodynamics-01、05、07 |
| 传热学 | heat-transfer-01、03、07 |
| 流体力学 | fluid-mechanics-01、06、07、10 |
| Python | python-01、06、07、20 |
| 机器学习 | machine-learning-01、04、05、07 |

每门课的起步目标、过关标准和已核对依赖位于 `content/learning-guides-*.json`，通过构建器校验链接、重复节点和严格依赖环，再生成本地数据包。非主线课文的旧版“先修”仅作为建议阅读展示，不冒充已核对的严格依赖。

## 阅读与知识框架

1. `#/path`：起步路线，可按课程筛选；每节列出解决的问题和具体过关标准。
2. `#/map`：七门课程框架，明确数学/编程工具与工程/数据应用之间的联系。
3. `#/map/<课程>`：按课程主题分组的完整知识图，所有课文均有可键盘访问的文本节点，可筛选主线、补基础或进阶选读。
4. `#/map/<课程>/<课号>`：带明确关系标签的局部依赖图。实线为已核对必备概念；虚线为建议补读。目录顺序不等同于依赖边。
5. 课文开头的长目标、修订说明和关系列表改为按需展开；主线侧栏优先显示核心点，完整目录仍可展开。
6. 课文图片可在页面内放大、缩小和滚动查看，手机初次打开按200%显示；关闭或安卓返回键会回到原课文，不依赖外部浏览器或网络。CI逐图计算放大后的最小字形尺寸，避免把“不裁切”误当成“字可读”。
7. 保留字号、主题、专注阅读、笔记、打印与备份。独立公式有自身可键盘滚动区域；长行内公式、表格和代码的溢出不应推动整页。

## 新增可复算实验

- `foundation-energy`：闭口系统热入/功出符号，逐项核对 `ΔU = Q − W`，明确边界和量纲。
- `foundation-projection`：投影、垂直残差与最小距离；坐标等比例，零方向向量明确无定义。
- `foundation-mass`：流入、流出与积累；到空罐时双泵停止，边界变化明确展示，不允许继续生成负质量。

三个实验均有预测问题、分步讲解、手动动画、重置和条件说明；没有自动播放、远程计算或联网依赖。挂接热力学 05、线性代数 10、流体力学 07；原有 21 个实验全部保留。

## 适量概念动画

在六个代表性本科问题旁增加原创、分阶段可播放图解：热力学05的能量收支、传热03的串联热阻、传热07的冷却时间演化、流体07的控制体积累、Python06的逐行循环、机器学习07的回归拟合。

教学节奏参考图形直觉讲解，图形、代码和例子独立实现。守恒记账、稳态热阻与模型拟合的过渡明确标为“讲解步骤”，不伪装成物理时间；冷却与容器积累使用带单位的时间。没有自动播放；支持播放/暂停、重看、前后步骤和键盘可调的进度条。减少动态效果偏好关闭中间过渡，仍保留手动步骤与文字说明。离开课文时销毁播放器，不改写学习记录。

这六处动画用于解释过程，不代表为253节全部制作动画；原有数学/工程交互实验继续可用。新概念动画与全部图片同样由 Android 打包器随 App 内置。

## 检查与待验证项

可在允许的开发环境运行：

```sh
python tools/build.py
node tools/validate.cjs
node tools/test-learning-state.cjs
node tools/test-research-labs.cjs
node tools/test-cfd-labs.cjs
node tools/test-foundation-labs.cjs
node tools/test-concept-stories.cjs
node tools/test-knowledge-map.cjs
python tools/test-offline-learning.py
python tools/security_check.py
cd tools/qa
npm ci --ignore-scripts
npx playwright install --with-deps chromium
npm test
```

DOM 全量检查可通过 `ZHIXU_JSDOM_MODULE` 指向已安装 jsdom 后运行 `tools/test-rendering.cjs` 与 `tools/test-learning-experience.cjs`。新增实验的 DOM/动画生命周期检查为 `node tools/test-foundation-labs.cjs --dom`。

浏览器测试覆盖 320/360/390/768/1165/1440 px。320 px 检查全部 253 节，其余宽度检查 26 节锚点；另查知识节点、筛选、关系图、展开、字号、深色、记录持久化及新实验，在390与1440px保存有代表性的截图供人工复核（失败时所有尺寸均保留截图）。测试能运行不代表视觉设计已经人工验收。浏览器断网用例仅检查已加载脚本与课文数据的站内导航，不声称普通网页无需首次联网或支持离线刷新；完整首次离线资源依靠 APK 打包与无联网权限的 Android 模拟器验证。

`.github/workflows/learning-ui.yml` 只响应 pull_request、只有 contents:read 权限、不发布网站或 APK。使用开发专用锁文件中精确固定的官方 `@playwright/test 1.63.0` 和 `jsdom 30.1.1`；版本和包完整性来自官方 npm registry，测试依赖不进入 `site/` 或 APK。

当前执行器的 Chromium 无法创建本地进程 socket（Operation not permitted），因此本地实际浏览器像素、视口溢出与截图测试未运行成功；不得把 DOM 检查当作这些项目通过。授权发布草稿 PR 后应由 CI 运行，再检查截图。Android 资源逐文件打包检查也不等同于 APK 编译、Android 模拟器或实机测试。Android 工作流已增加限定路径的 PR 触发，并新增知识框架与概念动画两项 instrumentation 测试，共12项；发布草稿后应检查编译、Lint 与 Android15 模拟器的实际结果，不把测试代码存在当成运行通过。

本分支未改变正式 APK 版本或签名，没有生成或发布正式安装包。发布时应另行增加 Android 版本并完成已有签名与升级验证流程。

## 中文教学组织参考

本轮只参考公开样章、讲义和课程介绍中的“说明符号—展示例子—归纳方法—独立练习”组织方式，正文、算例、图形和动画均独立编写。没有声称完整观看课程视频或通读整本教材，也不代表相关机构背书：

- [公开中文线性代数讲义](https://basics.sjtu.edu.cn/~yangqizhe/pdf/la2024s/slides/LALecFull-handout-zh.pdf)：抽查分量、符号、例子与归纳的组织方式
- [清华大学出版社 Python 实验指导试读](https://www.tup.tsinghua.edu.cn/upload/books/yz/091318-01.pdf)：抽查操作、输出与解释结合的练习方式
- [同济大学官方 MOOC 课程介绍](https://www.icourse163.org/course/TONGJI-53004)、[北京理工大学官方 MOOC 课程介绍](https://www.icourse163.org/course/BIT-268001)：仅查看公开课程介绍
