import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Zapis Przebiegu Terapii CBT", layout="wide")

# --- BAZA WIEDZY I DIAGRAMY MERMAID ---
slownik_modeli = {
    "F41.0": {
        "Model": "Model poznawczy lęku panicznego (D. Clark, 1986)",
        "Opis": "Skupienie na błędnej, katastroficznej interpretacji normalnych doznań z ciała (np. kołatanie serca = zawał).",
        "Interwencje": "Reatrybucja doznań, hiperwentylacja (eksperyment), eliminacja zachowań zabezpieczających.",
        "Wizualizacja": (
            "graph TD\n"
            "A[Wewnętrzny lub zewn. wyzwalacz] --> B[Postrzegane zagrożenie]\n"
            "B --> C[Lęk / Niepokój]\n"
            "C --> D[Doznania somatyczne np. serce]\n"
            "D --> E{Katastroficzna interpretacja}\n"
            "E -- Błędne koło paniki --> B\n"
            "style E fill:#4d0000,stroke:#ff3333,stroke-width:2px,color:#fff\n"
        )
    },
    "F32": {
        "Model": "Triada Poznawcza Becka / Model Aktywacji Behawioralnej (Martell)",
        "Opis": "Negatywna wizja siebie, świata i przyszłości. Spadek wzmocnień pozytywnych z otoczenia.",
        "Interwencje": "Monitorowanie aktywności, Aktywacja behawioralna (BA), restrukturyzacja myśli.",
        "Wizualizacja": (
            "graph TD\n"
            "A((Negatywne myśli O SOBIE)) <--> B((Negatywne myśli O ŚWIECIE))\n"
            "B <--> C((Negatywne myśli O PRZYSZŁOŚCI))\n"
            "C <--> A\n"
            "style A fill:#002b5e,stroke:#3399ff,color:#fff\n"
            "style B fill:#002b5e,stroke:#3399ff,color:#fff\n"
            "style C fill:#002b5e,stroke:#3399ff,color:#fff\n"
        )
    },
    "F40.1": {
        "Model": "Model Lęku Społecznego (Clark i Wells, 1995)",
        "Opis": "Koncentracja uwagi na sobie, tworzenie negatywnego obrazu siebie, silne zachowania zabezpieczające.",
        "Interwencje": "Trening uwagi na zewnątrz (task-concentration), wideo-feedback, eksperymenty.",
        "Wizualizacja": (
            "graph TD\n"
            "A[Sytuacja społeczna] --> B[Zagrożenie społeczniczne]\n"
            "B --> C[Skupienie uwagi na sobie]\n"
            "C <--> D[Objawy somatyczne i poznawcze]\n"
            "C <--> E[Zachowania zabezpieczające]\n"
            "D <--> E\n"
            "style C fill:#663300,stroke:#ff9900,color:#fff\n"
        )
    },
    "F42": {
        "Model": "Model poznawczy OCD (P. Salkovskis)",
        "Opis": "Przesadne poczucie odpowiedzialności (TAF). Myśl natrętna jest interpretowana jako realne zagrożenie.",
        "Interwencje": "ERP (Ekspozycja z powstrzymaniem reakcji), restrukturyzacja przekonań o odpowiedzialności.",
        "Wizualizacja": (
            "graph TD\n"
            "A[Sytuacja wyzwalająca] --> B[Natrętna myśl / Obraz]\n"
            "B --> C{Zagrożenie / Odpowiedzialność}\n"
            "C --> D[Lęk i Dyskomfort]\n"
            "D --> E[Kompulsje i Rytuały]\n"
            "E --> F[Chwilowa ulga]\n"
            "F -. Wzmocnienie .-> B\n"
            "style C fill:#4d004d,stroke:#cc00cc,color:#fff\n"
        )
    },
    "F41.1": {
        "Model": "Model Nietolerancji Niepewności (Dugas) / Metapoznawczy (Wells)",
        "Opis": "Zamartwianie się jako unikający styl radzenia sobie z lękiem oraz metaprzekonania.",
        "Interwencje": "Trening rozwiązywania problemów, ekspozycja na wyobrażenia, zmiana metaprzekonań.",
        "Wizualizacja": (
            "graph TD\n"
            "A[Sytuacja niepewna] --> B[Nietolerancja niepewności]\n"
            "B --> C[Pozytywne przekonania o martwieniu]\n"
            "C --> D[ZAMARTWIANIE SIĘ]\n"
            "D --> E[Negatywne przekonania / Lęk przed martwieniem]\n"
            "D --> F[Nieskuteczne unikanie]\n"
            "style D fill:#4d4d00,stroke:#cccc00,color:#fff\n"
        )
    }
}
slownik_modeli["F33"] = slownik_modeli["F32"]

