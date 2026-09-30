---json
{
  "id": "python-28",
  "title": "函数对象、闭包与装饰器",
  "group": "02 · 组织程序与数据",
  "minutes": 45,
  "level": "进阶",
  "tags": [
    "函数作为对象",
    "闭包与名字查找时机",
    "装饰器与参数转发"
  ],
  "objectives": [
    "函数作为对象",
    "闭包与名字查找时机",
    "装饰器与参数转发"
  ],
  "prerequisites": [
    "python-10"
  ],
  "summary": "闭包访问绑定；要理解行为必须说明名字何时查找、默认参数何时求值。",
  "quiz": {
    "question": "循环创建的 lambda 在以后调用时读取什么？",
    "options": [
      "一定读取第一次循环值",
      "按作用域读取当时可访问的绑定",
      "自动复制整个环境",
      "永远读取零"
    ],
    "answer": 1,
    "explanation": "闭包访问绑定；要理解行为必须说明名字何时查找、默认参数何时求值。"
  },
  "lab": null,
  "revision": "2026-09-28 · 概念分段、教学先修与练习复核"
}
---

## 严格定义
函数对象可以绑定给名字、放进容器、作为参数传入并作为结果返回。**高阶函数**接收函数或返回函数。

### 自由变量与闭包

**自由变量**是在当前函数体内使用但不在其中绑定、也不是其参数的外层名字。

### 外层调用结束后仍可访问

**闭包**使嵌套函数继续访问所需的外层绑定，即使外层调用已经结束。



### 绑定与当时数值的区别

闭包保存可访问的绑定，不意味着在创建函数的瞬间把所有变量值拍成照片。通俗地说，函数拿到的是一扇以后还能查看记录的窗口，而非必然拿到当时记录的复印件。

## 先看可靠用法，再解释常见误解
```python
def make_multiplier(factor):
    def multiply(value):
        return factor * value
    return multiply

twice = make_multiplier(2)
three_times = make_multiplier(3)
assert twice(5) == 10
assert three_times(5) == 15

def late_functions():
    functions = []
    for i in range(3):
        functions.append(lambda: i)
    return functions

assert [f() for f in late_functions()] == [2, 2, 2]
```
前两次外层调用各有独立的 factor 绑定，因此结果不同。后一个循环中的三个函数引用同一次外层调用的 i；真正调用它们时循环已经结束，i 为 2，所以都是 2。若要保存每轮值，可以使用 `lambda i=i: i`：右边 i 在定义时作为默认参数求值，每个函数就有各自默认值。这来自不同求值时机，不是 lambda 的随机缺陷。

## nonlocal 与状态
```python
def make_counter():
    count = 0
    def next_count():
        nonlocal count
        count += 1
        return count
    return next_count

counter = make_counter()
assert (counter(), counter(), counter()) == (1, 2, 3)
```
`nonlocal` 指定重绑定最近的外层函数作用域名字。没有它，函数体中的 `count += 1` 会把 count 作为局部名字处理，读取尚未初始化的局部值时失败。状态型闭包有副作用，调用次数影响结果，应写入契约；并发调用还需另考虑同步。

## 装饰器是明确的函数替换
`@decorate` 放在函数定义前，普通情形可理解为“先创建原函数 f，再执行 `f = decorate(f)`”。装饰器可以返回包装函数，添加日志、缓存或契约检查，但不自动保证保留原行为。

```python
from functools import wraps

def count_calls(function):
    calls = 0
    @wraps(function)
    def wrapper(*args, **kwargs):
        nonlocal calls
        calls += 1
        wrapper.calls = calls
        return function(*args, **kwargs)
    wrapper.calls = 0
    return wrapper

@count_calls
def area(width, height=1):
    return width * height

assert area(3, height=2) == 6
assert area(4) == 4
assert area.calls == 2
assert area.__name__ == "area"
```
第一步参数先进入 wrapper，计数加一，再原样转交 function，返回值原样交回调用者。`*args` 收集位置参数，`**kwargs` 收集关键词参数；`wraps` 保存常用元数据便于阅读与调试。函数对象也能保存自定义属性，`wrapper.calls` 用点号访问包装函数对象上的 calls 属性。此计数器统计调用尝试，因此被包装函数抛异常也已经加一；若只想数成功调用，应改变计数位置并更新契约。

## 练习与解析
1. 闭包是否总把外层变量的创建时数值固定下来？
<details><summary>查看解析</summary>不是，它可以继续访问外层绑定。循环中的延迟查找例子说明后续重绑定会影响调用结果。</details>

2. 包装器调用原函数却没有 return，会怎样？
<details><summary>查看解析</summary>原函数仍可能计算和产生副作用，但包装器返回 None，破坏原函数的返回值契约。</details>
