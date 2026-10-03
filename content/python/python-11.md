---json
{
  "id": "python-11",
  "title": "模块、包与虚拟环境",
  "group": "03 · 可靠的程序实践",
  "minutes": 50,
  "level": "基础",
  "tags": [
    "模块",
    "包",
    "虚拟环境"
  ],
  "objectives": [
    "区分模块与包",
    "创建独立依赖环境",
    "定义模块、包和导入初始化"
  ],
  "prerequisites": [
    "python-10"
  ],
  "summary": "让程序分工明确，并让不同项目拥有可复现的依赖环境。",
  "quiz": {
    "question": "入口保护的主要作用是？",
    "options": [
      "禁止导入模块",
      "区分直接执行与被导入",
      "自动安装依赖",
      "加密源码"
    ],
    "answer": 1,
    "explanation": "__name__ 在直接运行时为 __main__，可据此控制程序入口。"
  },
  "lab": null,
  "revision": "2026-09-28 · 概念分段、教学先修与练习复核"
}
---

## 到这里需要会什么

最低准备是[函数定义与调用](#/course/python/python-07)、基本列表/字符串，以及本页马上介绍的 `import`。先会把一个函数放进 `.py` 文件、导入后调用，再执行环境检查；不要求先学完异常、类、装饰器或第10—19节全部内容。

阅读顺序：先看 `conversions.py` 的直接运行与导入区别，再按本页步骤创建环境、确认解释器和包版本。命名空间包、循环导入与 `pyproject.toml` 属于第二层，遇到项目需要时回读。自查时必须说清“哪个 Python 正在运行、第三方包装在哪里”，不能只凭编辑器没有红线判断环境已经就绪。

## 先定义组织层级
**模块**是具有独立名字空间的代码组织单位，常由一个 `.py` 文件实现，也可能来自内建或扩展模块。

### 包组织多个模块

**包**是可包含子模块的模块；普通包常用 `__init__.py`，命名空间包允许没有该文件。

### 导入会执行初始化

**导入**负责寻找、初始化并提供模块对象，通常会用 `sys.modules` 缓存已载入的模块。

**虚拟环境**是一组解释器入口和隔离的第三方包位置，它不隔离操作系统权限，也不把不可信代码变安全。通俗地说，它像给项目分开工具柜，不是给程序建防护墙。

## 入口保护为什么有效
在普通的 `python conversions.py` 运行方式中，文件的 `__name__` 为 `"__main__"`，函数定义先创建对象，末尾条件为真，所以调用 `main()`。

### 被其他模块导入时

在另一个程序首次 `import conversions` 时，同样先执行顶层定义，但 `__name__` 为模块名 `"conversions"`，末尾条件为假，所以不启动示例计算。

注意：保护的只是缩进在条件里的行为；写在它上方的顶层 `print`、文件写入或网络请求仍会在首次导入时发生。不要误以为添加这一行便消除了全部导入副作用。

排查“安装了却找不到包”的顺序是：查看 `sys.executable` → 用该解释器的 `-m pip` 查看安装 → 核对模块名与发行包名。`import` 使用的名字不一定与安装包名字相同，安装来源需以项目官方文档为准。

## 从一个文件到一组文件
模块通常是一个 Python 文件，包用于组织相关模块。import 让我们复用已有功能，而不必把所有实现复制到当前文件。比如 `import math` 后使用 `math.sqrt(9)`，名称前缀让来源一目了然。`from math import sqrt` 更简短，但大量导入同名符号会降低可读性。初学阶段避免使用星号导入。

模块第一次被导入时，会执行顶层语句。因此，定义函数通常适合放在顶层，而读用户输入、启动长任务等操作不应在导入时意外发生。用入口保护可以让同一文件既可被导入，也可直接运行。

```python
# 保存为 conversions.py
def square_millimeters_to_square_meters(area):
    return area / 1_000_000

def main():
    print(square_millimeters_to_square_meters(2500))

if __name__ == "__main__":
    main()
```

直接运行时输出 0.0025；其他文件导入 conversions 时，不会自动运行 main。模块命名不要使用 math.py、json.py 等标准库名字，否则当前文件可能遮蔽真正的库，让导入错误看起来难以理解。包的公开接口应尽量小，让调用者依赖稳定功能，而非内部实现细节。

## 虚拟环境隔离什么
不同项目可能需要不同版本的依赖。虚拟环境为项目提供单独的解释器入口和安装目录，不是完整虚拟电脑，也不会自动复制所有系统资源。可在项目目录运行 `python -m venv .venv`，再按操作系统方式激活；也可以直接调用环境中的 Python。Windows 常为 `.venv\Scripts\python.exe`，类 Unix 系统常为 `.venv/bin/python`。

安装依赖时，使用所选解释器执行 `python -m pip install 包名`，减少“装到了另一个 Python”的混乱。安装需要网络时只在准备环境阶段发生，本教材示例不依赖运行时网络服务。记录直接依赖、版本范围或锁定版本，并写明 Python 版本；虚拟环境目录本身不应提交到版本库。

## 复现不止是保存代码
别人要复现项目，还需要知道入口命令、输入文件、单位约定、依赖和预期结果。可以提供 requirements.txt，并用 `python -m pip install -r requirements.txt` 安装。对于复杂项目，pyproject.toml 可描述项目元数据和构建配置，属于后续工程化方向。不要在不了解来源时安装同名近似包，应从项目官方文档确认包名。

## 查清正在使用哪个解释器
同一电脑可能同时安装系统 Python、项目虚拟环境和其他工具附带的解释器。编辑器选择的解释器与终端默认命令可能不同，因此“已经安装包却导入失败”首先应检查二者是否一致。可查看 sys.executable，确认实际启动路径。
安装依赖后还应记录版本，尤其当代码依赖某个接口行为时。更新依赖前阅读变更说明，在独立环境运行项目检查，再决定是否更新主环境。把整个环境目录复制到另一台电脑通常不如按依赖说明重建可靠。
模块之间应尽量保持依赖方向清楚。两个模块互相导入并在顶层使用尚未完成初始化的对象，可能造成循环导入问题。提取共同的数据结构或接口到第三个模块，往往比调整导入顺序更能解决设计上的纠缠。

## 为后面的科学计算课准备同一个环境

NumPy、SciPy、pandas、Matplotlib 与 scikit-learn 是第三方包，和 `math`、`csv` 等标准库不同。请先把终端切换到存放课程脚本的项目文件夹，创建环境。创建本身不需要下载第三方包；下面的安装步骤需要网络或事先准备好的包。

### 第一步：创建项目环境

在系统终端运行 `python -m venv .venv`。若本机入口是 `py` 或 `python3`，此处使用第1节已确认的命令。`.venv` 是项目文件夹中保存这个环境的位置。

### 第二步：明确使用该环境的解释器安装

Windows PowerShell：

```text
.\.venv\Scripts\python.exe -m pip install numpy scipy pandas matplotlib scikit-learn
```

macOS/Linux：

```text
./.venv/bin/python -m pip install numpy scipy pandas matplotlib scikit-learn
```

这种写法直接指定环境里的解释器，无需先激活，也不会因另一个同名 `pip` 把库装进其他环境。发行包名 `scikit-learn` 对应代码中的导入名 `sklearn`，二者拼写不同。

### 第三步：核对入口、导入和版本

把下面保存为 `check_science.py`。Windows 用 `.\.venv\Scripts\python.exe check_science.py`，macOS/Linux 用 `./.venv/bin/python check_science.py`；后面科学课脚本也沿用这同一个入口。

```python
import sys
import numpy as np
import scipy
import pandas as pd
import matplotlib
import sklearn

print("解释器:", sys.executable)
print("NumPy:", np.__version__)
print("SciPy:", scipy.__version__)
print("pandas:", pd.__version__)
print("Matplotlib:", matplotlib.__version__)
print("scikit-learn:", sklearn.__version__)
```

若出现 `ModuleNotFoundError`，先核对报错的导入名和 `sys.executable`，再用同一解释器的 `-m pip show 包名` 检查安装。不要先到处重复安装。运行成功后用该解释器的 `-m pip freeze > requirements.txt` 保存本次解析到的版本；这个文件记录实际环境，不能保证任意 Python 版本和操作系统都兼容。环境机制与命令依据见 [Python 官方虚拟环境教程](https://docs.python.org/3/tutorial/venv.html)。

## 练习
1. 为什么模块的输入提示应放在 main 中而非顶层？
<details><summary>查看解析</summary>导入模块会执行顶层代码。把交互过程放入受入口保护的 main，可避免其他程序仅为使用函数就被迫等待输入。</details>

2. 虚拟环境能代替记录依赖版本吗？
<details><summary>查看解析</summary>不能。环境隔离解决当前项目相互影响的问题，版本记录解决日后或另一台电脑如何重建环境的问题。</details>
