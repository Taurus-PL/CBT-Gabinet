import streamlit as st
import pandas as pd

# Konfiguracja strony
st.set_page_config(page_title="CBT Pro - Baza Terapii", layout="wide")

# --- INICJALIZACJA BAZY DANYCH (SESSION STATE) ---
if 'baza_pacjentow' not in st.session_state:
    st.session_state.baza_pacjentow = []

# --- PEŁNA LISTA DIAGNOZ ---
kategorie_diagnoz = {
    "Zaburzenia lękowe (6B00-6B05)": ["6B00 GAD", "6B01 Panika", "6B03 Lęk społeczny", "6B04 Agorafobia"],
    "Zaburzenia nastroju (6A70-6A8Z)": ["6A70 Depresja (epizod)", "6A71 Depresja nawracająca", "6A72 Dystymia", "6A60 ChAD"],
    "Stres i Trauma (6B40-6B4Z)": ["6B40 PTSD", "6B41 CPTSD", "6B42 Zaburzenia adaptacyjne"],
    "Obsesyjno-kompulsyjne (6B20-6B2Z)": ["6B20 OCD", "6B21 Dysmorfofobia", "6B22 Zbieractwo"],
    "Osobowość (6D10-6D11)": ["6D11.5 Borderline", "Anankastyczna", "Unikająca", "Zależna", "Narcystyczna"],
    "Odżywianie (6B80-6B8Z)": ["6B80 Anoreksja", "6B81 Bulimia", "6B82 Napadowe objadanie się"]
}

# --- MENU BOCZNE ---
with st.sidebar:
    st.title("🛡️ CBT System Pro")
    menu = st.radio("Nawigacja:", ["Nowa Karta Terapii", "Archiwum i Filtrowanie"])
    st.divider()
    if st.button("Wyczyść sesję (Reset)"):
        st.session_state.baza_pacjentow = []
        st.rerun()

# --- MODUŁ 1: NOWA KARTA TERAPII ---
if menu == "Nowa Karta Terapii":
    st.header("📝 Nowy Arkusz Przebiegu Terapii")
    
    with st.expander("Metryczka i Diagnoza", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            imie = st.text_input("Pacjent (inicjały)")
            wiek = st.number_input("Wiek", min_value=0)
        with col2:
            kat = st.selectbox("Grupa diagnostyczna", [""] + list(kategorie_diagnoz.keys()))
            diag = st.selectbox("Diagnoza główna (ICD-11/DSM-5)", kategorie_diagnoz[kat] if kat else [])
    
    with st.expander("Konceptualizacja i Przebieg"):
        abc_mysli = st.text_area("B - Myśli automatyczne")
        abc_zachowanie = st.text_area("C - Zachowanie")
        plan = st.text_area("Planowane interwencje (EBM)")

    if st.button("✅ ZAPISZ DO BAZY"):
        nowy_pacjent = {
            "Pacjent": imie,
            "Wiek": wiek,
            "Diagnoza": diag,
            "Grupa": kat,
            "Myśli": abc_mysli,
            "Zachowanie": abc_zachowanie,
            "Plan": plan
        }
        st.session_state.baza_pacjentow.append(nowy_pacjent)
        st.success(f"Pomyślnie zapisano pacjenta {imie} w grupie {diag}!")

# --- MODUŁ 2: ARCHIWUM I FILTROWANIE ---
elif menu == "Archiwum i Filtrowanie":
    st.header("📂 Archiwum Prowadzonych Terapii")
    
    if not st.session_state.baza_pacjentow:
        st.info("Baza jest pusta. Dodaj pierwszego pacjenta w zakładce 'Nowa Karta Terapii'.")
    else:
        # Filtrowanie
        st.subheader("🔍 Filtruj według diagnozy")
        wszystkie_diagnozy = list(set([p['Diagnoza'] for p in st.session_state.baza_pacjentow]))
        wybrany_filtr = st.selectbox("Wybierz jednostkę chorobową, aby zobaczyć historię leczenia:", ["Wszystkie"] + wszystkie_diagnozy)
        
        # Przygotowanie danych do tabeli
        df = pd.DataFrame(st.session_state.baza_pacjentow)
        
        if wybrany_filtr != "Wszystkie":
            df = df[df['Diagnoza'] == wybrany_filtr]
            st.write(f"Wyświetlasz pacjentów z rozpoznaniem: **{wybrany_filtr}**")
        
        # Wyświetlanie tabeli
        st.dataframe(df, use_container_width=True)
        
        # Szczegółowy podgląd
        st.divider()
        st.subheader("📄 Podgląd szczegółowy")
        for i, p in df.iterrows():
            with st.expander(f"Pacjent: {p['Pacjent']} | Diagnoza: {p['Diagnoza']}"):
                st.write(f"**Wiek:** {p['Wiek']}")
                st.write(f"**Konceptualizacja (Myśli):** {p['Myśli']}")
                st.write(f"**Interwencje:** {p['Plan']}")
