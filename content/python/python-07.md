---json
{
  "id": "python-07",
  "title": "函数、参数与作用域",
  "group": "02 · 组织程序与数据",
  "minutes": 50,
  "level": "基础",
  "tags": [
    "函数",
    "作用域",
    "接口"
  ],
  "objectives": [
    "设计可测试函数",
    "避免可变默认参数",
    "定义形参、实参、返回值和作用域",
    "阅读仅限位置、仅限关键词及实参展开的调用契约"
  ],
  "prerequisites": [
    "python-06"
  ],
  "summary": "通过输入输出契约拆分程序，理解局部名字和参数传递。",
  "quiz": {
    "question": "函数应优先怎样接收影响计算结果的数据？",
    "options": [
      "读取隐藏全局变量",
      "通过明确参数",
      "从屏幕输出反向读取",
      "依赖上次调用残留"
    ],
    "answer": 1,
    "explanation": "参数让依赖显式化，支持测试和复现。"
  },
  "lab": null,
  "revision": "2026-10-04 · 连续正文、定义次序与概念分段复核"
}
---

## 函数、参数、返回值与作用域
**函数定义**创建函数对象并绑定名称；函数体在调用时执行。

### 实参与形参

调用处提供的对象叫**实参**，定义中接收它的局部名字叫**形参**。

### 结果与副作用

`return` 终止当前调用并给调用者一个结果对象；没有明确返回值时结果是 `None`。**副作用**指返回值之外可被观察到的改变，例如修改输入列表、写文件或打印。

**作用域**是某名字绑定能直接被查找到的代码范围。参数通常是本次调用的局部绑定，重新绑定形参不会重新绑定调用者名字，但修改共享对象会被调用者观察到。通俗地说，传入的是使用同一份对象的入口，不是保证复制了一份内容。

## 例：温升计算函数

实验开始为 20 ℃、结束为 25 ℃，温升是 $25-20=5$ ℃。将这一计算定义为函数 `temperature_rise`：第一个参数表示开始温度，第二个参数表示结束温度，返回值为温升。相同的计算规则便可用于多组数据。

本例约定输入两个给定的有限数值，单位都为摄氏度；输出是“结束减开始”的温差，允许负数表示降温。这段入门代码演示调用与返回，不承担外部文本解析、传感器故障判断或所有类型的校验。

<figure class="teaching-figure"><a href="assets/diagrams/learn-python-07.svg" target="_blank" rel="noopener"><img src="assets/diagrams/learn-python-07.svg" alt="调用者提供20和25，分别绑定到本次调用的start_c和end_c；函数做25减20得到5，return把5交给调用处的rise；调用者再计算rise加2得到7。" loading="lazy"></a><figcaption>箭头是值的传递，框是本次调用的局部计算。返回值能进入下一次计算，屏幕文字本身不能代替它。</figcaption></figure>

### 函数调用的执行过程

```python
def temperature_rise(start_c, end_c):
    difference_c = end_c - start_c
    return difference_c

rise = temperature_rise(20, 25)
print(rise)
print(rise + 2)
```

1. `def` 创建一个有名字的函数，括号里的 `start_c`、`end_c` 是形参。此时还没有做减法，缩进的函数体要等调用才运行。
2. `temperature_rise(20, 25)` 是调用。20、25 是实参，按位置分别交给本次调用的两个形参。
3. 函数算出 `difference_c = 5`。`return` 把这个数交回调用处，并结束本次调用。
4. 整个调用表达式的结果是 5，于是外面的 `rise` 绑定到 5。两次输出依次为 `5`、`7`。第二次只是用返回值继续做算术，未表示新的实验测量。

“局部名字”表示 `difference_c` 在这次调用内部使用；外面要使用结果，就接住返回值。不要通过猜测内部变量名去拿结果。对于本例的不可变整数，计算不会修改传入的整数对象；下文的列表例子会说明共享可变对象为什么另有副作用。

### 位置参数与关键词参数

`temperature_rise(25, 20)` 得到 -5，含义是从 25 ℃ 降到 20 ℃；它不会自动猜出你原本想表示升温。写成 `temperature_rise(start_c=20, end_c=25)` 可把含义直接放在调用处。需要更复杂的参数限制时，再读下文的 `/` 与 `*`。

