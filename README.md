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
| U04.LAB12 | Auditoría de equidad con Fairlearn | ✅ Completo, decisión **REVIEW** |
| **Ejercicio 07** | Evaluación de impacto y auditoría de equidad (integra LAB11 y LAB12) | ✅ PDF entregado en el aula virtual, decisión **MODIFICAR y LIMITAR** |
| U04.LAB13 | Gobernanza y DSS responsable con Streamlit | ⏳ Pendiente |

**Ejercicio 07:** el PDF de síntesis se entrega en el aula virtual y **no se versiona** en este repositorio (`*.pdf` está en `.gitignore`). Su fuente editable está en [`docs/ejercicio07/INF8239_U04_E07_Mueses.html`](docs/ejercicio07/INF8239_U04_E07_Mueses.html). Para regenerar el PDF, abra el HTML en el navegador e imprímalo como PDF (tamaño Carta, sin encabezados).

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
uv run python scripts/lab12_audit.py --model tree
uv run python scripts/lab12_compare.py
uv run python scripts/validate_lab12_decision.py
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

## LAB12 · Auditoría de equidad con Fairlearn

Audita el clasificador por grupo (`protected_group`) y por intersección grupo × edad. El atributo sensible se usa solo para auditar y no entra al modelo. El conjunto de prueba es el 25 % final en orden temporal: 160 casos (G1 = 101, G2 = 59).

### Comparación de alternativas (`reports/lab12/model_comparison.csv`)

| Opción | Recall | Brecha de recall | Brecha de FPR | Tamaño | Umbrales |
|---|---|---|---|---|---|
| Línea base no predictiva | 0.435 | 0.144 | 0.010 | 0 KB | ❌ recall |
| Regresión logística | 0.717 | 0.138 | 0.125 | 3.6 KB | ✅ |
| Árbol de decisión | 0.717 | 0.181 | 0.168 | 7.9 KB | ❌ brechas |
| Logística sin `age_band` | 0.717 | 0.138 | 0.144 | 3.3 KB | ✅ |

Umbrales (`configs/governance.yml`): recall ≥ 0.68 y brechas ≤ 0.16. Los IC 95 % bootstrap de todas las brechas superan 0.16, porque la muestra de prueba es pequeña.

### Hallazgos

- El promedio oculta una falla localizada: el recall de G1 es 0.653, por debajo del mínimo, frente a 0.791 en G2. G2 recibe más falsos positivos (FPR de 0.375 frente a 0.250).
- Solo 1 de los 8 subgrupos grupo × edad (G1 \| 45-59, n = 35) alcanza el mínimo de **30 casos**. Los demás se reportan, pero no se interpretan.
- El árbol no mejora el recall, aumenta las brechas y pesa el doble, así que no se justifica (Green AI).
- Quitar `age_band` mantiene el recall y reduce el tamaño del modelo, lo que sirve de control para el riesgo R02.
- Las brechas indican algo a investigar, no prueban discriminación causal: la etiqueta puede estar sesgada, hay proxies, los IC son anchos y hay un único corte temporal.

### Decisión: REVIEW

Se descarta el árbol y la candidata preferida es la regresión logística sin `age_band`. Antes de GO hacen falta más datos para estrechar los IC, recall de G1 ≥ 0.68 y revisión del origen de la etiqueta. Ver [`reports/lab12/AUDIT_REPORT.md`](reports/lab12/AUDIT_REPORT.md) y [`student_inputs/lab12_decision.yml`](student_inputs/lab12_decision.yml).

### Evidencia generada (`reports/lab12/`)

| Salida | Descripción |
|---|---|
| `logistic/`, `tree/` | Métricas globales, por grupo e interseccionales de cada modelo (`lab12_audit.py`) |
| `model_comparison.csv` | Comparación de línea base, logistic, tree y logistic sin `age_band`: utilidad, brechas con IC 95 %, tiempo y tamaño |
| `intersectional_support.csv` | Métricas grupo × edad con la columna `sufficient_support` (n ≥ 30) |
| `comparison_meta.json` | Mínimo de soporte, semilla, bootstrap, tamaños de prueba y subgrupos sin soporte |
| `AUDIT_REPORT.md` | Informe completo con interpretación y decisión |

`scripts/lab12_compare.py` se agregó al proyecto base para cubrir la línea base y los intervalos de confianza que pide el checklist.

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

