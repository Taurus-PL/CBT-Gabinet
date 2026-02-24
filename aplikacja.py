import streamlit as st
import pandas as pd

# Konfiguracja strony
st.set_page_config(page_title="System CBT - Arkusz ICD-10", layout="wide")

# --- BAZA DANYCH ICD-10 (Pełna klasyfikacja F) ---
icd10_kategorie = {
    "F00-F09: Zaburzenia psychiczne organiczne": [
        "F00 Otępienie w chorobie Alzheimera", "F01 Otępienie naczyniowe", 
        "F06 Inne zaburzenia psychiczne spowodowane uszkodzeniem mózgu", "F07 Zaburzenia osobowości i zachowania spowodowane chorobą mózgu"
    ],
    "F10-F19: Zaburzenia spowodowane substancjami": [
        "F10 Zaburzenia spowodowane alkoholem", "F11 Zaburzenia spowodowane używaniem opioidów",
        "F12 Zaburzenia spowodowane kanabinoidami", "F17 Zaburzenia spowodowane paleniem tytoniu"
    ],
    "F20-F29: Schizofrenia i zaburzenia urojeniowe": [
        "F20 Schizofrenia", "F21 Zaburzenie schizotypowe", "F22 Uporczywe zaburzenia urojeniowe",
        "F23 Ostre i przemijające zaburzenia psychotyczne", "F25 Zaburzenia schizoafektywne"
    ],
    "F30-F39: Zaburzenia nastroju (afektywne)": [
        "F30 Epizod maniakalny", "F31 Zaburzenie afektywne dwubiegunowe (ChAD)",
        "F32 Epizod depresyjny", "F33 Zaburzenia depresyjne nawracające", "F34 Uporczywe zaburzenia nastroju (Dystymia/Cyklotymia)"
    ],
    "F40-F48: Zaburzenia nerwicowe i związane ze stresem": [
        "F40.0 Agorafobia", "F40.1 Fobia społeczna", "F41.0 Zaburzenie lękowe z napadami lęku (Lęk paniczny)",
        "F41.1 Zaburzenie lękowe uogólnione (GAD)", "F41.2 Zaburzenie lękowo-depresyjne mieszane",
        "F42 Zaburzenie obsesyjno-kompulsyjne (OCD)", "F43.1 Zaburzenie stresowe pourazowe (PTSD)",
        "F43.2 Zaburzenia adaptacyjne", "F45 Zaburzenia pod postacią somatyczną (Somatyzacyjne)"
    ],
    "F50-F59: Zespoły behawioralne (odżywianie, sen)": [
        "F50.0 Jadłowstręt psychiczny (Anoreksja)", "F50.2 Żarłoczność psychiczna (Bulimia)",
        "F51 Nieorganiczne zaburzenia snu", "F52 Dysfunkcje seksualne"
    ],
    "F60-F69: Zaburzenia osobowości i zachowania dorosłych": [
        "F60.0 Osobowość paranoiczna", "F60.1 Osobowość schizoidalna", "F60.2 Osobowość dyssocjalna",
        "F60.3 Osobowość chwiejna emocjonalnie (Borderline/Impulsywna)", "F60.4 Osobowość histrioniczna",
        "F60.5 Osobowość anankastyczna", "F60.6 Osobowość lękliwa (unikająca)", "F60.7 Osobowość zależna"
    ],
    "F90-F98: Zaburzenia wieku dziecięcego": [
        "F90 Zaburzenia hiperkinetyczne (ADHD)", "F91 Zaburzenia zachowania",
        "F94 Zaburzenia funkcjonowania społecznego", "F95 Tiki"
    ]
}

# --- OBSŁUGA ZAPISU (Session State) ---
if 'archiwum_terapii' not in st.session_state:
    st.session_state.archiwum_terapii = []

# --- NAWIGACJA ---
with st.sidebar:
    st.title("🛡️ CBT Gabinet Pro")
    opcja = st.radio("Menu:", ["Dodaj nową terapię", "Baza i Filtrowanie (ICD-10)"])
    st.divider()
    st.info("System oparty na formularzu Popiel/Pragłowska")

# --- MODUŁ: DODAWANIE TERAPII ---
if opcja == "Dodaj nową terapię":
    st.header("Nowy Zapis Przebiegu Terapii (ICD-10)")
    
    with st.form("arkusz_form"):
        # Metryczka
        c1, c2 = st.columns(2)
        with c1:
            imie = st.text_input("Pacjent (inicjały)")
            wiek = st.number_input("Wiek", 0, 120)
        with c2:
            terapeuta = st.text_input("Terapeuta")
            data = st.date_input("Data wpisu")

        # Diagnoza ICD-10
        st.subheader("I.1. Diagnoza nozologiczna")
        kat_icd = st.selectbox("Wybierz grupę ICD-10:", list(icd10_kategorie.keys()))
        kod_icd = st.selectbox("Wybierz konkretne rozpoznanie:", icd10_kategorie[kat_icd])
        
        # Funkcjonowanie (puste pola opisowe)
        st.subheader("Funkcjonowanie pacjenta")
        f_rodzina = st.text_area("Sfera rodzinna")
        f_praca = st.text_area("Sfera zawodowa/szkolna")
        f_spoleczna = st.text_area("Sfera społeczna")

        # Konceptualizacja ABC
        st.subheader("I.3. Konceptualizacja Poziom I")
        abc_a = st.text_area("A - Wyzwalacz")
        abc_b = st.text_area("B - Myśli automatyczne")
        abc_c = st.text_area("C - Emocje / Fizjologia / Zachowanie")

        # Przycisk zapisu
        submit = st.form_submit_button("Zapisz w bazie")
        
        if submit:
            nowy_wpis = {
                "Pacjent": imie, "Wiek": wiek, "Kod": kod_icd, "Grupa": kat_icd,
                "Rodzina": f_rodzina, "Praca": f_praca, "Społeczna": f_spoleczna,
                "Myśli": abc_b, "Data": data, "Terapeuta": terapeuta
            }
            st.session_state.archiwum_terapii.append(nowy_wpis)
            st.success(f"Zapisano terapię pacjenta {imie} pod kodem {kod_icd}")

# --- MODUŁ: ARCHIWUM I FILTROWANIE ---
elif opcja == "Baza i Filtrowanie (ICD-10)":
    st.header("📂 Baza Terapii wg Diagnoz")
    
    if not st.session_state.archiwum_terapii:
        st.warning("Baza danych jest pusta.")
    else:
        # Filtrowanie po diagnozie
        diagnozy_w_bazie = list(set([p['Kod'] for p in st.session_state.archiwum_terapii]))
        wybrany_kod = st.selectbox("🔍 Filtruj po diagnozie ICD-10:", ["Wszystkie"] + diagnozy_w_bazie)
        
        df = pd.DataFrame(st.session_state.archiwum_terapii)
        if wybrany_kod != "Wszystkie":
            df = df[df['Kod'] == wybrany_kod]
        
        st.dataframe(df[["Data", "Pacjent", "Kod", "Terapeuta"]], use_container_width=True)
        
        st.divider()
        st.subheader("Szczegóły wybranych przypadków")
        for i, r in df.iterrows():
            with st.expander(f"Pacjent: {r['Pacjent']} | Diagnoza: {r['Kod']}"):
                st.write(f"**Funkcjonowanie rodzinne:** {r['Rodzina']}")
                st.write(f"**Główne myśli automatyczne:** {r['Myśli']}")
                st.write(f"**Data wpisu:** {r['Data']}")
