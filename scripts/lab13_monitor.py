"""Monitoreo mensual simulado: referencia = periodo de entrenamiento; meses de operación = periodo de prueba."""
import json
from pathlib import Path
from inf8239_u04.data import load_data, features
from inf8239_u04.governance import load_config
from inf8239_u04.monitoring import monthly_report
from inf8239_u04.pipeline import run
cfg = load_config(); m = cfg["model"]; df = load_data()
result = run(df, cfg["gates"], m["kind"], m["exclude_features"], cfg); test = result["test"]; train = df.iloc[:len(df) - len(test)]
columns = list(features(test, m["exclude_features"]).columns); thresholds = {**cfg["gates"], **cfg["monitoring"]}
report = monthly_report(train, test, result["pred"], columns, thresholds, cfg["monitoring"]["min_support"])
out = Path("reports/lab13"); report.to_csv(out / "monitoring_report.csv", index=False)
summary = {"reference": f"{train.received_date.min().date()} a {train.received_date.max().date()} (n={len(train)})",
           "thresholds": thresholds, "months_with_alerts": report.loc[report.alerts != "none", ["month", "alerts"]].to_dict("records"),
           "owner": "ML Engineer (R) · Product Owner (A)", "cadence": cfg["monitoring"]["cadence"]}
(out / "monitoring_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
print(report[["month", "n", "selection_rate", "recall_G1", "recall_G2", "recall_gap", "low_support", "alerts"]].to_string(index=False))
