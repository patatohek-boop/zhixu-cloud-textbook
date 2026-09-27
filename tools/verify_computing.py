"""Verify the Python and machine-learning textbook examples and derivations.

Run: python tools/verify_computing.py [--report PATH]
Requirements: Python >=3.10, NumPy, pandas, Matplotlib, scikit-learn, Node.js.
Math rendering uses the repository's vendored KaTeX; it does not download packages.
Examples run in isolated temporary directories with a non-interactive plot backend.
A passing example is evidence for that example, not a substitute for a proof.
"""
from __future__ import annotations

import argparse
import contextlib
import importlib.metadata
import io
import itertools
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
COURSES = ("python", "machine-learning")
FENCE = chr(96) * 3
CODE = re.compile(re.escape(FENCE) + r"python[^\n]*\n(.*?)" + re.escape(FENCE), re.S)


def read_lessons():
    lessons = []
    for course_id in COURSES:
        folder = ROOT / "content" / course_id
        course = json.loads((folder / "course.json").read_text(encoding="utf-8"))
        positions = {name[:-3]: i for i, name in enumerate(course["lessons"])}
        for position, name in enumerate(course["lessons"]):
            raw = (folder / name).read_text(encoding="utf-8")
            match = re.match(r"---json\s*\n(.*?)\n---\s*\n(.*)", raw, re.S)
            if not match:
                raise AssertionError(f"Invalid front matter: {name}")
            meta = json.loads(match[1])
            body = match[2]
            if meta["id"] != name[:-3] or raw.count(FENCE) % 2 or "~~~" in raw:
                raise AssertionError(f"ID or fence inconsistency: {name}")
            for prerequisite in meta["prerequisites"]:
                if prerequisite in positions and positions[prerequisite] >= position:
                    raise AssertionError(f"Forward prerequisite: {name} -> {prerequisite}")
            lessons.append((course_id, meta, body))
        audit_path = ROOT / "reviews" / "content-audit-2026-09" / f"{course_id}.json"
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
        titles = {meta["id"]: meta["title"] for cid, meta, _ in lessons if cid == course_id}
        for record in audit["records"]:
            if titles.get(record["id"]) != record["title"]:
                raise AssertionError(f"Audit title mismatch: {record['id']}")
        records = [record["id"] for record in audit["records"]]
        if len(records) != len(set(records)) or set(records) != set(positions):
            raise AssertionError(f"Audit coverage mismatch: {course_id}")
        mapped = {item for row in audit["coverage_map"] for item in row["lesson_ids"]}
        if mapped != set(positions):
            raise AssertionError(f"Source-topic mapping mismatch: {course_id}")
    return lessons


def execute_examples(lessons):
    results = []
    for course_id, meta, body in lessons:
        for number, block in enumerate(CODE.findall(body), 1):
            with tempfile.TemporaryDirectory(prefix="zhixu-computing-") as directory:
                environment = dict(os.environ, MPLBACKEND="Agg", PYTHONIOENCODING="utf-8")
                process = subprocess.run(
                    [sys.executable, "-c", block],
                    cwd=directory, env=environment, capture_output=True,
                    text=True, encoding="utf-8", errors="replace", timeout=30,
                )
            record = {
                "course": course_id, "lesson_id": meta["id"], "block": number,
                "passed": process.returncode == 0,
                "stdout": process.stdout.strip()[-2000:],
                "stderr": process.stderr.strip()[-2000:],
            }
            results.append(record)
            if process.returncode:
                raise AssertionError(json.dumps(record, ensure_ascii=False))
    return results


def verify_formulas(lessons):
    payload = []
    for _, meta, body in lessons:
        quiz = meta["quiz"]
        payload.append({
            "id": meta["id"],
            "text": "\n".join([body, quiz["question"], *quiz["options"], quiz["explanation"]]),
        })
    javascript = r"""
const fs = require('fs'), path = require('path');
const katex = require(path.resolve(process.argv[1], 'site/assets/vendor/katex/katex.min.js'));
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
let count = 0;
const failures = [];
for (const lesson of input) {
  for (const match of lesson.text.matchAll(/\$\$([\s\S]+?)\$\$|\$([^\n$]+?)\$/g)) {
    try {
      katex.renderToString(match[1] || match[2], {
        displayMode: !!match[1], throwOnError: true, strict: false, trust: false
      });
      count++;
    } catch (error) {
      failures.push({id: lesson.id, formula: match[1] || match[2], error: error.message});
    }
  }
}
process.stdout.write(JSON.stringify({lessons: input.length, formulas: count, failures}));
if (failures.length) process.exitCode = 1;
"""
    process = subprocess.run(
        ["node", "-e", javascript, str(ROOT)],
        input=json.dumps(payload, ensure_ascii=False), capture_output=True,
        text=True, encoding="utf-8", errors="replace", timeout=30,
    )
    if process.returncode:
        raise AssertionError(process.stdout + process.stderr)
    return json.loads(process.stdout)


