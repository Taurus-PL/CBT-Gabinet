import streamlit as st
import pandas as pd

# Konfiguracja strony
st.set_page_config(page_title="System CBT - Pełne ICD-10", layout="wide")

# --- KOMPLETNA BAZA ICD-10 (F00-F99) ---
icd10_full = {
    "F00-F09 Zaburzenia psychiczne organiczne": [
        "F00 Otępienie w chorobie Alzheimera", "F01 Otępienie naczyniowe", "F02 Otępienie w innych chorobach", 
        "F03 Otępienie niesprecyzowane", "F04 Organiczny zespół amnestyczny", "F05 Majaczenie (niealkoholowe)",
        "F06 Inne zaburzenia psychiczne wskutek uszkodzenia mózgu", "F07 Zaburzenia osobowości wskutek choroby mózgu",
        "F09 Organiczne zaburzenia psychiczne niesprecyzowane"
    ],
    "F10-F19 Zaburzenia spowodowane substancjami psychoaktywnymi": [
        "F10 Zaburzenia spowodowane alkoholem", "F11 Zaburzenia spowodowane opioidami", "F12 Zaburzenia spowodowane kanabinoidami",
        "F13 Zaburzenia spowodowane lekami uspokajającymi i nasennymi", "F14 Zaburzenia spowodowane kokainą",
        "F15 Zaburzenia spowodowane innymi stymulantami (w tym kofeina)", "F16 Zaburzenia spowodowane halucynogenami",
        "F17 Zaburzenia spowodowane paleniem tytoniu", "F18 Zaburzenia spowodowane lotnymi rozpuszczalnikami",
        "F19 Zaburzenia spowodowane wieloma substancjami"
    ],
    "F20-F29 Schizofrenia, zaburzenia schizotypowe i urojeniowe": [
        "F20 Schizofrenia", "F21 Zaburzenie schizotypowe", "F22 Uporczywe zaburzenia urojeniowe",
        "F23 Ostre i przemijające zaburzenia psychotyczne", "F24 Indukowane zaburzenia urojeniowe",
        "F25 Zaburzenia schizoafektywne", "F28 Inne nieorganiczne zaburzenia psychotyczne",
        "F29 Nieorganiczna psychoza niesprecyzowana"
    ],
    "F30-F39 Zaburzenia nastroju (afektywne)": [
        "F30 Epizod maniakalny", "F31 Zaburzenie afektywne dwubiegunowe (ChAD)",
        "F32 Epizod depresyjny", "F33 Zaburzenia depresyjne nawracające",
        "F34 Uporczywe zaburzenia nastroju (Dystymia / Cyklotymia)", "F38 Inne zaburzenia nastroju",
        "F39 Zaburzenia nastroju niesprecyzowane"
    ],
    "F40-F48 Zaburzenia nerwicowe, związane ze stresem i somatoformiczne": [
        "F40.0 Agorafobia", "F40.1 Fobie społeczne", "F40.2 Specyficzne postacie fobii",
        "F41.0 Zaburzenie lękowe z napadami lęku (Lęk paniczny)", "F41.1 Zaburzenie lękowe uogólnione (GAD)",
        "F41.2 Zaburzenie lękowo-depresyjne mieszane", "F42 Zaburzenie obsesyjno-kompulsyjne (OCD)",
        "F43.0 Ostra reakcja na stres", "F43.1 Zaburzenie stresowe pourazowe (PTSD)",
        "F43.2 Zaburzenia adaptacyjne", "F44 Zaburzenia dysocjacyjne (konwersyjne)",
        "F45 Zaburzenia pod postacią somatyczną", "F48 Inne zaburzenia nerwicowe (Neurastenia)"
    ],
    "F50-F59 Zespoły behawioralne związane z czynnikami fizjologicznymi": [
        "F50.0 Jadłowstręt psychiczny (Anoreksja)", "F50.2 Żarłoczność psychiczna (Bulimia)",
        "F50.4 Przejadanie się związane z czynnikami psychologicznymi", "F51 Nieorganiczne zaburzenia snu",
        "F52 Dysfunkcje seksualne niespowodowane zmianami organicznymi", "F53 Zaburzenia psychiczne połogu",
        "F54 Czynniki psychologiczne związane z chorobami gdzie indziej sklasyfikowanymi", "F55 Nadużywanie substancji niepowodujących uzależnienia"
    ],
    "F60-F69 Zaburzenia osobowości i zachowania dorosłych": [
        "F60.0 Osobowość paranoiczna", "F60.1 Osobowość schizoidalna", "F60.2 Osobowość dyssocjalna",
        "F60.30 Osobowość chwiejna emocjonalnie - typ impulsywny", "F60.31 Osobowość chwiejna emocjonalnie - typ borderline",
        "F60.4 Osobowość histrioniczna", "F60.5 Osobowość anankastyczna (OCPD)",
        "F60.6 Osobowość lękliwa (unikająca)", "F60.7 Osobowość zależna", "F61 Mieszane zaburzenia osobowości",
        "F62 Trwałe zmiany osobowości niewynikające z uszkodzenia mózgu", "F63 Zaburzenia nawyków i popędów (Hazard, Piromania)",
        "F64 Zaburzenia identyfikacji płciowej", "F65 Zaburzenia preferencji seksualnych", "F66 Zaburzenia rozwoju seksualnego"
    ],
    "F70-F79 Upośledzenie umysłowe": [
        "F70 Upośledzenie umysłowe lekkie", "F71 Upośledzenie umysłowe umiarkowane",
        "F72 Upośledzenie umysłowe znaczne", "F73 Upośledzenie umysłowe głębokie"
    ],
    "F80-F89 Zaburzenia rozwoju psychicznego": [
        "F80 Zaburzenia rozwoju mowy i języka", "F81 Specyficzne zaburzenia rozwoju umiejętności szkolnych",
        "F82 Specyficzne zaburzenia rozwoju funkcji motorycznych", "F84 Zaburzenia głębokie rozwoju (Autyzm, Zespół Aspergera)"
    ],
    "F90-F98 Zaburzenia zachowania i emocji (dzieci i młodzież)": [
        "F90 Zaburzenia hiperkinetyczne (ADHD)", "F91 Zaburzenia zachowania",
        "F92 Mieszane zaburzenia zachowania i emocji", "F93 Zaburzenia emocjonalne specyficzne dla dzieciństwa",
        "F94 Zaburzenia funkcjonowania społecznego (Mutyzm wybiórczy)", "F95 Tiki",
        "F98 Inne zaburzenia (Moczenie nocne, Jąkanie)"
    ]
}

