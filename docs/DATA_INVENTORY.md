# Inventario de datos, minimización y retención

Sistema: *Territorial Review DSS – Synthetic*. Los datos son sintéticos; los plazos de retención se proponen **como si el sistema operara con datos reales** y deben ser aprobados por el Institutional Owner con Legal.

## 1. Inventario de campos (`data/territorial_risk_synthetic.csv`)

| Campo | Tipo / sensibilidad | Uso permitido | ¿Entra al modelo? | Decisión de minimización |
|---|---|---|---|---|
| `case_id` | Identificador seudónimo del caso | Trazabilidad, apelación | No | Se conserva solo para vincular decisión y apelación; nunca se combina con identificadores directos |
| `received_date` | Fecha de recepción | Corte temporal y monitoreo mensual | No | Se usa a nivel de mes en el monitoreo |
| `zone` | Territorio (4 zonas) · posible proxy (R05) | Modelo | Sí | Granularidad gruesa (4 zonas), sin direcciones ni coordenadas |
| `protected_group` | **Sensible** | Solo auditoría de equidad | No | Acceso restringido al Data Scientist; no se muestra en la cola del operador (`app.py`) |
| `age_band` | **Sensible** (edad en franjas) | Solo auditoría interseccional | **No** (excluida en LAB12) | Excluida por `configs/governance.yml → model.exclude_features`; la puerta `privacy` produce STOP si vuelve a entrar |
| `previous_incidents` | Historial del caso | Modelo | Sí | Conteo agregado, sin detalle de incidentes |
| `infrastructure_score` | Indicador técnico 0–1 | Modelo | Sí | — |
| `exposure` | Indicador técnico 0–1 | Modelo | Sí | — |
| `target` | Etiqueta histórica · posible sesgo (R01) | Entrenamiento y evaluación | No (es la salida) | No se usa en operación; se audita su origen |
| `name`, `document_number`, `email`, `phone` | **Identificadores directos** | Ninguno | — | **Prohibidos**: `validate_schema` rechaza el archivo antes de predecir (`tests/test_privacy.py`, `tests/test_data.py`) |

## 2. Inventario de artefactos derivados

| Artefacto | Contiene datos de casos | Se versiona en Git | Retención propuesta | Responsable de borrar |
|---|---|---|---|---|
| `data/territorial_risk_synthetic.csv` | Sí (sintéticos) | Sí (didáctico) | Duración del curso. En operación real: casos activos + 12 meses tras el cierre de la apelación, luego anonimización o agregación | Data Engineer |
| `models/*.joblib` | No (parámetros) | **No** (`.gitignore`); se regeneran | Mientras la versión esté vigente + 12 meses, identificada por commit y `sha256` de datos en `decision_record.json` | ML Engineer |
| `reports/lab12/`, `reports/lab13/fairness_by_group.csv`, `monitoring_report.csv` | No (métricas agregadas) | Sí | 5 años (rendición de cuentas) | Product Owner |
| `reports/lab13/prioritized_cases.csv` | Sí (`case_id`, fecha, zona, probabilidad; **sin** grupo ni edad) | Sí solo por ser sintético | En operación real: **no se versiona**; se conserva durante la ventana de revisión y apelación (90 días) | ML Engineer |
| Log de decisiones humanas y log de apelaciones | Sí | No (sistema institucional) | 12 meses tras la resolución de la apelación | Product Owner / Institutional Owner |
| `reports/lab13/incidents/<id>/` | Agregados + cola del momento | Sí | 5 años o hasta cerrar acciones legales | Institutional Owner |
| PDF de los Ejercicios 07 y 08 | No | **No** (`*.pdf` en `.gitignore`) | Entrega académica | Estudiante |

## 3. Reglas de minimización y retención

1. **Necesidad:** una variable entra al modelo solo si aporta utilidad medida y no es sensible (evidencia: `reports/lab12/model_comparison.csv`, donde quitar `age_band` mantiene el recall en 0.717).
2. **Separación de usos:** los atributos sensibles solo se usan para auditar, nunca para priorizar.
3. **Mínima exposición:** el operador ve `case_id`, fecha, zona, probabilidad, prioridad y acción; no ve grupo ni edad.
4. **Sin secretos ni datos personales en el repositorio:** `.streamlit/secrets.toml` y `*.pdf` están en `.gitignore`.
5. **Revisión de retención:** el Data Engineer revisa trimestralmente que se hayan borrado o agregado los datos vencidos y lo registra; el Institutional Owner aprueba excepciones.
