import streamlit as st
import pandas as pd

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Zapis Przebiegu Terapii CBT - System Pro", layout="wide")

# --- BAZA WIEDZY: MODELE CBT DOPASOWANE PO KODACH ---
slownik_modeli = {
    "F41.0": {
        "Model": "Model poznawczy lęku panicznego (D. Clark, 1986)",
        "Opis": "Skupienie na błędnej, katastroficznej interpretacji normalnych doznań z ciała (np. kołatanie serca = zawał).",
        "Interwencje": "Reatrybucja doznań, hiperwentylacja (eksperyment), eliminacja zachowań zabezpieczających."
    },
    "F41.1": {
        "Model": "Model Nietolerancji Niepewności (M. Dugas) / Model Metapoznawczy (A. Wells)",
        "Opis": "Zamartwianie się o martwienie (metaprzekonania) oraz unikanie poznawcze niepewności w życiu.",
        "Interwencje": "Trening rozwiązywania problemów, ekspozycja na wyobrażenia, restrukturyzacja metaprzekonań."
    },
    "F40.1": {
        "Model": "Model Lęku Społecznego (Clark i Wells, 1995)",
        "Opis": "Koncentracja uwagi na sobie, tworzenie negatywnego obrazu siebie w oczach innych, silne zachowania zabezpieczające.",
        "Interwencje": "Trening przenoszenia uwagi na zewnątrz (task-concentration), wideo-feedback, eksperymenty w sytuacjach społecznych."
    },
    "F42": {
        "Model": "Model poznawczy OCD (P. Salkovskis)",
        "Opis": "Przesadne poczucie odpowiedzialności (TAF - fuzja myśli z działaniem). Myśl natrętna jest interpretowana jako realne zagrożenie.",
        "Interwencje": "ERP (Ekspozycja z powstrzymaniem reakcji), restrukturyzacja przekonań o odpowiedzialności, tarcze dwojga (pie chart)."
    },
    "F32": {
        "Model": "Triada Poznawcza Becka / Model Aktywacji Behawioralnej (Martell)",
        "Opis": "Negatywna wizja siebie, świata i przyszłości. Spadek wzmocnień pozytywnych z otoczenia i wzrost zachowań unikających.",
        "Interwencje": "Monitorowanie aktywności, Aktywacja behawioralna (BA), identyfikacja i restrukturyzacja myśli automatycznych."
    },
    "F33": {
        "Model": "Triada Poznawcza Becka / Model Aktywacji Behawioralnej (Martell)",
        "Opis": "Negatywna wizja siebie, świata i przyszłości. Spadek wzmocnień pozytywnych z otoczenia.",
        "Interwencje": "Aktywacja behawioralna (BA), profilaktyka nawrotów (MBCT - Mindfulness)."
    },
    "F43.1": {
        "Model": "Model Przetwarzania Informacji (Foa i Kozak) / Model Ehlers i Clarka",
        "Opis": "Brak integracji wspomnienia traumatycznego z pamięcią autobiograficzną. Utrzymujące się poczucie bieżącego zagrożenia.",
        "Interwencje": "Przedłużona ekspozycja (PE), przetwarzanie poznawcze wspomnienia (CPT), praca nad 'hotspots'."
    },
    "F50.0": {
        "Model": "Transdiagnostyczny Model Zaburzeń Odżywiania (CBT-E, C. Fairburn)",
        "Opis": "Nadwartościowe znaczenie nadawane figurze, wadze i kontroli nad nimi. Perfekcjonizm kliniczny.",
        "Interwencje": "Regularne jedzenie, ważenie się w gabinecie, praca nad obrazem ciała i perfekcjonizmem."
    },
    "F50.2": {
        "Model": "Transdiagnostyczny Model Zaburzeń Odżywiania (CBT-E, C. Fairburn)",
        "Opis": "Błędne koło restrykcji dietetycznych, które prowadzą do napadów objadania się i zachowań kompensacyjnych.",
        "Interwencje": "Dzienniczek żywieniowy, opóźnianie reakcji, analiza korzyści i strat kompensacji."
    },
    "F60.31": {
        "Model": "Dialektyczna Terapia Behawioralna (DBT, M. Linehan) / Terapia Schematów (J. Young)",
        "Opis": "Biologiczna podatność na dysregulację emocji połączona z unieważniającym środowiskiem. Aktywne, nieadaptacyjne schematy wczesnodziecięce.",
        "Interwencje": "Trening umiejętności DBT (uważność, tolerancja na stres), praca z trybami schematów, reparenting."
    },
    "F51": {
        "Model": "Poznawczo-Behawioralna Terapia Bezsenności (CBT-I, A. Spielman)",
        "Opis": "Model 3P: czynniki predysponujące, wyzwalające i podtrzymujące (np. leżenie w łóżku bez snu, drzemki, lęk przed niespaniem).",
        "Interwencje": "Technika kontroli bodźców, restrykcja snu, higiena snu, zmiana przekonań o potrzebie 8h snu."
    },
    "F45": {
        "Model": "Model Lęku o Zdrowie / Hipochondrii (Salkovskis i Warwick)",
        "Opis": "Błędna interpretacja łagodnych objawów somatycznych jako oznak ciężkiej choroby, połączona z ciągłym skanowaniem ciała.",
        "Interwencje": "Eksperymenty behawioralne ze skanowaniem ciała, zapobieganie poszukiwaniu zapewnień (u lekarzy i w internecie)."
    }
}

