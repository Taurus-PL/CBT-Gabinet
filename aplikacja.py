import streamlit as st
import pandas as pd

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Zapis Przebiegu Terapii CBT", layout="wide")

# --- KOMPLEKSOWA BAZA WIEDZY I MODELE CBT ---
slownik_modeli = {
    "F41.0": [
        {
            "Model": "Model poznawczy lęku panicznego (D. Clark)",
            "Opis": "Skupienie na błędnej, katastroficznej interpretacji normalnych doznań z ciała (np. kołatanie serca = zawał).",
            "Interwencje": "Reatrybucja doznań, hiperwentylacja (eksperyment), eliminacja zachowań zabezpieczających.",
            "Wizualizacja": "graph TD\nA[Wyzwalacz] --> B[Postrzegane zagrożenie]\nB --> C[Lęk / Niepokój]\nC --> D[Doznania somatyczne]\nD --> E{Katastroficzna interpretacja}\nE -- Błędne koło --> B"
        }
    ],
    "F32": [
        {
            "Model": "Triada Poznawcza Depresji (A. Beck)",
            "Opis": "Negatywna wizja siebie, świata i przyszłości wynikająca z dysfunkcjonalnych schematów.",
            "Interwencje": "Tabela Becka, restrukturyzacja poznawcza, testowanie przekonań.",
            "Wizualizacja": "graph TD\nA((Negatywne myśli O SOBIE)) <--> B((Negatywne myśli O ŚWIECIE))\nB <--> C((Negatywne myśli O PRZYSZŁOŚCI))\nC <--> A"
        },
        {
            "Model": "Aktywacja Behawioralna (C. Martell)",
            "Opis": "Depresja jako wynik spadku wzmocnień pozytywnych. Bierność pogłębia brak wzmocnień.",
            "Interwencje": "Monitorowanie aktywności, planowanie 'przyjemność i mistrzostwo'.",
            "Wizualizacja": "graph TD\nA[Stresory] --> B[Obniżony nastrój]\nB --> C[Wycofanie / Bierność]\nC --> D[Mniej wzmocnień]\nD -- Błędne koło --> B"
        }
    ],
    "F42": [
        {
            "Model": "Model poznawczy OCD (P. Salkovskis)",
            "Opis": "Przesadne poczucie odpowiedzialności (TAF). Myśl natrętna interpretowana jako realne zagrożenie.",
            "Interwencje": "Restrukturyzacja odpowiedzialności, ciasto odpowiedzialności.",
            "Wizualizacja": "graph TD\nA[Wyzwalacz] --> B[Obsesja]\nB --> C{Ocena: Odpowiedzialność}\nC --> D[Lęk]\nD --> E[Kompulsja]\nE -- Ulga --> C"
        }
    ],
    "F41.1": [
        {
            "Model": "Model Nietolerancji Niepewności (M. Dugas)",
            "Opis": "Zamartwianie się jako unikający styl radzenia sobie z lękiem.",
            "Interwencje": "Trening rozwiązywania problemów, ekspozycja na wyobrażenia.",
            "Wizualizacja": "graph TD\nA[Niepewność] --> B{Nietolerancja}\nB --> C[Zamartwianie]\nC --> D[Iluzja kontroli]"
        }
    ],
    "F43.1": [
        {
            "Model": "Model poznawczy PTSD (Ehlers i Clark)",
            "Opis": "Poczucie ciągłego zagrożenia przez negatywną ocenę traumy i zaburzenia pamięci.",
            "Interwencje": "Aktualizacja pamięci traumy, restrukturyzacja punktów zapalnych.",
            "Wizualizacja": "graph TD\nA[Trauma] --> B[Negatywna ocena]\nA --> C[Pamięć zmysłowa]\nB --> D[Poczucie zagrożenia]\nC --> D\nD --> E[Unikanie]"
        }
    ]
}
slownik_modeli["F33"] = slownik_modeli["F32"]

