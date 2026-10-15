# Traspasos entre roles

Complementa `student_inputs/raci.csv` (10 actividades, un solo Accountable cada una, validado por `validate_raci`). Regla general: **ningún traspaso se acepta sin el artefacto indicado y su criterio de aceptación**; si falta, el receptor lo devuelve y el trabajo no avanza.

| # | De (R) | A (receptor) | Artefacto que se entrega | Criterio de aceptación | Evidencia verificable |
|---|---|---|---|---|---|
| 1 | Data Engineer | Data Scientist | Dataset validado y su huella | `validate_schema` sin errores; pruebas de datos y privacidad en verde | `tests/test_data.py`, `tests/test_privacy.py`, `data_sha256` en `decision_record.json` |
| 2 | Data Scientist | Product Owner | Auditoría de equidad y decisión del LAB12 | Métricas por grupo e interseccionales con soporte; `validate_lab12_decision.py` = documented | `reports/lab12/AUDIT_REPORT.md`, `student_inputs/lab12_decision.yml` |
| 3 | Data Scientist | ML Engineer | Configuración del modelo aprobado | Modelo sin `age_band`; puertas definidas | `configs/governance.yml → model, gates` |
| 4 | ML Engineer | Product Owner | Recomendación gobernada | Todas las puertas evaluadas; ninguna oculta | `reports/lab13/deployment_decision.json`, `decision_record.json` |
| 5 | Product Owner | Institutional Owner | Decisión de despliegue para firma | GO solo si todas las puertas pasan; si no, REVIEW/STOP con justificación | `decision_record.json` (status **REVIEW**, falla `min_group_recall`) |
| 6 | ML Engineer | Product Owner | Reporte mensual de monitoreo | Ejecutado en la fecha; alertas clasificadas según el runbook | `reports/lab13/monitoring_report.csv`, `monitoring_summary.json` |
| 7 | Operator | Independent supervisor | Caso apelado | Formulario completo; el supervisor no ve la puntuación del modelo | Log de apelaciones (institucional) |
| 8 | ML Engineer | Institutional Owner | Incidente SEV1 | Escalamiento en < 24 h con evidencia preservada | `docs/RUNBOOK.md`, `reports/lab13/incidents/<id>/SHA256SUMS.txt` |
| 9 | Data Scientist | Institutional Owner | Postmortem | Causa raíz, impacto por grupo y acciones con responsable y fecha | `reports/lab13/INCIDENT_POSTMORTEM.md` |

## Autoridad para detener
- **Cualquier rol** puede pedir STOP preventivo ante un uso prohibido o una fuga de identificadores (SEV1).
- **Product Owner** decide REVIEW (Accountable de despliegue, monitoreo y revisión humana).
- **Institutional Owner** decide reactivar, limitar o retirar (Accountable de privacidad, apelación, incidentes y retiro).

## Traspaso de guardia (cambio de responsable)
Cuando cambia la persona que ocupa un rol, quien sale entrega: estado actual (`decision_record.json`), alertas abiertas (`monitoring_summary.json`), acciones correctivas pendientes (`INCIDENT_POSTMORTEM.md` §6) y accesos que deben revocarse. Quien recibe confirma por escrito antes de asumir.
