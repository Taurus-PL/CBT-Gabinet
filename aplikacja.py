import streamlit as st
import pandas as pd

# --- KONFIGURACJA ---
st.set_page_config(page_title="Asystent CBT", layout="wide")

# --- BAZA WIEDZY (MODELE) ---
slownik_modeli = {
    "F41.0": [{"Model": "Model Clarka (Panika)", "Opis": "Katastroficzna interpretacja doznań."}],
    "F32": [
        {"Model": "Triada Becka (Depresja)", "Opis": "Negatywna wizja siebie/świata/przyszłości."},
        {"Model": "Aktywacja Behawioralna (Martell)", "Opis": "Błędne koło wycofania i braku wzmocnień."}
    ],
    "F40.1": [{"Model": "Model Clarka i Wellsa (Lęk społeczny)", "Opis": "Koncentracja na sobie i obrazie 'ja'."}],
    "F42": [{"Model": "Model Salkovskisa (OCD)", "Opis": "Nadmierna odpowiedzialność za myśli."}],
    "F41.1": [{"Model": "Model Dugasa (GAD)", "Opis": "Nietolerancja niepewności."}],
    "F43.1": [{"Model": "Przedłużona Ekspozycja (Foa)", "Opis": "Unikanie wspomnień traumatycznych."}]
}
slownik_modeli["F33"] = slownik_modeli["F32"]

# --- BAZA ASYSTENTA (SŁOWA KLUCZOWE) ---
baza_symptomow = [
    {"klucze": ["serce", "panika", "umrę", "zawał"], "diagnoza": "F41.0 Lęk paniczny", "cele": "Redukcja napadów, eliminacja zachowań zabezpieczających."},
    {"klucze": ["smutek", "brak sił", "beznadziejny", "leżę"], "diagnoza": "F32 Depresja", "cele": "Aktywizacja, zmiana NMA."},
    {"klucze": ["myję", "sprawdzam", "natrętne", "liczę"], "diagnoza": "F42 OCD", "cele": "Powstrzymanie reakcji (ERP)."},
    {"klucze": ["ludzie", "oceniają", "wstyd", "czerwienię"], "diagnoza": "F40.1 Fobia społeczna", "cele": "Trening uwagi, ekspozycja."},
    {"klucze": ["martwię", "niepewność", "a co jeśli"], "diagnoza": "F41.1 GAD", "cele": "Tolerancja niepewności, odraczanie martwienia."},
    {"klucze": ["trauma", "wypadek", "wraca", "flashback"], "diagnoza": "F43.1 PTSD", "cele": "Przetworzenie wspomnienia, ekspozycja."}
]

# --- INICJALIZACJA STANU ---
if 'diagnoza_wykryta' not in st.session_state: st.session_state.diagnoza_wykryta = "F32 Epizod depresyjny"
if 'problemy_text' not in st.session_state: st.session_state.problemy_text = ""
if 'cele_text' not in st.session_state: st.session_state.cele_text = ""

# --- UI ---
st.title("🛡️ System Wspomagania Decyzji CBT")

with st.sidebar:
    st.header("1. Szybka Analiza")
    skarga = st.text_area("Co zgłasza pacjent?")
    
    if st.button("🔍 Analizuj"):
        for poz in baza_symptomow:
            if any(k in skarga.lower() for k in poz["klucze"]):
                st.session_state.diagnoza_wykryta = poz["diagnoza"]
                st.session_state.cele_text = poz["cele"]
                st.rerun()

# --- GŁÓWNY FORMULARZ ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Konceptualizacja")
    diagnoza = st.selectbox("Rozpoznanie (ICD-10):", 
                            ["F32 Epizod depresyjny", "F41.0 Lęk paniczny", "F42 OCD", "F40.1 Fobia społeczna", "F41.1 GAD", "F43.1 PTSD"],
                            index=0)
    
    kod = diagnoza.split(" ")[0]
    
    st.session_state.problemy_text = st.text_area("Lista problemów:", value=st.session_state.problemy_text, height=150)
    st.session_state.cele_text = st.text_area("Cele SMART:", value=st.session_state.cele_text, height=100)

with col2:
    st.subheader("Sugerowane Modele CBT")
    
    # Logika sugerowania na podstawie listy problemów
    if kod in slownik_modeli:
        for m in slownik_modeli[kod]:
            with st.container(border=True):
                st.markdown(f"#### {m['Model']}")
                st.write(m['Opis'])
                if st.button(f"Wybierz {m['Model']}", key=m['Model']):
                    st.success(f"Wybrano model: {m['Model']}. Możesz go teraz opisać w planie terapii.")
    else:
        st.info("Wybierz diagnozę, aby zobaczyć modele.")

st.divider()
st.subheader("II. Plan Interwencji")
plan = st.text_area("Opisz wybrane interwencje i techniki:")

if st.button("💾 Zapisz sesję"):
    st.balloons()
    st.success("Dokumentacja przygotowana do skopiowania!")
