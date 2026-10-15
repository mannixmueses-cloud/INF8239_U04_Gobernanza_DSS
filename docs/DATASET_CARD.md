# Dataset Card

Synthetic territorial-risk dataset generated with a fixed educational seed. It contains no real persons, locations, rates or official Dominican Republic statistics. Intended only to practice contracts, temporal evaluation, subgroup auditing and governance. Prohibited: operational profiling or inference about real populations.

> Formato inspirado en Gebru et al., *Datasheets for Datasets*.

## Procedencia y composición
- **Archivo:** `data/territorial_risk_synthetic.csv`, con 640 filas y 9 columnas, generado para el curso INF-8239 (proyecto base de la Unidad 04).
- **Columnas:** `case_id` (identificador sintético único), `received_date` (2026), `zone` (Norte, Sur, Este y Oeste), `protected_group` (G1 = 396 y G2 = 244), `age_band` (18-29, 30-44, 45-59 y 60+), `previous_incidents`, `infrastructure_score` (0–1), `exposure` (0–1) y `target` (binaria, 55.2 % positivos).
- **Diferencia en la etiqueta entre grupos:** la tasa positiva es 0.64 en G2 y 0.50 en G1. Puede representar una diferencia real o un sesgo de registro (riesgo R01).

## Contrato y privacidad
- `validate_schema` (`src/inf8239_u04/data.py`) rechaza el archivo si falta alguna columna obligatoria, si `target` no es binaria o si aparece un identificador directo (`name`, `document_number`, `email` o `phone`). Lo cubren `tests/test_data.py`, `tests/test_privacy.py` y `tests/test_dss.py`.
- No hay datos personales. El repositorio no contiene secretos (`.streamlit/secrets.toml` está en `.gitignore`).

## Uso en el modelo
- **Corte temporal:** el 75 % inicial para entrenar (hasta el 2026-09-24) y el 25 % final para probar. Así no se usa el futuro para evaluar el pasado.
- **Excluidas del modelo:** `case_id`, `received_date`, `target`, `protected_group` (solo para auditar) y `age_band` (excluida en el LAB12). Quitar estas columnas no elimina los sesgos indirectos: `zone` puede actuar como proxy (riesgo R05).
