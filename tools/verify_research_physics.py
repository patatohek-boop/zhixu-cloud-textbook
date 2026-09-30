"""Recompute ML42-47 teaching examples; no network, training framework or writes.

These finite numerical checks do not prove PINN convergence or validate a real
experiment. The research example is executed directly from its Markdown source.
"""
from pathlib import Path
import contextlib
import io
import json
import math
import re
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def run_checks():
    checks = []

    def check(name, condition):
        if not bool(condition):
            raise AssertionError(name)
        checks.append(name)

    def close(name, actual, expected, atol=1e-9):
        check(name, np.allclose(actual, expected, rtol=0, atol=atol))

    pi = math.pi
    close("42 dimensionless time", 1e-5 * 100 / 0.1**2, 0.1)
    mid = 20 + 80 * math.exp(-pi**2 * 0.1)
    close("42 analytical midpoint temperature", mid, 49.816627108275036)
    x = np.linspace(0, 1, 1001)
    manufactured = np.exp(-0.1) * np.sin(pi * x)
    close("42 manufactured forcing", -manufactured + pi**2 * manufactured,
          (pi**2 - 1) * manufactured)
    amplitude_error = math.exp(-pi**2 * 0.1) / math.sqrt(2)
    close("42 doubled-amplitude solution error", amplitude_error, 0.26354424025464895)
    rnorm = 0.01
    ts = np.linspace(0.001, 0.2, 60)
    exact_error_sq = rnorm**2 / pi**4 * (1 - np.exp(-pi**2 * ts))**2
    error_bound_sq = rnorm**2 / pi**4 * (1 - np.exp(-pi**2 * ts))
    check("42 energy bound for a forced sine mode", np.all(exact_error_sq <= error_bound_sq))
    bound = rnorm * math.sqrt(1 - math.exp(-pi**2 * 0.1)) / pi**2
    close("42 quoted error-bound value", bound, 0.0008024817876334137)
    nodes = np.arange(11) / 10
    close("42 hidden residual vanishes at collocation nodes", np.sin(10 * pi * nodes), 0, 1e-14)
    check("42 hidden residual is nonzero between nodes", abs(math.sin(10 * pi * .05)) > .99)
    a, b, c, d, offset = 1.2, -0.7, 0.4, 0.1, 0.2
    xi, tau, step = .31, .07, 1e-4
    value = lambda xx, tt: c * math.tanh(a * xx + b * tt + d) + offset
    h = math.tanh(a * xi + b * tau + d)
    close("42 neuron time derivative", (value(xi, tau + step) - value(xi, tau - step)) / (2 * step),
          c * b * (1 - h*h), 1e-8)
    close("42 neuron second space derivative", (value(xi + step, tau) - 2*value(xi, tau) + value(xi - step, tau)) / step**2,
          -2*c*a*a*h*(1-h*h), 1e-7)

    hard = lambda xx, tt: np.sin(pi*xx) + tt*xx*(1-xx)*np.tanh(xx+tt)
    close("43 hard initial condition", hard(x, 0), np.sin(pi*x))
    close("43 hard boundary conditions", [hard(0, .1), hard(1, .1)], [0, 0])
    close("43 seconds-to-minutes residual square scaling", 60**2, 3600)
    eta = 1e-5
    # At theta=0 these two quadratic losses have gradients +1 and -2.
    new_theta = eta
    change = .5*(new_theta+1)**2 - .5
    close("43 conflicting-gradient first-order change", change/eta, 1, 1e-5)
    close("43 h-c nonidentifiability", 18*.01/(.2*900), 36*.01/(.2*1800))
    sensitivity = lambda time: 60*time*np.exp(-.001*time)
    check("43 local sensitivity maximum at 1000s", sensitivity(1000) > max(sensitivity(999), sensitivity(1001)))
    close("43 sensitivity value", -sensitivity(1000), -22072.76647028654)
    softplus = lambda z: np.logaddexp(0, z)
    close("43 softplus derivative", (softplus(-2+1e-5)-softplus(-2-1e-5))/(2e-5), 1/(1+math.exp(2)), 1e-9)

    phi = np.array([[1, 1], [1, -1]]) / math.sqrt(2)
    coeff = np.array([[2, 0, -2, 0], [0, 1, 0, -1]], dtype=float)
    snapshots = phi @ coeff
    u, sigma, _ = np.linalg.svd(snapshots / 2, full_matrices=False)
    close("44 weighted singular-value squares", sigma**2, [2, .5])
    reconstruction = u[:, :1] @ (u[:, :1].T @ snapshots)
    close("44 snapshot tail-sum error", np.mean(np.sum((snapshots-reconstruction)**2, axis=0)), .5)
    close("44 retained fraction", sigma[0]**2 / np.sum(sigma**2), .8)
    stiffness = np.array([[2., -1.], [-1., 2.]])
    reduced = phi.T @ stiffness @ phi
    close("44 Galerkin diffusion eigenvalues", reduced, np.diag([1., 3.]))
    check("44 projected dissipation matrix is PSD", np.linalg.eigvalsh(reduced).min() >= 0)
    close("44 new-initial-condition error", math.exp(-3*.5), .22313016014842982)
    close("44 unstable Euler fast-mode energy ratio", (1-1*3)**2, 4)
    close("44 implicit Euler fast-mode energy ratio", (1/(1+3))**2, 1/16)
    close("44 99 percent square energy means 10 percent norm error", math.sqrt((100-99)/100), .1)
    mass_half = np.diag([1., math.sqrt(3.)])
    w_u, w_s, _ = np.linalg.svd(mass_half @ snapshots / 2, full_matrices=False)
    weighted_phi = np.linalg.solve(mass_half, w_u[:, :1])
    mass = mass_half @ mass_half
    close("44 nonidentity-mass normalization", weighted_phi.T @ mass @ weighted_phi, np.eye(1))
    error = snapshots - weighted_phi @ (weighted_phi.T @ mass @ snapshots)
    close("44 nonidentity-mass tail sum", sum(error[:, j]@mass@error[:, j] for j in range(4))/4, w_s[1]**2)

    deep_value = 2*math.sin(pi/4)*math.exp(-pi*pi*.1) + .5*math.exp(-4*pi*pi*.1)
    close("45 DeepONet two-mode hand calculation", deep_value, .5367366319648063)
    grid = np.arange(64) / 64
    initial = np.sin(2*pi*grid) + .25*np.sin(6*pi*grid)
    freq = np.fft.fftfreq(64, d=1/64)
    evolved = np.fft.ifft(np.fft.fft(initial)*np.exp(-4*pi*pi*freq**2*.02)).real
    direct = np.exp(-4*pi*pi*.02)*np.sin(2*pi*grid) + .25*np.exp(-36*pi*pi*.02)*np.sin(6*pi*grid)
    close("45 FFT heat propagation", evolved, direct)
    close("45 eight-sensor aliasing counterexample", np.sin(16*pi*np.arange(8)/8), 0, 1e-14)
    close("45 erroneous zero-mode attenuation", .9**10, .3486784401)

    app_t = (.8*400**4 + .2*300**4)**.25
    close("46 graybody apparent temperature", app_t, 385.56541270345434)
    close("46 clock-offset temperature error", .8*.5, .4)
    covariance = .9*np.eye(100) + .1*np.ones((100, 100))
    close("46 correlated average variance", np.ones(100)@covariance@np.ones(100)/100**2, .109)
    close("46 energy-balance sign", -8-(0-10), 2)
    energy = lambda temperature: 900*temperature + .5*.1*temperature**2
    close("46 variable heat capacity uses integral internal energy", (energy(350.001)-energy(349.999))/.002, 935., 1e-6)

    source = (ROOT / "content/machine-learning/machine-learning-47.md").read_text(encoding="utf8")
    blocks = re.findall(r"```python\n(.*?)\n```", source, flags=re.S)
    check("47 exactly one complete runnable Python example", len(blocks) == 1)
    namespace = {}
    captured = io.StringIO()
    with contextlib.redirect_stdout(captured):
        exec(compile(blocks[0], "machine-learning-47-example", "exec"), namespace)
    close("47 baseline beta estimate", namespace["beta_hat"], .001002)
    close("47 h unit conversion", namespace["h_hat"], 18.036)
    check("47 14-5-5 disjoint run split", [len(namespace[k]) for k in ("train", "valid", "test")] == [14,5,5]
          and len(set(namespace["train_ids"]) | set(namespace["val_ids"]) | set(namespace["test_ids"])) == 24)
    check("47 validation selects degree and physics weight", namespace["pure"][1] == 5 and namespace["physical"][1:3] == (5, .01))
    metrics = {}
    for name, predict in namespace["models"]:
        metrics[name] = {
            "validation_rmse_K": namespace["rmse"](predict, namespace["valid"]),
            "test_observed_rmse_K": namespace["rmse"](predict, namespace["test"]),
            "test_latent_rmse_K": namespace["rmse"](predict, namespace["test"], target="truth"),
            "time_extrapolation_rmse_K": float(60*np.sqrt(np.mean((predict(namespace["future_t"])-namespace["future_true"])**2))),
            "unseen_h_rmse_K": float(60*np.sqrt(np.mean((predict(namespace["TIME"])-namespace["ood_true"])**2))),
        }
    check("47 wrong-physics ablation fails in range", metrics["wrong physics"]["test_observed_rmse_K"] > metrics["physics proxy"]["test_observed_rmse_K"])
    check("47 physics penalty is not an extrapolation guarantee", metrics["physics proxy"]["time_extrapolation_rmse_K"] > metrics["data proxy"]["time_extrapolation_rmse_K"])
    check("47 all models fail unseen h without that input", min(v["unseen_h_rmse_K"] for v in metrics.values()) > 7)
    old_test_y = [r["y"].copy() for r in namespace["test"]]
    for row in namespace["test"]:
        row["y"] += 1e6
    _, untouched_weights = namespace["fit_proxy"](namespace["physical"][1], namespace["physical"][2], namespace["gamma_hat"])
    close("47 poisoned test labels cannot change fitted weights", untouched_weights, namespace["physical"][4], 1e-12)
    for row, values in zip(namespace["test"], old_test_y):
        row["y"] = values
    close("47 next independent run measurement time", namespace["best_time"], 1000.)
    close("47 reference cooling temperature", 20+60/math.e, 42.07276647028654)
    return {"status": "passed", "checks_passed": len(checks), "checks": checks,
            "python": sys.version.split()[0], "numpy": np.__version__,
            "scope": "Numerical examples and actual NumPy code only; no PINN/FNO training or real experiments.",
            "example_47": {"beta_hat": namespace["beta_hat"], "h_hat": namespace["h_hat"],
                           "metrics": metrics, "stdout": captured.getvalue()}}


if __name__ == "__main__":
    report = run_checks()
    print(json.dumps({key: value for key, value in report.items() if key != "example_47"}, ensure_ascii=False, indent=2))
