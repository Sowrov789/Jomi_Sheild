import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from data_logic import load_data,get_plot,get_findings,get_dashboard_stats,search_plots,get_risk_level

def test_has_20_fictional_plots():
    assert len(load_data()["plots"]) == 20

def test_clean_scenario():
    d=load_data(); assert get_findings(d,"JP-1001") == []

def test_multiple_active_deeds_trigger_warning():
    d=load_data(); assert any(f["code"]=="MULTIPLE_ACTIVE_DEEDS" for f in get_findings(d,"JP-1007"))

def test_area_mismatch_trigger_warning():
    d=load_data(); assert any(f["code"]=="AREA_MISMATCH" for f in get_findings(d,"JP-1014"))

def test_pending_mutation_trigger_warning():
    d=load_data(); assert any(f["code"]=="MUTATION_PENDING" for f in get_findings(d,"JP-1002"))

def test_unknown_plot():
    assert get_plot(load_data(),"JP-9999") is None

def test_search_by_deed():
    assert search_plots(load_data(),"DEMO-D-030")[0]["plot_id"]=="JP-1001"

def test_stats_and_risk_level():
    d=load_data(); s=get_dashboard_stats(d)
    assert s["plots"]==20 and s["deeds"]>=20 and s["flagged"]>0
    assert get_risk_level(get_findings(d,"JP-1018"))[0]=="উচ্চ সতর্কতা"
