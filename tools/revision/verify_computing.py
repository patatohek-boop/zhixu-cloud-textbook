#!/usr/bin/env python3
"""Verify the published computing revision from this repository's actual lessons.
Run: python tools/revision/verify_computing.py
Requires the project's pinned NumPy, SciPy, and scikit-learn QA dependencies.
No network, staging files, historical Git objects, or report artifacts are needed.
"""
from pathlib import Path
from contextlib import redirect_stdout
from fractions import Fraction
from itertools import product
import hashlib
import io
import json
import math
import re
import numpy as np
from scipy import integrate, optimize, special, stats
from sklearn import metrics

ROOT = Path(__file__).resolve().parents[2]

def lesson(course, number):
    return (ROOT / 'content' / course / f'{course}-{number:02}.md').read_text(encoding='utf-8')

def snippets(text):
    return re.findall(r'```python\n(.*?)\n```', text, re.S)

def execute(code):
    namespace = {'__name__': '__main__'}
    with redirect_stdout(io.StringIO()):
        exec(compile(code, '<lesson snippet>', 'exec'), namespace)
    return namespace

def matrix_without_library(y, score, threshold):
    result = np.zeros((2, 2), dtype=int)
    for label, value in zip(y, score):
        result[int(label), int(value >= threshold)] += 1
    return result

def pair_auc(y, score):
    positives = [s for label, s in zip(y, score) if label == 1]
    negatives = [s for label, s in zip(y, score) if label == 0]
    return sum((p > n) + .5 * (p == n) for p in positives for n in negatives) / (len(positives) * len(negatives))

def grouped_ap(y, score):
    tp = fp = 0
    result = 0.
    for threshold in sorted(set(score), reverse=True):
        added = sum(label == 1 and s == threshold for label, s in zip(y, score))
        tp += added
        fp += sum(label == 0 and s == threshold for label, s in zip(y, score))
        result += added / sum(y) * tp / (tp + fp)
    return result

# Run the actual three complete statistical programs and recalculate independently.
stat_blocks = snippets(lesson('machine-learning', 3))
assert len(stat_blocks) == 3
stat_runs = [execute(code) for code in stat_blocks]
for raw, mu0, result in [([21, 22, 23, 24, 25], 20, stat_runs[0]),
                         ([18, 20, 21, 22, 24], 20, stat_runs[1])]:
    mean = sum(map(Fraction, raw)) / len(raw)
    variance = sum((Fraction(x) - mean) ** 2 for x in raw) / (len(raw) - 1)
    se = math.sqrt(variance / len(raw))
    t = float(mean - mu0) / se
    # Numerical integration of the analytic t4 density does not call the t CDF.
    p = 2 * integrate.quad(lambda z: 3/8 * (1 + z*z/4) ** (-2.5), abs(t), np.inf, epsabs=1e-13)[0]
    critical = optimize.brentq(lambda z: 2 * integrate.quad(lambda v: 3/8 * (1+v*v/4) ** (-2.5), z, np.inf)[0] - .05, 2, 4)
    expected_ci = [float(mean) - critical * se, float(mean) + critical * se]
    np.testing.assert_allclose(result['x'], raw)
    np.testing.assert_allclose(result['p'], p, rtol=1e-10, atol=1e-13)
    np.testing.assert_allclose(result.get('ci_c', result.get('ci')), expected_ci, atol=1e-9)
    np.testing.assert_allclose(stats.ttest_1samp(raw, mu0).pvalue, p, rtol=1e-10)
np.testing.assert_allclose([stat_runs[0]['mean_c'], stat_runs[0]['s_k'], stat_runs[0]['se_k'], stat_runs[0]['t_observed']],
                           [23., math.sqrt(2.5), math.sqrt(.5), math.sqrt(18)])
np.testing.assert_allclose([stat_runs[1]['s'], stat_runs[1]['se'], stat_runs[1]['t_obs']], [math.sqrt(5), 1., 1.])
p_one = integrate.quad(lambda z: 3/8 * (1 + z*z/4) ** (-2.5), math.sqrt(2), np.inf)[0]
np.testing.assert_allclose([stat_runs[2]['t_obs'], stat_runs[2]['p'], stat_runs[2]['lower']],
                           [math.sqrt(2), p_one, 21.49255668093768], atol=1e-9)
