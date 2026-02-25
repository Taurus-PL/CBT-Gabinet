import streamlit as st

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Zapis Terapii CBT", layout="wide")

st.markdown("""
    <style>
    .stExpanderHeader { font-weight: 500; }
    </style>
""", unsafe_allow_html=True)

# --- 1. KOMPLEKSOWA BAZA WIEDZY I MODELE CBT (PEŁNA WERSJA) ---
slownik_modeli = {
    "F41.0": [
        {
            "Model": "Model poznawczy lęku panicznego (D. Clark)",
            "Opis": "Skupienie na błędnej, katastroficznej interpretacji normalnych doznań z ciała (np. kołatanie serca = zawał).",
            "Interwencje": "Reatrybucja doznań, hiperwentylacja (eksperyment), eliminacja zachowań zabezpieczających.",
            "Wizualizacja": "graph TD\nA[Wyzwalacz] --> B[Postrzegane zagrożenie]\nB --> C[Lęk / Niepokój]\nC --> D[Doznania somatyczne]\nD --> E{Katastroficzna interpretacja}\nE -- Błędne koło paniki --> B"
        }
    ],
    "F32": [
        {
            "Model": "Triada Poznawcza Depresji (A. Beck)",
            "Opis": "Negatywna wizja siebie, świata i przyszłości wynikająca z dysfunkcjonalnych schematów.",
            "Interwencje": "Tabela Becka, restrukturyzacja poznawcza, testowanie przekonań.",
            "Wizualizacja": "graph TD\nA((Negatywne myśli O SOBIE)) <--> B((Negatywne myśli O ŚWIECIE))\nB <--> C((Negatywne myśli O PRZYSZŁOŚCI))\nC <--> A"
        },
        {
            "Model": "Model Aktywacji Behawioralnej - BA (C. Martell)",
            "Opis": "Depresja jako wynik spadku wzmocnień pozytywnych. Bierność pogłębia brak wzmocnień.",
            "Interwencje": "Monitorowanie aktywności, planowanie 'przyjemność i mistrzostwo'.",
            "Wizualizacja": "graph TD\nA[Stresory / Spadek wzmocnień] --> B[Obniżony nastrój]\nB --> C[Wycofanie / Bierność]\nC --> D[Brak okazji do poprawy]\nD -- Błędne koło --> B"
        }
    ],
    "F40.1": [
        {
            "Model": "Model Lęku Społecznego (Clark i Wells)",
            "Opis": "Koncentracja uwagi na sobie i tworzenie negatywnego obrazu własnego 'ja'.",
            "Interwencje": "Trening uwagi na zewnątrz, wideo-feedback, eksperymenty behawioralne.",
            "Wizualizacja": "graph TD\nA[Sytuacja społeczna] --> B[Zagrożenie społeczne]\nB --> C[Skupienie uwagi na sobie]\nC <--> D[Objawy somatyczne]\nC <--> E[Zachowania zabezpieczające]"
        }
    ],
    "F42": [
        {
            "Model": "Model poznawczy OCD (P. Salkovskis)",
            "Opis": "Przesadne poczucie odpowiedzialności (TAF). Myśl natrętna jako realne zagrożenie.",
            "Interwencje": "Restrukturyzacja odpowiedzialności, technika 'ciasta'.",
            "Wizualizacja": "graph TD\nA[Wyzwalacz] --> B[Obsesja]\nB --> C{Ocena: Odpowiedzialność}\nC --> D[Lęk]\nD --> E[Kompulsja]\nE -- Ulga --> C"
        }
    ],
    "F41.1": [
        {
            "Model": "Model Nietolerancji Niepewności (M. Dugas)",
            "Opis": "Zamartwianie się jako unikający styl radzenia sobie z lękiem.",
            "Interwencje": "Trening rozwiązywania problemów, ekspozycja na niepewność.",
            "Wizualizacja": "graph TD\nA[Niepewność] --> B{Nietolerancja}\nB --> C[Zamartwianie]\nC --> D[Iluzja kontroli]"
        }
    ],
    "F43.1": [
        {
            "Model": "Przedłużona Ekspozycja - PE (E. Foa)",
            "Opis": "PTSD wynika z niepełnego przetworzenia wspomnień przez unikanie bodźców.",
            "Interwencje": "Ekspozycja wyobrażeniowa, ekspozycja in vivo.",
            "Wizualizacja": "graph TD\nA[Trauma] --> B[Silny Lęk]\nB --> C[Unikanie wspomnień]\nC --> D[Brak przetwarzania]\nD -- Podtrzymanie --> B"
        }
    ]
}
slownik_modeli["F33"] = slownik_modeli["F32"]
slownik_modeli["F30"] = slownik_modeli["F32"] # Uproszczenie dla epizodu maniakalnego na potrzeby UI

