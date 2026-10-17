import json
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data" / "demo_data.json"

def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_plot(data, plot_id):
    return next((p for p in data.get("plots", []) if p.get("plot_id") == plot_id), None)

def search_plots(data, query):
    query = (query or "").strip().lower()
    if not query: return []
    results=[]
    for p in data.get("plots", []):
        fields=[p.get("plot_id",""),p.get("dag_no",""),p.get("khatian_no",""),p.get("district",""),p.get("upazila",""),p.get("mouza","")]
        fields += [d.get("deed_id","") for d in p.get("deeds",[])]
        if any(query in str(field).lower() for field in fields): results.append(p)
    return results

def get_findings(data, plot_id):
    p = get_plot(data, plot_id)
    if not p: return []
    out=[]
    deeds=p.get("deeds",[])
    active=[d for d in deeds if d.get("status")=="সক্রিয়"]
    active_owners={d.get("owner_label","অজানা") for d in active}
    if len(active)>1 and len(active_owners)>1:
        out.append({"severity":"উচ্চ","code":"MULTIPLE_ACTIVE_DEEDS","title":"একাধিক সক্রিয় দলিলের তথ্য","details":f"ডেমো রেকর্ডে {len(active)}টি সক্রিয় দলিল এবং একাধিক দাবিদারের নাম আছে: {', '.join(sorted(active_owners))}। এটি সম্ভাব্য অসংগতি; জালিয়াতির প্রমাণ নয়।","action":"মূল দলিল, নিবন্ধনের বিবরণ এবং প্রাসঙ্গিক রেকর্ড আইনগতভাবে যাচাই করুন।"})
    for deed in active:
        try: d_area=float(deed.get("area_decimal",p.get("area_decimal",0))); p_area=float(p.get("area_decimal",0))
        except (TypeError,ValueError): continue
        if abs(d_area-p_area)>0.25:
            out.append({"severity":"উচ্চ","code":"AREA_MISMATCH","title":"দলিল ও প্লটের পরিমাণে অমিল","details":f"প্লট প্রোফাইলে {p_area:g} শতক, কিন্তু {deed.get('deed_id','একটি দলিল')}-এ {d_area:g} শতক দেখানো আছে।","action":"দাগ/খতিয়ান, পরিমাপ এবং সংশ্লিষ্ট মূল দলিল মিলিয়ে দেখুন।"})
            break
    if p.get("mutation_status")=="চলমান":
        out.append({"severity":"মাঝারি","code":"MUTATION_PENDING","title":"নামজারি প্রক্রিয়া চলমান","details":"ডেমো রেকর্ডে নামজারির অবস্থা ‘চলমান’ হিসেবে চিহ্নিত।","action":"নামজারির আবেদন, বর্তমান অবস্থা এবং সংশ্লিষ্ট নথি যাচাই করুন।"})
    elif p.get("mutation_status")=="যাচাই বাকি":
        out.append({"severity":"মাঝারি","code":"MUTATION_UNKNOWN","title":"নামজারির অবস্থা নিশ্চিত নয়","details":"ডেমো রেকর্ডে নামজারির অবস্থা এখনও যাচাই করা হয়নি।","action":"সংশ্লিষ্ট নামজারি রেকর্ড ও আবেদনের অবস্থা যাচাই করুন।"})
    if p.get("record_status")=="তথ্য অসম্পূর্ণ":
        out.append({"severity":"মাঝারি","code":"INCOMPLETE_RECORD","title":"রেকর্ডের তথ্য অসম্পূর্ণ","details":"এই ডেমো প্রোফাইলে কিছু তথ্য অনুপস্থিত বা যাচাই বাকি হিসেবে চিহ্নিত।","action":"অনুপস্থিত নথি ও তথ্য সংশ্লিষ্ট অফিসিয়াল রেকর্ডের সঙ্গে মিলিয়ে দেখুন।"})
    if p.get("case_status")=="মামলার তথ্য যাচাই বাকি":
        out.append({"severity":"মাঝারি","code":"CASE_CHECK_PENDING","title":"মামলা-সংক্রান্ত তথ্য যাচাই বাকি","details":"ডেমো রেকর্ডে মামলা-সংক্রান্ত অবস্থা নিশ্চিত করা হয়নি।","action":"প্রযোজ্য ক্ষেত্রে উপযুক্ত কর্তৃপক্ষ বা আইনজীবীর সহায়তায় যাচাই করুন।"})
    if p.get("acquisition_status")=="যাচাই বাকি":
        out.append({"severity":"মাঝারি","code":"ACQUISITION_CHECK_PENDING","title":"অধিগ্রহণ/খাস-সংক্রান্ত তথ্য যাচাই বাকি","details":"ডেমো রেকর্ডে অধিগ্রহণ বা খাস-সংক্রান্ত অবস্থা নিশ্চিত করা হয়নি।","action":"প্রাসঙ্গিক অফিসিয়াল রেকর্ড থেকে তথ্য যাচাই করুন।"})
    if p.get("tax_status") in ("তথ্য অনুপস্থিত","অজানা"):
        out.append({"severity":"কম","code":"TAX_INFO_UNKNOWN","title":"ভূমি উন্নয়ন করের তথ্য অসম্পূর্ণ","details":"ডেমো ডেটায় কর পরিশোধের অবস্থা অনুপস্থিত বা অজানা। এর মানে কর বকেয়া—এমন নয়।","action":"প্রযোজ্য করের রসিদ ও সরকারি কর-রেকর্ড যাচাই করুন।"})
    return out

def get_risk_level(findings):
    if any(f["severity"]=="উচ্চ" for f in findings): return ("উচ্চ সতর্কতা","risk-high")
    if any(f["severity"]=="মাঝারি" for f in findings): return ("মাঝারি সতর্কতা","risk-medium")
    if findings: return ("কম সতর্কতা","risk-low")
    return ("সেট করা সতর্কতা নেই","risk-clear")

def get_dashboard_stats(data):
    plots=data.get("plots",[])
    return {"plots":len(plots),"deeds":sum(len(p.get("deeds",[])) for p in plots),"flagged":sum(bool(get_findings(data,p["plot_id"])) for p in plots),"pending_mutations":sum(p.get("mutation_status")=="চলমান" for p in plots)}
