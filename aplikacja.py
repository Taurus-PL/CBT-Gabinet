import streamlit as st

# Konfiguracja strony
st.set_page_config(page_title="Zapis Przebiegu Terapii CBT", layout="wide")

# Nagłówek i autorstwo zgodnie z plikiem
st.sidebar.title("Zapis Przebiegu Terapii 2021")
st.sidebar.caption("A. Popiel, E. Pragłowska")

# Nawigacja oparta na etapach z dokumentu
menu = st.sidebar.radio("Etapy Procesu:", [
    "Metryczka i Autorefleksja",
    "I.1. Diagnoza Kliniczna",
    "I.2. Lista Problemów",
    "I.3. Konceptualizacja (ABC)",
    "I.3. Konceptualizacja (Poziom II)",
    "II. Plan i Realizacja",
    "III. Podsumowanie i Efekty",
    "IV. Wnioski i Literatura"
])

# --- SEKCJA: METRYCZKA ---
if menu == "Metryczka i Autorefleksja":
    st.header("Dane podstawowe")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text_input("Terapeuta")
        st.text_input("Pacjent (inicjały/imię)")
    with col2:
        st.number_input("Wiek", min_value=0, step=1)
        st.radio("Płeć", ["K", "M"], horizontal=True)
    with col3:
        st.date_input("Czas terapii od")
        st.date_input("Czas terapii do")
        st.number_input("Liczba odbytych sesji", min_value=0)

    st.radio("Status terapii", ["zakończona", "w trakcie", "przerwana"], horizontal=True)
    st.text_area("Uwagi (superwizja, nagrania)")

    st.divider()
    st.header("Autorefleksja przed superwizją")
    st.text_area("Co jest problemem w pracy z tym pacjentem - na jakie pytania chcę uzyskać odpowiedź?")
    st.checkbox("Czy przejrzałem materiały CBT dotyczące tego problemu?")
    st.checkbox("Czy pacjent jest bezpieczny (ryzyko samobójstwa/zachowania ryzykowne)?")
    st.text_area("Moje własne ABC na myśl o terapii tego pacjenta")

# --- SEKCJA: DIAGNOZA ---
elif menu == "I.1. Diagnoza Kliniczna":
    st.header("I.1. Ogólna Diagnoza Kliniczna")
    st.text_area("Zgłaszane problemy, powód przyjścia (opis pacjenta)")
    st.text_area("Informacje ogólne (wywiad: sytuacja zawodowa, rodzinna, historia leczenia)")
    
    st.subheader("Badanie stanu psychicznego i diagnoza nozologiczna")
    st.text_area("Opis badania stanu psychicznego")
    st.text_input("Diagnoza wstępna (ICD/DSM) - Zaburzenie dominujące")
    st.text_input("Zaburzenia współwystępujące")
    st.text_input("Zaburzenia osobowości")
    st.text_input("Choroby somatyczne")
    
    st.subheader("Ogólne funkcjonowanie (0-100)")
    st.slider("Sfera rodzinna", 0, 100, 50)
    st.slider("Sfera zawodowa/szkolna", 0, 100, 50)
    st.slider("Sfera społeczna", 0, 100, 50)

# --- SEKCJA: LISTA PROBLEMÓW ---
elif menu == "I.2. Lista Problemów":
    st.header("I.2. Wyodrębnienie problemów do terapii")
    st.info("Pytanie pomocnicze: Czy lista odzwierciedla kryteria diagnostyczne?")
    
    st.text_area("Lista problemów (z opisem nasilenia 0-100)")
    st.text_area("Problem dominujący wybrany do konceptualizacji")
    st.text_input("Miara rozwiązania/ustąpienia problemu")
    st.text_area("Sytuacje z ubiegłego tygodnia ilustrujące problem")

# --- SEKCJA: KONCEPTUALIZACJA ABC ---
elif menu == "I.3. Konceptualizacja (ABC)":
    st.header("I.3. Konceptualizacja - Poziom I (ABC)")
    [attachment_0](attachment)
    st.text_input("Sytuacja ilustrująca problem")
    
    col1, col2 = st.columns(2)
    with col1:
        st.text_area("A - Czynnik wyzwalający")
        st.text_area("B - Automatyczne myśli")
    with col2:
        st.text_area("C - Emocje")
        st.text_area("C - Objawy fizjologiczne")
    
    st.text_area("C - Zachowanie (w tym zabezpieczające)")
    st.text_area("Konsekwencje (wzmocnienia +/-)")

# --- SEKCJA: POZIOM II ---
elif menu == "I.3. Konceptualizacja (Poziom II)":
    st.header("Drugi Poziom Konceptualizacji")
    st.text_area("Przekonania kluczowe (schematy poznawcze)")
    st.text_area("Przekonania warunkowe / Zasady pośredniczące")
    st.text_area("Zniekształcenia i ograniczenia poznawcze")
    
    st.subheader("Procesy Transdiagnostyczne")
    st.multiselect("Zidentyfikowane procesy podtrzymujące:", 
                   ["Unikanie poznawcze", "Zamartwianie", "Ruminacje", "Historia uczenia", "Perfekcjonizm", "Monitorowanie zagrożenia"])
    
    st.subheader("Profil rozwojowy")
    st.text_area("Przeszłość i związki z innymi (historia uczenia się)")
    st.text_area("Istotne wydarzenia i przeżycia traumatyczne")
    st.text_area("Czynniki wyzwalające obecne zaburzenie")
    st.text_area("Zasoby i rezyliencja (czynniki pozytywne)")
    st.text_area("Podsumowanie konceptualizacji (synteza wiedzy)")
    st.text_area("Cele terapii (uzgodnione z pacjentem)")

# --- SEKCJA: PLAN ---
elif menu == "II. Plan i Realizacja":
    st.header("II. Drugi etap terapii")
    st.text_area("Plan terapii (protokoły EBM, uzasadnienie wyboru)")
    st.text_area("Narzędzia oceny stanu psychicznego (monitorowanie zmian)")
    
    st.subheader("Realizacja planu - opis sesji")
    st.info("Opis powinien zawierać: plan sesji, zastosowane metody, wnioski i pracę osobistą.")
    st.text_area("Zapis przebiegu sesji i refleksje terapeuty")

# --- SEKCJA: PODSUMOWANIE ---
elif menu == "III. Podsumowanie i Efekty":
    st.header("III. Trzeci etap terapii - Osiągnięte cele")
    col1, col2 = st.columns(2)
    with col1:
        st.text_area("Według pacjenta")
    with col2:
        st.text_area("Według terapeuty")
    
    st.subheader("Zmiany w zakresie:")
    st.text_area("Funkcjonowania poznawczego")
    st.text_area("Emocji i Zachowań")
    
    st.subheader("Mechanizmy zmian")
    st.text_area("Strategie zapobiegania nawrotom")
    st.text_area("Relacja terapeutyczna (ocena jakości)")

# --- SEKCJA: WNIOSKI ---
elif menu == "IV. Wnioski i Literatura":
    st.header("IV. Podsumowanie terapii – wnioski")
    st.text_area("Końcowy zapis terapii do dokumentacji")
    st.text_area("Literatura (materiały wykorzystane w procesie)")
