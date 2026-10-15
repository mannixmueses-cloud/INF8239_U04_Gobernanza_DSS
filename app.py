from pathlib import Path
import pandas as pd
import streamlit as st
from inf8239_u04.data import load_data
from inf8239_u04.governance import load_config, decision_record
from inf8239_u04.pipeline import run, prioritize
st.set_page_config(page_title="Governed Green DSS",layout="wide")
st.title("DSS territorial sintético · Gobernanza y Green AI")
st.warning("Demostración educativa con datos sintéticos. No autoriza decisiones automáticas ni representa estadísticas reales.")
cfg=load_config(); m=cfg.get("model",{})
result=run(load_data(),cfg["gates"],m.get("kind","logistic"),m.get("exclude_features",[]),cfg); record=decision_record(cfg,result)

st.subheader("Propósito y límite de autoridad")
st.write(cfg["purpose"]); st.write("Usos prohibidos:",", ".join(cfg["prohibited_uses"]))
st.caption(record["authority_limit"])

st.subheader("Recomendación gobernada")
status=record["status"]; color={"GO":st.success,"REVIEW":st.warning,"STOP":st.error}[status]
color(f"Decisión: **{status}**" + (f" · puertas fallidas: {', '.join(record['failed_gates'])}" if record["failed_gates"] else ""))
c1,c2,c3,c4=st.columns(4)
c1.metric("Accuracy",f"{result['metrics']['accuracy']:.3f}"); c2.metric("Recall global",f"{result['metrics']['recall']:.3f}")
c3.metric("Recall mínimo por grupo",f"{result['metrics']['min_group_recall']:.3f}"); c4.metric("Decisión",status)
st.info(f"Acción humana: {record['human_action']}")
with st.expander("Trazabilidad: versión, política y evidencia"):
    st.json({"version":record["version"],"policy":record["policy"],"evidence":record["evidence"]})

st.subheader("Métricas por grupo")
st.dataframe(result["by_group"],width="stretch")
st.caption("protected_group se usa solo para auditar; no entra al modelo ni se muestra en la cola de casos.")

st.subheader("Puertas de calidad")
st.dataframe(pd.DataFrame({"puerta":list(record["checks"]),"cumple":list(record["checks"].values())}),width="stretch",hide_index=True)

comparison=Path("reports/lab12/model_comparison.csv")
if comparison.exists():
    st.subheader("Green AI · alternativas comparadas (LAB12)")
    st.dataframe(pd.read_csv(comparison)[["option","accuracy","recall","recall_gap","fpr_gap","training_seconds","model_kb","passes_gates"]],width="stretch",hide_index=True)

st.subheader("Cola de revisión priorizada")
queue=prioritize(result)
levels=st.multiselect("Prioridad",["Alta","Media","Baja"],default=["Alta","Media","Baja"])
st.dataframe(queue[queue.priority.isin(levels)],width="stretch",hide_index=True)
st.caption("La prioridad ordena la revisión humana. Ningún caso recibe una intervención, una negación de servicio ni una decisión automática.")
st.info("Acción humana: revisar evidencia, documentar la decisión y activar apelación o rollback cuando corresponda.")
