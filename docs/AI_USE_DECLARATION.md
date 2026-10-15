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

## Responsabilidad asumida
La responsabilidad final sobre el contenido entregado, la verificación de resultados y la decisión ética recae completamente en el estudiante.