assert stat_runs[2]['p'] > .05

# Run both demonstrations and both practice solutions in the classification lesson.
classification_blocks = snippets(lesson('machine-learning', 6))
assert len(classification_blocks) == 4
classification = [execute(code) for code in classification_blocks]
score_run, pipeline_run, tie_run, frozen_run = classification
np.testing.assert_allclose(score_run['manual_fpr'], [0., 0., .5, .5, 1.])
np.testing.assert_allclose(score_run['manual_tpr'], [0., .5, .5, 1., 1.])
np.testing.assert_allclose(pair_auc(score_run['y'], score_run['s']), .75)
np.testing.assert_allclose(grouped_ap(score_run['y'], score_run['s']), 5/6)
np.testing.assert_allclose(tie_run['pair_auc'], 13/18)
np.testing.assert_allclose(pair_auc(tie_run['y'], tie_run['s']), 13/18)
for result in [score_run, tie_run]:
    for threshold in [math.inf] + sorted(set(result['s']), reverse=True):
        expected = matrix_without_library(result['y'], result['s'], threshold)
        actual = metrics.confusion_matrix(result['y'], result['s'] >= threshold, labels=[0, 1])
        np.testing.assert_array_equal(actual, expected)

# Independent scalar optimization for the symmetric one-dimensional training set.
x = np.array([-4., -3., -2., -1., 1., 2., 3., 4.])
y = np.array([0, 0, 0, 1, 0, 1, 1, 1])
scale = math.sqrt(7.5)
z = x / scale
objective = lambda w: np.sum(np.logaddexp(0, w*z) - y*w*z) + .5*w*w
optimal = optimize.minimize_scalar(objective, bracket=(.5, 1.5), method='brent', options={'xtol': 1e-13}).x
np.testing.assert_allclose(pipeline_run['X_train'].ravel(), x)
np.testing.assert_array_equal(pipeline_run['y_train'], y)
np.testing.assert_allclose(pipeline_run['model'][0].mean_, [0.])
np.testing.assert_allclose(pipeline_run['model'][0].scale_, [scale])
np.testing.assert_allclose(pipeline_run['model'][1].coef_, [[optimal]], atol=1e-6)
np.testing.assert_allclose(pipeline_run['model'][1].intercept_, [0.], atol=1e-7)
expected_probability = special.expit(optimal*np.array([-3., -.5, .5, 3.])/scale)
np.testing.assert_allclose(pipeline_run['p_test'], expected_probability, atol=1e-7)
assert pipeline_run['frozen_threshold'] == .5
np.testing.assert_allclose(pipeline_run['validation_f1'], [2/3, .8, 2/3])
np.testing.assert_array_equal(pipeline_run['matrix'], [[1, 1], [1, 1]])
np.testing.assert_allclose(pipeline_run['brier'], np.mean((expected_probability - [0, 1, 0, 1])**2), atol=1e-8)
assert frozen_run['chosen'] == .4
np.testing.assert_array_equal(frozen_run['matrix'], [[1, 1], [1, 1]])
np.testing.assert_allclose(pair_auc(frozen_run['y_test'], frozen_run['s_test']), .5)
# Small exhaustive check: all 4-record binary labelings with both classes, all score ties.
auc_cases = 0
for labels in product([0, 1], repeat=4):
    if sum(labels) in (0, 4):
        continue
    for scores in product([0., .5, 1.], repeat=4):
        np.testing.assert_allclose(pair_auc(labels, scores), metrics.roc_auc_score(labels, scores))
        np.testing.assert_allclose(grouped_ap(labels, scores), metrics.average_precision_score(labels, scores))
        auc_cases += 1

