---json
{
  "id": "fluid-mechanics-61",
  "title": "可运行项目：从零实现有限体积",
  "group": "14 · 程序与软件实操",
  "summary": "围绕三对角求解、面通量、解析误差、网格阶数，逐步建立定义、适用条件、推导与可核对的实践。",
  "objectives": [
    "区分并解释三对角求解、面通量、解析误差、网格阶数",
    "在给定假设下复现一维输运解析解与守恒矩阵组装",
    "完成例题、检查单位与适用范围"
  ],
  "prerequisites": [
    "fluid-mechanics-60"
  ],
  "tags": [
    "三对角求解",
    "面通量",
    "解析误差",
    "网格阶数"
  ],
  "minutes": 75,
  "level": "专项进阶",
  "quiz": {
    "question": "Pe=0 时本例解析解是什么？",
    "options": [
      "φ=1/x",
      "φ=x",
      "φ=0"
    ],
    "answer": 1,
    "explanation": "纯扩散、两端值为0和1时得到线性解。"
  },
  "lab": "cfd-upwind",
  "revision": "2026-09-30 · 流动换热仿真专项"
}
---

## 本项目能做什么

我们从控制方程直接组装一个有限体积程序，用解析解检查误差、用各面通量检查守恒。程序只需 Python 3.10 或更新版本的标准库，不联网、不依赖商业软件。

这是 **一维稳态标量输运教学程序** ，没有求解压力、速度、三维流动或湍流。它让你亲眼看到离散、求解、后处理和验证如何连接，不能替代完整 CFD 软件。

## 严谨的问题定义

在无量纲区间 $0\le x\le1$，求

$$\frac{dJ}{dx}=0,\qquad J=Pe\,\phi-\frac{d\phi}{dx},\qquad \phi(0)=0,\quad\phi(1)=1.$$

$Pe\ge0$ 为整段区域的 Péclet 数，$\phi$ 是无量纲标量。扩散系数已经缩放为 1。它是含扩散的二阶边界值问题，因此两端 Dirichlet 条件是合理的；不可将相同条件直接套到纯单向双曲输运问题。

积分一次知 $J$ 为常数，再解一阶线性方程，得到

$$\phi(x)=\frac{e^{Pe x}-1}{e^{Pe}-1}\quad(Pe>0),\qquad \phi(x)=x\quad(Pe=0).$$

程序将解析解改写为 $e^{Pe(x-1)}(1-e^{-Pe x})/(1-e^{-Pe})$，分子和分母的指数差都用 `expm1` 计算，避免只保护分母而在分子发生消减误差。所有指数非正，也避免上溢。对于 $0<Pe<10^{-8}$，使用一阶展开 $\phi=x+Pe\,x(x-1)/2+O(Pe^2)$；该极限分支也避免次正规浮点数相除造成精度损失。恒定通量为 $J=-Pe/(e^{Pe}-1)$；在 $Pe\to0$ 时趋于 $-1$。

 **通俗解释** ：流向右，右端却规定较高的浓度或温度。扩散试图向左传播信息，对流把它推回右边，最后会在右端形成很陡的变化层。网格不够细时，这正是格式容易暴露问题的地方。

## 从面通量组装矩阵

将区间分成 $N$ 个单元，中心位于 $(i+1/2)/N$，$D=1/\Delta x=N$。对相邻中心 $i,i+1$，写 $J_e=a\phi_i+b\phi_{i+1}$：

|格式|$a$|$b$|
|---|---|---|
|一阶迎风|$D+Pe$|$-D$|
|中心插值|$D+Pe/2$|$-D+Pe/2$|

同一个面通量在左单元加上、右单元减去，内部通量严格相消。边界到首末中心的距离是半个单元，所以边界扩散导通系数为 $2D$。入口对流使用规定值；出口迎风使用上游末单元值，中心格式使用规定的边界值。这些边界细节也是程序的一部分，不能只证明内部格式。

每个单元满足 $J_e-J_w=0$，产生三对角方程。Thomas 算法通过前消元和回代在 $O(N)$ 时间内求解；若遇到近零主元，程序明确报错，不会静默修改答案。

## 完整代码

将以下内容保存为 `transport_fvm.py`。仓库中的 `examples/cfd/transport_fvm.py` 与本段代码由构建程序逐字核对。

