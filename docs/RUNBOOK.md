# Incident Runbook — Territorial Review DSS (synthetic)

Aplica a cualquier alerta del DSS. Los roles provienen de `student_inputs/raci.csv` y los umbrales de `configs/governance.yml`.

## Monitoreo (antes del incidente)
- **Cadencia:** mensual, con `uv run python scripts/lab13_monitor.py`. Responsable: ML Engineer. Accountable: Product Owner.
- **Referencia:** el periodo de entrenamiento (2026-01-01 a 2026-09-24, n = 480).
- **Señales por mes** (`reports/lab13/monitoring_report.csv`):
  - deriva de cada variable de entrada (PSI > 0.25);
  - tasa de selección global y por grupo;
  - recall por grupo y brecha de recall (> 0.16), y recall mínimo por grupo (< 0.68);
  - soporte: menos de 30 casos por grupo y mes se marca `low_support`, y esas métricas no se interpretan solas.
- **Resultado simulado:**
  - Desde 2026-11 hay deriva en `previous_incidents` (PSI de 0.459 y 0.405) y en `infrastructure_score` (0.303 y 0.264).
  - La tasa de selección sube de 0.433 a 0.609, sobre todo en G2 (de 0.500 a 0.812).
  - Las alertas de recall por grupo tienen soporte bajo (G2 tiene entre 16 y 22 casos por mes).
  - **Clasificación:** SEV2. Se mantiene REVIEW y se abre una investigación de deriva (acción 4 del postmortem).

1. **Detection and classification.** Las señales son:
   - una puerta fallida en `reports/lab13/deployment_decision.json` (recall < 0.68, recall de un grupo < 0.68, brecha de recall o de FPR > 0.16, latencia > 500 ms, modelo > 1024 KB o puerta `privacy`);
   - una deriva en el monitoreo mensual (cambio de la tasa de selección o del recall respecto a la referencia);
   - más del 20 % de apelaciones revocadas en un trimestre;
   - una evidencia de uso fuera de alcance o la aparición de identificadores directos.

   Severidad:
   - **SEV1:** privacidad o uso prohibido. Decisión STOP inmediata.
   - **SEV2:** falla de equidad o de desempeño. Decisión REVIEW.
   - **SEV3:** latencia o costo.

   Quién detecta: el ML Engineer (Responsible) o cualquier operador.
2. **Containment authority.**
   - Ante una SEV1, el **Institutional Owner** (Accountable) ordena detener el uso. En su ausencia, el ML Engineer puede suspender el modelo de forma preventiva y escalar en menos de 24 h.
   - Ante una SEV2 o SEV3, el **Product Owner** decide REVIEW y limita el uso a ordenar la cola con revisión humana reforzada.
   - Contención inmediata: activar la cola cronológica con lista de verificación (baseline seguro).
3. **Evidence preservation.** Antes de cambiar nada, el ML Engineer:
   - guarda `reports/lab13/deployment_decision.json`, `decision_record.json` (commit, modelo, variables y `sha256` de los datos), `fairness_by_group.csv` y `prioritized_cases.csv`;
   - crea una etiqueta de Git del estado del incidente;
   - conserva el log de decisiones y el de apelaciones.

   Los artefactos no se sobrescriben: se copian a `reports/lab13/incidents/<id>/`.
4. **Internal and affected-party communication.**
   - **Interna:** el Product Owner avisa al Institutional Owner, al Data Scientist y a Legal en menos de 24 h (SEV1) o 72 h (SEV2/3).
   - **Personas afectadas:** si su orden de revisión pudo cambiar por la falla, se las informa del incidente, de su derecho a apelar y de que su caso se revisará sin el modelo. Lo coordina el Institutional Owner con Legal.
   - **Usuarios:** los analistas reciben una instrucción escrita de usar la cola cronológica.
5. **Rollback or safe baseline.**
   - Se vuelve a la cola cronológica con lista de verificación (`infrastructure_score < 0.30` o `previous_incidents >= 5`), cuyo recall en la prueba es de 0.435 y su brecha de FPR de 0.010.
   - Si existe una versión anterior validada, se recupera por su etiqueta de Git y se vuelve a ejecutar `scripts/lab13_governance.py`, que debe dar GO o una decisión REVIEW documentada.
   - Responsable: ML Engineer. Aprueba el Product Owner.
6. **Postmortem, owner and due date.**
   - El Data Scientist redacta el postmortem en un plazo de 5 días hábiles: causa raíz, impacto por grupo, controles que fallaron y acciones correctivas, cada una con responsable y fecha.
   - El Institutional Owner lo aprueba y decide si el sistema se reactiva, se limita o se retira.
   - Se actualizan el registro de riesgos (`student_inputs/risk_register.csv`) y la Model Card.

Simulacro registrado: `reports/lab13/INCIDENT_POSTMORTEM.md`.