def verify_numerical_claims(lessons):
    import numpy as np

    bodies = {meta["id"]: body for _, meta, body in lessons}
    checks = []

    def check(name, condition):
        if not bool(condition):
            raise AssertionError(name)
        checks.append(name)

    def definitions(lesson_id):
        namespace = {}
        with contextlib.redirect_stdout(io.StringIO()):
            for block in CODE.findall(bodies[lesson_id]):
                exec(compile(block, lesson_id + "-example", "exec"), namespace)
        return namespace

    bisect = definitions("python-23")["bisect_root"]
    check("bisection square-root error", abs(bisect(lambda x: x*x-2, 1, 2) - math.sqrt(2)) <= 1e-10)
    for left, right, tolerance in [(2, 1, 1e-10), (0, 1, 0), (0, float("inf"), 1e-10)]:
        try:
            bisect(lambda x: x, left, right, tolerance)
        except ValueError:
            continue
        raise AssertionError("bisection accepted invalid bounds or tolerance")
    checks.append("bisection input contract")
    sorting = definitions("python-27")
    enumerated = 0
    for length in range(6):
        for values in itertools.product([-1, 0, 1], repeat=length):
            if sorting["insertion_sort"](values) != sorted(values):
                raise AssertionError("insertion sort")
            if sorting["merge_sort"](values) != sorted(values):
                raise AssertionError("merge sort")
            enumerated += 1
    checks.append(f"sorting exhaustive small inputs ({enumerated})")
    rng = np.random.default_rng(937)
    y = rng.normal(size=8)
    c = 0.4
    check("constant squared-loss decomposition", np.isclose(
        np.sum((y-c)**2), np.sum((y-y.mean())**2) + len(y)*(y.mean()-c)**2))
    check("Bayes alarm posterior", np.isclose(
        .9*.01/(.9*.01+.05*.99), .15384615384615385))
    joint_table = np.array([[.3, .2], [.1, .4]])
    marginal_x = joint_table.sum(axis=1)
    conditional_mean = joint_table[:, 1] / marginal_x
    overall_mean = joint_table[:, 1].sum()
    within = np.sum(marginal_x * conditional_mean * (1-conditional_mean))
    between = np.sum(marginal_x * (conditional_mean-overall_mean)**2)
    check("conditional expectation and total variance", np.isclose(
        marginal_x @ conditional_mean, overall_mean)
        and np.isclose(within, .2) and np.isclose(between, .04)
        and np.isclose(within+between, overall_mean*(1-overall_mean)))
    predictions = np.array([.2, .9])
    squared_risk = sum(joint_table[x, y] * (y-predictions[x])**2
                       for x in range(2) for y in range(2))
    check("conditional-mean squared-risk decomposition", np.isclose(
        squared_risk, within+np.sum(marginal_x*(conditional_mean-predictions)**2)))
    probabilities = np.array([.009, .020, .021, .20])
    accepted = np.where(probabilities <= .05*np.arange(1, 5)/4)[0]
    check("BH step-up and Bonferroni example",
          accepted[-1]+1 == 3 and np.sum(probabilities <= .05/4) == 1)
    theta, trials = .3, 8
    successes = np.arange(trials+1)
    binomial = np.array([math.comb(trials, int(s))*theta**s*(1-theta)**(trials-s)
                         for s in successes])
    check("Bernoulli MLE exact moments", np.isclose(binomial @ (successes/trials), theta)
          and np.isclose(binomial @ (successes/trials-theta)**2, theta*(1-theta)/trials))
    X = rng.normal(size=(12, 3))
    w = rng.normal(size=3)
    target = rng.normal(size=12)
    gradient = X.T @ (X@w-target) / 12
    loss = lambda vector: np.linalg.norm(X@vector-target)**2/24
    numerical = np.array([
        (loss(w+1e-6*np.eye(3)[j])-loss(w-1e-6*np.eye(3)[j]))/2e-6
        for j in range(3)
    ])
    check("least-squares gradient", np.allclose(gradient, numerical, atol=1e-8))
    estimate = np.linalg.lstsq(X, target, rcond=None)[0]
    check("normal-equation residual orthogonality",
          np.allclose(X.T@(target-X@estimate), 0, atol=1e-10))
    penalty = .4
    ridge = np.linalg.solve(X.T@X+12*penalty*np.eye(3), X.T@target)
    check("ridge stationary equation",
          np.allclose(X.T@(X@ridge-target)/12+penalty*ridge, 0))
    for center in [-4, -1, 0, .5, 3]:
        optimum = np.sign(center)*max(abs(center)-1, 0)
        grid = np.linspace(-6, 6, 12001)
        objective = .5*(grid-center)**2+abs(grid)
        check("L1 soft threshold " + str(center),
              .5*(optimum-center)**2+abs(optimum) <= objective.min()+1e-12)
    z = .7
    probability = 1/(1+math.exp(-z))
    logistic_loss = lambda value: math.log1p(math.exp(value))-value
    check("logistic p-y derivative", math.isclose(
        (logistic_loss(z+1e-6)-logistic_loss(z-1e-6))/2e-6,
        probability-1, abs_tol=1e-9))
    q, r = np.array([.2, .8]), np.array([.5, .5])
    check("KL nonnegative example", np.sum(q*np.log(q/r)) >= 0)
    data = rng.normal(size=(10, 4))
    data -= data.mean(0)
    eigenvalues, eigenvectors = np.linalg.eigh(data.T@data/10)
    directions = eigenvectors[:, -2:]
    check("PCA reconstruction spectral identity", np.isclose(
        np.sum((data-data@directions@directions.T)**2)/10, eigenvalues[:-2].sum()))
    kernel = np.array([[1, .3], [.3, 1]])
    covariance = kernel+.25*np.eye(2)
    cross = np.array([1, .3])
    check("GP predictive variance nonnegative",
          1-cross@np.linalg.solve(covariance, cross) >= -1e-12)
    check("single-point GP posterior",
          np.isclose(2/1.25, 1.6) and np.isclose(1-1/1.25, .2))
    noise_variance, prior_variance = .25, 1.4
    bayes_cov = np.linalg.inv(X.T@X/noise_variance+np.eye(3)/prior_variance)
    bayes_mean = bayes_cov@X.T@target/noise_variance
    new_x = np.array([.5, -.2, .7])
    linear_kernel = prior_variance*X@X.T
    cross_kernel = prior_variance*X@new_x
    observation_cov = linear_kernel+noise_variance*np.eye(len(X))
    gp_mean = cross_kernel @ np.linalg.solve(observation_cov, target)
    gp_variance = prior_variance*(new_x@new_x)-cross_kernel@np.linalg.solve(observation_cov, cross_kernel)
    check("linear-kernel GP and Bayesian regression equivalence",
          np.isclose(gp_mean, new_x@bayes_mean)
          and np.isclose(gp_variance, new_x@bayes_cov@new_x)
          and gp_variance >= -1e-12)
    check("fairness conditional-rate example",
          np.isclose(.8*.1/(.8*.1+.1*.9), .47058823529411764))
    check("finite-hypothesis bound numerical value",
          abs(math.sqrt(math.log(4000)/2000)-.0644) < .0001)
    check("Poisson MLE gradient", abs(3*math.exp(math.log(4/3))-4) < 1e-12)
    check("Poisson first IRLS step", np.isclose((np.array([0, 1, 3])-1).mean(), 1/3)
          and abs(math.exp(1/3)-1.396) < .001)
    for tilt in [-3., -.5, .5, 3.]:
        mgf = (1-theta)*math.exp(-tilt*theta)+theta*math.exp(tilt*(1-theta))
        check("bounded exponential moment " + str(tilt), mgf <= math.exp(tilt*tilt/8)+1e-12)
    transition = np.array([[[.2, .8], [1, 0]], [[.6, .4], [0, 1]]])
    reward = np.array([[1, 0], [0, 2]])
    discount = .9
    bellman = lambda value: np.max(
        reward+discount*np.einsum("sak,k->sa", transition, value), axis=1)
    u, v = np.array([-1., 3.]), np.array([2., 0.])
    check("Bellman contraction example",
          np.max(abs(bellman(u)-bellman(v))) <= discount*np.max(abs(u-v))+1e-12)
    x = rng.normal(size=(4, 3))
    Q, K, values = [x@rng.normal(size=(3, 2)) for _ in range(3)]

    def softmax(matrix):
        exponent = np.exp(matrix-matrix.max(axis=1, keepdims=True))
        return exponent/exponent.sum(axis=1, keepdims=True)

    weights = softmax(Q@K.T/np.sqrt(2))
    permutation = np.array([2, 0, 3, 1])
    check("attention permutation equivariance", np.allclose(
        softmax(Q[permutation]@K[permutation].T/np.sqrt(2))@values[permutation],
        (weights@values)[permutation]))
    joint = np.array([.12, .08])
    posterior, q = joint/joint.sum(), np.array([.7, .3])
    lower_bound = np.sum(q*np.log(joint/q))
    divergence = np.sum(q*np.log(q/posterior))
    check("EM lower-bound identity",
          np.isclose(math.log(joint.sum()), lower_bound+divergence))
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, help="Optional JSON verification report.")
    arguments = parser.parse_args()
    versions = {package: importlib.metadata.version(package)
                for package in ("numpy", "pandas", "matplotlib", "scikit-learn")}
    lessons = read_lessons()
    examples = execute_examples(lessons)
    formulas = verify_formulas(lessons)
    numerical = verify_numerical_claims(lessons)
    report = {
        "python_version": sys.version.split()[0], "dependencies": versions,
        "lessons": len(lessons), "code_blocks": len(examples),
        "code_results": examples, "formula_rendering": formulas,
        "numeric_and_contract_checks": numerical,
        "notes": [
            "No external data, credentials or runtime network services used.",
            "Formula parsing and example execution do not prove all mathematics.",
            "pandas 3.0 prose was checked against official documentation; runtime version is recorded above.",
        ],
    }
    if arguments.report:
        arguments.report.parent.mkdir(parents=True, exist_ok=True)
        arguments.report.write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({
        "lessons": len(lessons), "code_blocks_passed": len(examples),
        "formulas_passed": formulas["formulas"], "numeric_and_contract_checks_passed": len(numerical),
        "dependencies": versions,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
