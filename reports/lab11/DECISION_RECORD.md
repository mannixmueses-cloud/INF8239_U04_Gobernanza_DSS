# Decision record — U04.LAB11 · Evaluación de impacto ético

- **Sistema:** Territorial Review DSS - Synthetic (`configs/governance.yml`)
- **Fecha:** 2026-10-15
- **Responsable de la decisión:** Institutional Owner (aprueba) · Product Owner (ejecuta)
- **Insumos:** `student_inputs/lab11_impact.yml`, `student_inputs/stakeholders.csv`, `reports/lab11/risk_register_scored.csv`, `reports/lab11/rmf_summary.json`

## Decisión: **REVIEW**

Se recomienda **continuar solo hacia la fase de medición (LAB12)**, sin desplegar ni usar el sistema con casos de ninguna persona. El propósito está acotado y existe una alternativa no predictiva, un mecanismo de apelación y una condición de retiro. Sin embargo, los tres riesgos prioritarios siguen sin medirse y uno de ellos (R01) tiene riesgo residual alto. Una decisión GO no está justificada con la evidencia disponible, y una decisión STOP sería prematura porque los controles todavía se pueden verificar.

## Tres riesgos prioritarios

| Riesgo | Prioridad (P×I) | Evidencia actual | Incertidumbre | Responsable |
|---|---|---|---|---|
| **R01** Sesgo de la etiqueta histórica contra G2 | 16 (4×4) | La tasa positiva es 0.64 en G2 frente a 0.50 en G1 (`describe_dataset.py`, 640 casos). | No se sabe si la diferencia refleja una necesidad real o un sesgo de registro. Los datos no permiten distinguirlos. | Data Scientist |
| **R03** Sesgo de automatización y desvío hacia usos prohibidos | 12 (3×4) | La app muestra la advertencia de datos sintéticos y la lista de usos prohibidos. | Todavía no existe un log de decisiones humanas, así que no se puede medir si los analistas revisan o solo aceptan el orden. | Product Owner |
| **R02** `age_band` es sensible pero se usa como predictor | 12 (4×3) | Está declarada en `sensitive_features` y se usa en `build_model()`; es un hecho verificable en el código. | Se desconoce cuánto cambian el recall y las brechas al quitarla. | Data Scientist |

**Interpretación.** El orden del registro no es una verdad matemática: R03 y R02 empatan en 12. R03 queda por encima porque su impacto es mayor, ya que el uso para intervenir o negar servicios afecta directamente a personas. R01 es el riesgo dominante porque condiciona todo lo demás: si la etiqueta está sesgada, incluso un modelo "equitativo" según las métricas reproduciría la desigualdad histórica. Los riesgos con prioridad 6 (R05, R06, R07, R09) se revisaron uno por uno y no se aceptan como bajos solo por su puntuación. R05 (zona como proxy) se mide junto con R01 en el LAB12.

## Estado NIST AI RMF

- **GOVERN:** hay propietario, RACI y usos prohibidos definidos. ✅
- **MAP:** hay 9 riesgos documentados con responsable y evidencia. ✅
- **MEASURE:** pendiente, depende del LAB12 (métricas por grupo e interseccionales). ⏳ *Que exista un archivo de reporte no prueba que el control sea eficaz.*
- **MANAGE:** están documentadas la condición de retiro y la apelación, pero aún no se han probado en operación. ⏳

## Condiciones para pasar a GO (verificar en LAB12–LAB13)

1. Recall global ≥ 0.68, y brechas de recall y de FPR entre G1 y G2 ≤ 0.16 (`configs/governance.yml`).
2. Comparación del modelo con y sin `age_band`, documentando y justificando la variante elegida.
3. El modelo supera el recall de la línea base no predictiva (cola cronológica con lista de verificación) sin aumentar las brechas.
4. Log de decisiones con justificación humana obligatoria y formulario de apelación operativos.

## Condición de retiro (STOP)

Se suspende el sistema y se vuelve a la cola cronológica si: el recall es menor que 0.68, la brecha de recall o de FPR supera 0.16 en la revisión mensual, se revoca más del 20 % de las recomendaciones apeladas en un trimestre, hay evidencia de uso fuera de alcance o aparecen identificadores directos en los datos.

---
*Datos sintéticos y didácticos. Este registro no autoriza decisiones automáticas sobre personas.*
