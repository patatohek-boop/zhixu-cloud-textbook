# 网页验收中惰性加载图片测试的修正

日期：2026-10-04。范围仅为 `tools/qa/learning-ui.spec.cjs` 的图片测试前置动作；未修改教材、应用、部署工作流或任何验收阈值。

## 已观察到的失败

PR 12 的 head `c085ea46ee39d7a85c5dd977ba1fd0ad15bb54b6`：

- [内容验收 37152859758](https://github.com/patatohek-boop/zhixu-cloud-textbook/actions/runs/37152859758) 通过，PR 的 deploy 按条件跳过。
- [界面验收 37152859752](https://github.com/patatohek-boop/zhixu-cloud-textbook/actions/runs/37152859752) 中，前置数值与 4 个 DOM 命令通过；Chromium 36 个案例中 30 通过、6 失败。
- 六个失败都在原测试第 128 行：320、360、390、768、1165、1440 像素下直接断言 `learn-thermodynamics-05.svg` 可见，10 秒后收到 `hidden`。该图为正文例题插图，标记 `loading="lazy"`，不在折叠答案内；测试此前没有滚动到图。
- 失败截图及 trace 的 artifact ID 为 `11284568069`；完整报告为 `11285046757`，均对应上述 head。

## 最小修正

复用同文件现有保留插图验收采用的实际阅读顺序：先将图所在的 figure 滚入视区，再等待图片 `complete && naturalWidth > 0`，然后滚动图片并继续原有可见性检查。保留原定位目标、所有题图、六个屏幕宽度，以及点击放大、至少 14 像素标注、缩放按钮、无横向溢出、关闭后焦点、路由和键盘操作断言。

这修正的是惰性加载所需的测试前置动作；没有强制改变图片 loading 属性、注入图片内容、打开无关折叠、删除断言或增加超时。是否解决云端失败仍应由提交后的真实浏览器 CI 确认，不能由语法检查替代。

## 已完成检查与快照边界

- `node --check tools/qa/learning-ui.spec.cjs` 通过。
- 精确比较确认，除上述一处插入，测试的所有原字符内容均保留；六宽度配置未改。
- 当前 reader 清单的 359 个 `reviewed_files` 不包含这个测试文件；逐文件 SHA-256 仍全部匹配现有快照。因此无需因这次纯测试修订更新教材冻结清单。本次没有运行 build 或 freeze。
- 测试文件 SHA-256：修订前 `ee7b1d6a3c7fec78c6ba10582a3bf7366d64d527496c81e9470722054365729a`；修订后 `bdf9afa5200e7f885354a8e25c6ea003a947780faef6257c98c171ff55ab342d`。

本次仅修改测试与本记录，等待主任务提交后重跑 CI；没有将旧的失败结果记作通过。
