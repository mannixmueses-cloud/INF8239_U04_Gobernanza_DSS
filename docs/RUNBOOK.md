# Incident Runbook — Territorial Review DSS (synthetic)

Aplica a cualquier alerta del DSS. Los roles provienen de `student_inputs/raci.csv` y los umbrales de `configs/governance.yml`.

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
