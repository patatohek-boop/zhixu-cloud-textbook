---json
{
  "id": "python-25",
  "title": "完整项目：实验记录分析器",
  "group": "06 · 综合实践与进阶路线",
  "minutes": 25,
  "level": "进阶",
  "tags": [
    "项目",
    "CSV",
    "复现"
  ],
  "objectives": [
    "完成端到端分析流程",
    "保留无效记录的解释"
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
  "lab": null
}
---

## 项目目标与边界
我们要从 CSV 文本读取温度记录，检查字段，按传感器统计有效样本数与平均温度，并报告异常行。一个输入行表示一次观测，温度单位固定为摄氏度。项目只使用标准库，运行时无需联网；示例使用内嵌小数据，便于复制后直接验证。真实设备的安全判定与传感器校准不在本项目范围内。

```python
import csv
import io
import json
import math

def analyze(text):
    groups = {}
    errors = []
    reader = csv.DictReader(io.StringIO(text))
    if reader.fieldnames != ["sensor", "temp_c"]:
        raise ValueError("表头必须为 sensor,temp_c")
    for line_no, row in enumerate(reader, start=2):
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
         "mean_c": math.fsum(values) / len(values)}
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
DictReader 把每行转成按表头命名的字典。程序先检查表头契约，避免错误列名一路传播。每条记录单独解析并验证，合格值进入对应传感器列表；异常记录只保存行号与原因，不伪装成零度。最后按传感器名称排序，生成稳定输出，便于人工检查与版本比较。

预期 A 有两个有效值，均值为 21；B 有一个有效值，均值为 24；第 5 行被记录为无效。错误数量是报告的一部分，使用者应先看到数据损失，再解释平均值。这里的行号按简单单行 CSV 记录计数；若允许字段中嵌入换行，需要利用解析器实际行号制定更准确的定位策略。

## 如何继续工程化
下一步把输入换为 pathlib 读取文件，用 argparse 指定输入与输出路径，把函数放到模块，并用 unittest 检查空输入、缺列、空名称、NaN 和正常记录。大型数据不必保存每组全部读数，可维护数量与累计和；若还要方差，应采用数值稳定的在线算法。

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
