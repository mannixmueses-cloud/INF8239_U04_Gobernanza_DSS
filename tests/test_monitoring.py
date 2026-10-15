import numpy as np, pandas as pd
from inf8239_u04.monitoring import psi, monthly_report

def test_psi_is_near_zero_for_same_distribution_and_flags_shift():
    rng=np.random.default_rng(0); ref=rng.normal(0,1,2000)
    assert psi(ref,rng.normal(0,1,2000))<0.05 and psi(ref,rng.normal(1.5,1,2000))>0.25
    assert psi(pd.Series(list("ab"*50)),pd.Series(list("a"*90+"b"*10)))>0.25

def test_monthly_report_flags_alerts_and_low_support():
    dates=pd.to_datetime(["2026-10-05"]*40+["2026-11-05"]*40)
    cur=pd.DataFrame({"received_date":dates,"x":[0.1]*40+[5.0]*40,"protected_group":["G1","G2"]*40,"target":[1]*80})
    ref=pd.DataFrame({"x":np.linspace(0,1,100)}); pred=np.array([1]*40+[1,0]*20)
    r=monthly_report(ref,cur,pred,["x"],{"max_psi":.25,"max_recall_gap":.16,"min_group_recall":.68},min_support=30)
    nov=r[r.month=="2026-11"].iloc[0]
    assert "drift:x" in nov.alerts and "recall_gap" in nov.alerts and bool(nov.low_support)