打印与返回需要区别：打印是展示动作；返回是把对象交给调用者，供测试、批量处理或后续计算使用。两者可以同时存在，但用途不同。[Python 官方教程：函数定义](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)说明调用、局部名字及默认返回 `None` 的规则。

### 练习：打印与返回的区别

把 `return difference_c` 改成 `print(difference_c)`，其余代码不变。第一次调用显示什么？`rise` 是什么？最后一行能完成吗？

<details><summary>展开答案：区分副作用与返回对象</summary>

调用过程中先显示 `5`，但函数走到末尾而没有 `return` 一个数，因此返回 `None`。接着 `print(rise)` 显示 `None`；最后的 `rise + 2` 不能把 `None` 与整数相加，会产生 `TypeError`。修正方法是返回数值，让调用者决定何时打印。

</details>

## 例：摄氏温度转换的输入与输出
摄氏度转换函数的数学契约是：输入有限实数 t 且 $t\ge-273.15$，返回 $t+273.15$ 开尔文；非法输入抛出明确异常。下文最小示例只演示范围校验，若实际接收外部输入，还必须检查有限性，不能把 NaN 当有效温度。

下面的函数把摄氏温度加上 273.15，并拒绝低于绝对零度的输入。参数名和文档字符串说明单位；返回的数值可供打印、测试或下一步计算。此版本的调用者还须保证输入是有限数值。

```python
def celsius_to_kelvin(temperature_c):
    """将不低于绝对零度的摄氏温度转换为开尔文。"""
    if temperature_c < -273.15:
        raise ValueError("温度低于绝对零度")
    return temperature_c + 273.15

result = celsius_to_kelvin(25.0)
print(f"{result:.2f} K")  # 298.15 K
```

调用 `celsius_to_kelvin(25.0)` 返回 298.15。外层的格式化与打印只改变显示方式，不改变这个返回值。

### 把接口约定写出来

文档字符串说明输入单位、输出单位和错误条件，让使用者不用逐行阅读实现也能正确调用。

## 默认参数的求值时机
```python
def add_bad(x, items=[]):
    items.append(x)
    return items

first = add_bad(1)
second = add_bad(2)
assert first is second and first == [1, 2]

def add_good(x, items=None):
    if items is None:
        items = []
    items.append(x)
    return items

assert add_good(1) == [1]
assert add_good(2) == [2]
```
定义 `add_bad` 时只创建一次默认列表 L；第一次调用向 L 加 1，第二次仍使用 L，故两次返回同一列表。这是定义时求值规则的推论。

### 每次创建独立默认列表

`add_good` 在每次缺省调用时创建新列表；若调用者主动传入列表，仍会修改该列表，应写入接口说明。

## 局部名字与共享对象

<figure class="teaching-figure"><a href="assets/diagrams/python-function-scope.svg" target="_blank" rel="noopener" aria-label="打开大图：调用把外部值绑定给局部参数，return 把结果交回调用处；局部名字 c 不会重新绑定外部名字 t。"><img src="assets/diagrams/python-function-scope.svg" alt="调用把外部值绑定给局部参数，return 把结果交回调用处；局部名字 c 不会重新绑定外部名字 t。" loading="lazy"></a><figcaption>调用把外部值绑定给局部参数，return 把结果交回调用处；局部名字 c 不会重新绑定外部名字 t。<br><small>示例函数 to_kelvin(c) 返回 c + 273.15，输入为不可变数值。若参数引用可变对象，函数仍可能修改共享对象内容。 · 点按图形可放大。</small></figcaption></figure>

函数体内赋值的名字默认属于局部作用域，通常不会改变外部同名变量。查找名字遵循局部、外层函数、全局、内置等层次。应优先通过参数传入依赖、通过返回值传出结果，避免依赖隐藏的全局变量。这样同样输入更容易产生同样输出，也更容易测试。

参数绑定仍遵循对象模型：传入列表后，函数修改列表内容会影响调用者；在函数内给参数重新赋一个新列表，通常不会重新绑定调用者的名字。并不存在简单的“所有参数都按值复制”规则。接口应说明是否修改输入，必要时主动创建新对象。

## 函数对象与调用方式
位置参数按排列顺序绑定，关键词参数按名字绑定；省略有默认值的参数时，使用定义函数时求得的默认对象。共享默认列表的后果已由前例说明。`*args` 收集额外位置参数，`**kwargs` 收集额外关键词参数，只有接口确实需要时再使用。

