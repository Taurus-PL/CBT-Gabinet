import streamlit as st
import pandas as pd

# Konfiguracja wizualna
st.set_page_config(page_title="CBT Pro - System Wspomagania Terapii", layout="wide")

# STYLIZACJA
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

# SIDEBAR - NAWIGACJA
with st.sidebar:
    st.title("🛡️ CBT Pro v2.0")
    st.subheader("Moduły Terapeutyczne")
    opcja = st.radio("Wybierz obszar:", 
        ["Panel Główny", "Diagnostyka (Skale)", "Protokoły EBM", "Dziennik Pacjenta", "Baza Wiedzy (Pliki)"])
    st.divider()
    st.info("Zalogowany jako: Terapeuta (Taurus-PL)")

# --- PANEL GŁÓWNY ---
if opcja == "Panel Główny":
    st.title("Witaj w profesjonalnym systemie CBT")
    st.write("Wybierz moduł z lewej strony, aby rozpocząć sesję.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Aktywne Protokoły", "12")
    col2.metric("Skuteczność (EBM)", "94%")
    col3.metric("Ostatnia sesja", "Dzisiaj")

# --- PROTOKOŁY EBM ---
elif opcja == "Protokoły EBM":
    st.title("📚 Protokoły Potwierdzone Naukowo")
    zaburzenie = st.selectbox("Wybierz diagnozę:", ["Lęk Paniczny", "Depresja", "OCD", "Lęk Społeczny"])
    
    if zaburzenie == "Lęk Paniczny":
        st.header("Model Clarka (1986)")
        
        st.write("**Główny cel:** Reatrybucja doznań somatycznych.")
        st.warning("Skuteczność: Poziom A (najwyższa w badaniach meta-analitycznych).")
        
        with st.expander("Zobacz protokół krok po kroku"):
            st.write("1. Identyfikacja katastroficznych myśli.")
            st.write("2. Eksperymenty z hiperwentylacją.")
            st.write("3. Eliminacja zachowań zabezpieczających.")

# --- BAZA WIEDZY (PLIKI) ---
elif opcja == "Baza Wiedzy (Pliki)":
    st.title("📂 Twoje Dokumenty i Pliki")
    uploaded_file = st.file_uploader("Dodaj nowy protokół (PDF/CSV)")
    if uploaded_file is not None:
        st.success("Plik gotowy do analizy!")
    
    st.subheader("Dostępne materiały:")
    st.button("📄 Protokół_Depresja_Standard.pdf")
    st.button("📄 Formularz_ERP_OCD.pdf")

# --- DIAGNOSTYKA ---
elif opcja == "Diagnostyka (Skale)":
    st.title("📊 Skale i Pomiar Wyników")
    st.subheader("Skala GAD-7 (Lęk Uogólniony)")
    q1 = st.radio("Denerwowanie się lub poczucie napięcia:", [0, 1, 2, 3], horizontal=True)
    q2 = st.radio("Niemożność zaprzestania martwienia się:", [0, 1, 2, 3], horizontal=True)
    wynik = q1 + q2
    st.header(f"Wynik: {wynik} pkt")
