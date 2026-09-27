---json
{
  "id": "python-29",
  "title": "对象协议、上下文管理与结构匹配",
  "group": "04 · 抽象与工程基础",
  "minutes": 45,
  "level": "进阶",
  "tags": [
    "协议与特殊方法",
    "上下文管理器的异常语义",
    "结构匹配和模式绑定"
  ],
  "objectives": [
    "协议与特殊方法",
    "上下文管理器的异常语义",
    "结构匹配和模式绑定"
  ],
  "prerequisites": [
    "python-17",
    "python-28"
  ],
  "summary": "资源清理与异常恢复是不同责任，退出方法的返回值影响异常是否传播。",
  "quiz": {
    "question": "上下文管理器发生主体异常且 __exit__ 返回 False 时会怎样？",
    "options": [
      "异常被默认删除",
      "退出处理后异常继续传播",
      "主体从头执行",
      "文件自动变成正确数据"
    ],
    "answer": 1,
    "explanation": "资源清理与异常恢复是不同责任，退出方法的返回值影响异常是否传播。"
  },
  "lab": null,
  "revision": "2026-09 · 定义、条件与论证逐章修订"
}
---

## 协议是行为约定
**协议**规定对象需要提供哪些操作及其语义。支持 `len(obj)` 的对象通过 `__len__` 提供非负整数长度；可迭代对象通过 `__iter__` 提供迭代器。特殊方法不是任意命名捷径，必须遵守所参加的语言操作的契约。

**上下文管理协议**包含 `__enter__` 和 `__exit__`。进入时调用前者，其返回值绑定到 `as` 后的名字；成功进入后离开代码块时调用后者，并把异常信息传给它。若存在异常且 `__exit__` 返回真值，异常可被抑制；返回假值则继续传播。通俗地说，进入和退出是配对的流程钩子，是否吞掉错误必须明确决定。

## 一份可跟踪的上下文管理器
```python
class Recorder:
    def __init__(self):
        self.events = []

    def __enter__(self):
        self.events.append("enter")
        return self

    def __exit__(self, exception_type, exception, traceback):
        self.events.append("exit")
        return False

record = Recorder()
try:
    with record as active:
        assert active is record
        active.events.append("body")
        raise ValueError("示例失败")
except ValueError:
    record.events.append("caught")
assert record.events == ["enter", "body", "exit", "caught"]
```
按顺序先 enter、再 body，异常离开主体前仍执行 exit；因为返回 False，外层处理器最终 caught。若 enter 自身就抛异常，则主体未进入，不能依赖本对象的 exit 完成进入过程中尚未注册好的资源清理。标准资源优先使用已有文件或锁的上下文管理器。

## 用生成器表达一次性进入退出
```python
from contextlib import contextmanager

@contextmanager
def marked(events):
    events.append("start")
    try:
        yield "resource"
    finally:
        events.append("finish")

events = []
with marked(events) as value:
    assert value == "resource"
assert events == ["start", "finish"]
```
这个生成器应恰好 yield 一次：之前是进入逻辑，之后是退出逻辑；finally 保证普通异常路径也尝试清理。不要把它当成产出无穷资源的普通数据流。

## 结构模式匹配：匹配形状，不是任意表达式相等
Python 3.10 起支持 `match/case`。它按顺序尝试结构模式，匹配成功且守卫条件为真时执行对应分支。裸名字通常是**捕获绑定**，不是去比较该名字原来的值；固定值应使用字面量或明确的限定名。

```python
def describe(message):
    match message:
        case {"kind": "temperature", "value": value} if isinstance(value, (int, float)):
            return ("temperature", value)
        case ["move", x, y]:
            return ("move", (x, y))
        case _:
            raise ValueError("不支持的消息结构")

assert describe({"kind": "temperature", "value": 20}) == ("temperature", 20)
assert describe(["move", 2, 3]) == ("move", (2, 3))
```
映射模式默认允许额外键，所以它不是严格字段白名单校验。示例数值守卫也未拒绝 bool、NaN 等；若用于测量接口，应接着按业务契约校验。匹配决定结构如何分派，不代替完整验证。

## 练习与解析
1. 为了“程序继续运行”让所有 __exit__ 都返回 True 合理吗？
<details><summary>查看解析</summary>不合理，它会抑制异常并让调用者误以为成功。只有契约明确说明已经处理的异常才应抑制。</details>

2. case {"kind": "temperature", "value": value} 会自动拒绝第三个字段吗？
<details><summary>查看解析</summary>不会。映射模式匹配要求指定键存在，通常允许其他键；严格模式仍需显式校验键集合。</details>
