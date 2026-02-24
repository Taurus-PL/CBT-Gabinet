import streamlit as st
import pandas as pd

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Zapis Przebiegu Terapii CBT", layout="wide")

# --- BAZA WIEDZY I DIAGRAMY MERMAID ---
slownik_modeli = {
    "F41.0": [
        {
            "Model": "Model poznawczy lęku panicznego (D. Clark)",
            "Opis": "Skupienie na błędnej, katastroficznej interpretacji normalnych doznań z ciała.",
            "Interwencje": "Reatrybucja doznań, hiperwentylacja (eksperyment), eliminacja zachowań zabezpieczających.",
            "Wizualizacja": (
                "graph TD\n"
                "A[Wyzwalacz] --> B[Postrzegane zagrożenie]\n"
                "B --> C[Lęk / Niepokój]\n"
                "C --> D[Doznania somatyczne]\n"
                "D --> E{Katastroficzna interpretacja}\n"
                "E -- Błędne koło --> B\n"
            )
        }
    ],
    "F32": [
        {
            "Model": "Triada Poznawcza Depresji (A. Beck)",
            "Opis": "Negatywna wizja siebie, świata i przyszłości.",
            "Interwencje": "Tabela Becka, restrukturyzacja poznawcza, testowanie przekonań.",
            "Wizualizacja": (
                "graph TD\n"
                "A((Negatywne myśli O SOBIE)) <--> B((Negatywne myśli O ŚWIECIE))\n"
                "B <--> C((Negatywne myśli O PRZYSZŁOŚCI))\n"
                "C <--> A\n"
            )
        },
        {
            "Model": "Aktywacja Behawioralna (C. Martell)",
            "Opis": "Depresja jako wynik spadku wzmocnień pozytywnych. Bierność pogłębia obniżony nastrój.",
            "Interwencje": "Monitorowanie aktywności, planowanie zadań 'przyjemność i mistrzostwo'.",
            "Wizualizacja": (
                "graph TD\n"
                "A[Spadek wzmocnień] --> B[Obniżony nastrój]\n"
                "B --> C[Wycofanie / Bierność]\n"
                "C --> D[Brak okazji do poprawy nastroju]\n"
                "D -- Błędne koło --> B\n"
            )
        }
    ],
    "F40.1": [
        {
            "Model": "Model Lęku Społecznego (Clark i Wells)",
            "Opis": "Koncentracja uwagi na sobie i tworzenie negatywnego obrazu własnego 'ja'.",
            "Interwencje": "Trening uwagi na zewnątrz, wideo-feedback, eksperymenty behawioralne.",
            "Wizualizacja": (
                "graph TD\n"
                "A[Sytuacja społeczna] --> B[Zagrożenie społeczne]\n"
                "B --> C[Skupienie uwagi na sobie]\n"
                "C <--> D[Objawy somatyczne]\n"
                "C <--> E[Zachowania zabezpieczające]\n"
            )
        }
    ]
}
slownik_modeli["F33"] = slownik_modeli["F32"]

# --- BAZA ASYSTENTA ---
baza_symptomow = [
    {
        "slowa": ["serce", "panika", "umrę", "zawał", "duszno"],
        "diagnoza": "F41.0 Lęk paniczny",
        "problemy": "LĘK PANICZNY:\n- Katastroficzne myśli o zdrowiu\n- Zachowania zabezpieczające",
        "cele": "1. Redukcja napadów paniki.\n2. Rezygnacja z zachowań zabezpieczających.",
        "uzasadnienie": "Praca nad reatrybucją doznań fizycznych i eksperymenty behawioralne."
    },
    {
        "slowa": ["smutek", "brak sił", "beznadziejny", "leżę", "nic nie cieszy"],
        "diagnoza": "F32 Epizod depresyjny",
        "problemy": "DEPRESJA:\n- Negatywna triada poznawcza\n- Bierność i wycofanie",
        "cele": "1. Zwiększenie aktywności.\n2. Restrukturyzacja myśli automatycznych.",
        "uzasadnienie": "Aktywacja behawioralna oraz praca nad zniekształceniami poznawczymi."
    }
]

# --- STAN SESJI ---
if 'dane' not in st.session_state:
    st.session_state.dane = {"problemy": "", "cele": "", "uzasadnienie": "", "protokol": ""}

# --- INTERFEJS ---
st.sidebar.title("🛡️ Panel Terapeuty CBT")
nawigacja = st.sidebar.radio("Przejdź do:", ["Konceptualizacja", "Plan Terapii", "Archiwum"])

if nawigacja == "Konceptualizacja":
    st.title("I. Diagnoza i Konceptualizacja")
    
    with st.expander("🤖 Asystent Diagnozy", expanded=True):
        skarga = st.text_area("Wpisz objawy pacjenta:")
        if st.button("Generuj propozycję"):
            for item in baza_symptomow:
                if any(s in skarga.lower() for s in item["slowa"]):
                    st.session_state.dane["problemy"] = item["problemy"]
                    st.session_state.dane["cele"] = item["cele"]
                    st.session_state.dane["uzasadnienie"] = item["uzasadnienie"]
                    st.success(f"Dopasowano do: {item['diagnoza']}")

    c1, c2 = st.columns(2)
    kod_icd = c1.selectbox("Kod ICD-10:", ["F32", "F33", "F41.0", "F40.1", "F42", "F43.1"])
    
    st.subheader("Modele CBT dla tego rozpoznania")
    if kod_icd in slownik_modeli:
        for m in slownik_modeli[kod_icd]:
            st.info(f"**{m['Model']}**")
            st.write(m['Opis'])
            with st.expander("Zobacz diagram"):
                st.mermaid(m['Wizualizacja'])
    
    st.divider()
    st.session_state.dane["problemy"] = st.text_area("Lista problemów:", value=st.session_state.dane["problemy"], height=200)
    st.session_state.dane["cele"] = st.text_area("Cele SMART:", value=st.session_state.dane["cele"])

    st.subheader("Konceptualizacja - Poziom 2 i 3")
    st.text_area("Przekonania kluczowe (o sobie/świecie):")
    st.text_area("Strategie kompensacyjne:")
    st.text_area("Wydarzenia z dzieciństwa / Rozwojowe:")

elif nawigacja == "Plan Terapii":
    st.title("II. Plan i Interwencje")
    st.text_input("Wybrany protokół leczenia:", value=st.session_state.dane["protokol"])
    st.session_state.dane["uzasadnienie"] = st.text_area("Uzasadnienie planu:", value=st.session_state.dane["uzasadnienie"], height=150)
    st.divider()
    st.subheader("Rejestr sesji")
    st.text_area("Notatki z przebiegu sesji:", height=300)

elif nawigacja == "Archiwum":
    st.title("Archiwum")
    st.write("Lista pacjentów (w budowie)")