if 'baza' not in st.session_state:
    st.session_state.baza = []

# --- NAWIGACJA ---
st.sidebar.title("🛡️ System CBT Pro")
menu = st.sidebar.radio("Nawigacja:", ["Nowy Arkusz Terapii", "Archiwum Diagnoz"])

# --- MODUŁ 1: FORMULARZ ---
if menu == "Nowy Arkusz Terapii":
    st.header("Zapis Przebiegu Terapii (Pełne ICD-10)")
    
    with st.expander("Metryczka", expanded=True):
        col1, col2 = st.columns(2)
        imie = col1.text_input("Pacjent (inicjały)")
        wiek = col2.number_input("Wiek", 0, 110)
        terapeuta = col1.text_input("Terapeuta")
        data = col2.date_input("Data sesji")

    with st.expander("I.1. Diagnoza Kliniczna (Pełna lista)", expanded=True):
        # Kaskadowy wybór diagnozy
        kat_wybrana = st.selectbox("Wybierz grupę kategorii ICD-10:", list(icd10_full.keys()))
        kod_wybrany = st.selectbox("Wybierz konkretne rozpoznanie:", icd10_full[kat_wybrana])
        st.info(f"Wybrane rozpoznanie: **{kod_wybrany}**")
        
        st.multiselect("Zaburzenia współwystępujące:", 
                      [item for sublist in icd10_full.values() for item in sublist])
        
        st.text_area("Badanie stanu psychicznego")

    with st.expander("Funkcjonowanie Pacjenta (Pola opisowe)"):
        f_rodzina = st.text_area("Sfera rodzinna (funkcjonowanie i trudności)")
        f_praca = st.text_area("Sfera zawodowa / szkolna (funkcjonowanie i trudności)")
        f_spoleczna = st.text_area("Sfera społeczna (funkcjonowanie i trudności)")

    with st.expander("I.3. Konceptualizacja Poziom I (ABC)"):
        st.text_area("Sytuacja (A)")
        st.text_area("Myśli Automatyczne (B)")
        st.text_area("Emocje / Fizjologia / Zachowanie (C)")

    if st.button("💾 ZAPISZ TERAPIĘ DO BAZY"):
        wpis = {
            "Pacjent": imie, "Wiek": wiek, "Kod": kod_wybrany, 
            "Data": data, "Rodzina": f_rodzina, "Praca": f_praca, "Spoleczna": f_spoleczna
        }
        st.session_state.baza.append(wpis)
        st.success(f"Pomyślnie zapisano kartę pacjenta {imie} pod kodem {kod_wybrany}")

# --- MODUŁ 2: ARCHIWUM ---
elif menu == "Archiwum Diagnoz":
    st.header("📂 Baza pacjentów według diagnozy")
    
    if not st.session_state.baza:
        st.warning("Baza danych jest pusta.")
    else:
        df = pd.DataFrame(st.session_state.baza)
        
        # Filtrowanie
        lista_kodow = ["Wszystkie"] + list(df['Kod'].unique())
        filtr = st.selectbox("Filtruj bazę po diagnozie ICD-10:", lista_kodow)
        
        widok = df if filtr == "Wszystkie" else df[df['Kod'] == filtr]
        
        st.table(widok[["Data", "Pacjent", "Kod"]])
        
        st.divider()
        for i, r in widok.iterrows():
            with st.expander(f"Szczegóły: {r['Pacjent']} ({r['Kod']})"):
                st.write(f"**Funkcjonowanie rodzinne:** {r['Rodzina']}")
                st.write(f"**Funkcjonowanie zawodowe:** {r['Praca']}")
                st.write(f"**Funkcjonowanie społeczne:** {r['Spoleczna']}")
