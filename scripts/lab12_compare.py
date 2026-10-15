"""LAB12: compara línea base no predictiva, logistic, tree y logistic sin age_band.

Ejecutar después de `lab12_audit.py --model logistic` y `--model tree`.
"""
import json
from pathlib import Path
import numpy as np, pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from inf8239_u04.data import load_data, features, temporal_split
from inf8239_u04.fairness import audit, intersectional, gap
from inf8239_u04.governance import load_config
from inf8239_u04.model import build_model, fit_measure

MIN_SUPPORT = 30  # mínimo de casos para interpretar un subgrupo
N_BOOT, SEED = 1000, 42
out = Path("reports/lab12"); out.mkdir(parents=True, exist_ok=True)
gates = load_config()["gates"]

def baseline_rule(df):
    """Alternativa no predictiva de LAB11: lista de verificación fija y pública."""
    return ((df.infrastructure_score < 0.30) | (df.previous_incidents >= 5)).astype(int).to_numpy()

def no_age_model():
    prep = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore"), ["zone"]),
        ("num", StandardScaler(), ["previous_incidents", "infrastructure_score", "exposure"]),
    ])
    return make_pipeline(prep, LogisticRegression(max_iter=1200, class_weight="balanced", random_state=42))

def boot_gaps(y, p, g):
    """IC 95 % bootstrap de las brechas de recall y FPR entre grupos."""
    rng = np.random.default_rng(SEED); y, p, g = map(np.asarray, (y, p, g)); res = {"recall_gap": [], "fpr_gap": []}
    def rate(yb, pb, gb, grp, label):  # recall si label=1, FPR si label=0
        mask = (gb == grp) & (yb == label); return pb[mask].mean() if mask.any() else np.nan
    for _ in range(N_BOOT):
        i = rng.integers(0, len(y), len(y)); yb, pb, gb = y[i], p[i], g[i]; groups = np.unique(gb)
        for key, label in [("recall_gap", 1), ("fpr_gap", 0)]:
            vals = [v for v in (rate(yb, pb, gb, grp, label) for grp in groups) if not np.isnan(v)]
            res[key].append(max(vals) - min(vals) if vals else 0.0)
    return {k: [round(float(np.percentile(v, 2.5)), 3), round(float(np.percentile(v, 97.5)), 3)] for k, v in res.items()}

df = load_data(); train, test = temporal_split(df); y, g = test.target, test.protected_group
preds, resources = {"baseline_rule": baseline_rule(test)}, {"baseline_rule": {"training_seconds": 0.0, "model_kb": 0.0}}
for kind in ["logistic", "tree"]:
    m = build_model(kind); resources[kind] = fit_measure(m, features(train), train.target, f"models/{kind}.joblib"); preds[kind] = m.predict(features(test))
m = no_age_model(); cols = ["zone", "previous_incidents", "infrastructure_score", "exposure"]
resources["logistic_no_age"] = fit_measure(m, train[cols], train.target, "models/logistic_no_age.joblib"); preds["logistic_no_age"] = m.predict(test[cols])

rows, inter_rows = [], []
for name, p in preds.items():
    overall, by, _ = audit(y, p, g); ci = boot_gaps(y, p, g)
    rg, fg = gap(by, "recall"), gap(by, "fpr")
    rows.append({"option": name, "accuracy": overall["accuracy"], "recall": overall["recall"], "fpr": overall["fpr"],
                 "selection_rate": overall["selection_rate"], "recall_G1": by.loc["G1", "recall"], "recall_G2": by.loc["G2", "recall"],
                 "fpr_G1": by.loc["G1", "fpr"], "fpr_G2": by.loc["G2", "fpr"], "recall_gap": rg, "recall_gap_ci95": ci["recall_gap"],
                 "fpr_gap": fg, "fpr_gap_ci95": ci["fpr_gap"], "training_seconds": resources[name]["training_seconds"], "model_kb": resources[name]["model_kb"],
                 "passes_gates": overall["recall"] >= gates["min_recall"] and rg <= gates["max_recall_gap"] and fg <= gates["max_fpr_gap"] and resources[name]["model_kb"] <= gates["max_model_kb"]})
    _, inter, _ = audit(y, p, intersectional(test))
    inter = inter.assign(option=name, sufficient_support=inter["count"] >= MIN_SUPPORT); inter_rows.append(inter)

comparison = pd.DataFrame(rows).round(4); comparison.to_csv(out / "model_comparison.csv", index=False)
inter = pd.concat(inter_rows).reset_index(names="subgroup"); inter.round(4).to_csv(out / "intersectional_support.csv", index=False)
(out / "comparison_meta.json").write_text(json.dumps({"min_support": MIN_SUPPORT, "bootstrap_samples": N_BOOT, "seed": SEED, "test_rows": len(test),
    "test_by_group": g.value_counts().to_dict(), "gates": gates,
    "subgroups_below_min_support": sorted(inter.loc[~inter.sufficient_support, "subgroup"].unique().tolist())}, indent=2), encoding="utf-8")
print(comparison[["option", "accuracy", "recall", "recall_gap", "recall_gap_ci95", "fpr_gap", "fpr_gap_ci95", "model_kb", "passes_gates"]].to_string(index=False))
