# 安全检查与加固记录

检查日期：2026-09-23。范围：本站源码、静态依赖、学习记录处理、实际 HTTPS 响应和教材仓库的 GitHub Actions / Pages 配置。未对 GitHub 基础设施、用户电脑或所有上游源码进行渗透测试。

本轮未发现可由普通访问者直接利用的高危漏洞、已泄露的访问密钥或三项前端依赖命中的已知漏洞。发现的低风险问题和防护缺口已在本轮修复；这不代表不存在未知漏洞。

## 发现与处理

| 项目 | 实际影响 | 处理 |
| --- | --- | --- |
| 实验路由读取了对象继承属性（低风险） | `#/labs/__proto__`、`#/labs/constructor` 会令当前页面报错；未发现读取或外传资料的能力 | 仅允许实验对象自身存在的编号；异常链接回到实验列表 |
| 本地记录校验不足、备份写入失败仍显示成功（低风险） | 损坏记录可令页面异常；过大备份可能写不进浏览器，原逻辑仍宣称成功 | 白名单规范化；验证、合并和保存全部成功后才替换记录；失败保留原记录 |
| Markdown 在净化后追加公式 HTML（防御加固） | 没有复现普通用户输入导致的 XSS，但后处理可能改变原先安全的 HTML 上下文 | 全部转换结束后统一执行 DOMPurify；公式 `trust:false`；禁止脚本、表单和嵌入对象 |
| 缺少内容安全策略（防御加固） | 浏览器缺少限制异常脚本、联网和嵌入对象的额外防线 | 增加 CSP，限制本站脚本/字体/图片，禁止内联脚本、eval、脚本联网、表单提交、框架与插件；增加不发送 Referer 的策略 |
| 发布组件引用可变标签（供应链加固） | 上游标签被移动可能使发布过程运行不同代码 | 5 个官方 Actions 固定为已核验的完整提交 SHA；checkout 不保留 Git 凭据；只有 main 可部署 |

## 已完成验证

- 原仓库 296 个受版本管理文件的常见私钥、GitHub/AWS/OpenAI 令牌和带密码 URL 模式检查无命中；不等同于识别所有形式的秘密。
- GitHub 密钥扫描和推送保护已启用；检查时无待处理的密钥扫描告警。工作流默认只读，不能批准 PR；PR 构建不能进入部署作业。
- KaTeX 0.18.7、Marked 18.0.14、DOMPurify 3.4.15 共 67 个发行文件与 npm 官方包逐字节一致；发行包 SHA-512 与已记录 SHA-256 均一致。
- 按三个精确版本查询 OSV，均无匹配漏洞。第三方组件检查是当日快照，未来仍需关注公告。
- 7 组状态/备份/路由边界测试通过，包括非法键、null/数组记录、超大备份、存储配额失败和原笔记保留。
- 在 jsdom 30.1.1 中检查 12 组 HTML、SVG、MathML、URL、公式上下文恶意输入；未保留可执行脚本/事件处理器/危险协议链接。该测试不模拟浏览器 CSP 的全部行为。
- 全部 182 节内容的 1,265 条公式在最终净化之后仍可渲染；笔记中的 HTML 被显示为纯文本；实验和自测正常。
- 实际浏览器检查：加固后的课文、34 个公式、示意图与滑块正常，未记录脚本或 CSP 错误。
- CI 增加状态安全测试、CSP/发布权限检查、课程元数据检查，以及 68 项 vendor 文件（含版本清单）的完整性检查。

## 仍然存在的边界

1. **学习笔记是浏览器本地明文。** 同一 `patatohek-boop.github.io` 域名下的其他项目共享同源存储边界，仓库路径不形成隔离。本站没有上传笔记的代码，但同源的不可信网站或恶意浏览器扩展可能读取它们。不要在笔记或备份中保存密码、令牌、身份证件等敏感资料；备份也不要提交到公开仓库。参见 [浏览器同源存储规则](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage)。
2. **仓库及网站公开。** 课文和源码对外可读；GitHub 仍可能记录常规访问日志。GitHub 凭据不包含在网页或仓库中。
3. **main 尚未配置分支保护。** 有写入权限的账号可以直接更改并发布网站；网站无法阻止仓库拥有者账号被接管。为保持单人更新流程，本轮没有开启会阻止直接更新的强制审核规则。账户双重验证状态不在本次检查范围内。
4. **部分响应头受 GitHub Pages 托管限制。** 已观察到 HTTPS 与 HSTS；没有 `X-Frame-Options` / `frame-ancestors` 响应头，因此未宣称完全防止他站嵌入。`frame-ancestors` 不能用 HTML meta 生效，不能通过添加无效配置解决。若未来增加敏感操作，可采用支持自定义响应头的独立域名/托管。参见 [frame-ancestors 限制](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/frame-ancestors)。
5. 为 KaTeX 和动态布局保留内联样式权限，但未开放内联脚本或 eval。`script-src 'self'` 不是同源代码被篡改后的保护罩；文件哈希检查也不能替代上游漏洞维护。
6. 当前 vendor 组件没有自动升级；GitHub 依赖告警未启用，且静态复制的组件不能只靠常规包管理器扫描识别。更新时需核验官方公告、精确版本与完整性记录，不能把“当前无告警”理解为长期安全保证。

## 维护者复核

基础检查不需要下载依赖：

```sh
python tools/build.py
node tools/validate.cjs
node tools/test-learning-state.cjs
python tools/security_check.py
```

可选的 DOM 安全/排版回归仅用于开发，不发布到站点：在临时测试目录安装 `jsdom@30.1.1`（禁用安装脚本），将环境变量 `ZHIXU_JSDOM_MODULE` 指向其绝对模块路径，再运行 `node tools/test-rendering.cjs`。

官方依据：[DOMPurify 后处理注意事项](https://github.com/cure53/DOMPurify#is-there-any-foot-gun-potential)、[GitHub Actions 供应链防护](https://docs.github.com/en/actions/reference/security/secure-use#using-third-party-actions)、[CSP 说明](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy)。本轮核对的近期公告：[KaTeX](https://github.com/KaTeX/KaTeX/security/advisories/GHSA-238p-pmpm-9mq7)、[Marked](https://github.com/markedjs/marked/security/advisories/GHSA-6v9c-7cg6-27q7)、[DOMPurify](https://github.com/cure53/DOMPurify/security/advisories/GHSA-55q2-fjhq-7xh7)。