# --- BAZA ASYSTENTA DIAGNOZY (Słownik NLP - potoczny język pacjenta) ---
baza_symptomow = [
    {
        "slowa_kluczowe": ["serce mi wali", "zaraz umrę", "uduszę się", "brakuje mi tchu", "zawał", "tracę kontrolę", "zwariuję", "kłucie w klatce", "duszno", "miękną mi nogi", "nagle mnie łapie", "atak paniki", "myślałem że to zawał"], 
        "diagnoza": "F41.0 Zaburzenie lękowe z napadami lęku (Lęk paniczny)", 
        "roznicowa": "Agorafobia (F40.0), PTSD (F43.1), Zaburzenia kardiologiczne, Nadczynność tarczycy.",
        "kryteria": "• Nawracające, nieprzewidywalne napady paniki (niezwiązane z konkretną sytuacją).\n• Nagły początek i osiągnięcie maksimum w kilka minut.\n• Min. 4 objawy somatyczne/poznawcze (np. kołatanie serca, duszność, pocenie się, obawa przed śmiercią lub utratą kontroli)."
    },
    {
        "slowa_kluczowe": ["nie mam siły", "nic mnie nie cieszy", "nie chce mi się żyć", "budzę się w nocy", "płaczę bez powodu", "jestem beznadziejny", "nie mam apetytu", "wszystko jest bez sensu", "ciągle chce mi się spać", "zmuszam się do", "nic nie ma sensu", "poczucie winy", "smutek", "zrezygnowany"], 
        "diagnoza": "F32 Epizod depresyjny / F33 Zaburzenia depresyjne nawracające", 
        "roznicowa": "ChAD - epizod depresyjny (F31), Dystymia (F34.1), Niedoczynność tarczycy.",
        "kryteria": "• Trwanie objawów min. 2 tygodnie.\n• Przynajmniej 2 z 3 objawów podstawowych: obniżony nastrój, utrata zainteresowań (anhedonia), spadek energii/zwiększona męczliwość.\n• Objawy dodatkowe (np. zaburzenia snu, apetytu, poczucie winy, myśli samobójcze)."
    },
    {
        "slowa_kluczowe": ["muszę to sprawdzić", "ciągle myję", "głupie myśli", "nie mogę przestać o tym myśleć", "muszę policzyć", "mam wrażenie że coś się stanie", "natrętne", "rytuał", "robię to żeby nie zapeszyć", "ciągle wraca ta myśl", "czuję brud", "układam", "muszę ułożyć"], 
        "diagnoza": "F42 Zaburzenie obsesyjno-kompulsyjne (OCD)", 
        "roznicowa": "Osobowość anankastyczna (F60.5), Schizofrenia (F20), Tiki (F95).",
        "kryteria": "• Obsesje (myśli) i/lub kompulsje (czynności) obecne przez większość dni przez min. 2 kolejne tygodnie.\n• Są one źródłem cierpienia i zaburzają funkcjonowanie.\n• Pacjent uznaje je za własne (nie narzucone z zewnątrz), ale uważa za przesadne i próbuje się im opierać."
    },
    {
        "slowa_kluczowe": ["boję się odezwać", "wszyscy na mnie patrzą", "spalę się ze wstydu", "wyśmieją mnie", "robię się czerwony", "boję się ludzi", "trzęsą mi się ręce jak", "kompromitacja", "boję się co pomyślą", "wypaść głupio", "wzrok innych", "wystąpienia publiczne"], 
        "diagnoza": "F40.1 Fobia społeczna", 
        "roznicowa": "Osobowość unikająca (F60.6), Agorafobia (F40.0).",
        "kryteria": "• Wyraźna obawa przed znalezieniem się w centrum uwagi lub strach przed kompromitującym zachowaniem.\n• Unikanie sytuacji społecznych.\n• Objawy lęku w sytuacjach społecznych (np. czerwienienie się, drżenie, obawa przed wymiotami/oddaniem moczu)."
    },
    {
        "slowa_kluczowe": ["ciągle się martwię", "co będzie jak", "nie mogę się rozluźnić", "mam spięte mięśnie", "najgorsze scenariusze", "a co jeśli", "boli mnie kark", "niepokój", "czuję takie napięcie", "nie umiem przestać myśleć o problemach", "martwię się o zdrowie", "martwię się o bliskich"], 
        "diagnoza": "F41.1 Zaburzenie lękowe uogólnione (GAD)", 
        "roznicowa": "Lęk paniczny (F41.0), Fobia społeczna (F40.1), Hipochondria (F45.2).",
        "kryteria": "• Uogólniony i uporczywy lęk (tzw. wolnopłynący) trwający min. 6 miesięcy.\n• Objawy napięcia ruchowego (drżenie, napięcie mięśni).\n• Wzmożona aktywność układu autonomicznego (pocenie się, suchość w ustach).\n• Obawy i zamartwianie się codziennymi wydarzeniami/problemami."
    },
    {
        "slowa_kluczowe": ["ciągle mi się to śni", "wspomnienia wracają", "mam przed oczami", "unikam miejsc", "budzę się z krzykiem", "odkąd zdarzył się ten wypadek", "flashbacki", "czuję jakby to działo się znowu", "od tamtej pory", "trauma"], 
        "diagnoza": "F43.1 Zaburzenie stresowe pourazowe (PTSD)", 
        "roznicowa": "Ostra reakcja na stres (F43.0), Zaburzenia adaptacyjne (F43.2).",
        "kryteria": "• Ekspozycja na stresor o wyjątkowej sile (zagrażający życiu lub zdrowiu).\n• Uporczywe przypominanie sobie traumy (natrętne wspomnienia, flashbacki, sny).\n• Unikanie sytuacji przypominających traumę.\n• Wzbudzenie wegetatywne lub trudności z zasypianiem (objawy trwają powyżej 1 miesiąca)."
    }
]

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

