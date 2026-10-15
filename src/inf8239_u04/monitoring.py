import numpy as np
import pandas as pd

def psi(reference, current, bins=10, eps=1e-4):
    """Population Stability Index: < 0.10 estable, 0.10-0.25 vigilar, > 0.25 deriva."""
    ref, cur = pd.Series(reference).dropna(), pd.Series(current).dropna()
    if ref.dtype == object or str(ref.dtype) == "category":
        cats = sorted(set(ref) | set(cur)); r = ref.value_counts(normalize=True).reindex(cats, fill_value=0); c = cur.value_counts(normalize=True).reindex(cats, fill_value=0)
    else:
        edges = np.unique(np.quantile(ref, np.linspace(0, 1, bins + 1))); edges[0], edges[-1] = -np.inf, np.inf
        r = pd.Series(np.histogram(ref, edges)[0] / len(ref)); c = pd.Series(np.histogram(cur, edges)[0] / len(cur))
    r, c = r.to_numpy() + eps, c.to_numpy() + eps
    return float(np.sum((c - r) * np.log(c / r)))

def monthly_report(reference, current, pred, columns, thresholds, min_support=30):
    """Señales de monitoreo por mes: deriva de entradas, tasa de selección y recall por grupo."""
    cur = current.assign(pred=pred, month=current.received_date.dt.to_period("M").astype(str).replace({"2026-09": "2026-10"}))
    rows = []
    for month, w in cur.groupby("month"):
        row = {"month": month, "n": len(w), "selection_rate": round(float(w.pred.mean()), 3)}
        for col in columns: row[f"psi_{col}"] = round(psi(reference[col], w[col]), 3)
        for g, gw in w.groupby("protected_group"):
            pos = gw[gw.target == 1]
            row[f"n_{g}"] = len(gw); row[f"selection_{g}"] = round(float(gw.pred.mean()), 3)
            row[f"recall_{g}"] = round(float(pos.pred.mean()), 3) if len(pos) else np.nan
        recalls = [row[k] for k in row if k.startswith("recall_") and not pd.isna(row[k])]
        row["recall_gap"] = round(max(recalls) - min(recalls), 3) if recalls else np.nan
        alerts = [f"drift:{c}" for c in columns if row[f"psi_{c}"] > thresholds["max_psi"]]
        if row["recall_gap"] > thresholds["max_recall_gap"]: alerts.append("recall_gap")
        if min(row.get(f"recall_{g}", 1) for g in ("G1", "G2")) < thresholds["min_group_recall"]: alerts.append("min_group_recall")
        row["low_support"] = any(row.get(f"n_{g}", 0) < min_support for g in ("G1", "G2"))
        row["alerts"] = ";".join(alerts) if alerts else "none"
        rows.append(row)
    return pd.DataFrame(rows)
