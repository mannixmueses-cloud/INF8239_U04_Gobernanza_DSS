# Informe de auditoría de equidad — U04.LAB12

- **Sistema:** Territorial Review DSS - Synthetic
- **Fecha:** 2026-10-15
- **Responsable de la auditoría:** Data Scientist · **Aprueba:** Product Owner
- **Reproducción:**
  ```bash
  uv run python scripts/lab12_audit.py --model logistic
  uv run python scripts/lab12_audit.py --model tree
  uv run python scripts/lab12_compare.py
  uv run python scripts/validate_lab12_decision.py
  ```

> Datos sintéticos y didácticos. Ninguna cifra representa personas, territorios ni tasas reales.

## 1. Comprender el dataset (`scripts/describe_dataset.py`)

| Comprobación | Resultado | Interpretación |
|---|---|---|
| Distribución de `target` | 55.2 % positivos y 44.8 % negativos | El desbalance es leve, pero accuracy no basta: un promedio alto puede ocultar que un grupo pierde más casos positivos. |
| Tamaño por grupo | 640 casos en total: G1 = 396, G2 = 244. En prueba: G1 = 101, G2 = 59 | La comparación G1–G2 tiene soporte moderado. Los cruces grupo × edad tienen poco soporte (sección 4). |
| Corte temporal | Entrenamiento hasta el 2026-09-24 y prueba desde el 2026-09-25 (25 % final) | Evita usar el futuro para evaluar el pasado y se parece a la operación real, donde el modelo puntúa casos nuevos. |
| Variables excluidas | `case_id`, `received_date`, `protected_group` y `target` no entran al modelo | Quitar `protected_group` no elimina el sesgo: `zone` y la propia etiqueta pueden actuar como proxies (R01, R05). Además `age_band`, declarada sensible, **sí** entra al modelo (R02). |

## 2. Desempeño global y por grupo (regresión logística)

| Métrica | Global | G1 (n=101) | G2 (n=59) | Brecha |
|---|---|---|---|---|
| Accuracy | 0.719 | 0.703 | 0.746 | 0.043 |
| Recall (TPR) | 0.717 | **0.653** | 0.791 | **0.138** |
| FPR | 0.279 | 0.250 | **0.375** | **0.125** |
| Tasa de selección | 0.531 | 0.446 | 0.678 | 0.232 |
| Precisión | 0.776 | 0.711 | 0.850 | 0.139 |

**Lectura.** El recall global (0.717) supera el mínimo de 0.68, pero **G1 queda por debajo** (0.653): el promedio oculta una falla localizada. G2 recibe más alertas, tanto correctas como incorrectas: su tasa de selección es 0.678 y su FPR 0.375. Esto coincide con la mayor tasa positiva de la etiqueta en G2 (R01). La diferencia de tasa de selección (0.232) refleja en parte esa diferencia en la etiqueta, por lo que no se usa como criterio principal.

Fuentes: `reports/lab12/logistic/global_metrics.json` y `reports/lab12/logistic/fairness_by_group.csv`.

## 3. Comparación de alternativas (`reports/lab12/model_comparison.csv`)

| Opción | Accuracy | Recall | Brecha de recall [IC 95 %] | Brecha de FPR [IC 95 %] | Entrenamiento | Tamaño | Umbrales |
|---|---|---|---|---|---|---|---|
| Línea base no predictiva | 0.625 | 0.435 | 0.144 [0.009–0.332] | 0.010 [0.003–0.213] | 0 s | 0 KB | ❌ recall |
| Regresión logística | 0.719 | 0.717 | 0.138 [0.011–0.314] | 0.125 [0.005–0.398] | ~0.1 s | 3.6 KB | ✅ |
| Árbol de decisión (profundidad 5) | 0.706 | 0.717 | **0.181** [0.023–0.357] | **0.168** [0.009–0.489] | ~0.1 s | 7.9 KB | ❌ brechas |
| Logística sin `age_band` | **0.725** | 0.717 | 0.138 [0.011–0.322] | 0.144 [0.008–0.422] | ~0.03 s | **3.3 KB** | ✅ |

