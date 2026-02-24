import streamlit as st
import pandas as pd

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Zapis Przebiegu Terapii CBT - System Pro", layout="wide")

# --- BAZA WIEDZY I DIAGRAMY MERMAID ---
# Uwaga: Kod wizualizacji jest w czystym tekście, znaczniki dodawane są dynamicznie
slownik_modeli = {
    "F41.0": {
        "Model": "Model poznawczy lęku panicznego (D. Clark, 1986)",
        "Opis": "Skupienie na błędnej, katastroficznej interpretacji normalnych doznań z ciała (np. kołatanie serca = zawał).",
        "Interwencje": "Reatrybucja doznań, hiperwentylacja (eksperyment), eliminacja zachowań zabezpieczających.",
        "Wizualizacja": "graph TD\n A[Wewnętrzny lub zewn. wyzwalacz] --> B[Postrzegane zagrożenie]\n B --> C[Lęk / Niepokój]\n C --> D[Doznania somatyczne np. serce]\n D --> E{Katastroficzna interpretacja}\n E -- Błędne koło paniki --> B\n style E fill:#ffcccc,stroke:#ff0000,stroke-width:2px"
    },
    "F32": {
        "Model": "Triada Poznawcza Becka / Model Aktywacji Behawioralnej (Martell)",
        "Opis": "Negatywna wizja siebie, świata i przyszłości. Spadek wzmocnień pozytywnych z otoczenia.",
        "Interwencje": "Monitorowanie aktywności, Aktywacja behawioralna (BA), restrukturyzacja myśli.",
        "Wizualizacja": "graph TD\n A((Negatywne myśli O SOBIE)) <--> B((Negatywne myśli O ŚWIECIE))\n B <--> C((Negatywne myśli O PRZYSZŁOŚCI))\n C <--> A\n style A fill:#e6f2ff,stroke:#3399ff\n style B fill:#e6f2ff,stroke:#3399ff\n style C fill:#e6f2ff,stroke:#3399ff"
    },
    "F40.1": {
        "Model": "Model Lęku Społecznego (Clark i Wells, 1995)",
        "Opis": "Koncentracja uwagi na sobie, tworzenie negatywnego obrazu siebie, silne zachowania zabezpieczające.",
        "Interwencje": "Trening uwagi na zewnątrz (task-concentration), wideo-feedback, eksperymenty.",
        "Wizualizacja": "graph TD\n A[Sytuacja społeczna] --> B[Zagrożenie społeczne]\n B --> C[Skupienie uwagi na sobie]\n C <--> D[Objawy somatyczne i poznawcze]\n C <--> E[Zachowania zabezpieczające]\n D <--> E\n style C fill:#ffe6cc,stroke:#ff9900"
    },
    "F42": {
        "Model": "Model poznawczy OCD (P. Salkovskis)",
        "Opis": "Przesadne poczucie odpowiedzialności (TAF). Myśl natrętna jest interpretowana jako realne zagrożenie.",
        "Interwencje": "ERP (Ekspozycja z powstrzymaniem reakcji), restrukturyzacja przekonań o odpowiedzialności.",
        "Wizualizacja": "graph TD\n A[Sytuacja wyzwalająca] --> B[Natrętna myśl / Obraz]\n B --> C{Zagrożenie / Odpowiedzialność}\n C --> D[Lęk i Dyskomfort]\n D --> E[Kompulsje i Rytuały]\n E --> F[Chwilowa ulga]\n F -. Wzmocnienie .-> B\n style C fill:#ffccff,stroke:#cc00cc"
    },
    "F41.1": {
        "Model": "Model Nietolerancji Niepewności (Dugas) / Metapoznawczy (Wells)",
        "Opis": "Zamartwianie się jako unikający styl radzenia sobie z lękiem oraz metaprzekonania.",
        "Interwencje": "Trening rozwiązywania problemów, ekspozycja na wyobrażenia, zmiana metaprzekonań.",
        "Wizualizacja": "graph TD\n A[Sytuacja niepewna] --> B[Nietolerancja niepewności]\n B --> C[Pozytywne przekonania o martwieniu]\n C --> D[ZAMARTWIANIE SIĘ]\n D --> E[Negatywne przekonania / Lęk przed martwieniem]\n D --> F[Nieskuteczne unikanie]\n style D fill:#ffffcc,stroke:#cccc00"
    }
}
slownik_modeli["F33"] = slownik_modeli["F32"]

