import os
import streamlit as st


def _read_secret(name, default=""):
    """Read Streamlit secrets first, then environment variables."""
    try:
        value = st.secrets.get(name, default)
    except Exception:
        value = os.getenv(name, default)
    return str(value or "").strip()


def _get_api_key():
    key = _read_secret("GEMINI_API_KEY", "")
    placeholders = {"", "paste_your_real_key_here", "paste_your_key_here", "আপনার_API_KEY", "your_api_key_here"}
    return "" if key.lower() in {v.lower() for v in placeholders} else key


def gemini_ready():
    """True only when a non-placeholder API key is present; it does not validate the key."""
    return bool(_get_api_key())


def local_answer(question, plot, findings):
    if findings:
        rows = [f"- **{f['title']} ({f['severity']} সতর্কতা)**: {f['details']}\n  - করণীয়: {f['action']}" for f in findings]
        return (f"**{plot['plot_id']}** ডেমো জমির জন্য এই সম্ভাব্য সতর্কতাগুলো পাওয়া গেছে:\n\n"
                + "\n".join(rows)
                + "\n\nএটি সম্ভাব্য অসংগতির ব্যাখ্যা—মালিকানা বা জালিয়াতির চূড়ান্ত সিদ্ধান্ত নয়।")
    return (f"**{plot['plot_id']}**-এর ডেমো রেকর্ডে নির্ধারিত নিয়ম অনুযায়ী কোনো সতর্কতা পাওয়া যায়নি। "
            "এর অর্থ জমি আইনগতভাবে নিরাপদ বা মালিকানা নিশ্চিত—এমন নয়। "
            "মূল দলিল, নামজারি, খতিয়ান ও কর-সংক্রান্ত তথ্য যাচাই করুন।")


def _api_error_message(exc):
    """Return useful troubleshooting instructions without revealing the API key."""
    message = str(exc).lower()
    if any(x in message for x in ("api key not valid", "invalid api key", "unauthorized", "401")):
        return "Gemini API key গ্রহণ করা হয়নি। Google AI Studio-তে key ঠিক আছে কি না দেখুন এবং `secrets.toml`-এ অতিরিক্ত quote/space নেই নিশ্চিত করুন।"
    if any(x in message for x in ("permission_denied", "permission denied", "403", "forbidden")):
        return "Gemini API access denied হয়েছে। API key-এর project/access setting পরীক্ষা করুন।"
    if any(x in message for x in ("quota", "resource_exhausted", "429", "rate limit")):
        return "Gemini API-এর quota বা request limit শেষ হয়েছে। কিছুক্ষণ পরে চেষ্টা করুন এবং AI Studio-তে usage/quota পরীক্ষা করুন।"
    if any(x in message for x in ("not found", "404", "unsupported model")):
        return "নির্বাচিত Gemini model পাওয়া যায়নি বা এই key-তে উপলভ্য নয়। `GEMINI_MODEL`-এ `gemini-3.8-flash` দিন এবং model availability পরীক্ষা করুন।"
    if any(x in message for x in ("connection", "timeout", "network", "dns")):
        return "Gemini-তে সংযোগ করা যায়নি। ইন্টারনেট সংযোগ পরীক্ষা করে আবার চেষ্টা করুন।"
    return f"Gemini request ব্যর্থ হয়েছে ({type(exc).__name__})। API key, model name, internet connection এবং free-tier quota পরীক্ষা করুন।"


def answer_question(question, plot, findings):
    api_key = _get_api_key()
    if not api_key:
        return (local_answer(question, plot, findings)
                + "\n\n_Gemini key পড়া যায়নি। Local app হলে `.streamlit/secrets.toml` দেখুন; Streamlit Cloud হলে Settings → Secrets-এ key যোগ করুন।_")
    try:
        from google import genai
        model = _read_secret("GEMINI_MODEL", "gemini-3.8-flash") or "gemini-3.8-flash"
        client = genai.Client(api_key=api_key)
        prompt = f"""
তুমি JOMI-SHIELD-এর বাংলা সহায়ক। শুধু নিচে দেওয়া কাল্পনিক demo record ও rule-based findings ব্যাখ্যা করবে।
তথ্য অনুপস্থিত থাকলে অনুমান করবে না; বলবে তথ্যটি ডেমো ডেটায় নেই।
কোনো ব্যক্তিকে আইনগত মালিক ঘোষণা করবে না, জমিকে নিশ্চিত নিরাপদ বলবে না, এবং সতর্কতাকে জালিয়াতির প্রমাণ বলবে না।
সহজ বাংলায় সংক্ষিপ্ত ও ব্যবহারিক উত্তর দাও; ইংরেজিতে প্রশ্ন হলে ইংরেজিতে উত্তর দাও।
পরবর্তী যাচাইয়ের ধাপ উল্লেখ করো এবং প্রয়োজনে সরকারি যাচাই/আইনজীবীর পরামর্শ নিতে বলো।

কাল্পনিক প্লটের তথ্য:\n{plot}\n\nPython-এর rule-based findings:\n{findings}\n\nব্যবহারকারীর প্রশ্ন:\n{question}
"""
        result = client.models.generate_content(model=model, contents=prompt)
        response_text = getattr(result, "text", None)
        return response_text.strip() if response_text else local_answer(question, plot, findings)
    except Exception as exc:
        return (local_answer(question, plot, findings)
                + "\n\n**Gemini সংযোগের সমস্যা:** " + _api_error_message(exc)
                + "\n\n_আপনার API key এখানে প্রদর্শন করা হচ্ছে না।_")
