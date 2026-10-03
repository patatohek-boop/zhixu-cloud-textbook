# 1.6.0 发布前本地封版验收（2026-10-04）

## 范围与结论

本记录只确认本机已执行的检查。253 节内容与原有课尾测验标识保留，78 道进阶题已由四份专项报告逐题审读；本轮按认可的修订冻结 359 个源文件，并保留 367 条逐项内容变更说明。最终网站构建、公式排版、内容保全、练习展示、渲染与离线资源检查通过。

这不表示教学内容可以仅靠程序证明无误，也不表示安卓正式 APK 已通过安装或迁移验收。安卓正式签名包、两种旧版并存及 JSON 迁移仍需后续实际模拟器 / CI 执行；本记录未执行远程上传、提交或发布。

## 人工审读依据

- [数学 24 题](prepublication-mastery-math-2026-10-04.md)
- [热工 18 题](prepublication-mastery-thermal-2026-10-04.md)
- [流体与 Python 24 题](prepublication-mastery-fluid-python-2026-10-04.md)
- [机器学习 12 题](prepublication-mastery-machine-learning-2026-10-04.md)
- [七科内容与本轮 78 题审查汇总](prepublication-summary-2026-10-04.md)
- [目录重排后的正文课次引用复核](prepublication-order-reference-2026-10-04.md)

四份题目报告、汇总及课次引用复核已加入 `reader-revision-1.6.0.json` 的审读依据。数学 2 字段、热工 11 字段修订以精确 before / after、原因与报告写入 [进阶题变更清单](prepublication-mastery-dispositions-1.6.0.json)，所有最终数值答案保持。

新验收分支从原始 1.5.0 归档提取四份完整题库文本，先用历史 SHA-256 校验其字节，再仅施加这 13 个指定字段改动，要求与当前全部 78 道题对象深度相等，同时校验新审稿快照。原有 1.5.0 分支与不可变基线保留。六项内存反例检查确认：批准内容通过；擅改题文、历史基线、before 字段、遗漏修订或新增未批准字段均被拒绝。

## 本机实际执行结果

| 检查 | 结果与边界 |
|---|---|
| `tools/build.py` | 通过；7 科、253 节、78 道进阶题、26 个题组入口。重复构建的首页、data.js、content-stats.json 字节相同。 |
| `tools/verify_reader_revision.py --freeze-reviewed` | 通过；最终构建后冻结 359 文件，253 个 ID 与课尾测验、367 条逐项说明保留。 |
| `tools/validate.cjs` | 通过；253 节、12,351 处公式、24 个交互实验的结构与公式排版检查。公式能够排版不等于证明数学论述正确。 |
| `tools/verify_report_revision.py` | 通过；原报告修订检查与新版精确保全检查。 |
| `tools/test-learning-preservation.py` | 通过；课号、测验、原公式 / 代码 / 图像及有说明的重组检查。 |
| `tools/verify_final_review.py` | 通过；253 个稳定 ID、原测验键与获准条件澄清及相关回归。 |
| `tools/revision/verify_math.py` | 2,336 项通过、0 项失败；含数值 / 符号与图形结构断言，并非 2,336 份独立数学证明。 |
| `tools/mastery/verify_math.py` | 24 题对应案例及 8 个题组入口检查通过；人工前提与证明检查见数学专项。 |
| `tools/mastery/verify_thermal.py` | 成功复算 18 题记录；脚本并非对每个结果都自动断言，18 题逐项比较与条件判断见热工专项。换行统一后重跑。 |
| `tools/mastery/verify_fluid.py` | 12 题的 40 个独立量校验通过。 |
| `tools/mastery/verify_computing.py` | 24 题检查通过，实际执行 9 个解答 Python 代码块，并核对数据划分示例。 |
| `tools/test-mastery-exercises.cjs --dom` | 78 题完整对象保全与 26 课练习展示通过；三级题目、解答 / 检查点、折叠交互、手机目录与原进度 / 分数存储接口通过。 |
| `tools/test-rendering.cjs` | 253 课、12,351 公式、12 项攻击输入、笔记转义、无效路由、实验、测验、事务式备份、安卓适配隔离与返回处理通过。 |
| `tools/test-offline-learning.py` | 打包 156 个安卓离线文件，77 个阅读资源与网站源一致；入口无远程资源依赖。这是资源检查，不是 APK 安装测试。 |