# --- 2. BAZA ASYSTENTA NLP (PEŁNA WERSJA) ---
baza_symptomow = [
    {
        "klucze": ["minimum", "pretensje", "radość", "nie zależy", "nie mam energii", "anhedonia", "nic mnie nie cieszy"], 
        "diagnoza_grupa": "F30-F39 Zaburzenia nastroju (afektywne)",
        "diagnoza": "F32 Epizod depresyjny", 
        "roznicowa": "ChAD, Dystymia, Niedoczynność tarczycy, Wypalenie zawodowe.",
        "problemy": "POZNAWCZE: Ruminacje na temat własnej efektywności, negatywna ocena siebie.\nBEHAWIORALNE: Bierność, unikanie relacji, robienie 'minimum'.\nEMOCJONALNE: Anhedonia, dystansowanie się od pozytywnych emocji.",
        "cele": "1. Zwiększenie aktywności przynoszących satysfakcję o 20%.\n2. Identyfikacja i podważanie przekonań o 'robieniu minimum'.\n3. Trening odczuwania i uważności na emocje pozytywne.",
        "protokol": "Protokół Aktywacji Behawioralnej (BA) + CBT Becka",
        "uzasadnienie": "Kluczowe jest przerwanie cyklu bierności, który podtrzymuje anhedonię, oraz praca nad poczuciem winy z powodu nieefektywności."
    },
    {
        "klucze": ["serce", "panika", "umrę", "zawał", "duszno", "zemdleję"], 
        "diagnoza_grupa": "F40-F48 Zaburzenia lękowe",
        "diagnoza": "F41.0 Lęk paniczny", 
        "roznicowa": "Agorafobia, PTSD, Tarczyca, Kardiologia.",
        "problemy": "Katastroficzna interpretacja doznań somatycznych, zachowania zabezpieczające.",
        "cele": "1. Redukcja napadów paniki do 0.\n2. Eliminacja zachowań zabezpieczających.",
        "protokol": "Terapia Poznawcza wg Clarka",
        "uzasadnienie": "Reatrybucja doznań poprzez eksperymenty i ekspozycję interoceptywną."
    },
    {
        "klucze": ["myję", "sprawdzam", "liczę", "natrętne", "rytuał", "brud"], 
        "diagnoza_grupa": "F40-F48 Zaburzenia lękowe",
        "diagnoza": "F42 OCD", 
        "roznicowa": "Osobowość anankastyczna, Tiki.",
        "problemy": "Nadmierna odpowiedzialność, kompulsje redukujące lęk.",
        "cele": "1. Powstrzymanie reakcji (ERP).\n2. Redukcja zachowań upewniających się.",
        "protokol": "Ekspozycja z Powstrzymaniem Reakcji (ERP)",
        "uzasadnienie": "Habituacja lęku bez wykonywania rytuału (Model Salkovskisa)."
    }
]

# --- 3. PEŁNA BAZA ICD-10 ---
icd10_full = {
    "F30-F39 Zaburzenia nastroju (afektywne)": ["F30 Epizod maniakalny", "F31 ChAD", "F32 Epizod depresyjny", "F33 Zaburzenia depresyjne nawracające", "F34.1 Dystymia"],
    "F40-F48 Zaburzenia lękowe": ["F40.0 Agorafobia", "F40.1 Fobia społeczna", "F41.0 Lęk paniczny", "F41.1 GAD", "F42 OCD", "F43.1 PTSD"],
    "F50-F59 Zespoły behawioralne": ["F50.0 Jadłowstręt", "F50.2 Żarłoczność"],
    "F60-F69 Zaburzenia osobowości": ["F60.31 Borderline", "F60.5 Anankastyczna", "F60.6 Unikająca"]
}

# --- INICJALIZACJA STANU SESJI ---
if 'skarga_text' not in st.session_state: 
    st.session_state.skarga_text = "nie zależy albo ze mnie ocenia. W pracy (albo w domu) robię minimum, a potem mam do siebie pretensje, że robię minimum. I tak w kółko.\n\nNajgorsze jest to, że nawet gdy pojawia się coś potencjalnie miłego, nie umiem tego poczuć. Jakby radość była gdzieś za szybą. Unikam ludzi bo nie mam energii udawać że jest okej, a potem czuję..."
for k in ['p_txt', 'c_txt', 'pr_txt', 'u_txt']:
    if k not in st.session_state: st.session_state[k] = ""

