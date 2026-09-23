# 知序 · 理工学习手册

面向初学者、可以持续修订的中文云教材。包含微积分、线性代数、工程热力学、传热学、流体力学、Python 学习和机器学习。

目前为 2026 年 9 月初版：182 节原创课文、每节两道带解析练习和一题概念自测，配有教学示意图与交互实验。正文约 17 万汉字，公式、代码、元数据另计。准确统计见 `site/assets/content-stats.json`。

**覆盖定位：本科核心知识体系与部分高级主题导读。尚未经过外部专业教师逐章审校，不宣称穷尽七个学科所有知识。** 关键工程、科研或考试结论请结合引用资料核验。每科标注结构参考和延伸阅读；本站并非 MIT、Stanford 或北航的官方教材或翻译。

## 直接阅读

公式组件与字体均已包含，无需外部 CDN。建议通过正式网址或下面的本机预览方式阅读；直接打开 `site/index.html` 时，浏览器对本地文件来源、安全策略和剪贴板的处理可能不同：

```sh
python -m http.server 8765 --directory site
```

打开 `http://localhost:8765/`。Windows 用户也可双击 `本地预览.cmd`，然后按照窗口中的网址访问。

## 教材功能

安卓离线 App：[下载 Android 1.0.0 APK](https://github.com/patatohek-boop/zhixu-cloud-textbook/releases/tag/android-v1.0.0)。安装、备份迁移和持续构建说明见 [ANDROID.md](ANDROID.md)。

- 课程书架、分组目录、前后课导航、先修关系与学习路线。
- 全文搜索、公式排版、代码复制、折叠例题解析、即时自测反馈。
- 导数、积分、矩阵、梯度、卡诺热机、导热、冷却、伯努利、回归、梯度下降与 Python 循环等交互实验。
- 手机竖屏阅读、可展开目录、深浅色主题、字号调整、专注模式与打印。
- 本设备学习进度、收藏、笔记、答题记录，以及 JSON 备份导出与合并导入。

学习记录只保存在当前浏览器。不同浏览器、域名和设备不会自动同步。网站没有账户、云端笔记数据库、埋点或广告。换设备或清理浏览器之前，请在“我的学习记录”导出备份。

## 修改课文

所有可编辑正文放在 `content/<课程>/<课文编号>.md`，不是压缩在网页里。

课文顶部 `---json` 与 `---` 之间是 JSON 元数据：标题、分组、学习目标、先修、标签、自测题等。下面是普通 Markdown 正文。

1. 找到课文并修改正文。行内公式写 `$...$`，独立公式写 `$$...$$`。
2. 保留课文的 `id`，这样读者已有记录仍能对应。
3. 新增课文时，复制相邻课文作为格式参考，使用全新编号，再把文件名加入该课程 `course.json` 的 `lessons` 数组；数组顺序就是阅读顺序。
4. 解析可用 `<details><summary>查看解析</summary>`，标签内 Markdown 前后留空行。
5. 提交前运行检查：

```sh
python tools/build.py
node tools/validate.cjs
node tools/test-learning-state.cjs
python tools/security_check.py
```

生成器只使用 Python 标准库。公式检查使用仓库自带的 KaTeX，无需安装 Node 包。正式发布会自动运行同样的校验。

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
site/assets/diagrams/  原创教学示意图
site/assets/vendor/    公式、Markdown、安全过滤组件及其许可
tools/build.py         内容校验与生成
tools/validate.cjs     全部公式与交互模型检查
.github/workflows/     持续校验与自动发布
```

## 维护原则

用小而清晰的更新改善教材：补定义、注明条件、验证单位、重算例题、给出反例、修正图示。新知识点至少应包含“解释—条件—例题—练习—解析”，并记录来源。不要将未写完的目录条目标成完整章节。

更新记录见 [CHANGELOG.md](CHANGELOG.md)，内容审校说明见 [CONTENT_REVIEW.md](CONTENT_REVIEW.md)。第三方组件许可见 [THIRD_PARTY.md](THIRD_PARTY.md) 及对应许可文件。教材内容的后续公开许可由仓库所有者决定。

## 安全与笔记隐私

本次安全检查、修复证据与剩余边界见 [SECURITY_REVIEW.md](SECURITY_REVIEW.md)。笔记与导出备份为明文，不适合保存密码或其他敏感资料，也不要上传到公开仓库。相同 GitHub Pages 用户域名下的其他项目共享浏览器同源存储；不同仓库路径并不能隔离笔记。站点已设置内容安全策略，限制脚本联网和不需要的嵌入功能。

发布组件固定到完整提交版本，升级时应核验官方版本；第三方前端组件升级后需核对官方发行包并更新 `tools/vendor-integrity.json`，不可为通过检查而跳过来源验证。
