"""Conservative 1-D steady transport, standard library only; not a CFD solver."""
import argparse
import csv
import json
import math
from pathlib import Path


def exact(x, pe):
    if pe == 0:
        return x
    return (math.exp(pe * (x - 1)) - math.exp(-pe)) / (-math.expm1(-pe))


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
