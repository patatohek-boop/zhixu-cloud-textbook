"""Recompute the original examples in machine-learning-36 through -41.

Run: python tools/verify_research_foundations.py [--report PATH]
Python 3.10+ standard library only; no network or experimental data required.
Checks include numerical ODE integration, finite differences, joint Gaussian
conditioning, factorial orthogonality and independent integration of EI.
Numerical agreement supports these examples; it does not prove general claims.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def verify() -> list[dict]:
    checks: list[dict] = []

    def check(name, value, expected, tolerance=1e-8, method="independent arithmetic"):
        if not math.isfinite(value) or abs(value - expected) > tolerance:
            raise AssertionError(f"{name}: {value!r} != {expected!r}; tolerance={tolerance}")
        checks.append({
            "name": name, "value": value, "expected": expected,
            "absolute_tolerance": tolerance, "method": method, "passed": True,
        })

    # Chapter 36: SI units, lumped baseline and nondimensionalization.
    mass, capacity, area, coefficient = 0.2, 900.0, 0.01, 18.0
    density, conductivity = 2700.0, 180.0
    volume = mass / density
    length = volume / area
    diffusivity = conductivity / (density * capacity)
    beta = coefficient * area / (mass * capacity)
    biot = coefficient * length / conductivity
    check("36 Bi", biot, 0.0007407407407407407)
    check("36 Bi*Fo equals beta*t", biot * diffusivity * 600 / length**2, beta * 600)
    check("36 cooling at 600 s", 20 + 60 * math.exp(-beta * 600), 52.92869816564159)
    check("36 initial cooling derivative", -coefficient * area * 60 / (mass * capacity), -0.06)
    check("36 minutes error at 10 seconds", 20 + 60 * math.exp(-beta * 10), 79.40299002495008)

    # Chapter 37: calibration, dynamic response and correlated measurements.
    check("37 static calibration gain", (82.6 - 21.4) / 60, 1.02)
    check("37 inverse calibration", (52.0 - 1.0) / 1.02, 50.0)
    check("37 sensor response 20 s", 80 - 60 * math.exp(-1), 57.92723352971346)
    check("37 sensor response 60 s", 80 - 60 * math.exp(-3), 77.01277589792817)
    step, sensor = 0.001, 20.0
    for _ in range(60_000):
        sensor += step * (80 - sensor) / 20
    check("37 step response independently integrated", sensor, 80 - 60 * math.exp(-3),
          0.0003, "60000-step explicit Euler integration")
    variance = sum(0.5**abs(i - j) for i in range(4) for j in range(4)) / 16
    check("37 correlated mean variance from all covariance entries", variance, 0.515625)
    check("37 correlated effective sample count", 1 / variance, 1.9393939393939394)
    check("37 response half-life", 30 / math.log(2), 43.2808512266689)

    # Chapter 38: an inverse problem with known mass, heat capacity and area.
    def temperature(time, h, c=900.0):
        return 20 + 60 * math.exp(-h * area * time / (mass * c))

    time, perturbation = 1000.0, 1e-4
    sensitivity = (
        temperature(time, coefficient + perturbation)
        - temperature(time, coefficient - perturbation)
    ) / (2 * perturbation)
    check("38 analytic sensitivity checked by finite difference", sensitivity,
          -10 / (3 * math.e), 1e-8, "central difference of temperature")
    inverse_h = -mass * capacity / (area * time) * math.log(
        (temperature(time, coefficient) - 20) / 60
    )
    check("38 inverse coefficient", inverse_h, 18.0)
    for scale in (0.5, 2.0, 3.0):
        for sample_time in (0.0, 500.0, 1000.0, 2000.0):
            check(f"38 scaling invariance scale={scale} time={sample_time}",
                  temperature(sample_time, coefficient * scale, capacity * scale),
                  temperature(sample_time, coefficient, capacity))
    check("38 Fisher information at tau", sensitivity**2, 1.5037253692956962, 1e-7)
    check("38 inverse-root information", 1 / abs(sensitivity), 0.8154845485377136)
    winner = max(range(3001), key=lambda t: t * t * math.exp(-2 * beta * t))
    check("38 sampled information maximum time", float(winner), 1000.0, 0,
          "independent integer-grid maximization")

    # Chapter 39: Gaussian noise is on z=-log(Theta), NOT on temperature.
    inputs, observations, deviations = [0.5, 1.0], [0.48, 1.04], [0.02, 0.04]
    precision = sum(t * t / s**2 for t, s in zip(inputs, deviations))
    rhs = sum(t * z / s**2 for t, z, s in zip(inputs, observations, deviations))
    estimate = rhs / precision
    check("39 weighted regression", estimate, 1.0)
    residual_q = sum(((z - estimate * t) / s)**2
                     for t, z, s in zip(inputs, observations, deviations))
    check("39 residual Q", residual_q, 2.0)
    ordinary = sum(t * z for t, z in zip(inputs, observations)) / sum(t * t for t in inputs)
    check("39 ordinary regression", ordinary, 1.024)
    posterior_mean = (rhs + 0.8 / 0.2**2) / (precision + 1 / 0.2**2)
    posterior_variance = 1 / (precision + 1 / 0.2**2)
    check("39 posterior mean", posterior_mean, 0.996078431372549)
    check("39 posterior lower interval", posterior_mean - 1.96 * math.sqrt(posterior_variance),
          0.9411874520786511)
    check("39 posterior upper interval", posterior_mean + 1.96 * math.sqrt(posterior_variance),
          1.0509694106664471)
    predictive_variance = 2.25 * posterior_variance + 0.03**2
    predictive_mean = 1.5 * posterior_mean
    check("39 predictive variance", predictive_variance, 0.002664705882352941)
    check("39 predictive lower", predictive_mean - 1.96 * math.sqrt(predictive_variance),
          1.3929409001371762)
    check("39 predictive upper", predictive_mean + 1.96 * math.sqrt(predictive_variance),
          1.595294393980471)

    # Chapter 40: joint conditioning, separate from the chapter's sequential calculation.
    covariance = [[5.0, 4.0], [4.0, 5.2]]
    determinant = covariance[0][0] * covariance[1][1] - covariance[0][1]**2
    inverse = [[covariance[1][1] / determinant, -covariance[0][1] / determinant],
               [-covariance[1][0] / determinant, covariance[0][0] / determinant]]

    def dot(a, b):
        return sum(x * y for x, y in zip(a, b))

    def matvec(matrix, vector):
        return [dot(row, vector) for row in matrix]

    cross = [4.0, 5.0]
    gp_mean = dot(cross, matvec(inverse, [2.0, 3.0]))
    gp_variance = 5.0 - dot(cross, matvec(inverse, cross))
    check("40 full joint GP mean", gp_mean, 2.86, 1e-12,
          "2x2 joint covariance conditioning, independent of sequential hand solution")
    check("40 full joint GP variance", gp_variance, 0.18, 1e-12,
          "2x2 joint covariance conditioning")
    check("40 posterior cross covariance", -dot([4.0, 4.0], matvec(inverse, [0.0, 1.0])), -0.4)
    check("40 latent interval lower", 50 + gp_mean - 1.96 * math.sqrt(gp_variance),
          52.02844242532462)
    check("40 observation interval upper", 50 + gp_mean + 1.96 * math.sqrt(gp_variance + 0.2),
          54.068225144581916)
    check("40 rho versus correlation", 8 / math.sqrt(4 * 17), 0.9701425001453319)

    # Chapter 41: full factorial algebra, EI quadrature and scalar mutual information.
    design = [[1, -1, -1, 1], [1, 1, -1, -1], [1, -1, 1, -1], [1, 1, 1, 1]]
    responses = [6, 4, 8, 2]
    for i in range(4):
        for j in range(4):
            check(f"41 orthogonality {i},{j}", sum(row[i] * row[j] for row in design),
                  4.0 if i == j else 0.0, 0)
    for j, expected in enumerate([5, -2, 0, -1]):
        check(f"41 factorial coefficient {j}",
              sum(row[j] * y for row, y in zip(design, responses)) / 4, expected)

    def normal_pdf(z):
        return math.exp(-z * z / 2) / math.sqrt(2 * math.pi)

    def normal_cdf(z):
        return (1 + math.erf(z / math.sqrt(2))) / 2

    def simpson(function, left, right, panels=20_000):
        width = (right - left) / panels
        return width / 3 * (
            function(left) + function(right)
            + sum((4 if i % 2 else 2) * function(left + i * width) for i in range(1, panels))
        )

    for label, mean, deviation in [("A", 1.8, 0.1), ("B", 2.1, 0.5)]:
        threshold = (2 - mean) / deviation
        ei = (2 - mean) * normal_cdf(threshold) + deviation * normal_pdf(threshold)
        # Integrate the defining expectation rather than calling an EI implementation.
        integral = simpson(lambda z: (2 - mean - deviation * z) * normal_pdf(z), -12, threshold)
        check("41 EI " + label + " by numerical density integration", integral, ei, 1e-10,
              "Simpson integral of weighted Gaussian density; negligible lower tail below -12")
    check("41 information A", 0.5 * math.log1p(0.01 / 0.04), 0.11157177565710488)
    check("41 information B", 0.5 * math.log1p(0.25 / 0.04), 0.9905007344332917)
    check("41 information with noise nine", 0.5 * math.log1p(1 / 9), 0.052680257828913175)
    return checks


def main():
    from verify_audit_errata import verify as verify_errata
    verify_errata()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, help="Optionally save the complete numerical results.")
    arguments = parser.parse_args()
    checks = verify()
    report = {
        "chapters": [f"machine-learning-{number}" for number in range(36, 42)],
        "checks_passed": len(checks), "dependencies": "Python 3.10+ standard library",
        "numeric_checks": checks,
        "limitations": [
            "All data and examples are synthetic; no physical experiments were performed.",
            "Numerical checks do not establish general mathematical or physical validity.",
            "Run verify_computing.py and test-rendering.cjs separately for lesson code and rendering.",
        ],
    }
    if arguments.report:
        arguments.report.parent.mkdir(parents=True, exist_ok=True)
        arguments.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"chapters": len(report["chapters"]), "checks_passed": len(checks),
                      "dependencies": report["dependencies"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