# Preserve the old CSV analyzer exactly, and check the new specification against it.
project_blocks = snippets(lesson('python', 25))
assert len(project_blocks) == 2
assert hashlib.sha256(project_blocks[0].encode()).hexdigest() == 'd303b8ba63d02bda334c97dea688440cbb824979ad3b549494e91dd4b0676595'
original = execute(project_blocks[0])['analyze']
modified = execute(project_blocks[1])['analyze_with_threshold']
project_cases = 0
for values in product([-273.15, 0., 21., 22., 23.], repeat=3):
    text = 'sensor,temp_c\n' + ''.join(f'A,{value}\n' for value in values)
    for threshold in [-273.15, 0., 22., 100.]:
        report = modified(text, threshold_c=threshold)
        row = report['summary'][0]
        assert row['high_count'] == len([x for x in values if x >= threshold])
        np.testing.assert_allclose(row['mean_c'], float(sum(Fraction(str(x)) for x in values)/3))
        assert row['count'] == 3
        projection = {'summary': [{k: v for k, v in entry.items() if k != 'high_count'} for entry in report['summary']], 'errors': report['errors']}
        assert projection == original(text)
        project_cases += 1
for text in ['sensor,temp_c\n', 'sensor,temp_c\n"A\nA",22\nB,25,extra\nC\nD,-300\n', 'sensor,temp_c\nA,NaN\nB,inf\n,20\n']:
    report = modified(text)
    projection = {'summary': [{k: v for k, v in entry.items() if k != 'high_count'} for entry in report['summary']], 'errors': report['errors']}
    assert projection == original(text)
# A deliberately wrong > implementation must fail the threshold equality contract.
wrong_code = project_blocks[1].split('text = "sensor,temp_c', 1)[0].replace('value >= threshold_c', 'value > threshold_c')
wrong = execute(wrong_code)['analyze_with_threshold']
assert wrong('sensor,temp_c\nA,22\n')['summary'][0]['high_count'] == 0
assert modified('sensor,temp_c\nA,22\n')['summary'][0]['high_count'] == 1

# ML47's published implementation remains unchanged; verify live numerical results.
research_blocks = snippets(lesson('machine-learning', 47))
assert len(research_blocks) == 1
assert hashlib.sha256(research_blocks[0].encode()).hexdigest() == 'dcebe3bf74aa28bdd962b88e2474a661e7ccd4e71b3657874fe1a5dc50c5e258'
research = execute(research_blocks[0])
np.testing.assert_allclose([research['beta_hat'], research['h_hat']], [.001002, 18.036], atol=1e-12)
assert research['pure'][1] == research['physical'][1] == 5
assert research['physical'][2] == .01
observed = [research['rmse'](predict, research['test']) for _, predict in research['models']]
np.testing.assert_allclose(observed, [.27425, .27657, .27574, .51370], atol=5e-6)
# Independently compare the published stacked residual with all three loss terms.
rng = np.random.default_rng(47)
for lam in [0., .01, 3.]:
    phi, residual = rng.normal(size=(7, 3)), rng.normal(size=(5, 3))
    w, y, s = rng.normal(size=3), rng.normal(size=7), rng.uniform(.5, 2., size=7)
    gamma, eta = 1.1, .02
    matrix = np.vstack([s[:, None]*phi/math.sqrt(7), math.sqrt(lam/5)*residual, math.sqrt(eta)*np.eye(3)])
    rhs = np.r_[s*(y-1)/math.sqrt(7), -gamma*math.sqrt(lam/5)*np.ones(5), np.zeros(3)]
    direct = sum((s[i]*(1+sum(phi[i, j]*w[j] for j in range(3))-y[i]))**2 for i in range(7))/7
    direct += lam*sum((gamma+sum(residual[i, j]*w[j] for j in range(3)))**2 for i in range(5))/5 + eta*sum(w*w)
    np.testing.assert_allclose(sum((matrix@w-rhs)**2), direct)
print(json.dumps({'status': 'passed', 'actual_lesson_blocks_executed': 10, 'auc_ap_cases': auc_cases, 'project_cases': project_cases,
                  'statistical_integral_and_interval': True, 'independent_classifier_fit': True,
                  'original_project_and_ml47_code_preserved': True}, ensure_ascii=False))
