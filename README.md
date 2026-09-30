# 知序 · 理工学习手册

面向初学者、可以持续修订的中文云教材。包含微积分、线性代数、工程热力学、传热学、流体力学、Python 学习和机器学习。

当前源码为 2026 年 9 月 30 日 1.3.1 修订版（修正本轮审核确认的 12 项教学与交互问题），共 253 节。保留已有 229 节稳定编号，新增 24 节流动换热仿真专项，流体力学共 62 节。新增 4 个交互实验（共 21 个）、2 张示意图（共 31 张）、六阶段仿真路线与标准库有限体积程序。正文包括定义、通俗解释、假设、推导、案例与解析练习；模型闭合和未执行的三维案例明确标注。统计见 `site/assets/content-stats.json`。

**覆盖定位：本科核心知识体系与部分高级主题导读。尚未经过外部专业教师逐章审校，不宣称穷尽七个学科所有知识。** 关键工程、科研或考试结论请结合引用资料核验。每科标注结构参考和延伸阅读；本站并非 MIT、Stanford 或北航的官方教材或翻译。

## 直接阅读

公式组件与字体均已包含，无需外部 CDN。建议通过正式网址或下面的本机预览方式阅读；直接打开 `site/index.html` 时，浏览器对本地文件来源、安全策略和剪贴板的处理可能不同：

```sh
python -m http.server 8765 --directory site
```

打开 `http://localhost:8765/`。Windows 用户也可双击 `本地预览.cmd`，然后按照窗口中的网址访问。

## 教材功能

