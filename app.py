import streamlit as st
import google.generativeai as genai
import json, os, pandas as pd
from datetime import datetime

# Design-Optimierung: Minimalistischer "App-Look"
st.set_page_config(page_title="Macro AI", page_icon="🍏")
st.markdown("""
    <style>
    div.stButton > button { border-radius: 20px; width: 100%; background: #007aff; color: white; border: none; }
    .stTextInput > div > div > input { border-radius: 15px; }
    .css-1544g2n { padding: 1rem; }
    </style>
""", unsafe_allow_html=True)

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# Einfache Speicherung in einer Datei
DB_FILE = "data.json"
def load():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f: return json.load(f)
    return {"mahlzeiten": []}

data = load()

st.title("🍏 Macro AI")

# UI Eingabe
input_text = st.text_input("", placeholder="Was hast du gegessen?")
if st.button("Hinzufügen"):
    if input_text:
        with st.spinner("Berechne..."):
            prompt = f"Du bist ein Ernährungsberater. Analysiere: '{input_text}'. Antworte NUR als JSON: {{\"beschreibung\": \"...\", \"kcal\": 0, \"protein\": 0, \"carbs\": 0, \"fett\": 0}}"
            response = model.generate_content(prompt)
            
            try:
                content = response.text.replace("```json", "").replace("```", "").strip()
                item = json.loads(content)
                item["uhrzeit"] = datetime.now().strftime("%H:%M")
                data["mahlzeiten"].insert(0, item)
                with open(DB_FILE, "w") as f: json.dump(data, f)
                st.rerun()
            except:
                st.error("Fehler bei der KI-Antwort.")

# Anzeige
for m in data["mahlzeiten"]:
    st.markdown(f"""
    <div style="background:white; padding:10px; border-radius:15px; margin-bottom:10px; box-shadow: 0 2px 5px #eee;">
        <strong>{m['beschreibung']}</strong><br>
        <small>{m['kcal']} kcal | P:{m['protein']}g C:{m['carbs']}g F:{m['fett']}g</small>
    </div>
    """, unsafe_allow_html=True)
