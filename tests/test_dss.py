from pathlib import Path
import pandas as pd, pytest
from streamlit.testing.v1 import AppTest
from inf8239_u04.data import load_data,validate_schema
from inf8239_u04.governance import load_config,deployment_decision,decision_record,validate_raci
from inf8239_u04.pipeline import run,prioritize

OK_METRICS={"recall":.8,"min_group_recall":.75}; OK_GAPS={"recall_gap":.05,"fpr_gap":.05}; OK_RES={"latency_ms":1,"model_kb":5}
GATES={"min_recall":.68,"min_group_recall":.68,"max_recall_gap":.16,"max_fpr_gap":.16,"max_latency_ms":500,"max_model_kb":1024}
POLICY={"direct_identifiers":["name"],"sensitive_features":["protected_group","age_band"]}

@pytest.fixture(scope="module")
def governed():
    cfg=load_config(); m=cfg["model"]; result=run(load_data(),cfg["gates"],m["kind"],m["exclude_features"],cfg)
    return cfg,result

def test_missing_column_rejected_before_predicting():
    with pytest.raises(ValueError,match="Missing columns"): validate_schema(load_data().drop(columns=["exposure"]))

def test_gap_out_of_tolerance_requires_review():
    d=deployment_decision(OK_METRICS,{"recall_gap":.30,"fpr_gap":.05},OK_RES,GATES)
    assert d["status"]=="REVIEW" and "recall_gap" in d["failed"]

def test_group_below_min_recall_requires_review():
    d=deployment_decision({"recall":.8,"min_group_recall":.6},OK_GAPS,OK_RES,GATES); assert d["status"]=="REVIEW"

def test_sensitive_feature_in_model_stops():
    d=deployment_decision(OK_METRICS,OK_GAPS,OK_RES,GATES,["zone","age_band"],POLICY)
    assert d["status"]=="STOP" and "privacy" in d["failed"]

def test_all_gates_pass_is_go():
    assert deployment_decision(OK_METRICS,OK_GAPS,OK_RES,GATES,["zone"],POLICY)["status"]=="GO"

def test_recommendation_is_traceable(governed):
    cfg,result=governed; r=decision_record(cfg,result)
    for key in ["version","policy","evidence","human_action","authority_limit"]: assert r[key]
    assert r["version"]["data_sha256"] and r["policy"]["prohibited_uses"] and "age_band" not in r["version"]["model_features"]

def test_priority_queue_never_acts_automatically(governed):
    q=prioritize(governed[1])
    assert "protected_group" not in q.columns and q.probability.is_monotonic_decreasing
    assert q.recommended_action.str.contains("Revisión humana|Cola cronológica").all()

def test_raci_requires_single_accountable():
    validate_raci(pd.read_csv("student_inputs/raci.csv"))
    with pytest.raises(ValueError,match="exactly one"): validate_raci(pd.DataFrame([{"activity":"deploy","R":"ML","A":"Product Owner, Legal","C":"DS","I":"Users"}]))

def test_app_shows_governed_recommendation():
    at=AppTest.from_file(Path(__file__).parents[1]/"app.py",default_timeout=30).run(); assert not at.exception
    assert any("Acción humana" in x.value for x in at.info)