# --- PEŁNA BAZA ICD-10 ---
icd10_full = {
    "F00-F09 Zab. psychiczne organiczne": ["F00 Otępienie w ch. Alzheimera", "F01 Otępienie naczyniowe", "F06 Inne zab. wskutek uszkodzenia mózgu", "F07 Zaburzenia osobowości wskutek choroby mózgu"],
    "F10-F19 Zab. spowodowane substancjami": ["F10 Zab. spowodowane alkoholem", "F11 Zab. spowodowane opioidami", "F12 Zab. spowodowane kanabinoidami", "F13 Leki uspokajające i nasenne", "F17 Palenie tytoniu"],
    "F20-F29 Schizofrenia i urojeniowe": ["F20 Schizofrenia", "F21 Zaburzenie schizotypowe", "F22 Uporczywe zaburzenia urojeniowe", "F23 Ostre zaburzenia psychotyczne", "F25 Zaburzenia schizoafektywne"],
    "F30-F39 Zaburzenia nastroju (afektywne)": ["F30 Epizod maniakalny", "F31 ChAD", "F32 Epizod depresyjny", "F33 Zaburzenia depresyjne nawracające", "F34 Uporczywe zaburzenia nastroju (Dystymia)"],
    "F40-F48 Zaburzenia nerwicowe i lękowe": ["F40.0 Agorafobia", "F40.1 Fobie społeczne", "F40.2 Specyficzne fobie", "F41.0 Zaburzenie lękowe z napadami lęku", "F41.1 Zaburzenie lękowe uogólnione (GAD)", "F41.2 Zab. lękowo-depresyjne mieszane", "F42 Zaburzenie obsesyjno-kompulsyjne (OCD)", "F43.0 Ostra reakcja na stres", "F43.1 Zaburzenie stresowe pourazowe (PTSD)", "F43.2 Zaburzenia adaptacyjne", "F44 Zaburzenia dysocjacyjne", "F45 Zaburzenia pod postacią somatyczną"],
    "F50-F59 Zespoły behawioralne": ["F50.0 Jadłowstręt psychiczny (Anoreksja)", "F50.2 Żarłoczność psychiczna (Bulimia)", "F51 Nieorganiczne zaburzenia snu", "F52 Dysfunkcje seksualne"],
    "F60-F69 Zaburzenia osobowości": ["F60.0 Osobowość paranoiczna", "F60.1 Osobowość schizoidalna", "F60.2 Osobowość dyssocjalna", "F60.30 Os. chwiejna emocjonalnie typ impulsywny", "F60.31 Os. chwiejna emocjonalnie typ borderline", "F60.4 Os. histrioniczna", "F60.5 Os. anankastyczna (OCPD)", "F60.6 Os. lękliwa (unikająca)", "F60.7 Os. zależna", "F61 Mieszane zab. osobowości"],
    "F90-F98 Zaburzenia wieku dziecięcego": ["F90 Zaburzenia hiperkinetyczne (ADHD)", "F91 Zaburzenia zachowania", "F95 Tiki"]
}

# --- BAZA DANYCH W PAMIĘCI (Session State) ---
if 'baza_terapii' not in st.session_state:
    st.session_state.baza_terapii = []

# --- MENU BOCZNE ---
st.sidebar.title("🛡️ CBT System Pro")
menu = st.sidebar.radio("Nawigacja:", [
    "1. Metryczka i Diagnoza", 
    "2. Konceptualizacja ABC", 
    "3. Plan, Sesje i Podsumowanie",
    "📂 Archiwum Diagnoz"
])
st.sidebar.divider()
st.sidebar.caption("Oparte na: Zapis przebiegu terapii CBT, A. Popiel i E. Pragłowska")

