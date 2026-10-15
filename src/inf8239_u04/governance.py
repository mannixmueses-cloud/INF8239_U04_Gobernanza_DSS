import hashlib, subprocess
from pathlib import Path
import pandas as pd
import yaml
from . import __version__

def load_config(path="configs/governance.yml"):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))

def validate_raci(df):
    required={"activity","R","A","C","I"}
    if required-set(df.columns): raise ValueError("RACI columns missing")
    if df[["R","A"]].fillna("").apply(lambda s:s.str.strip().eq("")).any().any(): raise ValueError("Every activity needs R and A")
    if df["A"].str.contains(r",|;|\band\b|\by\b",regex=True).any(): raise ValueError("Every activity needs exactly one Accountable")
    return True

def deployment_decision(metrics, gaps, resources, gates, model_features=None, policy=None):
    checks={
      "recall": metrics["recall"] >= gates["min_recall"],
      "recall_gap": gaps["recall_gap"] <= gates["max_recall_gap"],
      "fpr_gap": gaps["fpr_gap"] <= gates["max_fpr_gap"],
      "latency": resources["latency_ms"] <= gates["max_latency_ms"],
      "model_size": resources["model_kb"] <= gates["max_model_kb"],
    }
    if "min_group_recall" in gates: checks["min_group_recall"]=metrics["min_group_recall"] >= gates["min_group_recall"]
    if policy is not None and model_features is not None:
        banned=set(policy.get("direct_identifiers",[]))|set(policy.get("sensitive_features",[]))
        checks["privacy"]=not (banned & set(model_features))
    failed=[k for k,v in checks.items() if not v]
    status="STOP" if "privacy" in failed else "REVIEW" if failed else "GO"
    return {"status":status, "checks":checks, "failed":failed, "human_action":"Document review and final decision"}

def _git_commit():
    try: return subprocess.run(["git","rev-parse","--short","HEAD"],capture_output=True,text=True,timeout=5).stdout.strip() or "unknown"
    except Exception: return "unknown"

def decision_record(cfg, result, data_path="data/territorial_risk_synthetic.csv", evidence=()):
    """Recomendación trazable: versión, política, evidencia y acción humana."""
    d=result["decision"]
    actions={"GO":"Un responsable humano confirma la puesta en marcha y la revisión humana de cada caso sigue siendo obligatoria.",
             "REVIEW":"El Product Owner analiza la evidencia con el Data Scientist y registra su decisión; el DSS no se usa en operación hasta entonces.",
             "STOP":"Se detiene el uso del modelo, se activa la cola cronológica (baseline seguro) y se abre un incidente según docs/RUNBOOK.md."}
    return {
      "system":cfg["system_name"], "status":d["status"], "failed_gates":d["failed"], "checks":d["checks"],
      "version":{"package":__version__,"git_commit":_git_commit(),"model":result["kind"],"model_features":result["model_features"],
                 "excluded_features":result["exclude"],"data_sha256":hashlib.sha256(Path(data_path).read_bytes()).hexdigest()[:16]},
      "policy":{"purpose":cfg["purpose"],"prohibited_uses":cfg["prohibited_uses"],"gates":cfg["gates"],"accountable":cfg.get("accountable","")},
      "evidence":{"metrics":result["metrics"],"gaps":result["gaps"],"resources":result["resources"],"files":list(evidence)},
      "human_action":actions[d["status"]],
      "authority_limit":"El DSS solo prioriza la revisión. No declara emergencias, culpabilidad, elegibilidad ni intervención automática.",
    }
