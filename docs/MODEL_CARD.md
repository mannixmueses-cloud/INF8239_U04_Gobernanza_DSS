# Model Card — Territorial Review DSS (synthetic)

> Formato basado en Mitchell et al. (2019), *Model Cards for Model Reporting*. Datos sintéticos y didácticos.

## Intended use
Ordenar la cola de casos territoriales **sintéticos** para que un analista humano revise primero los que muestran mayor señal de riesgo de infraestructura. La salida por caso es una probabilidad, una prioridad (Alta ≥ 0.70, Media ≥ 0.50, Baja < 0.50) y una acción recomendada que **siempre** es una forma de revisión humana (`reports/lab13/prioritized_cases.csv`).

- **Usuarios:** analistas territoriales y su supervisor.
- **Decisión asistida:** qué caso se revisa primero. Inspeccionar, intervenir o descartar sigue siendo una decisión humana registrada.

## Out-of-scope use
- Intervención automática, decisiones de elegibilidad para ayudas o servicios y declaración de emergencia (`configs/governance.yml`).
- Perfilamiento de personas o grupos, y priorizar usando `protected_group` o `age_band`.
- Cualquier inferencia sobre poblaciones reales de la República Dominicana.

## Data and split
- **Datos:** `data/territorial_risk_synthetic.csv`, con 640 casos sintéticos y 9 columnas (ver `docs/DATASET_CARD.md`). Huella `sha256` registrada en `reports/lab13/decision_record.json`.
- **Partición temporal:** el 75 % inicial para entrenamiento (hasta el 2026-09-24) y el 25 % final para prueba (desde el 2026-09-25, n = 160; G1 = 101, G2 = 59).
- **Variables del modelo:** `zone`, `previous_incidents`, `infrastructure_score` y `exposure`.
- **Excluidas:** `case_id`, `received_date` y `target`; `protected_group` (solo se usa para auditar); y `age_band`, excluida en el LAB12 como control del riesgo R02.
- **Modelo:** `LogisticRegression(class_weight="balanced", max_iter=1200, random_state=42)` con one-hot y estandarización (`src/inf8239_u04/model.py`), configurado en `configs/governance.yml → model`.

## Global and subgroup evaluation
Fuente: `reports/lab13/deployment_decision.json`, `reports/lab13/fairness_by_group.csv` y `reports/lab12/`.

| Métrica | Global | G1 (n=101) | G2 (n=59) | Brecha | Umbral |
|---|---|---|---|---|---|
| Accuracy | 0.725 | 0.713 | 0.746 | — | — |
| Recall | 0.717 | **0.653** | 0.791 | 0.138 | ≥ 0.68 global y por grupo; brecha ≤ 0.16 |
| FPR | 0.265 | 0.231 | 0.375 | 0.144 | brecha ≤ 0.16 |

- **IC 95 % bootstrap** (LAB12): brecha de recall [0.011–0.322] y brecha de FPR [0.008–0.422]. Ambos superan 0.16, así que el cumplimiento no es estable.
- **Interseccional:** solo G1 | 45-59 (n = 35) alcanza el mínimo de 30 casos; los demás subgrupos no se interpretan.
- **Puerta fallida:** `min_group_recall`, porque G1 tiene 0.653. Por eso la decisión es **REVIEW**.

## Green AI evidence
| Opción | Recall | Brecha de recall | Brecha de FPR | Entrenamiento | Tamaño |
|---|---|---|---|---|---|
| Línea base no predictiva | 0.435 | 0.144 | 0.010 | 0 s | 0 KB |
| Logística con `age_band` | 0.717 | 0.138 | 0.125 | ~0.1 s | 3.6 KB |
| Árbol (profundidad 5) | 0.717 | 0.181 | 0.168 | ~0.1 s | 7.9 KB |
| **Logística sin `age_band` (elegida)** | 0.717 | 0.138 | 0.144 | ~0.1 s | **3.3 KB** |

Se eligió la opción suficiente más liviana: el árbol duplica el tamaño sin mejorar el recall. La latencia es de unos 0.05 ms por caso, frente a un límite de 500 ms. Fuente: `reports/lab12/model_comparison.csv`.

## Limitations, human oversight and appeal
- **Limitaciones:**
  - La etiqueta puede estar sesgada (tasa positiva de 0.64 en G2 frente a 0.50 en G1, riesgo R01).
  - `zone` puede actuar como proxy del grupo.
  - La muestra de prueba es pequeña y hay un solo corte temporal.
  - Una brecha no prueba discriminación causal.
- **Supervisión humana:** el DSS solo ordena la cola. El analista revisa y justifica cada decisión, y el Product Owner registra la decisión ante un REVIEW. Cualquier responsable del RACI puede escalar un STOP.
- **Puertas automáticas** (`src/inf8239_u04/governance.py`): si falla una puerta de desempeño, equidad o costo, la decisión es REVIEW. Si el modelo usa un identificador directo o un atributo sensible (puerta `privacy`), la decisión es STOP.
- **Apelación:** cualquier persona o analista puede pedir revisión. La hace un supervisor independiente que no ve la puntuación del modelo, en un plazo de 10 días hábiles, y queda en el log de apelaciones (`student_inputs/lab11_impact.yml`).
- **Retiro:** ver la condición de retiro de `student_inputs/lab11_impact.yml` y `docs/RUNBOOK.md`.

## Owner and review date
- **Accountable:** Institutional Owner. **Responsable operativo:** Product Owner. **Mantenimiento técnico:** Data Scientist y ML Engineer (`student_inputs/raci.csv`).
- **Versión:** paquete `inf8239_u04` 0.1.0. La versión exacta del commit, del modelo y de los datos se registra en `reports/lab13/decision_record.json`.
- **Revisión:** mensual, y obligatoria antes de cualquier cambio de modelo, de datos o de umbrales. El estado actual es **REVIEW**: no se usa en operación hasta que el recall de G1 llegue a 0.68 o más con IC de las brechas por debajo de 0.16.
- **Monitoreo:** mensual, con `scripts/lab13_monitor.py` (deriva PSI, tasa de selección y recall por grupo). Ver `docs/RUNBOOK.md` y `reports/lab13/monitoring_report.csv`. Los traspasos entre roles están en `docs/RACI_HANDOFFS.md`.
