---json
{
  "id": "python-13",
  "title": "CSV、JSON 与数据交换",
  "group": "03 · 可靠的程序实践",
  "minutes": 20,
  "level": "基础",
  "tags": [
    "CSV",
    "JSON",
    "校验"
  ],
  "objectives": [
    "读取 CSV 记录",
    "解释 JSON 类型限制"
  ],
  "prerequisites": [
    "python-12"
  ],
  "summary": "用标准格式保存结构化记录，避免手工拆分和无意的数据类型损失。",
  "quiz": {
    "question": "解析成功意味着什么？",
    "options": [
      "数据单位一定正确",
      "格式语法有效，但仍需语义校验",
      "记录一定无缺失",
      "可以忽略字段定义"
    ],
    "answer": 1,
    "explanation": "语法解析与数据语义校验是两个不同步骤。"
  },
  "lab": null
}
---

## 表格和树状结构
CSV 适合行列记录，JSON 适合字典、列表与标量组成的嵌套结构。格式选择取决于数据形状和交换对象。扩展名只是约定，真正重要的是字段定义、单位、缺失规则与编码。相同的“temperature”字段若一份表示摄氏度、一份表示开尔文，语法完全合法也会造成科学错误。

```python
import csv
import io
import json

text = 'sensor,temp_c\n"A, north",20.5\nB,21.0\n'
rows = []
for row in csv.DictReader(io.StringIO(text)):
    rows.append({"sensor": row["sensor"], "temp_c": float(row["temp_c"])})
payload = {"schema_version": 1, "measurements": rows}
encoded = json.dumps(payload, ensure_ascii=False, allow_nan=False)
restored = json.loads(encoded)
print(restored["measurements"][0]["sensor"])  # A, north
```

名称中含逗号，但被引号包围，所以是一列内容。csv 模块理解这些规则，普通 split(",") 则会把一条记录拆错。DictReader 用表头作为键，读出的数值仍是字符串，必须按字段契约转换。读取真实 CSV 文件时通常使用 `newline=""`，让 csv 模块正确处理换行。

## 类型变化要明确
JSON 支持对象、数组、字符串、数值、布尔值和 null，不直接支持 Python 集合、日期对象或任意类实例。Python 的 None 对应 JSON 的 null。JSON 对象的键是字符串；把数字作为 Python 字典键导出再读回，键的类型可能改变。日期应制定一致格式，必要时附带时区；不要让不同读者猜测“09/10”是哪一天。

标准 JSON 不接受 NaN 和无穷大。本例设置 allow_nan=False，遇到这类值会报错，促使我们先定义缺失和异常处理策略，而不是生成某些读取器无法接受的文件。ensure_ascii=False 让中文保持可读，不影响其应当使用 UTF-8 保存的约定。

## 校验比解析多一步
解析成功只说明格式符合语法，不说明数据满足业务规则。应验证必需字段、数值范围、唯一键、单位和记录粒度。例如传感器名称不能为空，温度需有限，时间戳需能排序。用 schema_version 标记格式版本，未来增加字段或调整结构时，旧程序就有机会识别并迁移，而不是静默误解。

不要用 eval 读取 JSON；不要把 pickle 当作不可信来源的数据交换格式，因为反序列化可能执行代码。CSV 和 JSON 本身也需要大小限制与字段校验，但它们更适合开放的数据交换。输出文件应连同数据字典保存：一行是什么、每列是什么、缺失怎么表示。

## 为交换格式写数据字典
数据字典至少包含字段名、含义、类型、单位、允许范围和缺失表示。例如温度字段允许有限浮点数，空字符串表示缺失，而零度仍是有效观测。接收方据此实现验证，双方才真正共享同一种数据含义。
数字标识符不一定是数值。邮编、设备编号或带前导零的批次号应经常保持字符串，否则转换后可能丢失身份信息。时间字段还需说明时区和精度，单写一个日期格式并不足以表达瞬时测量。
格式升级时可添加新字段并保留旧字段含义，或显式提高版本并提供迁移说明。不能在字段名不变时悄悄把摄氏度改成开尔文。交换格式的稳定性来自语义契约，而不仅是文件能被打开。

## 练习
1. CSV 字段中含逗号时，为什么不能简单 split？
<details><summary>查看解析</summary>CSV 允许引号包围含分隔符的字段。split 不理解引号和转义，会错误增加列数；应使用 csv 解析器。</details>

2. 读入 JSON 后记录缺少 temp_c，能直接当作零吗？
<details><summary>查看解析</summary>不能。缺失与测得零度含义不同，应根据数据契约报错、标记缺失或采用有依据的处理规则。</details>
