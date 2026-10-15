import json
from pathlib import Path
import pandas as pd
from inf8239_u04.data import load_data
from inf8239_u04.governance import load_config,validate_raci,decision_record
from inf8239_u04.pipeline import run,prioritize
cfg=load_config(); validate_raci(pd.read_csv("student_inputs/raci.csv"))
m=cfg.get("model",{}); result=run(load_data(),cfg["gates"],m.get("kind","logistic"),m.get("exclude_features",[]),cfg)
out=Path("reports/lab13"); out.mkdir(parents=True,exist_ok=True)
evidence=["reports/lab11/DECISION_RECORD.md","reports/lab12/AUDIT_REPORT.md","reports/lab13/fairness_by_group.csv","reports/lab13/prioritized_cases.csv","docs/MODEL_CARD.md","docs/RUNBOOK.md"]
(out/"deployment_decision.json").write_text(json.dumps({"metrics":result["metrics"],"gaps":result["gaps"],"resources":result["resources"],"decision":result["decision"]},indent=2),encoding="utf-8")
(out/"decision_record.json").write_text(json.dumps(decision_record(cfg,result,evidence=evidence),indent=2,ensure_ascii=False),encoding="utf-8")
result["by_group"].to_csv(out/"fairness_by_group.csv"); prioritize(result).to_csv(out/"prioritized_cases.csv",index=False)
print(result["decision"])
