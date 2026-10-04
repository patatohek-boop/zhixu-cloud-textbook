---json
{
  "id": "python-14",
  "title": "异常处理与输入契约",
  "group": "03 · 可靠的程序实践",
  "minutes": 35,
  "level": "基础",
  "tags": [
    "异常",
    "契约",
    "健壮性"
  ],
  "objectives": [
    "捕获具体异常",
    "设计失败时的行为",
    "定义异常传播与处理器匹配",
    "区分 try 正常完成、提前离开、异常层级和清理边界"
  ],
  "prerequisites": [
    "python-13"
  ],
  "summary": "把可预期失败表达清楚，避免吞掉错误后产生貌似正常的结果。",
  "quiz": {
    "question": "验证用户输入范围更合适的方法是？",
    "options": [
      "只用 assert",
      "if 检查并抛出明确异常",
      "忽略所有错误",
      "把错误返回为零"
    ],
    "answer": 1,
    "explanation": "输入校验必须稳定执行，且不应将错误伪装为有效零值。"
  },
  "lab": null,
  "revision": "2026-10-04 · 连续正文、定义次序与概念分段复核"
}
---

## 异常与传播
**异常**是执行过程中发出的失败信号对象。发生异常后，当前顺序执行中断，沿调用关系寻找匹配的 `except`；找到后进入处理器，找不到则继续向外传播。正常返回数值零与抛异常是两种不同结果，调用者不能混用。

接口应说明：接受什么输入、成功返回什么、违反哪些条件抛什么异常。例如有效的 0 ℃ 应正常返回数值零，无法解析的文本则应报告失败，不能也用零表示。

## try、except、else 与 finally
```python
events = []
try:
    events.append("try")
    number = int("12")
except ValueError:
    events.append("except")
else:
    events.append("else")
finally:
    events.append("finally")
assert events == ["try", "else", "finally"]
```
将 `"12"` 改成 `"bad"`，`int` 抛 `ValueError`，匹配处理器后得到 try、except、finally；else 不执行。若抛的是未匹配的异常，finally 仍先执行，然后异常向外传播。若在 finally 中 return，可能覆盖原异常或返回值，因此资源清理不应顺便改写计算结果。

`assert` 表达开发时预期成立的内部性质，优化执行可删除它；必须始终执行的输入验证应使用 `if ...: raise ...`。检查函数应明确文本输入的类型：下文 `parse_temperature` 面向字符串，`float(None)` 产生的 `TypeError` 不是被它声明为可恢复的文本格式错误。

## 例：温度文本的解析与校验
外部输入不总是符合预期：用户可能输入“二十”，文件可能不存在，分母可能为零。异常将失败从正常结果中分离，使调用者决定重试、提示、跳过还是终止。异常不等于程序设计失败，无法区分错误与正常数据才更危险。

```python
import math

def parse_temperature(text):
    try:
        value = float(text)
    except ValueError as exc:
        raise ValueError("温度必须是可解析的数值") from exc
    if not math.isfinite(value):
        raise ValueError("温度必须是有限数值")
    if value < -273.15:
        raise ValueError("温度不能低于绝对零度")
    return value

for raw in ["20.5", "abc", "nan"]:
    try:
        print(parse_temperature(raw))
    except ValueError as exc:
        print(f"输入 {raw!r} 无效：{exc}")
```

float 可以接受某些特殊字符串，如 nan，因此“成功转换成浮点数”还不足以证明它是有效温度。代码先检查语法，再检查有限性，最后检查物理范围。这三个检查分别针对文本语法、数值有限性和物理范围。

## 异常捕获范围与清理
只把预期可能失败且需要处理的操作放进 try。捕获过宽的 Exception 并直接 pass，会隐藏拼写错误、逻辑错误甚至资源问题，让后续结果不可信。通常应捕获具体类型，并给出足以定位问题的上下文；若无法合理恢复，就让异常向上传递。raise ... from ... 保留原始原因，兼顾用户提示与调试信息。

else 在 try **正常运行到末尾**时执行；通过 return、break、continue 提前离开也会跳过 else。

### finally 的执行范围

finally 在普通控制流离开 try 时执行，包括异常传播与 return，但进程被强制终止、断电或程序根本未离开无限循环时不能保证清理发生。资源清理通常更适合 with。不要在 finally 中随意 return，因为它可能覆盖原本的返回值或异常。

### 检查与使用之间仍可能变化

检查条件不等于保证条件永远成立，例如先判断文件存在，文件仍可能在打开前被其他程序移走，因此文件打开操作仍需处理异常。

处理器从上到下匹配异常类型及其子类，只进入第一个匹配项；故更具体的 `FileNotFoundError` 应写在 `OSError` 前，否则会被后者接住。

### 业务异常与退出信号

`except Exception` 不包含所有控制性信号，例如 `KeyboardInterrupt`、`SystemExit` 直接属于更上层的 `BaseException` 体系。裸 `except` 连这些也会接住，通常不适合常规业务恢复。

### 继续传播与新的异常

处理异常时单独写 `raise` 可保留当前异常继续向外传播；在 except 或 else 中新出现的异常，不会再被同一个 try 的兄弟 except 接住。这些是[官方异常教程](https://docs.python.org/3/tutorial/errors.html)规定的控制流语义，执行跟踪用于核对理解，不把它们称为数学定理。

## 返回 None 还是抛异常
两者都可能合理，关键是契约明确。查找可选项时返回 None 很自然；输入违反函数前提时抛 ValueError 往往更清晰。不要一会返回数字、一会返回错误文字，迫使调用者猜测结果类型。批量处理时可以分别保存成功记录与错误记录，并报告失败数量，不能默默丢弃异常数据。

assert 适合检查开发时应成立的内部不变量，不宜用作外部输入验证，因为优化模式可以移除断言。真正必须执行的用户输入校验，应使用 if 与明确异常。错误消息应包含预期条件，而非只说“出错了”。

## 错误恢复与报告
单条观测格式错误时，批处理可以记录该行并继续；配置文件缺少必需字段时，继续计算可能没有意义，应尽早终止。两者都使用异常机制，但恢复策略不同。设计接口时应由最了解业务的一层决定如何恢复。
异常信息最好包含操作、位置和预期条件，但不要无节制输出整份私人数据。对学习项目，行号与简短输入摘要常已足够。底层函数可以抛出具体异常，上层把它转成适合用户理解的提示，同时保留调试链。
不要通过返回一个看似正常的默认数值来隐藏失败，除非默认值确有业务定义并被明确记录。缺失、零、失败和未计算是不同状态，混在一起会让后续统计无法解释。

## 练习
1. 为什么不能用 except: pass 处理所有读数转换问题？
<details><summary>查看解析</summary>它会吞掉与数据无关的程序错误，并隐藏丢失的数据。应捕获具体异常、记录行号或输入摘要，并明确处理策略。</details>

2. float("nan") 成功后是否可直接当有效测量？
<details><summary>查看解析</summary>不可以。NaN 是非数值特殊值，应使用 math.isfinite 等检查，再依据数据契约处理。</details>
