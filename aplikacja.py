import streamlit as st

# Konfiguracja strony
st.set_page_config(page_title="Zapis Przebiegu Terapii - System Pro", layout="wide")

# --- SŁOWNIK DIAGNOSTYCZNY (ICD-11 / DSM-5) ---
# Struktura pogrupowana dla ułatwienia nawigacji
kategorie_diagnoz = {
    "Zaburzenia lękowe i związane ze strachem": [
        "6B00 Zaburzenie lękowe uogólnione (GAD)",
        "6B01 Zaburzenie lękowe z napadami lęku (Lęk paniczny)",
        "6B02 Specyficzna fobia",
        "6B03 Zaburzenie lękowe społeczne (Fobia społeczna)",
        "6B04 Agorafobia",
        "6B05 Zaburzenie lękowe separacyjne"
    ],
    "Zaburzenia nastroju (Afektywne)": [
        "6A70 Pojedynczy epizod depresyjny",
        "6A71 Zaburzenie depresyjne nawracające",
        "6A72 Zaburzenie dystymiczne",
        "6A60 Zaburzenie afektywne dwubiegunowe typu I",
        "6A61 Zaburzenie afektywne dwubiegunowe typu II",
        "6A62 Zaburzenie cyklotymiczne"
    ],
    "Zaburzenia obsesyjno-kompulsyjne i pokrewne": [
        "6B20 Zaburzenie obsesyjno-kompulsyjne (OCD)",
        "6B21 Zaburzenie dysmorficzne (Body Dysmorphic Disorder)",
        "6B22 Zaburzenie zbieractwa (Hoarding)",
        "6B24 Trichotillomania",
        "6B25 Zaburzenie skubania skóry (Excoriation)"
    ],
    "Zaburzenia związane ze stresem": [
        "6B40 Zaburzenie stresowe pourazowe (PTSD)",
        "6B41 Złożone zaburzenie stresowe pourazowe (CPTSD)",
        "6B42 Zaburzenie adaptacyjne",
        "6B43 Przedłużona reakcja żałoby"
    ],
    "Zaburzenia odżywiania i jedzenia": [
        "6B80 Jadłowstręt psychiczny (Anorexia Nervosa)",
        "6B81 Żarłoczność psychiczna (Bulimia Nervosa)",
        "6B82 Zaburzenie z napadami objadania się (Binge Eating)",
        "6B83 Unikanie/restrykcyjne przyjmowanie pokarmów (ARFID)"
    ],
    "Zaburzenia neurorozwojowe": [
        "6A02 Zaburzenie ze spektrum autyzmu (ASD)",
        "6A05 Zaburzenie z deficytem uwagi i nadaktywnością (ADHD)",
        "6A00 Zaburzenia rozwoju intelektualnego",
        "6A01 Zaburzenia rozwojowe mowy lub języka"
    ],
    "Zaburzenia osobowości": [
        "6D10 Łagodne zaburzenie osobowości",
        "6D11 Umiarkowane zaburzenie osobowości",
        "6D11.5 Typ Borderline (Wzorce osobowości)",
        "DSM-5: Osobowość paranoiczna",
        "DSM-5: Osobowość narcystyczna",
        "DSM-5: Osobowość unikająca",
        "DSM-5: Osobowość zależna",
        "DSM-5: Osobowość antyspołeczna"
    ],
    "Zaburzenia psychotyczne": [
        "6A20 Schizofrenia",
        "6A21 Zaburzenie schizoafektywne",
        "6A23 Zaburzenie urojeniowe"
    ]
}

# --- INTERFEJS ---
st.title("ZAPIS PRZEBIEGU TERAPII 2021 – FORMULARZ")
st.caption("Zgodny z arkuszem A. Popiel i E. Pragłowskiej")

with st.sidebar:
    sekcja = st.radio("Sekcje arkusza:", [
        "Metryczka", "I.1. Diagnoza", "I.2. Problemy", "I.3. Konceptualizacja", "II. Plan", "III. Ewaluacja"
    ])

if sekcja == "Metryczka":
    st.header("Metryczka i Autorefleksja")
    st.text_input("Terapeuta")
    st.text_input("Pacjent")
    st.checkbox("Czy pacjent jest bezpieczny?")
    st.text_area("Moje własne ABC (terapeuty)")

elif sekcja == "I.1. Diagnoza":
    st.header("I.1. Ogólna diagnoza kliniczna")
    st.text_area("Zgłaszane problemy i wywiad")
    st.text_area("Opis badania stanu psychicznego")
    
    st.subheader("Wybór diagnozy (ICD-11 / DSM-5)")
    
    # KROK 1: Wybór kategorii
    kat = st.selectbox("Wybierz grupę zaburzeń:", [""] + list(kategorie_diagnoz.keys()))
    
    # KROK 2: Wybór konkretnego zaburzenia
    if kat:
        diagnoza = st.selectbox("Wybierz jednostkę statystyczną:", kategorie_diagnoz[kat])
        st.success(f"Wybrano: {diagnoza}")
    
    st.multiselect("Zaburzenia współwystępujące:", 
                  [item for sublist in kategorie_diagnoz.values() for item in sublist])
    
    st.text_input("Inna diagnoza / Kod spoza listy:")
    st.text_input("Choroby somatyczne")

    st.subheader("Opis funkcjonowania")
    st.text_area("Sfera rodzinna")
    st.text_area("Sfera zawodowa/szkolna")
    st.text_area("Sfera społeczna")

elif sekcja == "I.3. Konceptualizacja":
    st.header("I.3. Konceptualizacja")
    
    st.subheader("Poziom I (ABC)")
    col1, col2 = st.columns(2)
    with col1:
        st.text_area("A - Wyzwalacz")
        st.text_area("B - Myśli")
    with col2:
        st.text_area("C - Emocje/Fizjologia")
        st.text_area("C - Zachowanie")
    
    st.divider()
    st.subheader("Poziom II")
    st.text_area("Przekonania kluczowe")
    st.text_area("Historia uczenia się")

# --- RESZTA KODU ANALOGICZNIE ---
