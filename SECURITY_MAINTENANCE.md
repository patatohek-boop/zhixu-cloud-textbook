# 安全维护与更新

公开仓库允许别人查看、复制源码和提出修改建议，并不自动赋予他们修改本仓库的权限。下面是今后的维护流程；本文不代表已核验账号的双重验证状态。

## 更新教材和网页

1. 从最新的 `main` 创建一个新分支，在新分支中修改教材或程序。
2. 提交修改后，创建合并到 `main` 的 Pull Request（简称 PR，即修改申请）。
3. 等待 **Textbook validation** 检查通过；若检查失败，先修正问题。若提示分支落后于 `main`，先更新分支，再等待检查。
4. 查看修改内容，确认无误后自行合并 PR。合并到 `main` 后，网站发布流程会更新网页。

单人维护时，PR 不要求第二个人批准，自己可以在检查通过后合并。不要为了绕过失败的检查而临时关闭保护，也不要强制覆盖或删除 `main`。自动检查能发现部分问题，不能替代对教材内容和修改的核对。

## 发布安卓 APK

1. 按 [安卓维护说明](ANDROID.md) 构建新版，使用本机保存的原签名密钥签名，并核验签名与文件校验值。
2. 在 GitHub 创建新版本的 **Draft release（发布草稿）**，选择正确的源码提交和版本标签。
3. 将已签名的正式 APK 和对应的 SHA-256 校验文件上传到草稿；核对版本、文件、校验值及发布说明。
4. 确认全部附件齐全后，再发布草稿，并检查发布页面显示 **Immutable（不可变）**。

不可变发布后，附件不能增加、替换或删除；在该发布仍存在时，关联标签不能移动或删除。标题和发布说明仍可编辑。发现需要修正的安装包时，应发布新版本。不要先发布空版本再补传 APK。

**现有 Android 1.0.0 不会因启用此设置而追溯锁定。**后续发布按上述流程进行，不能把旧版本描述为已受到不可变保护。

## 保管账号、密钥和学习记录

- 在 GitHub 的账号安全设置中自行启用双重验证，用手机上的验证器或自己控制的安全验证方式完成设置。恢复码应私下妥善保存，避免仅保存在唯一一部手机上；不要发到聊天或公开仓库。
- 安卓签名密钥、签名口令、GitHub 令牌、私人笔记和笔记备份都不要上传到仓库、PR、Issue 或 Release。签名密钥需要单独安全备份，否则将来可能无法正常覆盖安装新版。
- 合并别人的 PR 前，特别检查程序、构建流程和依赖的改动；不要因自动检查通过就直接信任陌生人的修改。

仓库管理员仍可以更改保护设置；账号、授权令牌或本机失守仍可能影响安全。这些设置可以降低误操作和篡改风险，不构成绝对防盗保证。

参考：[GitHub 分支保护](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)、[不可变发布](https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases)、[不可变设置只影响后续发布](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/establish-provenance-and-integrity/prevent-release-changes)。
