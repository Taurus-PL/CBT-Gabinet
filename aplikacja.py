import streamlit as st

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Zapis Terapii CBT", layout="wide")

# --- BAZA WIEDZY I MODELE ---
slownik_modeli = {
    "F41.0": [
        {
            "Model": "Model poznawczy lęku panicznego (D. Clark)",
            "Opis": "Skupienie na błędnej, katastroficznej interpretacji normalnych doznań z ciała.",
            "Wizualizacja": "graph TD\nA[Wyzwalacz] --> B[Zagrożenie]\nB --> C[Lęk]\nC --> D[Doznania z ciała]\nD --> E{Błędna interpretacja}\nE -- Błędne koło --> B"
        }
    ],
    "F32": [
        {
            "Model": "Triada Poznawcza Depresji (A. Beck)",
            "Opis": "Negatywna wizja siebie, świata i przyszłości.",
            "Wizualizacja": "graph TD\nA((O SOBIE)) <--> B((O ŚWIECIE))\nB <--> C((O PRZYSZŁOŚCI))\nC <--> A"
        },
        {
            "Model": "Aktywacja Behawioralna (C. Martell)",
            "Opis": "Bierność pogłębia obniżony nastrój przez brak wzmocnień.",
            "Wizualizacja": "graph TD\nA[Spadek wzmocnień] --> B[Obniżony nastrój]\nB --> C[Bierność]\nC --> D[Brak poprawy]\nD -- Koło bierności --> B"
        }
    ],
    "F40.1": [
        {
            "Model": "Model Lęku Społecznego (Clark i Wells)",
            "Opis": "Koncentracja uwagi na sobie i tworzenie negatywnego obrazu własnego 'ja'.",
            "Wizualizacja": "graph TD\nA[Sytuacja] --> B[Zagrożenie]\nB --> C[Skupienie na sobie]\nC <--> D[Objawy]\nC <--> E[Zabezpieczenia]"
        }
    ]
}

# --- ASYSTENT LOGIKI ---
baza_symptomow = [
    {
        "slowa": ["serce", "panika", "umrę", "zawał"],
        "diagnoza": "F41.0 Lęk paniczny",
        "problemy": "POZNAWCZE: Katastrofizacja doznań fizycznych.\nBEHAWIORALNE: Zachowania zabezpieczające.",
        "cele": "1. Redukcja napadów paniki.\n2. Rezygnacja z zachowań zabezpieczających."
    },
    {
        "slowa": ["smutek", "brak sił", "beznadziejny", "leżę"],
        "diagnoza": "F32 Epizod depresyjny",
        "problemy": "POZNAWCZE: Negatywna triada.\nBEHAWIORALNE: Bierność i wycofanie.",
        "cele": "1. Zwiększenie aktywności.\n2. Restrukturyzacja myśli."
    }
]

# --- STAN SESJI ---
if 'problemy' not in st.session_state: st.session_state.problemy = ""
if 'cele' not in st.session_state: st.session_state.cele = ""

# --- UI ---
st.title("🛡️ Profesjonalny Zapis Terapii CBT")

menu = st.sidebar.radio("Etap pracy:", ["Konceptualizacja", "Plan Terapii"])

if menu == "Konceptualizacja":
    with st.expander("🤖 Szybki Asystent (wpisz objawy)", expanded=True):
        skarga = st.text_area("Co zgłasza pacjent?")
        if st.button("Analizuj"):
            for item in baza_symptomow:
                if any(s in skarga.lower() for s in item["slowa"]):
                    st.session_state.problemy = item["problemy"]
                    st.session_state.cele = item["cele"]
                    st.success(f"Dopasowano: {item['diagnoza']}")

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Dane kliniczne")
        kod_icd = st.selectbox("Kod ICD-10:", ["F32", "F41.0", "F40.1", "F42", "F43.1"])
        st.session_state.problemy = st.text_area("Lista problemów:", value=st.session_state.problemy, height=200)
        st.session_state.cele = st.text_area("Cele SMART:", value=st.session_state.cele, height=150)

    with col2:
        st.subheader("Sugerowane Modele Pracy")
        if kod_icd in slownik_modeli:
            for m in slownik_modeli[kod_icd]:
                with st.container(border=True):
                    st.markdown(f"**{m['Model']}**")
                    st.caption(m['Opis'])
                    if st.checkbox(f"Pokaż schemat: {m['Model']}", key=m['Model']):
                        st.markdown(f"```mermaid\n{m['Wizualizacja']}\n```")
        else:
            st.info("Brak szczegółowego modelu dla tego kodu w bazie.")

    st.divider()
    st.subheader("Poziom 2 i 3 (Mechanizmy i Historia)")
    st.text_area("Przekonania kluczowe i warunkowe:")
    st.text_area("Historia uczenia się (czynniki rozwojowe):")

elif menu == "Plan Terapii":
    st.title("II. Plan i Interwencje")
    st.text_input("Wybrany protokół:")
    st.text_area("Uzasadnienie planu leczenia:", height=150)
    st.divider()
    st.subheader("Notatki z sesji")
    st.text_area("Przebieg sesji i zadania domowe:", height=300)