函数也是对象，可以赋给变量、传给其他函数；lambda 适合短小表达式，不应塞进复杂业务规则。递归是函数调用自身，必须有基本情况，并让问题规模向基本情况靠近。递归不必然比循环优雅，过深递归还会受到调用栈限制。

## 函数签名与参数绑定
**函数签名**是参数名称、排列、默认值及调用限制的说明。`/` 前面的参数只能按位置给出，`*` 后面的参数只能按关键词给出；中间的普通参数两种方式都可以。二者是定义中的分隔符，不会占一个实参位置。

```python
def scale(value, /, factor=1.0, *, offset=0.0):
    return value * factor + offset

assert scale(3, 2, offset=1) == 7
assert scale(3, factor=2, offset=1) == 7
try:
    scale(value=3)  # value 只能按位置传入
except TypeError:
    pass
else:
    raise AssertionError("位置限制未生效")
```
这里 factor 有默认值，offset 既有默认值又只能写名字。`scale(3,2,1)` 会失败，因为第三个位置没有可绑定参数；`scale(3,2,factor=4)` 会失败，因为 factor 收到两次值。错误发生在参数绑定阶段，不能靠函数体内调整补救。

例中的 `try/except TypeError` 表示尝试一次调用并接住预期的参数类型/绑定异常；`else` 中主动报错则检查“非法调用确实被拒绝”。其完整流程在[异常处理](#/course/python/python-14)学习，这里先用它让整个示例能够运行结束。

在调用处，`f(*sequence)` 把元素展开成位置实参，`f(**mapping)` 把字符串键值展开成关键词实参；在定义处，`*args`、`**kwargs` 则分别收集多余实参为元组与字典。这是相反方向的操作。容器与展开的例子在学完[序列](#/course/python/python-08)和[字典](#/course/python/python-09)后可回看：`scale(*[3,2], **{"offset":1})` 等于上面的第一次调用。

参数名没有特殊魔法，args、kwargs 只是惯例；给公开接口起明确的关键词名可以减少单位和顺序混淆。可对照 [Python 官方教程特殊参数与实参展开](https://docs.python.org/3/tutorial/controlflow.html#special-parameters)。

## 输入、计算与输出的分工
以读取摄氏度并输出开尔文为例，可以分成读取文本、转换与验证、展示结果。中间的计算函数只接收数值并返回数值，不调用输入或打印；外层负责用户交互。这样同一计算可用于终端、网页、测试和文件批处理。
函数太长时，先找出可以独立命名的概念，而不是按固定行数随意切开。拆分后的参数应少而明确，返回值应具有稳定结构。若一个函数需要十几个互相关联的参数，可以考虑具名记录，但也要检查是否承担了太多职责。
阅读调用时应能猜到它做什么；阅读文档时应知道输入限制；运行测试时应知道关键承诺是否仍成立。这三层清楚之后，再学习装饰器、闭包等更高级的函数工具会更容易。

## 练习：带关键词参数的校正函数

实现 `calibrate(value, *, offset=0.0)`：对本题给定的有限实数返回 `value + offset`，不在函数内部打印。检查不传 offset、传正偏移、传负偏移三种调用，并说明为什么 `calibrate(20, 2)` 不符合接口。

<details><summary>参考实现与核查</summary>

```python
def calibrate(value, *, offset=0.0):
    return value + offset

assert calibrate(20.0) == 20.0
assert calibrate(20.0, offset=2.0) == 22.0
assert calibrate(20.0, offset=-2.0) == 18.0
```

`*` 后的 offset 必须按关键字传入；位置调用会产生 `TypeError`。本题只承诺题设有限数值，不将三次断言冒称所有输入验证。
</details>

## 练习
1. 函数里只有 `print(3)`，执行 `x = f()` 后 x 是什么？
<details><summary>查看解析</summary>x 是 None。屏幕上出现 3 不代表函数返回 3；应写 return 3 才能把数值交给调用者。</details>

2. 为什么 `items=None` 常比 `items=[]` 更合适？
<details><summary>查看解析</summary>None 可以作为未提供参数的标记，每次调用时创建新的列表，避免不同调用意外共享可变默认对象。</details>