## 检查中暴露并处理的问题

1. 原练习测试冻结了历史题库文件哈希，拒绝已审定的热工改动，首次失败确实发生并保留日志。新增精确的 13 字段重建分支后，全部题目、DOM 与上述六项反例通过，未删除历史哈希或放宽为无条件跳过。
2. 第一次先冻结后构建，构建更新了首页资源指纹，两项保全检查因此失败。确认仅为生成首页变化且重建稳定后，改为先构建最终文件再冻结；两项检查重新通过。失败日志仍保留。
3. 热工题库最终修订写入了 457 对 CRLF。只将该可变 JSON 换行为 LF，解析后的全部对象完全相同；新变更清单仅更新 reviewed_sha256，13 项 before / after 与历史字节保持。再次检查 436 个相关路径的 Git clean / raw 对象一致，避免上传后 Linux 的字节校验差异。
4. 主代理在 390 / 320 像素浏览器视口发现短行内点积 / 根号的字形末端约 2 像素越界，触发多余横滚条。其补充行内 KaTeX 边缘空间并实看确认：短公式宽度不再越界，长公式保留必要横向滚动及键盘焦点，页面无横向溢出。本地重新构建、冻结、公式 / 渲染 / 练习 DOM / 离线检查均通过。浏览器实看由主代理执行，本子任务未重复模拟该观察。

## 字节与审计记录

4 份不可变历史基线、65 张 SVG、68 个第三方资源共 137 文件与换行处理前 SHA-256 完全一致。359 个最终冻结源文件逐一匹配快照，367 条内容说明保持；全部 436 个所检路径上传过滤前后字节一致。

当前生成物 SHA-256：

- `site/index.html`：`6237b7a095c536c07ec099ef8ebdd7ecef3374a4c2df8e1644f177e7a959d466`
- `site/assets/data.js`：`809a3e5fa8cc69e7075644606133bea69f8c0ba74bd132238bbf330256cdfbd3`
- `site/assets/content-stats.json`：`1d8fd72c9cb75afb5a31ef76ef0f4acf24060f36ff5b3191c840598df2cfd189`
- 热工进阶题库（最终 LF）：`70f7e79195c836cca79fb8e00518917571ee60018fe796b72cee36e9934dbfb3`

本机精确命令、退出码、输出、耗时与日志摘要保存在未发布的 `work/prepublication-release-local/`，汇总为 `summary.json`；原失败分别保留于 `mastery-dom-before-amendment`、`report-revision-before-final-index`、`learning-preservation-before-final-index` 及 `git-filter-mismatch-before` 记录。公开审查结论以本报告和上述专项为准，未将本机工作目录作为必需网站资源。

## 最后课次引用修订已完成验收

13 个文件的 14 处错误课次标签已按专项报告改为主题链接，稳定 ID、测验、数学表达、代码与答案均未改。已将该报告纳入审读依据，随后依次完成最终构建、冻结，再执行 `validate`、`report-revision`、`learning-preservation`、`final-review`、`rendering`、`mastery-dom`、`offline`，全部退出码为 0。再次构建的三个生成物字节相同，359 个冻结源文件与快照一致，137 个受保护文件未变，436 个路径 Git 上传换行一致。上述生成物摘要已更新为此次最后构建值。

本次标签修订不涉及数值，未重复前轮数学及四组进阶题数值复算；表中对应数值检查记录是此前已完成、此次仍适用的结果。此前快照与日志另存于本机 `work/prepublication-release-local/before-order-reference/`，新命令记录和汇总使用本轮结果。课程引用标签已闭环；仍待后续执行的是安卓正式 APK 安装、并存与 JSON 迁移 CI。
