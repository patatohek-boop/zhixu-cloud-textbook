---json
{
  "id": "python-25",
  "title": "完整项目：实验记录分析器",
  "group": "06 · 综合实践与进阶路线",
  "minutes": 40,
  "level": "进阶",
  "tags": [
    "项目",
    "CSV",
    "复现"
  ],
  "objectives": [
    "完成端到端分析流程",
    "保留无效记录的解释",
    "定义记录契约与失败分区"
  ],
  "prerequisites": [
    "python-24"
  ],
  "summary": "把读取、验证、计算和输出连成一个可独立运行的小项目。",
  "quiz": {
    "question": "本项目将无效温度如何处理？",
    "options": [
      "作为零参与平均",
      "保存错误行号与原因",
      "自动猜测正确值",
      "删除整个报告"
    ],
    "answer": 1,
    "explanation": "无效记录与有效数据分开报告，避免污染统计。"
  },
  "lab": null,
  "revision": "2026-09-28 · 概念分段、教学先修与练习复核"
}
---

## 在写程序前写完整的输入输出契约
输入为 CSV 文本，列名和顺序严格为 `sensor,temp_c`；一条逻辑记录表示一次观测，名称去除两侧空白后须非空，温度须可解析、有限且不低于 −273.15°C。

### 成功与失败的输出

无效记录进入错误列表，不参与均值；表头不合约定则整个任务失败。输出按名称排序，每组包含有效数量及算术均值，并另报错误位置和原因。

这里允许同一设备多次出现，不把相同数值自动去重；它不检查传感器校准，也不判断温度是否适合某种真实设备。通俗地说，程序负责按一份明确的登记规则做账，不能替代实验设计。

## 数据流不变量与终止
处理完前 k 个已解析逻辑记录后，保持：

- 每个有效记录的数值恰好出现在其设备组一次；
- 每个违反内容契约的记录恰好出现在错误列表一次；
- 所有组的长度之和加错误条数等于 k。

初始化为空成立。每轮校验成功才追加，失败则只记录错误，两条路径互斥且覆盖本例声明的内容失败，因此保持不变量；有限输入遍历结束后，输出 count 正好等于每组有效观测数。均值公式的分母从组长度取得，非空组保证没有除零。

CSV 语法损坏、资源耗尽等不属于“逐条内容错误”的恢复承诺，不能用捕获所有异常掩盖。

### 逻辑记录与物理行

字段可能嵌入换行，下文已用解析器的 `line_num` 报告该记录**结束所在的物理行号**，不能再把枚举记录号冒称精确文件行号。

## 项目目标与边界
我们要从 CSV 文本读取温度记录，检查字段，按传感器统计有效样本数与平均温度，并报告异常行。一个输入行表示一次观测，温度单位固定为摄氏度。项目只使用标准库，运行时无需联网；示例使用内嵌小数据，便于复制后直接验证。真实设备的安全判定与传感器校准不在本项目范围内。

```python
import csv
import io
import json
import math
import statistics

def analyze(text):
    groups = {}
    errors = []
    reader = csv.DictReader(io.StringIO(text))
    if reader.fieldnames != ["sensor", "temp_c"]:
        raise ValueError("表头必须为 sensor,temp_c")
    for row in reader:
        line_no = reader.line_num
        try:
            if None in row or any(value is None for value in row.values()):
                raise ValueError("列数与表头不一致")
            sensor = row["sensor"].strip()
            value = float(row["temp_c"])
            if not sensor or not math.isfinite(value):
                raise ValueError("名称为空或读数非有限")
            if value < -273.15:
                raise ValueError("低于绝对零度")
            groups.setdefault(sensor, []).append(value)
        except (ValueError, TypeError, AttributeError) as exc:
            errors.append({"line": line_no, "reason": str(exc)})
    summary = [
        {"sensor": sensor, "count": len(values),
         "mean_c": statistics.mean(values)}
        for sensor, values in sorted(groups.items())
    ]
    return {"summary": summary, "errors": errors}

def main():
    text = "sensor,temp_c\nA,20\nA,22\nB,24\nB,invalid\n"
    report = analyze(text)
    assert report["summary"][0]["mean_c"] == 21.0
    assert len(report["errors"]) == 1
    print(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False))

if __name__ == "__main__":
    main()
```

## 逐步读懂数据流
DictReader 把每行转成按表头命名的字典。程序先检查表头契约，避免错误列名一路传播。

