# Declaración de uso de IA

## Herramienta
Claude (Anthropic), modelo Opus 5.5, usado mediante Claude Code en la aplicación de escritorio.

## Finalidad
Apoyo en el LAB11 (evaluación de impacto ético) para:
- leer el manual de laboratorio y planificar los pasos;
- preparar el entorno (`uv sync --frozen`, `git init`, pruebas y comprobación del entorno);
- detectar y corregir errores en los scripts del proyecto base;
- redactar una propuesta inicial de la ficha de impacto, los actores, el registro de riesgos y el registro de decisión.

Prompts textuales usados con Claude:
- «que necesitas para trabajar estra practica» (junto con el manual del LAB11);
- el envío del zip `INF8239_U04_Gobernanza_DSS_Proyecto_Base_uv.zip` y del enlace a mi perfil de GitHub para que hiciera la práctica.

## Fragmentos afectados
- `student_inputs/lab11_impact.yml`, `student_inputs/stakeholders.csv` y `student_inputs/risk_register.csv`: borrador redactado por la IA a partir del caso sintético y del perfil del dataset.
- `reports/lab11/DECISION_RECORD.md`: borrador de la decisión REVIEW y de su justificación.
- `scripts/lab11_impact.py` y `scripts/simulate_incident.py`: corrección de errores de sintaxis.
- `README.md`: estado de los laboratorios, resumen del LAB11 e instrucciones de ejecución.

## Errores detectados y correcciones
- `scripts/lab11_impact.py` y `scripts/simulate_incident.py` del proyecto base fallaban con `SyntaxError`, porque usaban cadenas normales que ocupaban varias líneas. Se corrigieron en un commit aparte (`fix: repair multi-line strings…`).
- `lab11_impact.py` sobrescribía `DECISION_RECORD.md` en cada ejecución. Ahora conserva el archivo si ya existe.
- Al perfilar los datos se encontró que `age_band` está declarada como sensible en `configs/governance.yml` pero el modelo la usa como predictor. Esto se registró como riesgo R02 y no se modificó el código del modelo.

## LAB12 · Auditoría de equidad

Prompts textuales usados con Claude:
- «que necesitas para hacer el U04.LAB12» (junto con el manual del LAB12);
- «Sí, haz el LAB12 con lo que propones: línea base no predictiva, mínimo de 30 casos por subgrupo, y sin commits; dame los comandos al final.»

Fragmentos afectados:
- `scripts/lab12_compare.py`: script nuevo escrito por la IA. Compara la línea base no predictiva, la regresión logística, el árbol y la logística sin `age_band`, calcula IC 95 % bootstrap de las brechas y marca los subgrupos con menos de 30 casos.
- `student_inputs/lab12_decision.yml`, `reports/lab12/AUDIT_REPORT.md` y la sección LAB12 del `README.md`: borradores redactados por la IA a partir de los resultados generados.

Errores detectados y correcciones:
- La primera versión del bootstrap usaba `MetricFrame` en cada remuestreo y tardaba unos 4 minutos. Se reemplazó por un cálculo directo con numpy; se obtuvieron los mismos resultados en unos 8 segundos.

Verificaciones humanas del LAB12:
<!-- El estudiante debe completar o confirmar esta sección antes de entregar. -->
- [x] Ejecuté `lab12_audit.py` con los dos modelos, `lab12_compare.py` y `validate_lab12_decision.py`, y comprobé que las cifras del informe coinciden con los CSV.
- [x] Revisé que el mínimo de 30 casos y los subgrupos sin soporte estén bien interpretados.
- [x] Estoy de acuerdo con la decisión REVIEW y con preferir la logística sin `age_band`, o la cambié con mi propia justificación.

## Verificaciones humanas (LAB11)
<!-- El estudiante debe completar o confirmar esta sección antes de entregar. -->
- [x] Revisé y ajusté al caso el propósito, la alternativa no predictiva, la condición de retiro y la apelación.
- [x] Revisé la probabilidad, el impacto y el responsable de cada uno de los 9 riesgos.
- [x] Confirmé que estoy de acuerdo con la decisión REVIEW o la cambié con mi propia justificación.
- [x] Ejecuté `uv run python scripts/lab11_impact.py` y `uv run pytest -q` y obtuve resultados en verde.

## Ejercicio 07 · Síntesis PDF

Prompts textuales usados con Claude:
- «el LAB11 y LAB12, cumplen con este mandato» (junto con el mandato de la Unidad 04);
- «agrega la sección Observación / Evidencia / Interpretación / Decisión al DECISION_RECORD del LAB11 y al AUDIT_REPORT del LAB12»;
- «hacer lo que pide para el Ejercicio 07» (junto con el mandato y la rúbrica del ejercicio).

Fragmentos afectados:
- `docs/ejercicio07/INF8239_U04_E07_Mueses.html` (fuente editable) y el PDF generado a partir de ella, que se entrega en el aula virtual y no se versiona: estructura y redacción hechas por la IA. Todas las cifras se copiaron de los archivos de `reports/lab11/` y `reports/lab12/`.
- La sección "Regla de interpretación" de `reports/lab11/DECISION_RECORD.md` y `reports/lab12/AUDIT_REPORT.md`.
- La tabla de marco normativo (obligación legal, marco voluntario y recomendación ética): propuesta de la IA que el estudiante debe verificar en las fuentes oficiales.

Correcciones:
- La primera versión del PDF tenía saltos de página forzados que dejaban una página casi vacía. Se quitaron y el documento pasó de 8 a 6 páginas.

