# JOMI-SHIELD | বাংলা ভূমি যাচাই সহায়ক

A polished Bengali-first Streamlit MVP inspired by the clear service-card and information architecture of Bangladesh's public land-service portal. This is an independent educational demo and is **not** a government website or an official verification service.

## Features
- Government-portal-inspired top banner, clear navigation, service cards, dashboard and help section; custom JOMI-SHIELD branding.
- Bengali search across 20 fictional plots by Plot ID, Dag, Khatian, district/upazila and deed ID.
- JOMI-PASS-style plot profile and fictional ownership timeline.
- JOMI-SHIELD explainable checks: multiple active deeds, plot/deed area mismatch, pending or unknown mutation, incomplete records, case/acquisition verification pending, unknown tax information.
- Optional Gemini assistant that explains existing rule-based results (does not decide legal ownership).
- Verification summary downloadable as JSON and CSV.
- Local fallback explanation works when no Gemini API key is configured.

## Run on Windows (PowerShell)
Open this folder in VS Code, open Terminal, and run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```



4. Restart `streamlit run app.py`.
5. For Streamlit Community Cloud deployment, open the app's **Settings → Secrets** and paste the same TOML entries there.

**Never commit `secrets.toml` or expose the API key in screenshots, source code, or GitHub.** `.gitignore` already excludes this file. Model access and free-tier limits may vary; check [Gemini API pricing and availability](https://ai.google.dev/gemini-api/docs/pricing) before relying on free usage. Requests in this prototype include synthetic demo records only.

## 20 fictional plots
`JP-1001` through `JP-1020`; all owner labels, deed IDs, statuses and locations are fictional test data. `JP-1001` is the no-configured-warning scenario, `JP-1007` and `JP-1018` contain multiple-active-deed scenarios, and `JP-1014` contains a deed/plot area mismatch. Additional records demonstrate pending mutation, unknown tax, incomplete records, or pending status checks.

## Test the rule logic
Install pytest if needed, then run:

```powershell
python -m pip install pytest
pytest -q
```

## Project structure
- `app.py` — Bengali UI, navigation and page layouts
- `data_logic.py` — JSON loading, search, rules and dashboard metrics
- `chatbot.py` — optional Gemini API and local fallback
- `data/demo_data.json` — 20 fictional plots and linked sample deeds
- `.streamlit/secrets.toml.example` — safe template for configuring key
- `tests/test_data_logic.py` — logic tests

## Important limitations
- No connection to government databases or APIs.
- Fictional sample data is not evidence about any real parcel.
- A warning indicates a scenario requiring further checking; it does not prove fraud.
- No warning means only that the configured demo rules did not trigger, not that a plot is legally safe.
- Gemini can make mistakes and must not provide a final legal ownership conclusion.
- The public land portal is available at https://land.gov.bd/.

## AI usage disclosure
Before submitting, describe the AI coding assistants actually used by your team and what they helped with. Team members should understand and be able to explain the interface, data structure, each rule, chatbot prompt, limitations and testing process.


## If Gemini still says the key is missing
- Filename must be exactly `.streamlit/secrets.toml` (not `secrets.toml.example` and not `secrets.toml.txt`).
- The file belongs inside the project's `.streamlit` folder, next to `config.toml`.
- It should contain:
  ```toml
  GEMINI_API_KEY = "your-real-key"
  GEMINI_MODEL = "gemini-3.8-flash"
  ```
- Restart Streamlit after saving. For Streamlit Community Cloud, add the TOML values in **Settings → Secrets**; a local secret file does not upload to GitHub.
- The actual key is never displayed in the UI. The chatbot now gives a short, sanitized explanation for common API failures.


## Troubleshooting Gemini configuration
- The correct TOML format includes double quotes around the key: `GEMINI_API_KEY = "your-real-key"`. Replace the placeholder with the actual key but keep the quotes.
- Save the file (`Ctrl+S`); an unsaved dot on the VS Code tab means your latest edit has not been saved.
- The exact local file is `<project-folder>/.streamlit/secrets.toml`, next to `.streamlit/config.toml`. Do not put the key in `secrets.toml.example`.
- Stop Streamlit with `Ctrl+C` and run `streamlit run app.py` again after changing secrets. Make sure the terminal is in the same project folder as `app.py`.
- On Streamlit Community Cloud, configure the same TOML values under **App → Settings → Secrets**; a local secrets file is not uploaded with GitHub.
- The key is a secret. Never commit `secrets.toml`, publish screenshots containing it, or paste it into chats.


## UI design notes
- The four main service cards use matching fixed height and title spacing. Their “খুলুন” buttons should align evenly.
- Secondary buttons have a light grey-green background with green text and outline; primary buttons remain green.
- Chat input and chat messages are styled for readable dark text on light backgrounds.
- Streamlit's theme is explicitly set to light in `.streamlit/config.toml`.