在线阅读：[知序云教材](https://patatohek-boop.github.io/zhixu-cloud-textbook/)。逐节变更、课程讲义对照和未展开范围可在[修订与覆盖](https://patatohek-boop.github.io/zhixu-cloud-textbook/#/review)查看。

安卓离线 App：[已发布的正式 APK](https://github.com/patatohek-boop/zhixu-cloud-textbook/releases)。源码版本与已发布版本可能不同，请以发布页的版本号和检查结果为准。安装、备份迁移和持续构建说明见 [ANDROID.md](ANDROID.md)。

- 课程书架、分组目录、前后课导航、先修关系与学习路线。
- [AI × 传热与实验研究路线](https://patatohek-boop.github.io/zhixu-cloud-textbook/#/research)：测量与标定、可辨识性、贝叶斯反演、GP 与多保真、实验设计、PINN、POD、神经算子、热像与可复现项目。
- 六个引导实验连接热模态、冷却反演、Fisher 信息、不确定性区间、物理残差和按实验批次验证；先预测，再分步观察与复算。
- 全文搜索、公式排版、代码复制、折叠例题解析、即时自测反馈。
- 导数、积分、矩阵、梯度、卡诺热机、导热、冷却、伯努利、回归、梯度下降与 Python 循环等交互实验。
- 手机竖屏阅读、可展开目录、深浅色主题、字号调整、专注模式与打印。
- 手机节内目录分层定位具体概念、定义、证明步骤和练习；可点击先修链接补学前置概念。
- 每节公开核对过的概念、证明、具体修改与范围限制，附课程主题映射和参考讲义。
- 本设备学习进度、收藏、笔记、答题记录，以及 JSON 备份导出与合并导入。

学习记录只保存在当前浏览器。不同浏览器、域名和设备不会自动同步。网站没有账户、云端笔记数据库、埋点或广告。换设备或清理浏览器之前，请在“我的学习记录”导出备份。

## 修改课文

所有可编辑正文放在 `content/<课程>/<课文编号>.md`，不是压缩在网页里。

课文顶部 `---json` 与 `---` 之间是 JSON 元数据：标题、分组、学习目标、先修、标签、自测题等。下面是普通 Markdown 正文。

1. 找到课文并修改正文。行内公式写 `$...$`，独立公式写 `$$...$$`。
2. 保留课文的 `id`，这样读者已有记录仍能对应。
3. 新增课文时，复制相邻课文作为格式参考，使用全新编号，再把文件名加入该课程 `course.json` 的 `lessons` 数组；数组顺序就是阅读顺序。
4. 解析可用 `<details><summary>查看解析</summary>`，标签内 Markdown 前后留空行。
5. 同步修改 `reviews/content-audit-2026-09/` 内对应记录和覆盖映射；未来修订可新建目录并修改 `version.json`。提交前运行检查：

```sh
python tools/build.py
node tools/validate.cjs
node tools/test-learning-state.cjs
node tools/test-research-labs.cjs
python tools/verify_fluid.py
python tools/verify_thermal.py
python tools/security_check.py
```

生成器只使用 Python 标准库。公式检查使用仓库自带的 KaTeX，无需安装 Node 包。正式发布会自动运行同样的校验。

数学独立复算工具 `tools/verify_math.py` 需要 SymPy；编程与机器学习的 `tools/verify_computing.py` 需要 NumPy、pandas、Matplotlib、scikit-learn。`tools/test-rendering.cjs` 需要 jsdom，可用环境变量 `ZHIXU_JSDOM_MODULE` 指定安装路径。它们用于核验实例和阅读器，不能代替证明的人工逻辑审查。

## 发布到 GitHub Pages

仓库已包含 `.github/workflows/pages.yml`：向 `main` 提交后，校验教材并发布 `site/`。

第一次发布需要在 GitHub 仓库的 **Settings → Pages → Build and deployment → Source** 中选择 **GitHub Actions**。随后在 **Actions** 中查看 `Validate and publish textbook` 工作流。成功后 Pages 页面会显示正式网址。

项目网站使用相对资源路径与 hash 路由，兼容 `用户名.github.io/仓库名/` 子路径；不需要私钥、数据库或付费服务。GitHub Free 通常要求源仓库公开才能使用 Pages。

如果采用网页上传，请上传解压后的文件和目录，而不是只上传 ZIP 压缩包。更适合持续维护的方法是使用 GitHub Desktop 或 Git。

官方参考：[GitHub Pages 发布流程](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)。

## 目录结构

```text
content/               可维护的课文与课程元数据
site/index.html        网站入口
site/assets/app.js     阅读、搜索与学习记录
site/assets/labs.js    数学与工程交互实验
site/assets/research-guide.js  AI 传热研究路线
site/assets/diagrams/  原创教学示意图
site/assets/vendor/    公式、Markdown、安全过滤组件及其许可
tools/build.py         内容校验与生成
tools/validate.cjs     全部公式与交互模型检查
reviews/              逐节核对记录、公开课程映射与旧编号基线
version.json          网站与离线教材的统一内容版本
.github/workflows/     持续校验与自动发布
```

## 维护原则

用小而清晰的更新改善教材：先严谨定义，再通俗解释；定理先列假设，再写证明，标明每一步所用结论，并给例题、练习与解析。物理经验定律不能包装成数学定理，模型推导应列假设、边界与量纲。编程规则应区分语言保证与实现细节。来源应具体到讲义或章节，不把目录占位、证明思路或高级导读标成完整证明。

逐章修订见 [教学审读报告](reviews/teaching-review-2026-09-28.md)，新增研究方向和可视化见 [AI 传热扩展核对记录](reviews/research-review-2026-09-30.md)。更新记录见 [CHANGELOG.md](CHANGELOG.md)，内容审校说明见 [CONTENT_REVIEW.md](CONTENT_REVIEW.md)。第三方组件许可见 [THIRD_PARTY.md](THIRD_PARTY.md) 及对应许可文件。教材内容的后续公开许可由仓库所有者决定。

## 安全与笔记隐私

本次安全检查、修复证据与剩余边界见 [SECURITY_REVIEW.md](SECURITY_REVIEW.md)。笔记与导出备份为明文，不适合保存密码或其他敏感资料，也不要上传到公开仓库。相同 GitHub Pages 用户域名下的其他项目共享浏览器同源存储；不同仓库路径并不能隔离笔记。站点已设置内容安全策略，限制脚本联网和不需要的嵌入功能。

发布组件固定到完整提交版本，升级时应核验官方版本；第三方前端组件升级后需核对官方发行包并更新 `tools/vendor-integrity.json`，不可为通过检查而跳过来源验证。