# --- BAZA DANYCH W PAMIĘCI ---
if 'baza_terapii' not in st.session_state:
    st.session_state.baza_terapii = []

# Zmienna do przechowywania tekstu dla Listy Problemów
if 'lista_problemow' not in st.session_state:
    st.session_state.lista_problemow = ""

# --- MENU BOCZNE ---
st.sidebar.title("🛡️ Zapis Terapii CBT")
menu = st.sidebar.radio("Spis treści:", [
    "I. Diagnoza i Konceptualizacja", 
    "II. Plan i Interwencje", 
    "III. Podsumowanie",
    "📂 Archiwum Diagnoz"
])
st.sidebar.divider()
st.sidebar.caption("Oparte na: Zapis przebiegu terapii CBT (A. Popiel, E. Pragłowska)")

# ==========================================================
# MODUŁ I: DIAGNOZA I KONCEPTUALIZACJA ZJAWISKA
# ==========================================================
if menu == "I. Diagnoza i Konceptualizacja":
    st.title("I. Diagnoza i konceptualizacja zjawiska")
    
    st.header("I.1. Metryczka")
    col1, col2 = st.columns(2)
    imie = col1.text_input("Pacjent (inicjały/kod)")
    wiek = col2.number_input("Wiek", 0, 110)
    terapeuta = col1.text_input("Terapeuta")
    superwizor = col2.text_input("Superwizor")
    st.checkbox("Czy pacjent jest bezpieczny? (ryzyko samobójstwa / heteroagresji)")

    st.divider()
    st.header("I.2. Diagnoza kliniczna")
    
    # ASYSTENT DIAGNOZY Z AUTOMATYCZNYM PRZEPISYWANIEM
    with st.expander("🤖 Asystent Diagnozy (Język Pacjenta)", expanded=True):
        st.write("Wpisz objawy własnymi słowami pacjenta (np. 'nie mam siły wstać z łóżka, nic mnie nie cieszy'), a następnie kliknij przycisk poniżej.")
        objawy_input = st.text_area("Cytaty pacjenta / Skarga główna:")
        
        if st.button("🔍 Analizuj objawy i skopiuj do Listy Problemów"):
            if objawy_input:
                # Automatyczne przepisanie tekstu do session_state
                st.session_state.lista_problemow = objawy_input
                
                znaleziono = False
                input_do_analizy = objawy_input.lower()
                
                for el in baza_symptomow:
                    if any(fraza in input_do_analizy for fraza in el["slowa_kluczowe"]):
                        st.success(f"🎯 **Sugerowana diagnoza:** {el['diagnoza']}")
                        st.warning(f"⚖️ **Diagnoza różnicowa:** {el['roznicowa']}")
                        st.info(f"📋 **Główne kryteria (ICD-10):**\n\n{el['kryteria']}")
                        znaleziono = True
                if not znaleziono:
                    st.info("Brak oczywistych dopasowań w bazie. Zastosuj wywiad diagnostyczny i wybierz rozpoznanie poniżej.")
            else:
                st.warning("Wpisz najpierw to, co zgłasza pacjent!")

    c1, c2 = st.columns(2)
    kat_wybrana = c1.selectbox("Grupa ICD-10:", list(icd10_full.keys()))
    pelna_diagnoza = c2.selectbox("Rozpoznanie główne:", icd10_full[kat_wybrana])
    kod_icd = pelna_diagnoza.split(" ")[0]
    
    inne_rozpoznania = st.text_input("Inne rozpoznania (np. somatyczne, psychiatryczne współwystępujące):")

    # WIEDZA EBM I SCHEMATY
    if kod_icd in slownik_modeli:
        dane = slownik_modeli[kod_icd]
        st.success(f"🧠 **Sugerowany protokół EBM dla: {kod_icd}**")
        st.write(f"**Model:** {dane['Model']} | **Mechanizm:** {dane['Opis']}")
        if "Wizualizacja" in dane:
            kod_html = (
                "<div class='mermaid' style='display: flex; justify-content: center;'>"
                + dane["Wizualizacja"] +
                "</div><script type='module'>import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';mermaid.initialize({ startOnLoad: true, theme: 'dark' });</script>"
            )
            components.html(kod_html, height=450)

    st.divider()
    st.header("I.3. Konceptualizacja problemu")
    
    st.subheader("I.3.1. Lista problemów i cele terapii")
    # POLE Z POWIĄZANYM KLUCZEM (KEY) - AUTO-UZUPEŁNIANIE
    st.text_area("Lista problemów (w ujęciu poznawczo-behawioralnym)", key="lista_problemow")
    st.text_area("Cele terapii (zoperacjonalizowane, mierzalne, SMART)")

    st.subheader("I.3.2. Poziom pierwszy (Sytuacja bieżąca - przekrój poprzeczny)")
    st.text_area("Sytuacja (typowa sytuacja ilustrująca problem)")
    c3, c4 = st.columns(2)
    with c3:
        st.text_area("Myśli automatyczne / Obrazy")
        st.text_area("Emocje (rodzaj i nasilenie)")
    with c4:
        st.text_area("Doznania z ciała (fizjologiczne)")
        st.text_area("Zachowanie (w tym zachowania zabezpieczające/unikające)")

    st.subheader("I.3.3. Poziom drugi (Mechanizmy podtrzymujące i Przekonania)")
    st.text_area("Przekonania kluczowe (o sobie, innych, świecie)")
    st.text_area("Przekonania warunkowe (Założenia / Zasady / Postawy)")
    st.text_area("Strategie radzenia sobie (kompensacyjne)")

    st.subheader("I.3.4. Historia uczenia się (Profil rozwojowy)")
    st.text_area("Wydarzenia z przeszłości i wczesne doświadczenia kształtujące schematy")
    st.text_area("Zdarzenia wyzwalające (Czynniki spustowe wystąpienia obecnego epizodu)")

    st.divider()
    st.header("I.4. Zasoby pacjenta")
    st.text_area("Mocne strony, wsparcie społeczne, umiejętności, inteligencja, motywacja itp.")

    if st.button("💾 Zapisz Diagnozę i Konceptualizację"):
        st.session_state.baza_terapii.append({"Pacjent": imie, "Wiek": wiek, "Kod ICD": kod_icd, "Diagnoza": pelna_diagnoza})
        st.success("Zapisano do Archiwum!")

