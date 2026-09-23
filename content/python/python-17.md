---json
{
  "id": "python-17",
  "title": "数据类、类型注解与接口",
  "group": "04 · 抽象与工程基础",
  "minutes": 20,
  "level": "进阶",
  "tags": [
    "dataclass",
    "类型注解",
    "接口"
  ],
  "objectives": [
    "使用 dataclass",
    "理解类型提示不自动验证"
  ],
  "prerequisites": [
    "python-16"
  ],
  "summary": "让记录结构可读，让工具协助发现类型错误，并保留运行时校验。",
  "quiz": {
    "question": "类型注解的正确理解是？",
    "options": [
      "自动保证所有输入有效",
      "描述接口并支持静态检查",
      "自动检查物理单位",
      "使程序无需测试"
    ],
    "answer": 1,
    "explanation": "注解不是完整运行时验证，也不能代替测试和科学假设检查。"
  },
  "lab": null
}
---

## 给数据一份明确说明
当对象主要用来保存一组有名字的字段时，dataclass 可以减少初始化和打印等重复代码。类型注解说明接口意图，让编辑器和静态检查工具提前发现部分错误。它像容器上的标签，告诉读者预期装什么；默认情况下，它不会自动拦住所有不符合标签的物品。

```python
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class Measurement:
    sensor: str
    temperature_c: float

    def __post_init__(self):
        if not self.sensor:
            raise ValueError("传感器名称不能为空")
        if not math.isfinite(self.temperature_c):
            raise ValueError("温度必须有限")

def average(items: list[Measurement]) -> float:
    if not items:
        raise ValueError("至少需要一条记录")
    return sum(item.temperature_c for item in items) / len(items)

records = [Measurement("A", 20.0), Measurement("B", 22.0)]
print(average(records))  # 21.0
```

dataclass 根据字段生成常用方法，frozen=True 阻止通常的字段重新赋值，有助于表达不可变记录。但它不是深层冻结：若字段是列表，列表内部仍可能改变。__post_init__ 在初始化后执行，可用于检查跨字段约束；类型错误仍可能在这里或其他操作处暴露。

## 注解与验证的分工
`list[Measurement]` 表示预期为 Measurement 组成的列表，`-> float` 表示返回浮点数。Python 3.10 起可用 `float | None` 表达数值或缺失。静态检查工具在不执行程序的情况下分析类型关系，但无法自动证明所有数据范围、单位与科学假设正确。用户输入仍应在边界显式解析和校验。

类型注解不应伪装确定性。一个函数可能返回 None，就要在注解和调用处处理；不要为了通过检查而随意使用 Any 或强制转换。类型别名可改善复杂结构的可读性，Protocol 可描述一组所需行为，适合后续学习。本课目标是读懂和写出简单接口，而非掌握完整类型系统。

## 接口稳定性的价值
一旦其他代码依赖字段名称和函数参数，改名就可能影响调用者。把数据结构、单位和可选字段写清楚，能减少维护成本。更新接口时考虑提供迁移步骤，或使用版本化格式。数据类只是表达方式，真正的可靠性来自稳定契约、验证和测试。

默认可变字段应使用 `field(default_factory=list)`，让每个实例获得独立列表。不要把列表直接写成共享默认值。对于只需要少量字段的临时记录，字典也很合适；选择数据类的理由应是结构稳定、需要具名访问和工具支持，而非语法更“高级”。

## 类型与物理意义仍是两层
温度和压力都可能注解为浮点数，但二者不能随意相加。类型系统能发现部分结构错误，却未必理解单位。可通过变量命名、专门记录类型或单位库进一步表达含义，复杂度应与项目风险相匹配。
类型注解还帮助发现缺失分支：若函数可能返回记录或空值，调用者必须先判断，再访问字段。把所有结果写成同一个宽泛类型，虽然减少检查提示，却也失去提前发现错误的机会。
为数据类添加字段时，注意默认值、构造方式和序列化格式的兼容性。公开接口的变化需要同步更新示例、测试和文档。结构更明确后，维护者才能在不阅读全部实现的情况下判断一处修改会影响哪里。

## 练习
1. 写了 `age: int` 后，运行时一定拒绝字符串吗？
<details><summary>查看解析</summary>默认不会。类型注解供工具和读者使用，运行时验证仍需显式代码或专门验证工具。</details>

2. frozen=True 的对象包含列表字段时，列表内容一定无法修改吗？
<details><summary>查看解析</summary>不一定。冻结主要阻止字段重新绑定，内部可变对象仍可变化。需要深层不可变时可选择元组等结构。</details>