# --- MODUŁ 1: METRYCZKA I DIAGNOZA ---
if menu == "1. Metryczka i Diagnoza":
    st.header("I.1 Metryczka i Diagnoza Kliniczna")
    
    with st.expander("Dane pacjenta i autorefleksja", expanded=True):
        col1, col2 = st.columns(2)
        imie = col1.text_input("Pacjent (inicjały/imię)")
        wiek = col2.number_input("Wiek", 0, 110)
        terapeuta = col1.text_input("Terapeuta")
        st.checkbox("Czy pacjent jest bezpieczny? (ryzyko samobójstwa)")
        st.text_area("Moje własne ABC na myśl o pracy z pacjentem")

    with st.expander("Wybór Diagnozy ICD-10", expanded=True):
        c1, c2 = st.columns(2)
        kat_wybrana = c1.selectbox("Grupa ICD-10:", list(icd10_full.keys()))
        pelna_diagnoza = c2.selectbox("Rozpoznanie główne:", icd10_full[kat_wybrana])
        kod_icd = pelna_diagnoza.split(" ")[0]

        # SILNIK WIEDZY EBM
        st.divider()
        if kod_icd in slownik_modeli:
            dane = slownik_modeli[kod_icd]
            st.success(f"🧠 **Sugerowany protokół EBM dla: {kod_icd}**")
            st.write(f"**Model:** {dane['Model']}")
            st.write(f"**Mechanizm podtrzymujący:** {dane['Opis']}")
            st.write(f"**Interwencje:** {dane['Interwencje']}")
            
            if "Wizualizacja" in dane:
                st.markdown("### Graficzny schemat mechanizmu:")
                kod_wizualizacji = "```mermaid\n" + dane['Wizualizacja'] + "\n```"
                st.markdown(kod_wizualizacji)
        else:
            st.info("💡 Dla wybranego kodu zaleca się stosowanie standardowego modelu poznawczego ABC.")

    with st.expander("Ogólne funkcjonowanie"):
        f_rodzina = st.text_area("Sfera rodzinna (funkcjonowanie i trudności)")
        f_praca = st.text_area("Sfera zawodowa / szkolna (funkcjonowanie i trudności)")
        f_spoleczna = st.text_area("Sfera społeczna (funkcjonowanie i trudności)")
        
    # Przycisk zapisu w sesji (aby przenieść do archiwum)
    if st.button("💾 Zapisz Diagnozę w Archiwum"):
        st.session_state.baza_terapii.append({
            "Pacjent": imie, "Wiek": wiek, "Kod ICD": kod_icd, 
            "Diagnoza": pelna_diagnoza, "Terapeuta": terapeuta
        })
        st.success("Zapisano pacjenta do bazy!")

# --- MODUŁ 2: KONCEPTUALIZACJA ---
elif menu == "2. Konceptualizacja ABC":
    st.header("I.3 Konceptualizacja Problemu")
    
    st.subheader("Poziom Pierwszy (ABC)")
    st.text_area("Sytuacja ilustrująca problem")
    col1, col2 = st.columns(2)
    with col1:
        st.text_area("A – Czynnik wyzwalający")
        st.text_area("B – Automatyczne myśli")
    with col2:
        st.text_area("C – Emocje")
        st.text_area("C – Objawy fizjologiczne")
    st.text_area("C – Zachowanie (w tym strategie zabezpieczające)")
    
    st.divider()
    st.subheader("Poziom Drugi (Procesy i Schematy)")
    st.text_area("Przekonania kluczowe (schematy poznawcze)")
    st.text_area("Przekonania warunkowe (zasady)")
    st.multiselect("Zidentyfikowane procesy transdiagnostyczne:", 
                   ["Unikanie poznawcze", "Zamartwianie się", "Ruminacje", "Lęk przed lękiem", "Monitorowanie zagrożenia", "Perfekcjonizm"])
    st.text_area("Profil rozwojowy (Historia uczenia się)")

# --- MODUŁ 3: PLAN I PODSUMOWANIE ---
elif menu == "3. Plan, Sesje i Podsumowanie":
    st.header("II. Etap Terapeutyczny")
    st.text_area("Plan terapii (protokół EBM i uzasadnienie)")
    st.text_area("Zapis przebiegu kolejnych sesji (metody, wnioski, zadania)")
    
    st.divider()
    st.header("III. Etap Końcowy (Ewaluacja)")
    col1, col2 = st.columns(2)
    with col1:
        st.text_area("Osiągnięte cele (wg pacjenta)")
    with col2:
        st.text_area("Osiągnięte cele (wg terapeuty)")
    st.text_area("Zidentyfikowane mechanizmy zmiany i zapobieganie nawrotom")
    st.text_area("IV. Literatura wykorzystana do pracy z pacjentem")

# --- MODUŁ 4: ARCHIWUM ---
elif menu == "📂 Archiwum Diagnoz":
    st.header("Baza Terapii i Filtrowanie")
    
    if not st.session_state.baza_terapii:
        st.warning("Baza jest pusta. Dodaj pacjenta w zakładce '1. Metryczka i Diagnoza'.")
    else:
        df = pd.DataFrame(st.session_state.baza_terapii)
        
        # Filtrowanie po kodzie ICD
        lista_diagnoz = ["Wszystkie"] + list(df['Kod ICD'].unique())
        wybrany_kod = st.selectbox("Filtruj bazę według diagnozy:", lista_diagnoz)
        
        if wybrany_kod != "Wszystkie":
            df = df[df['Kod ICD'] == wybrany_kod]
            st.write(f"Znaleziono pacjentów dla kodu: **{wybrany_kod}**")
            
        st.dataframe(df, use_container_width=True)