# --- PASEK BOCZNY (SIDEBAR Z UI ZE ZDJĘCIA) ---
with st.sidebar:
    st.markdown("### 🛡️ Zapis Terapii CBT")
    st.write("Spis treści:")
    
    nawigacja = st.radio(
        "Ukryta etykieta", 
        [
            "🔴 I. Diagnoza i Konceptualizacja",
            "⚪ II. Plan i Interwencje",
            "⚪ III. Podsumowanie",
            "📁 Archiwum Diagnoz"
        ],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.caption("Oparte na: Zapis przebiegu terapii CBT")


# --- GŁÓWNA ZAWARTOŚĆ ---
if nawigacja == "🔴 I. Diagnoza i Konceptualizacja":
    
    st.header("I.2. Diagnoza kliniczna")

    with st.expander("⚙️ Asystent Diagnozy (NLP)", expanded=True):
        st.markdown("Wpisz objawy językiem pacjenta. System wypełni: Listę Problemów, Cele SMART oraz protokoły EBM w zakładce II.")
        
        skarga = st.text_area(
            "Cytaty pacjenta / Skarga główna:", 
            value=st.session_state.skarga_text,
            height=150
        )
        
        if st.button("🔍 Analizuj i przygotuj dokumentację"):
            found = False
            for el in baza_symptomow:
                if any(k in skarga.lower() for k in el["klucze"]):
                    st.session_state.p_txt = el["problemy"]
                    st.session_state.c_txt = el["cele"]
                    st.session_state.pr_txt = el["protokol"]
                    st.session_state.u_txt = el["uzasadnienie"]
                    st.success(f"Analiza zakończona. Wykryto wzorzec: {el['diagnoza']}")
                    st.warning(f"Zalecana diagnoza różnicowa: {el['roznicowa']}")
                    found = True
            if not found:
                st.info("Nie znaleziono bezpośredniego dopasowania. Wypełnij pola ręcznie.")

    col1, col2 = st.columns(2)
    with col1:
        grupa = st.selectbox("Grupa ICD-10:", list(icd10_full.keys()), index=0)
    with col2:
        diag = st.selectbox("Rozpoznanie główne potwierdzone ręcznie:", icd10_full[grupa], index=0)
        kod_icd = diag.split(" ")[0]

    st.text_input("Inne rozpoznania (np. somatyczne, psychiatryczne współwystępujące):")

    st.markdown("---")
    
    # --- Modułowe łączenie modeli CBT ---
    st.markdown("### 🧩 Modułowe łączenie modeli CBT 🔗")
    
    c_mod1, c_mod2 = st.columns([1, 1])
    
    with c_mod1:
        st.info("**Dane wygenerowane klinicznie:**")
        st.session_state.p_txt = st.text_area("Lista Problemów:", value=st.session_state.p_txt, height=200)
        st.session_state.c_txt = st.text_area("Cele SMART:", value=st.session_state.c_txt, height=150)
        
    with c_mod2:
        st.info("**Dopasowane modele CBT (Baza EBM):**")
        if kod_icd in slownik_modeli:
            for m in slownik_modeli[kod_icd]:
                with st.container(border=True):
                    st.markdown(f"**{m['Model']}**")
                    st.caption(m['Opis'])
                    st.write(f"*Interwencje:* {m['Interwencje']}")
                    with st.expander("Schemat graficzny mechanizmu (Mermaid)"):
                        st.markdown(f"```mermaid\n{m['Wizualizacja']}\n```")
        else:
            st.warning("Dla tego kodu brakuje szczegółowego modelu graficznego w bazie. Zastosuj ogólny model poznawczy.")
            
    st.divider()
    st.subheader("Mechanizmy pogłębione (Poziom 2 i 3 Konceptualizacji)")
    col_a, col_b = st.columns(2)
    with col_a:
        st.text_area("Przekonania kluczowe (o sobie, świecie, innych):", placeholder="Np. Jestem niewystarczający...")
        st.text_area("Przekonania warunkowe (Założenia / Zasady):", placeholder="Np. Jeśli nie robię 100%, to jestem bezwartościowy.")
    with col_b:
        st.text_area("Strategie kompensacyjne (Radzenie sobie):", placeholder="Np. Wycofanie, robienie 'minimum'.")
        st.text_area("Historia rozwojowa (Czynniki predysponujące):", placeholder="Wydarzenia z dzieciństwa kształtujące schematy...")

elif nawigacja == "⚪ II. Plan i Interwencje":
    st.header("II. Plan i Interwencje")
    st.session_state.pr_txt = st.text_input("Sugerowany protokół EBM:", value=st.session_state.pr_txt)
    st.session_state.u_txt = st.text_area("Uzasadnienie planu terapeutycznego:", value=st.session_state.u_txt, height=200)
    st.divider()
    st.subheader("Harmonogram pracy")
    st.text_area("Etap edukacji, pracy behawioralnej i poznawczej (w czasie):", height=150)

elif nawigacja == "⚪ III. Podsumowanie":
    st.header("III. Podsumowanie i zalecenia")
    st.text_area("Notatki końcowe po zamknięciu terapii:", height=300)

elif nawigacja == "📁 Archiwum Diagnoz":
    st.header("Archiwum")
    st.write("Baza zapisanych konceptualizacji (funkcja w przygotowaniu).")