### 逐条校验与分组

每条记录单独解析并验证，合格值进入对应传感器列表；异常记录只保存行号与原因，不伪装成零度。

### 稳定输出与检查

最后按传感器名称排序，生成稳定输出，便于人工检查与版本比较。

均值使用标准库 `statistics.mean`。输入均为有限数，不代表直接求和也不会溢出：两个 `1e308` 的均值可表示为 `1e308`，但先用 `math.fsum` 求和会溢出。`fsum` 改善求和精度，并不扩展浮点数的范围；这里用 `mean` 避免该中间求和溢出。结果仍是有限精度数值，不能据此认为计算没有舍入误差。

预期 A 有两个有效值，均值为 21；B 有一个有效值，均值为 24；第 5 行被记录为无效。错误数量是报告的一部分，使用者应先看到数据损失，再解释平均值。这里使用 CSV 解析器的 line_num，记录的是该逻辑记录结束所在的物理行号；多行字段的起点需要另外记录。

## 如何继续工程化
下一步把输入换为 pathlib 读取文件，用 argparse 指定输入与输出路径，把函数放到模块，并用 unittest 检查空输入、缺列、空名称、NaN 和正常记录。大型数据不必保存每组全部读数，可采用经过溢出与精度分析的在线均值算法；不能直接假定累计和总能表示；若还要方差，应采用数值稳定的在线算法。

当前版本对字段顺序要求严格，且没有时间戳、重复观测识别或单位转换。它们是明确的扩展方向，不是已经实现的能力。先把小项目的契约与测试稳定下来，再加新功能，维护成本会更可控。课程中的程序应被当作可验证的学习对象，而不是未经验证直接控制真实设备的软件。

## 从示例走向用户输入
若把内嵌文本换成真实文件，先保留 analyze 作为纯处理函数，再增加薄的文件读取层。文件读取错误与记录内容错误应分开报告：前者可能使整个任务无法开始，后者可以按本项目规则逐条记录。
程序同时校验每行字段数，避免额外列被悄悄忽略。CSV 解析器会把多出的字段放在特殊键下，缺少字段则可能得到空值，因此严格格式明确拒绝这两种情况。温度上下界、重复记录和允许的传感器名称也应由任务契约决定，不能凭代码作者随意猜测。
对于连续采集项目，加入时间戳后再计算平均，需要说明是观测等权还是时间加权。采样间隔不一致时，二者可能不同。把统计定义写进输出元数据，比仅显示一个平均数更可追溯。
完成后请用一份全新环境从头运行，核对示例输出与错误计数。能在作者已有环境中运行只是第一步，清楚的依赖和入口才让别人能够接续维护。

## 练习
1. 若增加一行 A,24，A 的 count 和 mean_c 应是多少？
<details><summary>查看解析</summary>count 为 3，mean_c 为 (20+22+24)/3=22。可将此场景加入测试。</details>

2. 为什么错误行不能填成零再参与平均？
<details><summary>查看解析</summary>零是有效温度，替换会制造并不存在的观测并拉低均值。应保留错误信息，按事先定义的规则处理。</details>

### 练习三：只改一项规格，先写出会失败的测试

把本章分析器另存为一个练习版本，保留原版作为对照。新需求是：在原有每个传感器的 `count`、`mean_c` 旁增加 `high_count`，统计**有效温度中不低于阈值**的条数。函数签名改为 `analyze_with_threshold(text, *, threshold_c=22.0)`；阈值单位℃，题设输入为有限float，非有限阈值须报 `ValueError`。高于阈值仍是有效读数，必须继续参与原来的总数和均值。其他CSV、物理行号、无效记录与排序规则不变。

先用下面输入写测试，再修改实现。不要先运行程序，把期望值从原始记录手算出来：

```text
sensor,temp_c
A,20
A,22
B,0
B,invalid
A,24
C,NaN
```

1. 默认阈值22 ℃下，A、B的count、mean_c、high_count及错误行号各是多少？C是否应该出现在有效汇总中？
2. 阈值改成0 ℃时，如何证明有效零没有被当缺失？只有表头没有数据、表头顺序错误和阈值NaN各该怎样处理？
3. 说明原版为什么未满足新增测试；若把“不低于”误写成 `>`，哪一个边界测试能抓住它？

<details><summary>查看完整解析、可运行改造与失败解释</summary>

