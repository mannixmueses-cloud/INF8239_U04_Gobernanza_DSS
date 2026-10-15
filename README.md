# INF-8239 · Unidad 04 · Gobernanza y DSS responsable

- **Asignatura:** INF-8239 Ciencia de Datos II
- **Unidad:** 04 · Ética y roles en Ciencia de Datos
- **Estudiante:** Manicaotex Mueses Ruiz
- **Repositorio:** https://github.com/mannixmueses-cloud/INF8239_U04_Gobernanza_DSS

Proyecto base acumulativo para LAB11–13. El estudiante completa archivos pequeños en `student_inputs/`, ejecuta scripts y concentra su esfuerzo en interpretar y justificar decisiones.

## Estado de los laboratorios

| Laboratorio | Tema | Estado |
|---|---|---|
| U04.LAB11 | Evaluación de impacto ético | ✅ Completo, decisión **REVIEW** |
| U04.LAB12 | Auditoría de equidad con Fairlearn | ⏳ Pendiente |
| U04.LAB13 | Gobernanza y DSS responsable con Streamlit | ⏳ Pendiente |

## Inicio

Ejecute los comandos **dentro de esta carpeta** (`INF8239_U04_Gobernanza_DSS`). Si se ejecutan desde una carpeta superior, `uv` puede tomar otro `pyproject.toml`.

```bash
uv sync --frozen
uv run pytest -q
uv run python scripts/check_environment.py
```

Resultado esperado: `10 passed` y `{'python_project': 'ok', 'dataset_status': 'valid', 'rows': 640, 'columns': 9}`.

> Si se renombra o mueve la carpeta, el entorno `.venv` conserva la ruta anterior. Se repara con `uv sync --frozen --reinstall`.

## Ruta
```bash
uv run python scripts/lab11_impact.py
uv run python scripts/lab12_audit.py --model logistic
uv run python scripts/lab13_governance.py
uv run streamlit run app.py
```

## LAB11 · Evaluación de impacto ético

**Caso:** *Territorial Review DSS - Synthetic*. El sistema ordena la cola de casos territoriales sintéticos para revisión humana. No decide intervenciones, elegibilidad ni emergencias.

### Insumos completados

| Archivo | Contenido |
|---|---|
| `student_inputs/lab11_impact.yml` | Propósito, decisión asistida, usuarios, población afectada, propietario, alternativa no predictiva, uso fuera de alcance, condición de retiro y mecanismo de apelación |
| `student_inputs/stakeholders.csv` | Beneficio, daño, poder y participación de los 4 actores |
| `student_inputs/risk_register.csv` | 9 riesgos con escenario, afectado, probabilidad, impacto, control, responsable, evidencia y riesgo residual |

### Evidencia generada (`reports/lab11/`)

| Salida | Descripción |
|---|---|
| `risk_register_scored.csv` | Riesgos ordenados por prioridad (probabilidad × impacto) |
| `rmf_summary.json` | Resumen NIST AI RMF (GOVERN, MAP, MEASURE, MANAGE) |
| `stakeholders.csv` | Copia validada de los actores |
| `DECISION_RECORD.md` | Decisión justificada con evidencia, incertidumbre, responsable y condición de retiro |

### Riesgos prioritarios

| ID | Riesgo | Prioridad |
|---|---|---|
| R01 | La etiqueta histórica está sesgada contra G2 (tasa positiva de 0.64 frente a 0.50 en G1) | 16 |
| R03 | Sesgo de automatización y desvío hacia usos prohibidos | 12 |
| R02 | `age_band` está declarada sensible pero se usa como predictor | 12 |

### Decisión: REVIEW

Se continúa solo hacia la fase de medición (LAB12), sin desplegar. Para pasar a GO hace falta verificar recall ≥ 0.68 y brechas de recall y FPR ≤ 0.16 entre grupos, comparar el modelo con y sin `age_band`, superar la línea base no predictiva y tener operativos el log de decisiones y la apelación. Ver [`reports/lab11/DECISION_RECORD.md`](reports/lab11/DECISION_RECORD.md).

### Correcciones al proyecto base

`scripts/lab11_impact.py` y `scripts/simulate_incident.py` fallaban con `SyntaxError` por cadenas de texto que ocupaban varias líneas. Se corrigieron, y `lab11_impact.py` ahora conserva un `DECISION_RECORD.md` existente en lugar de sobrescribirlo.

## Estructura

```
configs/          umbrales de gobernanza y usos prohibidos
data/             dataset sintético (640 casos)
docs/             Dataset Card, Model Card, Runbook y declaración de uso de IA
reports/lab11-13/ evidencia generada por cada laboratorio
scripts/          scripts de cada laboratorio
src/inf8239_u04/  código del paquete (datos, modelo, equidad, gobernanza, impacto)
student_inputs/   archivos que completa el estudiante
tests/            pruebas automatizadas
```

## Uso de IA

Ver [`docs/AI_USE_DECLARATION.md`](docs/AI_USE_DECLARATION.md).

## Aviso

Los datos son sintéticos y didácticos. El sistema no autoriza decisiones automáticas sobre personas.

