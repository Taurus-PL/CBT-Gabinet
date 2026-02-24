import streamlit as st

st.set_page_config(page_title="System Wspomagania Terapii CBT", layout="wide")

st.sidebar.title("📋 Arkusz Przebiegu Terapii")
nawigacja = st.sidebar.radio("Przejdź do sekcji:", [
    "1. Dane i Autorefleksja",
    "2. Diagnoza i Problemy",
    "3. Konceptualizacja (ABC)",
    "4. Przekonania i Historia",
    "5. Plan i Realizacja Sesji",
    "6. Podsumowanie Terapii"
])

# --- SEKCJA 1: DANE I AUTOREFLEKSJA ---
if nawigacja == "1. Dane i Autorefleksja":
    st.header("I. Dane pacjenta i autorefleksja terapeuty")
    col1, col2 = st.columns(2)
    with col1:
        pacjent = st.text_input("Pacjent (inicjały/imię)")
        wiek = st.number_input("Wiek", min_value=0)
    with col2:
        st.radio("Płeć", ["K", "M"], horizontal=True)
        status = st.selectbox("Status terapii", ["w trakcie", "zakończona", "przerwana"])

    st.subheader("Autorefleksja przed superwizją")
    st.text_area("Co jest problemem w pracy z tym pacjentem?")
    st.checkbox("Czy znam model teoretyczny najlepiej opisujący problem?")
    st.checkbox("Czy pacjent jest bezpieczny (ryzyko samobójstwa)?")

# --- SEKCJA 3: KONCEPTUALIZACJA ABC ---
elif nawigacja == "3. Konceptualizacja (ABC)":
    st.header("I.3. Konceptualizacja - Poziom Pierwszy")
    st.info("Sytuacja wyzwalająca → Myśli ↔ Emocje ↔ Fizjologia ↔ Zachowanie")
    
    sytuacja = st.text_area("Sytuacja ilustrująca problem (A)")
    
    col1, col2 = st.columns(2)
    with col1:
        mysli = st.text_area("Automatyczne myśli (B)")
        emocje = st.text_area("Emocje (C)")
    with col2:
        fizjologia = st.text_area("Reakcje fizjologiczne (C)")
        zachowanie = st.text_area("Zachowania / Strategie zabezpieczające")
    
    st.subheader("Konsekwencje")
    st.text_area("Wzmocnienia pozytywne i negatywne")

# --- SEKCJA 4: PRZEKONANIA ---
elif nawigacja == "4. Przekonania i Historia":
    st.header("Drugi Poziom Konceptualizacji")
    st.text_area("Przekonania kluczowe (schematy)")
    st.text_area("Przekonania warunkowe (zasady)")
    
    st.subheader("Procesy transdiagnostyczne")
    st.multiselect("Zidentyfikowane procesy:", 
                   ["Unikanie poznawcze", "Zamartwianie się", "Ruminacje", "Perfekcjonizm", "Monitorowanie zagrożenia"])
    
    st.subheader("Profil rozwojowy")
    st.text_area("Istotne wydarzenia z przeszłości i ich znaczenie")

# Pozostałe sekcje (Planowanie, Podsumowanie) budujemy analogicznie...