A的有效值是20、22、24 ℃，count=3、mean_c=22 ℃、high_count=2；B只有有效0 ℃，count=1、mean_c=0 ℃、high_count=0。第5、7物理行无效，C没有有效读数，不能凭NaN建立一个平均为零的组。阈值改为0 ℃时，A的high_count=3，B的high_count=1。空数据应返回两个空列表，错误表头应使整个任务失败，非有限阈值也应在处理记录前使任务失败。

最小改动是保存原来的有效分组，在汇总每组时对同一批有效值数达标数量；不要为计算high_count另建一套放宽校验的读取流程。下段代码可单独保存运行，只依赖标准库：

```python
import csv
import io
import math
import statistics

def analyze_with_threshold(text, *, threshold_c=22.0):
    # Contract: threshold_c is a float in degC; nonfinite thresholds are rejected.
    if not math.isfinite(threshold_c):
        raise ValueError("阈值必须有限")
    groups, errors = {}, []
    reader = csv.DictReader(io.StringIO(text))
    if reader.fieldnames != ["sensor", "temp_c"]:
        raise ValueError("表头必须为 sensor,temp_c")
    for row in reader:
        line_no = reader.line_num
        try:
            if None in row or any(value is None for value in row.values()):
                raise ValueError("列数与表头不一致")
            sensor = row["sensor"].strip()
            value = float(row["temp_c"])
            if not sensor or not math.isfinite(value):
                raise ValueError("名称为空或读数非有限")
            if value < -273.15:
                raise ValueError("低于绝对零度")
            groups.setdefault(sensor, []).append(value)
        except (ValueError, TypeError, AttributeError) as exc:
            errors.append({"line": line_no, "reason": str(exc)})
    summary = []
    for sensor, values in sorted(groups.items()):
        summary.append({"sensor": sensor, "count": len(values),
                        "mean_c": statistics.mean(values),
                        "high_count": sum(value >= threshold_c for value in values)})
    return {"summary": summary, "errors": errors}

text = "sensor,temp_c\nA,20\nA,22\nB,0\nB,invalid\nA,24\nC,NaN\n"
report = analyze_with_threshold(text)
assert report["summary"] == [
    {"sensor": "A", "count": 3, "mean_c": 22.0, "high_count": 2},
    {"sensor": "B", "count": 1, "mean_c": 0.0, "high_count": 0},
]
assert [error["line"] for error in report["errors"]] == [5, 7]
assert all(error["reason"] for error in report["errors"])
zero_threshold = analyze_with_threshold(text, threshold_c=0.0)
assert [row["high_count"] for row in zero_threshold["summary"]] == [3, 1]
assert analyze_with_threshold("sensor,temp_c\n") == {"summary": [], "errors": []}
for bad_text, threshold in [("temp_c,sensor\n20,A\n", 22.0),
                            ("sensor,temp_c\nA,20\n", float("nan"))]:
    try:
        analyze_with_threshold(bad_text, threshold_c=threshold)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
print(report["summary"])
print("invalid end lines:", [error["line"] for error in report["errors"]])
print("all checks passed")
```

预期第一行是两个字典组成的列表，与断言中的A/B结果一致；第二行为 `invalid end lines: [5, 7]`，最后为 `all checks passed`。错误信息的具体英文措辞可能随Python版本变化，因此关键断言核对行号与原因非空，不依赖转换异常的某一条英文原文。`sum(条件 for ...)` 是[推导式/生成器](#/course/python/python-10)的用法，True计1、False计0；这里数的是事件次数，不是把温度数值相加。

原版没有 `high_count` 字段，按新增规格访问它会得到 `KeyError`。这说明旧程序不满足**新需求**，不表示旧规格下的均值计算错误。改成严格 `>` 的版本会漏掉A的22 ℃，得到high_count=1；默认测试要求2，能直接抓住端点错误。若只测试20和24，就发现不了这一错误。

易错点：不能把达标值从均值组中移除；不能把invalid或NaN填零；不能用温度的真假判断筛掉0 ℃。自查：每组high_count应在0与count之间（含端点）；改变阈值只应改变high_count，不能改变有效count、mean_c或错误列表。题设未承诺验证任意阈值类型、CSV语法损坏或资源耗尽，真实接口需要另定这些策略。数据解析和物理行号语义可核对[Python csv.DictReader](https://docs.python.org/3/library/csv.html#csv.DictReader)与[reader.line_num](https://docs.python.org/3/library/csv.html#csv.csvreader.line_num)。

</details>
