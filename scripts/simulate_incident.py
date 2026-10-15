import json
from datetime import datetime,timezone
from pathlib import Path
decision=Path("reports/lab13/deployment_decision.json")
failed=json.loads(decision.read_text(encoding="utf-8"))["decision"]["failed"] if decision.exists() else []
signal=f"failed gates: {', '.join(failed)}" if failed else "recall gap exceeded"
text=f"""# Incident simulation

- detected_at: {datetime.now(timezone.utc).isoformat()}
- signal: {signal}
- containment: REVIEW and safe baseline
- evidence: preserved report and model version
- communication: REPLACE
- corrective actions, owners and dates: REPLACE
"""
path=Path("reports/lab13/INCIDENT_POSTMORTEM.md"); path.parent.mkdir(parents=True,exist_ok=True)
if path.exists(): print(f"{path} already exists; not overwritten")
else: path.write_text(text,encoding="utf-8"); print(path)
