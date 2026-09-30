import math
import numpy as np

SEED = 20260930
MASS, CP, AREA, H_TRUE = 0.2, 900.0, 0.01, 18.0
CAPACITY = MASS * CP
T_SCALE = 1000.0
BETA_TRUE = H_TRUE * AREA / CAPACITY
TIME = np.linspace(0.0, 1800.0, 19)
DEGREES = (2, 3, 4, 5)
LAMBDAS = (1e-4, 1e-2, 1.0, 100.0)
RIDGE = 1e-8


def make_runs():
    rng = np.random.default_rng(SEED)
    runs = []
    for run_id in range(24):
        t0 = 80.0 + rng.uniform(-5.0, 5.0)
        ta = 20.0 + rng.uniform(-2.0, 2.0)
        truth = ta + (t0 - ta) * np.exp(-BETA_TRUE * TIME)
        run_bias = rng.normal(0.0, 0.25)
        observed = truth + run_bias + rng.normal(0.0, 0.20, TIME.size)
        runs.append(dict(id=run_id, t0=t0, ta=ta,
                         y=observed, truth=truth))
    return runs


runs = make_runs()  # All data in this program are SYNTHETIC.
order = np.random.default_rng(SEED + 1).permutation(len(runs))
train_ids, val_ids, test_ids = order[:14], order[14:19], order[19:]
assert set(train_ids).isdisjoint(val_ids)
assert set(train_ids).isdisjoint(test_ids)
assert set(val_ids).isdisjoint(test_ids)
train = [runs[int(i)] for i in train_ids]
valid = [runs[int(i)] for i in val_ids]
test = [runs[int(i)] for i in test_ids]


def rmse(predict_u, selected_runs, target="y"):
    # Equal weight per run, then equal weight per time within each run.
    per_run = []
    for run in selected_runs:
        prediction = run["ta"] + (run["t0"] - run["ta"]) * predict_u(TIME)
        per_run.append(np.mean((prediction - run[target]) ** 2))
    return math.sqrt(float(np.mean(per_run)))


# Fit the one-parameter physical baseline using TRAIN only.
gamma_grid = np.linspace(0.4, 1.6, 601)
train_errors = [rmse(lambda t, g=g: np.exp(-g * t / T_SCALE), train)
                for g in gamma_grid]
gamma_hat = float(gamma_grid[int(np.argmin(train_errors))])
beta_hat = gamma_hat / T_SCALE
h_hat = beta_hat * CAPACITY / AREA


def basis(x, degree):
    powers = np.arange(1, degree + 1)
    return x[:, None] ** powers[None, :]


def fit_proxy(degree, lam, gamma):
    x = np.tile(TIME / T_SCALE, len(train))
    y = np.concatenate([(r["y"] - r["ta"]) / (r["t0"] - r["ta"])
                        for r in train])
    phi = basis(x, degree)
    sample_scale = np.repeat([r["t0"] - r["ta"] for r in train], TIME.size) / 60.0
    z = np.linspace(0.0, TIME[-1] / T_SCALE, 81)
    powers = np.arange(1, degree + 1)
    derivative = powers[None, :] * z[:, None] ** (powers[None, :] - 1)
    residual_matrix = derivative + gamma * basis(z, degree)
    matrix = np.vstack([sample_scale[:, None] * phi / math.sqrt(x.size),
                        math.sqrt(lam / z.size) * residual_matrix,
                        math.sqrt(RIDGE) * np.eye(degree)])
    rhs = np.concatenate([sample_scale * (y - 1.0) / math.sqrt(x.size),
                          -gamma * math.sqrt(lam / z.size) * np.ones(z.size),
                          np.zeros(degree)])
    weights = np.linalg.lstsq(matrix, rhs, rcond=None)[0]

    def predict(t):
        return 1.0 + basis(np.asarray(t) / T_SCALE, degree) @ weights

    return predict, weights


# Validation chooses the degree for each family, and lambda for physics.
def select(candidates):
    results = []
    for degree, lam in candidates:
        predict, weights = fit_proxy(degree, lam, gamma_hat)
        results.append((rmse(predict, valid), degree, lam, predict, weights))
    return min(results, key=lambda item: (item[0], item[1], item[2]))


pure = select([(degree, 0.0) for degree in DEGREES])
physical = select([(degree, lam) for degree in DEGREES for lam in LAMBDAS])
wrong_predict, wrong_weights = fit_proxy(physical[1], physical[2], 1.6 * gamma_hat)
models = [
    ("ODE baseline", lambda t: np.exp(-beta_hat * np.asarray(t))),
    ("data proxy", pure[3]),
    ("physics proxy", physical[3]),
    ("wrong physics", wrong_predict),
]

print("SYNTHETIC ONLY; NumPy", np.__version__, "seed", SEED)
print("train / validation / test run IDs:")
print(train_ids.tolist(), val_ids.tolist(), test_ids.tolist())
print("beta_hat [1/s] = %.6f; h_hat [W/(m^2 K)] = %.3f" % (beta_hat, h_hat))
print("data degree =", pure[1])
print("physics degree, lambda =", physical[1], physical[2])
print("model | validation K | test observed K | test latent K")
# These test evaluations occur AFTER selection; do not use them to retune.
for name, predict in models:
    print("%s | %.5f | %.5f | %.5f" %
          (name, rmse(predict, valid), rmse(predict, test),
           rmse(predict, test, target="truth")))

# A prespecified time-extrapolation failure test, using the same physical law.
future_t = np.linspace(2000.0, 4000.0, 21)
future_true = np.exp(-BETA_TRUE * future_t)
# A different h has NOT been supplied as an input to any model.
ood_true = np.exp(-1.6 * BETA_TRUE * TIME)
print("model | future 2000-4000s K | unseen h=28.8 K")
for name, predict in models:
    future_error = 60.0 * np.sqrt(np.mean((predict(future_t) - future_true) ** 2))
    ood_error = 60.0 * np.sqrt(np.mean((predict(TIME) - ood_true) ** 2))
    print("%s | %.5f | %.5f" % (name, future_error, ood_error))

# One measurement in a NEW independent run, equal temperature noise variance.
# This is a local, one-parameter design calculation, not a global optimum.
candidate_t = np.linspace(100.0, 1800.0, 171)
sensitivity = 60.0 * candidate_t * np.exp(-beta_hat * candidate_t)
best_time = float(candidate_t[int(np.argmax(sensitivity ** 2))])
print("next-run single measurement time [s] =", best_time)
print("continuous sensitivity optimum [s] =", 1.0 / beta_hat)
print("reference T(1000s) [C] =", 20.0 + 60.0 / math.e)