# --- BAZA ICD-10 (Fragmenty do nawigacji) ---
icd10_full = {
    "F30-F39 Zaburzenia nastroju (afektywne)": [
        "F32 Epizod depresyjny", "F33 Zaburzenia depresyjne nawracające", "F34 Uporczywe zaburzenia nastroju (Dystymia)"
    ],
    "F40-F48 Zaburzenia nerwicowe, lękowe i pod postacią somatyczną": [
        "F40.0 Agorafobia", "F40.1 Fobie społeczne", "F41.0 Zaburzenie lękowe z napadami lęku",
        "F41.1 Zaburzenie lękowe uogólnione (GAD)", "F42 Zaburzenie obsesyjno-kompulsyjne (OCD)",
        "F43.1 Zaburzenie stresowe pourazowe (PTSD)", "F43.2 Zaburzenia adaptacyjne", "F45 Zaburzenia pod postacią somatyczną"
    ],
    "F50-F59 Zespoły behawioralne związane z zaburzeniami fizjologicznymi": [
        "F50.0 Jadłowstręt psychiczny (Anoreksja)", "F50.2 Żarłoczność psychiczna (Bulimia)", "F51 Nieorganiczne zaburzenia snu"
    ],
    "F60-F69 Zaburzenia osobowości": [
        "F60.31 Osobowość chwiejna emocjonalnie typ borderline", "F60.6 Osobowość lękliwa (unikająca)"
    ]
}

# --- UI GŁÓWNE ---
st.title("ZAPIS PRZEBIEGU TERAPII 2021")
st.caption("Arkusz A. Popiel, E. Pragłowskiej | Wzbogacony o EBM CBT")

# MENU
menu = st.sidebar.radio("Nawigacja:", ["I. Diagnoza i Konceptualizacja", "II. Plan i Interwencje", "III. Podsumowanie"])

if menu == "I. Diagnoza i Konceptualizacja":
    st.header("I.1 Diagnoza Nozologiczna (ICD-10)")
    
    col1, col2 = st.columns(2)
    with col1:
        kat_wybrana = st.selectbox("Wybierz grupę ICD-10:", list(icd10_full.keys()))
    with col2:
        pelna_nazwa_diagnozy = st.selectbox("Wybierz rozpoznanie:", icd10_full[kat_wybrana])
    
    # SILNIK WIEDZY (WYODRĘBNIANIE KODU)
    kod_icd = pelna_nazwa_diagnozy.split(" ")[0]  # Pobiera samo "F41.0" z długiej nazwy
    
    # WYŚWIETLANIE MODELU
    st.divider()
    if kod_icd in slownik_modeli:
        st.subheader(f"🧠 Sugerowany protokół EBM dla: {kod_icd}")
        dane = slownik_modeli[kod_icd]
        
        st.success(f"**Wytyczne i Model:** {dane['Model']}")
        st.write(f"**Mechanizm podtrzymujący:** {dane['Opis']}")
        st.write(f"**Sugerowane Interwencje:** {dane['Interwencje']}")
        
        # Wyzwalanie diagramów edukacyjnych
        if kod_icd == "F41.0":
            st.markdown("**(Wizualizacja):**")
            
        elif kod_icd in ["F32", "F33"]:
            st.markdown("**(Wizualizacja):**")
            [attachment_0](attachment)
        elif kod_icd == "F40.1":
            st.markdown("**(Wizualizacja):**")
            
        elif kod_icd == "F42":
            st.markdown("**(Wizualizacja):**")
            

    else:
        st.info("💡 Dla wybranego kodu zaleca się stosowanie standardowego modelu poznawczego ABC i ogólnych technik CBT.")
    
    st.divider()
    st.header("I.3 Konceptualizacja Poziom I")
    st.text_area("A - Wyzwalacz")
    st.text_area("B - Myśli Automatyczne")
    st.text_area("C - Emocje, Fizjologia, Zachowanie")

elif menu == "II. Plan i Interwencje":
    st.header("II. Plan Terapii")
    st.text_area("Zaplanowane techniki i uzasadnienie ich wyboru w oparciu o model CBT")
    st.text_area("Zapis przebiegu kolejnych sesji")

elif menu == "III. Podsumowanie":
    st.header("Ewaluacja Terapii")
    st.text_area("Osiągnięte cele terapii")
    st.text_area("Zidentyfikowany mechanizm zmiany")