```python
"""Conservative 1-D steady transport, standard library only; not a CFD solver."""
import argparse
import csv
import json
import math
from pathlib import Path


def exact(x, pe):
    if pe == 0:
        return x
    if pe < 1e-8:
        # First-order Taylor limit; also avoids dividing subnormal numbers.
        return x + 0.5 * pe * x * (x - 1)
    # Protect BOTH differences from cancellation and keep exponents nonpositive.
    return math.exp(pe * (x - 1)) * (-math.expm1(-pe * x)) / (-math.expm1(-pe))


def solve(cells=20, pe=10.0, scheme="upwind"):
    if not isinstance(cells, int) or not 2 <= cells <= 10000:
        raise ValueError("cells must be an integer in [2, 10000]")
    if not math.isfinite(pe) or not 0 <= pe <= 100:
        raise ValueError("Pe must be finite and in [0, 100]")
    if scheme not in ("upwind", "central"):
        raise ValueError("scheme must be upwind or central")
    d = float(cells)  # diffusion conductance: 1 / dx
    west = [0.0] * cells
    diag = [0.0] * cells
    east = [0.0] * cells
    rhs = [0.0] * cells
    a = d + (pe if scheme == "upwind" else pe / 2)
    b = -d + (0 if scheme == "upwind" else pe / 2)
    for i in range(cells - 1):
        diag[i] += a
        east[i] += b
        west[i + 1] -= a
        diag[i + 1] -= b
    # Boundary values phi(0)=0, phi(1)=1. Half-cell diffusion distances.
    diag[0] += 2 * d
    diag[-1] += 2 * d + (pe if scheme == "upwind" else 0)
    rhs[-1] += 2 * d - (pe if scheme == "central" else 0)
    # Thomas elimination; fail explicitly rather than hide an invalid pivot.
    for i in range(1, cells):
        if abs(diag[i - 1]) < 1e-14:
            raise ArithmeticError("zero pivot: change scheme or refine mesh")
        factor = west[i] / diag[i - 1]
        diag[i] -= factor * east[i - 1]
        rhs[i] -= factor * rhs[i - 1]
    phi = [0.0] * cells
    for i in range(cells - 1, -1, -1):
        if abs(diag[i]) < 1e-14:
            raise ArithmeticError("zero pivot: change scheme or refine mesh")
        phi[i] = (rhs[i] - (east[i] * phi[i + 1] if i + 1 < cells else 0)) / diag[i]
    x = [(i + 0.5) / cells for i in range(cells)]
    reference = [exact(t, pe) for t in x]
    flux = [-2 * d * phi[0]]
    flux.extend(a * phi[i] + b * phi[i + 1] for i in range(cells - 1))
    flux.append((2 * d + (pe if scheme == "upwind" else 0)) * phi[-1]
                + (pe if scheme == "central" else 0) - 2 * d)
    return {
        "cells": cells, "pe": pe, "scheme": scheme, "cell_pe": pe / cells,
        "x": x, "phi": phi, "exact": reference, "flux": flux,
        "l2": math.sqrt(sum((u - v) ** 2 for u, v in zip(phi, reference)) / cells),
        "max_cell_imbalance": max(abs(v - u) for u, v in zip(flux, flux[1:])),
        "global_imbalance": abs(flux[-1] - flux[0]),
        "bounded": min(phi) >= -1e-12 and max(phi) <= 1 + 1e-12,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cells", type=int, default=20)
    parser.add_argument("--pe", type=float, default=10)
    parser.add_argument("--scheme", choices=("upwind", "central"), default="upwind")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--study", action="store_true")
    args = parser.parse_args()
    previous = None
    for n in ([10, 20, 40, 80, 160] if args.study else [args.cells]):
        result = solve(n, args.pe, args.scheme)
        metrics = {k: v for k, v in result.items() if not isinstance(v, list)}
        if previous and result["l2"] > 1e-14 and previous > 1e-14:
            metrics["observed_order"] = math.log(previous / result["l2"], 2)
        previous = result["l2"]
        print(json.dumps(metrics, allow_nan=False))
        if args.out:
            args.out.mkdir(parents=True, exist_ok=True)
            with (args.out / f"{args.scheme}-{n}.csv").open("w", newline="", encoding="utf-8") as handle:
                writer = csv.writer(handle)
                writer.writerow(["x", "phi", "exact", "error"])
                writer.writerows((x, u, v, u - v) for x, u, v in
                                 zip(result["x"], result["phi"], result["exact"]))


if __name__ == "__main__":
    main()
```

## 运行与阅读输出

```bash
python transport_fvm.py --pe 5 --scheme central --study --out results-central
python transport_fvm.py --pe 5 --scheme upwind --study --out results-upwind
python transport_fvm.py --pe 60 --cells 10 --scheme central
```

`l2` 是单元中心误差的离散均方根；`max_cell_imbalance` 是最大单元通量缺口；`global_imbalance` 是出口与入口通量差。每套网格的 CSV 保存坐标、数值解、解析解和误差。输出文件夹会被创建；同名 CSV 会被新结果覆盖，保留对比时请使用不同目录。

预期第一组在充分细网格上接近二阶，第二组接近一阶。第三组的单元 $Pe_\Delta=6$，中心格式可能出现负值或振荡，因为邻接系数不再满足简单的有界性条件。 **通量守恒仍可很好** ：这正说明守恒是必要检查，却不是准确或有界的充分条件。

观察阶 $p=\log(E_N/E_{2N})/\log2$ 必须使用正且明显高于舍入误差的误差。在 $Pe=0$ 时线性解可被精确重现，不应从接近机器误差的数值强行计算阶数。

## 如何继续扩展

先增加体积源项并用制造解核对，再扩展到非均匀网格和变扩散系数。之后才进入二维输运、压力速度耦合和能量方程。每加一个机制，都保留一个能手算或具有解析解的小问题作为回归检验。

## 练习与解析

<details><summary>练习 1：所有单元通量缺口都接近零，误差是否一定接近零？</summary>

不是。它说明离散守恒方程被很好求解；离散方程本身仍可能有较大截断误差。粗网格迎风的数值扩散和中心格式的振荡都可在守恒前提下出现。
</details>

<details><summary>练习 2：Pe=0 时应看到什么结果？它能检验哪些部分？</summary>

应得到各中心的 $\phi=x$，所有面通量约为 −1。它可检查扩散符号、半单元边界距离、三对角求解和通量后处理，但不能单独检验对流格式。
</details>

## 参考

离散原理参见 [CFD Direct · General Principles](https://doc.cfd.direct/notes/cfd-general-principles/)。本站程序为独立教学实现，解析解和面通量表达式均在本节推导。