- **Línea base no predictiva** (`infrastructure_score < 0.30` o `previous_incidents >= 5`): es casi igual de equitativa en FPR, pero solo detecta el 43 % de los casos reales. Se mantiene como respaldo, no como sistema principal.
- **Árbol:** no mejora el recall, aumenta las dos brechas por encima de 0.16 y pesa el doble. Un modelo más complejo que no mejora **no está justificado** (Green AI).
- **Logística sin `age_band`:** el recall es idéntico, la accuracy es ligeramente mayor y el modelo es el más pequeño. Quita el uso directo de la edad (control de R02), a cambio de +0.019 en la brecha de FPR, que queda dentro de la tolerancia.
- **Incertidumbre:** con n = 160, **todos los IC 95 % de las brechas superan 0.16**. Que una brecha puntual cumpla el umbral no demuestra que se cumpla de forma estable.

Los tiempos de entrenamiento varían entre ejecuciones; lo que importa es el orden de magnitud (segundos o menos). El tamaño serializado sí es estable. Todos los modelos están muy por debajo de los límites de 500 ms de latencia y 1024 KB de tamaño.

## 4. Análisis interseccional (grupo × edad, mínimo de 30 casos)

Fuente: `reports/lab12/intersectional_support.csv` (columna `sufficient_support`).

| Subgrupo | n | ¿Se puede interpretar? |
|---|---|---|
| G1 \| 45-59 | 35 | ✅ Sí |
| G1 \| 18-29, G1 \| 30-44, G1 \| 60+ | 18, 24, 24 | ⚠️ Soporte insuficiente |
| G2 \| 18-29, G2 \| 30-44, G2 \| 45-59, G2 \| 60+ | 11, 14, 8, 26 | ⚠️ Soporte insuficiente |

- **G1 \| 45-59 (único con soporte):** el recall de la logística es 0.588, por debajo del 0.653 de G1. Este es el subgrupo donde más se concentra la pérdida de casos reales. Con el árbol sube a 0.647, pero el árbol incumple los umbrales globales.
- **Subgrupos sin soporte:** se reportan pero **no se interpretan**. Por ejemplo, el FPR de 1.0 del árbol en G2 \| 30-44 (n = 14) o el recall de 1.0 en G2 \| 45-59 (n = 8) son inestables. No se ocultan: indican dónde hacen falta más datos.

## 5. Por qué una brecha no prueba discriminación causal

Las brechas observadas **requieren investigación, pero no prueban por sí solas discriminación causal**, por cuatro razones:
1. **Etiqueta:** si `target` refleja registros históricos sesgados (R01), el modelo puede reproducir la diferencia del dato, no una diferencia real de riesgo.
2. **Proxies y confusores:** `zone`, la infraestructura y los incidentes previos se distribuyen de forma distinta entre grupos. La brecha puede venir de estas variables y no del grupo en sí.
3. **Incertidumbre:** los IC son anchos y algunas brechas podrían desaparecer o duplicarse con otra muestra.
4. **Un solo corte temporal:** no se ha verificado si el patrón se mantiene en otros periodos.

Siguiente paso: revisar con el equipo de campo una muestra de los falsos negativos de G1 (en especial en 45-59), auditar el origen de la etiqueta y repetir la evaluación con más datos o con validación temporal móvil.

## 6. Decisión contextual

**REVIEW.** Detalle en `student_inputs/lab12_decision.yml`.

- Se descarta el árbol.
- La candidata preferida es la regresión logística sin `age_band`. La logística original es equivalente y es la que usa por defecto el pipeline del LAB13.
- **Acción humana obligatoria:** el sistema solo ordena la cola; el analista revisa y justifica cada decisión, y el caso puede apelarse (LAB11).
- **Condiciones para pasar a GO:** IC de las brechas por debajo de 0.16 con más datos, recall de G1 de al menos 0.68 y revisión de la etiqueta (R01).
- **Límite:** esta auditoría no autoriza decisiones automáticas sobre personas.

## Estado NIST AI RMF (actualización respecto del LAB11)

- **MEASURE:** ✅ métricas globales, por grupo e interseccionales con conteos, IC bootstrap y costo computacional.
- **MANAGE:** ⏳ la decisión REVIEW tiene condiciones explícitas; el despliegue gobernado y el runbook corresponden al LAB13.