Verificaciones humanas del Ejercicio 07:
<!-- El estudiante debe completar o confirmar esta sección antes de entregar. -->
- [x] Verifiqué en las fuentes oficiales los artículos 39, 44 y 70 de la Constitución, la Ley 172-13, la Ley 200-04, la ENIA y el AI Act citados en la sección 4.
- [x] Revisé que las cifras del PDF coinciden con `reports/lab12/model_comparison.csv` y `reports/lab12/logistic/fairness_by_group.csv`.
- [x] Estoy de acuerdo con la decisión final MODIFICAR y LIMITAR, o la cambié con mi propia justificación.

## LAB13 · Gobernanza y DSS responsable

Prompts textuales usados con Claude:
- «que necesitas para hacer el lab13» (junto con el manual del LAB13);
- las decisiones elegidas por el estudiante: modelo «Sin age_band», «Sí, agregarlo» (trazabilidad y prioridad por caso) y publicación «Solo local»;
- «Sí, haz el LAB13 con esas decisiones. Sin commits; al final dame los comandos, incluida la etiqueta u04-lab13.»

Fragmentos afectados (escritos por la IA):
- Código: `src/inf8239_u04/data.py`, `model.py`, `pipeline.py` y `governance.py`; `app.py`; `scripts/lab13_governance.py` y `scripts/simulate_incident.py`; `configs/governance.yml`.
- Pruebas nuevas: `tests/test_dss.py` (9 pruebas).
- Documentos: `student_inputs/raci.csv`, `docs/MODEL_CARD.md`, `docs/RUNBOOK.md`, `docs/DATASET_CARD.md`, `reports/lab13/INCIDENT_POSTMORTEM.md`, la sección LAB13 del `README.md` y `requirements.txt` (generado con `uv export`).

Decisiones de valor tomadas por el estudiante: excluir `age_band`, agregar la trazabilidad y la cola priorizada, y no publicar en la nube. La IA propuso la puerta `min_group_recall` ≥ 0.68 a partir de la condición del LAB12 y fijó que una falla de privacidad produzca STOP.

Verificaciones y correcciones:
- Se comprobó que los cambios al código no alteran los resultados del LAB12: la logística con `age_band` da las mismas métricas y solo varía el tiempo de entrenamiento.
- La puerta `min_group_recall` produce REVIEW con la evidencia real (G1 = 0.653), coherente con la decisión del LAB12. El simulacro usa esa señal real y no un texto fijo.
- `simulate_incident.py` sobrescribía el postmortem en cada ejecución; ahora lo conserva.

Verificaciones humanas del LAB13:
<!-- El estudiante debe completar o confirmar esta sección antes de entregar. -->
- [x] Ejecuté `lab13_governance.py`, `simulate_incident.py`, `streamlit run app.py` y `pytest -q` (19 passed), y revisé el tablero.
- [x] Revisé el RACI, la Model Card, el Runbook y el postmortem, incluidos sus responsables y fechas.
- [x] Estoy de acuerdo con las puertas nuevas (`min_group_recall` y `privacy`) y con la decisión REVIEW, o las cambié con mi propia justificación.

## Ejercicio 08 · Expediente de gobernanza y simulacro

Prompts textuales usados con Claude:
- «que mas queda por hacer del lab13»;
- «si lab13 dices que ya esta completo, pues procede con lo indicado y hazme el documento pdf sin fecha de entrega» (junto con el mandato y la rúbrica del Ejercicio 08).

Fragmentos afectados (escritos por la IA):
- Monitoreo: `src/inf8239_u04/monitoring.py`, `scripts/lab13_monitor.py`, la sección `monitoring` de `configs/governance.yml` y `tests/test_monitoring.py` (2 pruebas). Genera `reports/lab13/monitoring_report.csv` y `monitoring_summary.json`.
- Documentos: `docs/DATA_INVENTORY.md`, `docs/RACI_HANDOFFS.md`, la sección "Monitoreo" de `docs/RUNBOOK.md`, los enlaces añadidos en la Model Card y la Dataset Card, y la sección del Ejercicio 08 del `README.md`.
- `docs/ejercicio08/INF8239_U04_E08_Mueses.html` (fuente editable) y el PDF generado a partir de ella. El PDF no tiene fecha de entrega ni fechas en sus metadatos, se entrega en el aula virtual y no se versiona.

Valores propuestos por la IA que el estudiante debe aprobar: los plazos de retención, el umbral de deriva PSI > 0.25 y el mínimo de 30 casos por grupo y mes.

Verificaciones y correcciones:
- Las cifras del monitoreo provienen de `reports/lab13/monitoring_report.csv`. Las alertas de recall por grupo se presentan con soporte bajo, no como conclusiones.
- La primera versión del PDF dejaba el título de la sección 4 separado de su tabla y partía los meses en dos líneas; se corrigió.

Verificaciones humanas del Ejercicio 08:
<!-- El estudiante debe completar o confirmar esta sección antes de entregar. -->
- [ ] Revisé y apruebo los plazos de retención de `docs/DATA_INVENTORY.md` y los traspasos de `docs/RACI_HANDOFFS.md`.
- [ ] Ejecuté `lab13_monitor.py` y `pytest -q` (21 passed), y las cifras del PDF coinciden con los CSV.
- [ ] Verifiqué en sus fuentes oficiales la Ley 172-13, los arts. 44 y 70 de la Constitución, la Ley 200-04 e ISO/IEC 42001.
- [ ] Estoy de acuerdo con la decisión final LIMITAR y MODIFICAR, o la cambié con mi propia justificación.

## Responsabilidad asumida
La responsabilidad final sobre el contenido entregado, la verificación de resultados y la decisión ética recae completamente en el estudiante.