# --- BAZA ASYSTENTA DIAGNOZY (PEŁNA) ---
baza_symptomow = [
    {
        "slowa_kluczowe": ["serce", "panika", "umrę", "zawał", "duszno", "zemdleję"], 
        "diagnoza": "F41.0 Lęk paniczny", 
        "roznicowa": "Agorafobia, PTSD, Zaburzenia kardiologiczne, Tarczyca.",
        "cbt_problemy": "Katastroficzna interpretacja doznań somatycznych, silne zachowania zabezpieczające.",
        "cele_smart": "1. Redukcja napadów paniki do 0.\n2. Eliminacja zachowań zabezpieczających (noszenie leków).",
        "protokol_nazwa": "Terapia Poznawcza D. Clarka",
        "uzasadnienie_planu": "Reatrybucja doznań poprzez eksperymenty behawioralne i ekspozycję interoceptywną."
    },
    {
        "slowa_kluczowe": ["smutek", "brak sił", "beznadziejny", "leżę", "nie cieszy", "płaczę"], 
        "diagnoza": "F32 Epizod depresyjny", 
        "roznicowa": "ChAD, Dystymia, Niedoczynność tarczycy.",
        "cbt_problemy": "Negatywna triada Becka, bierność, deficyt wzmocnień pozytywnych.",
        "cele_smart": "1. Zwiększenie aktywności (spacery 3x/tydz).\n2. Redukcja ruminacji poprzez zapis myśli.",
        "protokol_nazwa": "Aktywacja Behawioralna (BA) / Terapia Becka",
        "uzasadnienie_planu": "Przerwanie cyklu bierności i restrukturyzacja negatywnych schematów poznawczych."
    }
]

# --- PEŁNA BAZA ICD-10 ---
icd10_full = {
    "F30-F39 Zaburzenia nastroju": ["F32 Epizod depresyjny", "F33 Zaburzenia depresyjne nawracające", "F31 ChAD", "F34.1 Dystymia"],
    "F40-F48 Zaburzenia lękowe": ["F41.0 Lęk paniczny", "F40.1 Fobia społeczna", "F41.1 GAD", "F42 OCD", "F43.1 PTSD", "F40.0 Agorafobia"],
    "F60-F69 Zaburzenia osobowości": ["F60.31 Borderline", "F60.5 Anankastyczna", "F60.6 Unikająca", "F60.7 Zależna"]
}

# --- INICJALIZACJA STANU ---
if 'st_problemy' not in st.session_state: st.session_state.st_problemy = ""
if 'st_cele' not in st.session_state: st.session_state.st_cele = ""
if 'st_protokol' not in st.session_state: st.session_state.st_protokol = ""
if 'st_uzasadnienie' not in st.session_state: st.session_state.st_uzasadnienie = ""

# --- UI ---
st.sidebar.title("🛡️ Panel CBT")
menu = st.sidebar.radio("Menu:", ["I. Konceptualizacja", "II. Plan Terapii", "III. Notatki"])

if menu == "I. Konceptualizacja":
    st.title("I. Diagnoza i Konceptualizacja")
    
    with st.expander("🤖 Asystent Diagnozy (NLP)", expanded=True):
        objawy_in = st.text_area("Wpisz wywiad/objawy:")
        if st.button("Generuj dokumentację"):
            for el in baza_symptomow:
                if any(k in objawy_in.lower() for k in el["slowa_kluczowe"]):
                    st.session_state.st_problemy = el["cbt_problemy"]
                    st.session_state.st_cele = el["cele_smart"]
                    st.session_state.st_protokol = el["protokol_nazwa"]
                    st.session_state.st_uzasadnienie = el["uzasadnienie_planu"]
                    st.success(f"Wykryto: {el['diagnoza']}")

    col1, col2 = st.columns(2)
    with col1:
        kat = st.selectbox("Grupa:", list(icd10_full.keys()))
        diag = st.selectbox("Rozpoznanie:", icd10_full[kat])
        kod_icd = diag.split(" ")[0]
        
        st.session_state.st_problemy = st.text_area("Problemy:", value=st.session_state.st_problemy, height=150)
        st.session_state.st_cele = st.text_area("Cele SMART:", value=st.session_state.st_cele, height=150)

    with col2:
        st.subheader("Baza Wiedzy EBM")
        if kod_icd in slownik_modeli:
            for m in slownik_modeli[kod_icd]:
                with st.container(border=True):
                    st.markdown(f"#### {m['Model']}")
                    st.write(m['Opis'])
                    with st.expander("Schemat"):
                        st.markdown(f"```mermaid\n{m['Wizualizacja']}\n```")
        else:
            st.info("Brak modelu dla tego kodu.")

    st.divider()
    st.subheader("Poziom 2 i 3")
    st.text_area("Przekonania kluczowe (o sobie, innych, świecie):")
    st.text_area("Historia uczenia się (czynniki rozwojowe):")

elif menu == "II. Plan Terapii":
    st.title("II. Plan i Interwencje")
    st.session_state.st_protokol = st.text_input("Protokół:", value=st.session_state.st_protokol)
    st.session_state.st_uzasadnienie = st.text_area("Uzasadnienie:", value=st.session_state.st_uzasadnienie, height=200)

elif menu == "III. Notatki":
    st.title("III. Przebieg Sesji")
    st.text_area("Notatki z sesji:", height=400)
