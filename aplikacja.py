import streamlit as st
import pandas as pd

# Konfiguracja strony
st.set_page_config(page_title="System CBT Pro - Modele EBM", layout="wide")

# --- BAZA WIEDZY: MODELE CBT DLA ICD-10 ---
slownik_modeli = {
    "F41.0 Zaburzenie lękowe z napadami lęku (Lęk paniczny)": {
        "Model": "Model poznawczy lęku panicznego D. Clarka (1986)",
        "Opis": "Skupienie na błędnej, katastroficznej interpretacji doznań z ciała (np. kołatanie serca = zawał).",
        "Interwencje": "Reatrybucja doznań, eksperymenty behawioralne (indukcja objawów), eliminacja zachowań zabezpieczających."
    },
    "F41.1 Zaburzenie lękowe uogólnione (GAD)": {
        "Model": "Model Nietolerancji Niepewności (Dugas) lub Model Metapoznawczy (Wells)",
        "Opis": "Zamartwianie się o samo martwienie (metaprzekonania) oraz unikanie poznawcze niepewności.",
        "Interwencje": "Trening rozwiązywania problemów, ekspozycja na niepewność, restrukturyzacja metaprzekonań."
    },
    "F40.1 Fobie społeczne": {
        "Model": "Model Clarka i Wellsa (1995)",
        "Opis": "Koncentracja uwagi na sobie, negatywny obraz siebie w oczach innych, zachowania zabezpieczające.",
        "Interwencje": "Trening koncentracji uwagi na zewnątrz, wideo-feedback, eksperymenty behawioralne."
    },
    "F42 Zaburzenie obsesyjno-kompulsyjne (OCD)": {
        "Model": "Model poznawczy Salkovskisa",
        "Opis": "Przesadne poczucie odpowiedzialności i fuzja myśli z działaniem. Myśl natrętna = zagrożenie.",
        "Interwencje": "ERP (Ekspozycja z powstrzymaniem reakcji), restrukturyzacja przekonań o odpowiedzialności."
    },
    "F32 Epizod depresyjny": {
        "Model": "Triada Poznawcza Becka / Model Aktywacji Behawioralnej",
        "Opis": "Negatywna wizja siebie, świata i przyszłości. Spadek wzmocnień pozytywnych z otoczenia.",
        "Interwencje": "Aktywacja behawioralna (BA), identyfikacja myśli automatycznych, zmiana schematów."
    },
    "F43.1 Zaburzenie stresowe pourazowe (PTSD)": {
        "Model": "Model przetwarzania emocjonalnego Foa i Kozaka / Model Ehlers i Clarka",
        "Opis": "Brak integracji wspomnienia traumatycznego z pamięcią autobiograficzną. Utrzymujące się poczucie bieżącego zagrożenia.",
        "Interwencje": "Przedłużona ekspozycja (PE), przetwarzanie poznawcze wspomnienia, praca nad 'hotspots'."
    }
}

# --- PEŁNA BAZA ICD-10 (Fragment dla przykładu, reszta kaskadowo) ---
icd10_full = {
    "F40-F48 Zaburzenia nerwicowe": [
        "F40.0 Agorafobia", "F40.1 Fobie społeczne", "F41.0 Zaburzenie lękowe z napadami lęku (Lęk paniczny)",
        "F41.1 Zaburzenie lękowe uogólnione (GAD)", "F42 Zaburzenie obsesyjno-kompulsyjne (OCD)",
        "F43.1 Zaburzenie stresowe pourazowe (PTSD)", "F43.2 Zaburzenia adaptacyjne"
    ],
    "F30-F39 Zaburzenia nastroju": ["F32 Epizod depresyjny", "F33 Zaburzenia depresyjne nawracające", "F34.1 Dystymia"],
    "F60-F69 Zaburzenia osobowości": ["F60.31 Osobowość borderline", "F60.6 Osobowość unikająca"]
}

# --- UI ---
st.sidebar.title("🧠 System Ekspercki CBT")
menu = st.sidebar.radio("Nawigacja:", ["Nowa Karta", "Baza Wiedzy i Archiwum"])

if menu == "Nowa Karta":
    st.header("Zapis Przebiegu Terapii + Wsparcie EBM")
    
    with st.expander("I.1. DIAGNOZA NOZOLOGICZNA", expanded=True):
        kat_wybrana = st.selectbox("Wybierz grupę ICD-10:", list(icd10_full.keys()))
        kod_wybrany = st.selectbox("Wybierz rozpoznanie:", icd10_full[kat_wybrana])
        
        # --- DYNAMICZNA PODPOWIEDŹ MODELU ---
        if kod_wybrany in slownik_modeli:
            dane_modelu = slownik_modeli[kod_wybrany]
            st.success(f"💡 **Sugerowany Model CBT:** {dane_modelu['Model']}")
            st.info(f"**Mechanizm:** {dane_modelu['Opis']}")
            st.warning(f"**Kluczowe interwencje:** {dane_modelu['Interwencje']}")
        else:
            st.write("Dla tego kodu brak specyficznego modelu w bazie podręcznej – stosuj ogólny protokół CBT.")

    with st.expander("I.3. KONCEPTUALIZACJA"):
        st.subheader("Wizualizacja modelu dla wybranego zaburzenia")
        if kod_wybrany == "F41.0 Zaburzenie lękowe z napadami lęku (Lęk paniczny)":
             st.write("")
        elif kod_wybrany == "F32 Epizod depresyjny":
             st.write("[attachment_0](attachment)")
        
        st.text_area("A - Sytuacja / Wyzwalacz")
        st.text_area("B - Myśli (zgodnie z sugerowanym modelem)")
        st.text_area("C - Reakcje i Zachowania")

    with st.expander("II. PLAN TERAPII"):
        if kod_wybrany in slownik_modeli:
            st.write(f"**Uzasadnienie wyboru metody:** Zgodnie z modelem {slownik_modeli[kod_wybrany]['Model']}...")
        st.text_area("Szczegółowy plan interwencji")

# --- ARCHIWUM ---
elif menu == "Baza Wiedzy i Archiwum":
    st.header("Archiwum i Przegląd Modeli")
    st.write("Tu możesz przeglądać wszystkich pacjentów leczonych danym modelem.")
