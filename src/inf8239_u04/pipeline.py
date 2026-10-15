import time
from sklearn.metrics import accuracy_score, recall_score
from .data import features, temporal_split
from .fairness import audit, gap
from .governance import deployment_decision
from .model import build_model, fit_measure

def run(df, gates, kind="logistic", exclude=(), policy=None):
    train,test=temporal_split(df); model=build_model(kind,exclude); resources=fit_measure(model,features(train,exclude),train.target)
    start=time.perf_counter(); pred=model.predict(features(test,exclude)); resources["latency_ms"]=(time.perf_counter()-start)*1000/len(test)
    overall,by_group,_=audit(test.target,pred,test.protected_group)
    metrics={"accuracy":float(accuracy_score(test.target,pred)),"recall":float(recall_score(test.target,pred,zero_division=0)),
             "min_group_recall":float(by_group["recall"].min())}
    gaps={"recall_gap":gap(by_group,"recall"),"fpr_gap":gap(by_group,"fpr")}
    model_features=list(features(test,exclude).columns)
    decision=deployment_decision(metrics,gaps,resources,gates,model_features,policy)
    return {"model":model,"test":test,"pred":pred,"overall":overall,"by_group":by_group,"metrics":metrics,"gaps":gaps,
            "resources":resources,"decision":decision,"model_features":model_features,"kind":kind,"exclude":list(exclude)}

def prioritize(result, threshold=.5, high=.7):
    """Salida del DSS: probabilidad, prioridad y acción recomendada por caso. Nunca decide sobre la persona."""
    test=result["test"]; proba=result["model"].predict_proba(features(test,result["exclude"]))[:,1]
    out=test[["case_id","received_date","zone"]].assign(received_date=test.received_date.dt.date,probability=proba.round(3))
    out["priority"]=out.probability.map(lambda p:"Alta" if p>=high else "Media" if p>=threshold else "Baja")
    out["recommended_action"]=out.priority.map({"Alta":"Revisión humana prioritaria","Media":"Revisión humana en la cola regular","Baja":"Cola cronológica (sin acción automática)"})
    return out.sort_values("probability",ascending=False).reset_index(drop=True)