# ==========================================================
# MODUŁ II: PLAN TERAPII I INTERWENCJE
# ==========================================================
elif menu == "II. Plan i Interwencje":
    st.title("II. Plan terapii i interwencje")
    
    st.header("II.1. Plan terapii")
    st.text_area("Uzasadnienie poznawczo-behawioralne (dlaczego wybrano taki plan, jaki protokół EBM)", height=150)
    
    st.header("II.2. Zapis przebiegu poszczególnych sesji")
    st.info("Tutaj dokumentuj krótko kolejne spotkania: datę, główne interwencje, zadania domowe i wnioski.")
    st.text_area("Rejestr sesji (np. Sesja 1 [Data] - Psychoedukacja i BA...)", height=300)

# ==========================================================
# MODUŁ III: PODSUMOWANIE I EWALUACJA
# ==========================================================
elif menu == "III. Podsumowanie":
    st.title("III. Podsumowanie i Ewaluacja Terapii")
    
    st.header("III.1. Osiągnięte cele terapii")
    col1, col2 = st.columns(2)
    with col1:
        st.text_area("Według pacjenta")
    with col2:
        st.text_area("Według terapeuty (odniesienie do celów z I.3.1)")

    st.header("III.2. Zidentyfikowane mechanizmy zmiany")
    st.text_area("Co dokładnie pomogło pacjentowi? (np. zmiana przekonania X, zaprzestanie unikania Y)")

    st.header("III.3. Zapobieganie nawrotom")
    st.text_area("Sygnały ostrzegawcze i plan radzenia sobie z nawrotem objawów")

    st.header("III.4. Literatura")
    st.text_area("Materiały, protokoły i książki wykorzystane do pracy z pacjentem")

# ==========================================================
# MODUŁ IV: ARCHIWUM
# ==========================================================
elif menu == "📂 Archiwum Diagnoz":
    st.title("Baza Terapii i Filtrowanie")
    
    if not st.session_state.baza_terapii:
        st.warning("Baza jest pusta. Dodaj pacjenta w zakładce I.")
    else:
        df = pd.DataFrame(st.session_state.baza_terapii)
        lista_diagnoz = ["Wszystkie"] + list(df['Kod ICD'].unique())
        wybrany_kod = st.selectbox("Filtruj bazę według diagnozy:", lista_diagnoz)
        
        if wybrany_kod != "Wszystkie":
            df = df[df['Kod ICD'] == wybrany_kod]
            
        st.dataframe(df, use_container_width=True)
