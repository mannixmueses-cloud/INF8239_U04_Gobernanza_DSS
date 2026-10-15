# Incident simulation

- detected_at: 2026-10-15T16:29:18.314844+00:00
- signal: failed gates: min_group_recall
- containment: REVIEW and safe baseline
- evidence: preserved report and model version
- communication: Interna al Institutional Owner, Data Scientist y Legal en < 72 h (SEV2); instrucción escrita a los analistas de usar la cola cronológica; aviso a personas afectadas con derecho de apelación si su orden de revisión cambió.
- corrective actions, owners and dates: ver tabla de acciones correctivas (sección 6).

---

## Postmortem del simulacro SIM-001

> Simulacro sobre datos sintéticos, según `docs/RUNBOOK.md`. La señal no es inventada: es la puerta que realmente falla en `reports/lab13/deployment_decision.json`.

### 1. Detección y clasificación
- **Señal:** la puerta `min_group_recall` falla. El recall de G1 es **0.653**, por debajo del umbral de 0.68. Las demás puertas se cumplen: recall global 0.717, brecha de recall 0.138, brecha de FPR 0.144, latencia de unos 0.05 ms por caso, modelo de 3.3 KB y privacidad sin `age_band`.
- **Severidad:** SEV2, falla de equidad o desempeño en un grupo. No es SEV1, porque la privacidad pasa y no hay uso prohibido.
- **Detecta:** el ML Engineer, al ejecutar `scripts/lab13_governance.py`.

### 2. Contención
- **Autoridad:** el Product Owner (Accountable de Deployment y Monitoring en `student_inputs/raci.csv`) mantiene la decisión **REVIEW**. El DSS no se usa en operación.
- **Medida:** se usa la cola cronológica con lista de verificación (baseline seguro). La cola priorizada solo se consulta como apoyo y con revisión humana de cada caso.

### 3. Preservación de evidencia
Se copiaron a `reports/lab13/incidents/SIM-001/`, con su huella en `SHA256SUMS.txt`:
- `deployment_decision.json` y `decision_record.json`. Este último registra el commit, el modelo (logística sin `age_band`), las variables y el `sha256` de los datos (`2af1858fe874f391`).
- `fairness_by_group.csv` y `prioritized_cases.csv`.

### 4. Comunicación
| Destinatario | Mensaje | Responsable | Plazo |
|---|---|---|---|
| Institutional Owner, Data Scientist y Legal | Puerta fallida, decisión REVIEW y evidencia preservada | Product Owner | < 72 h |
| Analistas (usuarios) | Usar la cola cronológica; la cola del DSS solo es de consulta | Product Owner | Inmediato |
| Personas afectadas | No aplica en el simulacro: el DSS no llegó a operar. En operación real se avisaría a quienes vieron alterado su orden de revisión, junto con su derecho de apelación | Institutional Owner + Legal | < 72 h |

### 5. Rollback o baseline seguro
Se vuelve a la cola cronológica con lista de verificación (`infrastructure_score < 0.30` o `previous_incidents >= 5`). Su recall en la prueba es 0.435 y su brecha de FPR 0.010. Es menos útil, pero no depende del modelo. No hay una versión anterior validada con GO, así que no se recupera ningún modelo previo.

### 6. Causa raíz y acciones correctivas
**Causa probable:** la etiqueta histórica tiene una tasa positiva distinta por grupo (R01). Además, la muestra de prueba es pequeña: 101 casos de G1 y un IC de la brecha de recall de [0.011–0.322]. Es una falla que hay que investigar, no una prueba de discriminación causal.

| # | Acción | Responsable | Fecha límite |
|---|---|---|---|
| 1 | Revisar con el equipo de campo los falsos negativos de G1, sobre todo en 45-59 (n = 35) | Data Scientist | 2026-10-22 |
| 2 | Auditar el origen de la etiqueta `target` por grupo (R01) | Data Scientist + Data Engineer | 2026-10-29 |
| 3 | Evaluar un umbral de decisión por debajo de 0.5 o una recalibración, y volver a medir el recall por grupo y las brechas con IC | Data Scientist | 2026-11-05 |
| 4 | Ampliar la evaluación con validación temporal móvil o más datos | ML Engineer | 2026-11-12 |
| 5 | Actualizar `risk_register.csv`, `MODEL_CARD.md` y volver a ejecutar `lab13_governance.py` | Product Owner | 2026-11-16 |
| 6 | Aprobar la reactivación (GO), mantener REVIEW o retirar el sistema | Institutional Owner | 2026-11-19 |

### 7. Lecciones
- La puerta `min_group_recall` (añadida en el LAB13) detectó una falla que el recall global (0.717) ocultaba.
- La decisión REVIEW coincide con la del LAB12 y con la del Ejercicio 07: los controles automáticos y el juicio humano llegan a la misma conclusión.
