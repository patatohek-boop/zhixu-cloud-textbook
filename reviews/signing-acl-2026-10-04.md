# Windows 签名备份目录权限复核

本次仅使用临时目录和内容为“synthetic”的文件验证权限代码，没有读取真实签名密钥或口令。

旧实现先移除继承，再以 `icacls /grant:r` 为允许主体授权。这不会删除其他主体已有的显式访问规则。合成测试确认：目录和既有受保护文件中预置的 Everyone 读权限仍会残留；Windows 上的 `chmod` 不能弥补这一点。

新版对专用备份目录及其中每个普通文件重建精确DACL。允许主体仅为运行账号、明确传入的已核验人类账号SID、SYSTEM。文件使用直接授权，目录使用可向新建文件传递的授权。应用后重新读取安全描述符，逐条确认主体、FullControl、Allow、继承/传播标志、继承保护以及原owner/group未变。创建签名文件后再次执行同样的检查。

读取和常规设置采用 Get-Acl/Set-Acl。在当前受限Windows账号下，Set-Acl对既有受保护文件会请求本任务不需要的SeSecurityPrivilege；仅对此特定异常，使用.NET的DACL写入路径，写入同一个只标记DACL为已修改的对象，不请求额外权限，不改owner、group或SACL，再执行完全相同的结果核验。其他失败直接终止，不输出凭据或外部命令的敏感输出。

使用实际已核验的人类账号SID，已验证：

- 目录、已有文件、新建文件的最终DACL均精确包含三个允许主体，Everyone规则消失。
- 人类账号访问保留；没有遗留其他显式规则或继承规则。
- 重复调用结果不变。
- 格式错误的SID被拒绝；不遍历意外子目录或重解析点。

这项检查验证权限处理函数，不等于已完成正式APK签名、设备安装或升级验收。签名身份仍须由证书摘要校验，具体APK仍须单独验收。

微软的[Set-Acl文档](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.security/set-acl)说明该命令按给定安全描述符设置目标；[PowerShell问题21095](https://github.com/PowerShell/PowerShell/issues/21095)记录其在受限账号下比较owner/group/SACL的回退路径。本机的具体异常和DACL写入结果来自上述合成测试，不将该历史问题当作本机所有失败的唯一原因。
