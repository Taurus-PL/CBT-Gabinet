import streamlit as st
import pandas as pd
import re

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Zapis Przebiegu Terapii CBT", layout="wide")

# --- BAZA WIEDZY I DIAGRAMY MERMAID Z KRYTERIAMI DOPASOWANIA ---
slownik_modeli = {
    "F41.0": [
        {
            "Model": "Model poznawczy lęku panicznego (D. Clark)",
            "Opis": "Skupienie na błędnej, katastroficznej interpretacji normalnych doznań z ciała (np. kołatanie serca = zawał).",
            "Interwencje": "Reatrybucja doznań, hiperwentylacja (eksperyment), eliminacja zachowań zabezpieczających.",
            "slowa_kluczowe": ["zawał", "uduszę się", "umrę", "serce", "oddech", "tchu", "zwariuję", "zemdleję", "kłucie", "gorąc"],
            "Wizualizacja": (
                "graph TD\n"
                "A[Wewnętrzny lub zewn. wyzwalacz] --> B[Postrzegane zagrożenie]\n"
                "B --> C[Lęk / Niepokój]\n"
                "C --> D[Doznania somatyczne np. serce]\n"
                "D --> E{Katastroficzna interpretacja}\n"
                "E -- Błędne koło paniki --> B\n"
                "style E fill:#4d0000,stroke:#ff3333,stroke-width:2px,color:#fff\n"
            )
        }
    ],
    "F32": [
        {
            "Model": "Triada Poznawcza Depresji (A. Beck)",
            "Opis": "Negatywna wizja siebie, świata i przyszłości wynikająca z dysfunkcjonalnych schematów i błędów poznawczych.",
            "Interwencje": "Zapisywanie myśli (Tabela Becka), restrukturyzacja poznawcza, testowanie przekonań.",
            "slowa_kluczowe": ["do niczego", "beznadziejny", "nikt mnie nie rozumie", "zawsze tak będzie", "bez sensu", "wina", "jestem najgorszy", "głupi", "nic nie osiągnę"],
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
        {
            "Model": "Model Aktywacji Behawioralnej - BA (C. Martell)",
            "Opis": "Depresja jako wynik spadku wzmocnień pozytywnych ze środowiska. Obniżony nastrój prowadzi do wycofania, co pogłębia brak wzmocnień.",
            "Interwencje": "Monitorowanie aktywności, planowanie aktywności (przyjemność i mistrzostwo), ocena barier.",
            "slowa_kluczowe": ["nie mam siły", "leżę", "łóżk", "nie chce mi się", "nic mnie nie cieszy", "brak energii", "wycofan", "zmęczeni", "bierno", "weget", "zmuszam"],
            "Wizualizacja": (
                "graph TD\n"
                "A[Stresory / Spadek wzmocnień] --> B[Obniżony nastrój / Brak energii]\n"
                "B --> C[Wycofanie / Bierność / Ruminacje]\n"
                "C --> D[Jeszcze mniej wzmocnień i więcej problemów]\n"
                "D -- Błędne koło --> B\n"
                "style C fill:#333333,stroke:#666666,color:#fff\n"
            )
        },
        {
            "Model": "Model Wyuczonej Bezradności (M. Seligman)",
            "Opis": "Depresja jako skutek poczucia braku wpływu na negatywne zdarzenia oraz przypisywania im wewnętrznych, stałych i globalnych przyczyn.",
            "Interwencje": "Zmiana stylu atrybucyjnego, budowanie poczucia sprawstwa (empowerment).",
            "slowa_kluczowe": ["brak wpływu", "nie mam kontroli", "to moja wina", "pech", "zawsze mam pod górkę", "bezradn", "nie ma wyjścia", "poddaję się"],
            "Wizualizacja": (
                "graph TD\n"
                "A[Negatywne zdarzenie] --> B{Brak poczucia kontroli}\n"
                "B --> C[Styl atrybucyjny: Wewn., Stały, Globalny]\n"
                "C --> D[Poczucie bezradności i beznadziei]\n"
                "D --> E[Objawy depresyjne]\n"
                "style C fill:#4d4d4d,stroke:#808080,color:#fff\n"
            )
        },
        {
            "Model": "MBCT - Mindfulness (Segal, Williams, Teasdale)",
            "Opis": "Nawroty depresji wynikają z reaktywacji starych wzorców myślenia. Pacjent wpada w ruminacje i 'tryb działania'.",
            "Interwencje": "Trening uważności, decentracja, świadome przejście do trybu 'bycia'.",
            "slowa_kluczowe": ["nawrót", "znowu wraca", "krążą myśli", "ruminacj", "analizuj", "nie mogę przestać myśleć", "tryb działania", "kolejny raz to samo"],
            "Wizualizacja": (
                "graph TD\n"
                "A[Spadek nastroju] --> B[Zautomatyzowane negatywne myślenie]\n"
                "B --> C[Ruminacje / Próba naprawienia nastroju]\n"
                "C --> D[Pogłębienie depresji]\n"
                "D --> B\n"
                "style C fill:#336699,stroke:#6699cc,color:#fff\n"
            )
        },
        {
            "Model": "Model Elastyczności Psychologicznej - ACT (S. Hayes)",
            "Opis": "Cierpienie depresyjne to wynik unikania trudnych emocji i fuzji poznawczej, co odcina pacjenta od wartości.",
            "Interwencje": "Defuzja, akceptacja, klaryfikacja wartości, zaangażowane działanie.",
            "slowa_kluczowe": ["uciekam", "unikam", "odcinam się", "nie chcę czuć", "walczę", "pustka", "nie wiem kim jestem", "wartości", "straciłem sens", "znieczulam się"],
            "Wizualizacja": (
                "graph TD\n"
                "A[Trudne myśli i emocje] --> B[Unikanie doświadczania]\n"
                "A --> C[Fuzja poznawcza]\n"
                "B --> D[Oderwanie od wartości]\n"
                "C --> D\n"
                "D --> E[Bierność i Epizod Depresyjny]\n"
                "style D fill:#660033,stroke:#99004d,color:#fff\n"
            )
        }
    ],
    "F40.1": [
        {
            "Model": "Model Lęku Społecznego (Clark i Wells)",
            "Opis": "Koncentracja uwagi na sobie, tworzenie negatywnego obrazu siebie jako obiektu społecznego.",
            "Interwencje": "Trening uwagi na zewnątrz (task-concentration), wideo-feedback, eksperymenty.",
            "slowa_kluczowe": ["patrzą", "wstyd", "oceniają", "wyśmieją", "czerwony", "kompromitacj", "wypaść głupio", "wzrok innych", "pośmiewisko", "ocena"],
            "Wizualizacja": (
                "graph TD\n"
                "A[Sytuacja społeczna] --> B[Zagrożenie społeczzne]\n"
                "B --> C[Skupienie uwagi na sobie]\n"
                "C <--> D[Objawy somatyczne]\n"
                "C <--> E[Zachowania zabezpieczające]\n"
                "D <--> E\n"
                "style C fill:#663300,stroke:#ff9900,color:#fff\n"
            )
        }
    ],
    "F42": [
        {
            "Model": "Model poznawczy OCD (P. Salkovskis)",
            "Opis": "Przesadne poczucie odpowiedzialności (TAF). Myśl natrętna jest interpretowana jako realne zagrożenie i znak moralny.",
            "Interwencje": "Restrukturyzacja przekonań o odpowiedzialności, ciasto odpowiedzialności.",
            "slowa_kluczowe": ["odpowiedzialność", "moja wina", "zły człowiek", "znak", "magiczne", "znaczy że chcę", "kara", "moraln"],
            "Wizualizacja": (
                "graph TD\n"
                "A[Wyzwalacz] --> B[Natrętna myśl]\n"
                "B --> C{Nadmierna Odpowiedzialność}\n"
                "C --> D[Silny Lęk i Wina]\n"
                "D --> E[Kompulsje]\n"
                "E --> F[Chwilowa ulga]\n"
                "F -.-> C\n"
                "style C fill:#4d004d,stroke:#cc00cc,color:#fff\n"
            )
        },
        {
            "Model": "Model habituacyjny OCD / ERP (E. Foa)",
            "Opis": "Mechanizm warunkowania strachu. Kompulsje zapobiegają naturalnemu wygasaniu lęku.",
            "Interwencje": "Ekspozycja z powstrzymaniem reakcji (ERP), hierarchia lęku.",
            "slowa_kluczowe": ["muszę sprawdzić", "rytuał", "zapeszyć", "układam", "liczę", "powtarzam", "myję", "czyszczę", "brud"],
            "Wizualizacja": (
                "graph LR\n"
                "A[Ekspozycja] --> B[Wzrost Lęku]\n"
                "B --> C[Powstrzymanie Kompulsji]\n"
                "C --> D[Naturalna Habituacja Lęku]\n"
                "style C fill:#006600,stroke:#009900,color:#fff\n"
            )
        }
    ],
    "F41.1": [
        {
            "Model": "Model Nietolerancji Niepewności (M. Dugas)",
            "Opis": "Zamartwianie się jako unikający styl radzenia sobie z lękiem. Pacjent uważa, że niepewność jest nie do zniesienia.",
            "Interwencje": "Trening rozwiązywania problemów, tolerancja na niepewność.",
            "slowa_kluczowe": ["muszę wiedzieć", "planuję wszystko", "niespodziank", "najgorsze scenariusze", "a co jeśli", "niepewność", "przygotowany", "w razie czego"],
            "Wizualizacja": (
                "graph TD\n"
                "A[Sytuacja niepewna] --> B{Nietolerancja Niepewności}\n"
                "B --> C[Zamartwianie się]\n"
                "C --> D[Iluzja kontroli]\n"
                "style B fill:#4d4d00,stroke:#cccc00,color:#fff\n"
            )
        },
        {
            "Model": "Model Metapoznawczy - MCT (A. Wells)",
            "Opis": "Skupienie na metaprzekonaniach. Pozytywnych ('martwienie chroni') i negatywnych ('stracę kontrolę').",
            "Interwencje": "Odraczanie martwienia, Detached Mindfulness.",
            "slowa_kluczowe": ["nie mogę przestać", "zwariuję od tego", "martwienie mnie chroni", "gdybym się nie martwił", "utrata kontroli nad", "głowa pęka", "natłok myśli"],
            "Wizualizacja": (
                "graph TD\n"
                "A[A co jeśli...] --> B[Pozytywne metaprzekonania]\n"
                "B --> C[ZAMARTWIANIE]\n"
                "C --> D[Negatywne metaprzekonania - Typ 2]\n"
                "D --> E[Lęk, nieskuteczne unikanie]\n"
                "style D fill:#993300,stroke:#cc3300,color:#fff\n"
            )
        }
    ],
    "F43.1": [
        {
            "Model": "Przedłużona Ekspozycja - PE (E. Foa)",
            "Opis": "PTSD wynika z niepełnego przetworzenia wspomnień traumatycznych z powodu silnego unikania.",
            "Interwencje": "Ekspozycja wyobrażeniowa, ekspozycja in vivo.",
            "slowa_kluczowe": ["unikam miejsc", "odrętwienie", "nie chcę o tym", "unikam myśli", "nie wychodzę z domu", "omijam", "nie czuję nic"],
            "Wizualizacja": (
                "graph TD\n"
                "A[Trauma] --> B[Silny Lęk warunkowy]\n"
                "B --> C[Unikanie bodźców i wspomnień]\n"
                "C --> D[Brak przetwarzania emocjonalnego]\n"
                "D --> B\n"
                "style C fill:#003366,stroke:#006699,color:#fff\n"
            )
        },
        {
            "Model": "Model poznawczy PTSD (Ehlers i Clark)",
            "Opis": "Poczucie ciągłego zagrożenia 'tu i teraz' przez negatywną ocenę traumy i zaburzenia pamięci.",
            "Interwencje": "Aktualizacja pamięci traumy, restrukturyzacja punktów zapalnych.",
            "slowa_kluczowe": ["flashbacki", "czuję jakby", "teraz się działo", "znowu", "koszmary", "wspomnienia wracają", "dźwięk", "ciągle na krawędzi", "zawsze niebezpiecznie"],
            "Wizualizacja": (
                "graph TD\n"
                "A[Trauma] --> B[Negatywna ocena]\n"
                "A --> C[Pamięć oparta na zmysłach]\n"
                "B --> D[Poczucie AKTUALNEGO zagrożenia]\n"
                "C --> D\n"
                "D --> E[Intruzje / Pobudzenie]\n"
                "E --> F[Unikanie]\n"
                "style D fill:#660000,stroke:#990000,color:#fff\n"
            )
        }
    ]
}
slownik_modeli["F33"] = slownik_modeli["F32"]

# --- FUNKCJA DOPASOWANIA MODELI ---
def dopasuj_modele(kod_icd, tekst_pacjenta):
    if kod_icd not in slownik_modeli:
        return []
    
    tekst = tekst_pacjenta.lower()
    wyniki = []
    
    for model in slownik_modeli[kod_icd]:
        punkty = 0
        for slowo in model.get("slowa_kluczowe", []):
            if slowo in tekst:
                punkty += 1
        wyniki.append({"model": model, "punkty": punkty})
        
    wyniki.sort(key=lambda x: x["punkty"], reverse=True)
    return wyniki

# --- BAZA ASYSTENTA DIAGNOZY (skrócona dla czytelności NLP) ---
baza_symptomow = [
    {
        "slowa_kluczowe": ["serce mi wali", "zaraz umrę", "uduszę się", "zawał", "zwariuję", "kłucie", "duszno", "miękną mi nogi", "atak paniki", "nogi z waty"], 
        "diagnoza": "F41.0 Zaburzenie lękowe z napadami lęku", "roznicowa": "Agorafobia (F40.0), PTSD (F43.1)",
        "cbt_problemy": "LĘK PANICZNY:\n- Poznawcze: Katastroficzna interpretacja doznan fizjologicznych...\n- Behawioralne: Unikanie...",
        "cele_smart": "1. Zmniejszenie napadów paniki do 0.\n2. Eliminacja 2 zachowań zabezpieczających.",
        "uzasadnienie_planu": "Reatrybucja poznawcza doznań i eksperymenty behawioralne."
    },
    {
        "slowa_kluczowe": ["nie mam siły", "nic mnie nie cieszy", "nie chce mi się", "budzę się w nocy", "beznadziejny", "smutek", "wegetuję", "wina", "leżę"], 
        "diagnoza": "F32 Epizod depresyjny", "roznicowa": "ChAD (F31), Dystymia (F34.1)",
        "cbt_problemy": "ZESPÓŁ DEPRESYJNY:\n- Poznawcze: Negatywna triada Becka...\n- Behawioralne: Bierność, izolacja...",
        "cele_smart": "1. Wzrost aktywności celowej min. 3x w tygodniu.\n2. Zapisywanie myśli w Tabeli Becka.",
        "uzasadnienie_planu": "Aktywizacja pacjenta i praca nad zniekształceniami."
    },
    {
        "slowa_kluczowe": ["muszę to sprawdzić", "ciągle myję", "natrętne", "rytuał", "zapeszyć", "brud", "odliczam", "pewność", "magiczne"], 
        "diagnoza": "F42 Zaburzenie obsesyjno-kompulsyjne", "roznicowa": "OCPD (F60.5)",
        "cbt_problemy": "OCD:\n- Poznawcze: Obsesje, fuzja myśli (TAF)...\n- Behawioralne: Kompulsje, rytuały.",
        "cele_smart": "1. Odroczenie kompulsji o 30 min.\n2. Trening ERP.",
        "uzasadnienie_planu": "Ekspozycja i Habitualizacja lęku (ERP)."
    },
    {
        "slowa_kluczowe": ["boję się odezwać", "patrzą", "wstyd", "wyśmieją", "czerwony", "kompromitacja", "oceny", "pośmiewisko"], 
        "diagnoza": "F40.1 Fobia społeczna", "roznicowa": "Osobowość unikająca (F60.6)",
        "cbt_problemy": "LĘK SPOŁECZNY:\n- Poznawcze: Skupienie na sobie...\n- Behawioralne: Izolacja społeczna.",
        "cele_smart": "1. Inicjowanie rozmowy 2x w tyg.\n2. Porzucenie zachowania zabezpieczającego.",
        "uzasadnienie_planu": "Trening koncentracji zadaniowej i ekspozycja."
    },
    {
        "slowa_kluczowe": ["ciągle się martwię", "co będzie jak", "spięte mięśnie", "najgorsze scenariusze", "a co jeśli", "niepokój", "natłok myśli"], 
        "diagnoza": "F41.1 Zaburzenie lękowe uogólnione", "roznicowa": "Fobia społeczna (F40.1)",
        "cbt_problemy": "GAD:\n- Poznawcze: Nietolerancja niepewności, martwienie się...\n- Fizjologiczne: Napięcie.",
        "cele_smart": "1. Wyznaczenie czasu na martwienie.\n2. PMR (relaksacja).",
        "uzasadnienie_planu": "Praca z nietolerancją niepewności i odraczaniem."
    },
    {
        "slowa_kluczowe": ["śni", "wspomnienia", "przed oczami", "unikam miejsc", "flashbacki", "czuję jakby to działo", "trauma", "koszmary"], 
        "diagnoza": "F43.1 Zaburzenie stresowe pourazowe", "roznicowa": "Ostra reakcja na stres (F43.0)",
        "cbt_problemy": "PTSD:\n- Poznawcze: Poczucie aktualnego zagrożenia...\n- Behawioralne: Unikanie bodźców.",
        "cele_smart": "1. Ekspozycja wyobrażeniowa.\n2. Ekspozycja in vivo na 2 miejsca.",
        "uzasadnienie_planu": "Przetworzenie wspomnień traumatycznych."
    }
]

# --- BAZA ICD-10 ---
icd10_full = {"F30-F39 Zaburzenia nastroju (afektywne)": ["F32 Epizod depresyjny", "F33 Zab. depresyjne nawracające"], "F40-F48 Zaburzenia lękowe": ["F40.1 Fobie społeczne", "F41.0 Zab. lękowe z napadami lęku", "F41.1 Zab. lękowe uogólnione", "F42 Zab. obsesyjno-kompulsyjne", "F43.1 PTSD"]}

# --- STAN APLIKACJI ---
for key in ['baza_terapii', 'lista_problemow', 'cele_terapii', 'wybrany_protokol', 'uzasadnienie_planu', 'ui_problemy', 'ui_cele', 'ui_protokol', 'ui_uzasadnienie']:
    if key not in st.session_state: st.session_state[key] = [] if key == 'baza_terapii' else ""
if 'rekomendowany_model_dane' not in st.session_state:
    st.session_state.rekomendowany_model_dane = None

def sync_fields():
    st.session_state.lista_problemow = st.session_state.ui_problemy
    st.session_state.cele_terapii = st.session_state.ui_cele
    st.session_state.wybrany_protokol = st.session_state.ui_protokol
    st.session_state.uzasadnienie_planu = st.session_state.ui_uzasadnienie

# --- MENU BOCZNE ---
st.sidebar.title("🛡️ Zapis Terapii CBT")
menu = st.sidebar.radio("Spis treści:", ["I. Diagnoza i Konceptualizacja", "II. Plan i Interwencje", "III. Podsumowanie", "📂 Archiwum"])

# ==================================
# MODUŁ I
# ==================================
if menu == "I. Diagnoza i Konceptualizacja":
    st.title("I. Diagnoza i konceptualizacja")
    
    with st.expander("🤖 Asystent Diagnozy (NLP z autoselekcją modelu)", expanded=True):
        objawy_input = st.text_area("Wpisz skargi pacjenta (im więcej szczegółów dot. zachowań i myśli, tym lepsze dopasowanie modelu):")
        
        if st.button("🔍 Analizuj i dopasuj model"):
            znaleziono_diagnoze = False
            
            if objawy_input:
                tekst = objawy_input.lower()
                
                # 1. SZUKANIE GŁÓWNEJ DIAGNOZY
                for el in baza_symptomow:
                    if any(fraza in tekst for fraza in el["slowa_kluczowe"]):
                        kod_glowny = el['diagnoza'].split(" ")[0]
                        
                        st.session_state.lista_problemow = el['cbt_problemy']
                        st.session_state.cele_terapii = el['cele_smart']
                        st.session_state.uzasadnienie_planu = el['uzasadnienie_planu']
                        znaleziono_diagnoze = True
                        st.success(f"🎯 **Wykryto rozpoznanie:** {el['diagnoza']}")
                        
                        # 2. DOPASOWANIE KONKRETNEGO MODELU CBT
                        dopasowane = dopasuj_modele(kod_glowny, objawy_input)
                        
                        if dopasowane and dopasowane[0]["punkty"] > 0:
                            # Wybieramy najlepszy model (lub modele jeśli remis)
                            max_pkt = dopasowane[0]["punkty"]
                            najlepsze_modele = [m["model"]["Model"] for m in dopasowane if m["punkty"] == max_pkt]
                            
                            st.session_state.wybrany_protokol = " / ".join(najlepsze_modele)
                            st.session_state.rekomendowany_model_dane = dopasowane
                            st.info(f"💡 Na podstawie analizy słów kluczowych, algorytm rekomenduje model(e): **{st.session_state.wybrany_protokol}**")
                        else:
                            st.session_state.wybrany_protokol = "Ogólny model poznawczo-behawioralny"
                            st.session_state.rekomendowany_model_dane = dopasowane
                            
                        break # Kończymy pętlę po pierwszym trafnym rozpoznaniu
                        
                if not znaleziono_diagnoze:
                    st.warning("Nie rozpoznano jednoznacznie diagnozy. Wypełnij pola ręcznie.")
                
                st.session_state.ui_problemy = st.session_state.lista_problemow
                st.session_state.ui_cele = st.session_state.cele_terapii
                st.session_state.ui_protokol = st.session_state.wybrany_protokol
                st.session_state.ui_uzasadnienie = st.session_state.uzasadnienie_planu
    
    c1, c2 = st.columns(2)
    kat_wybrana = c1.selectbox("Grupa ICD-10:", list(icd10_full.keys()))
    pelna_diagnoza = c2.selectbox("Rozpoznanie główne:", icd10_full[kat_wybrana])
    kod_icd = pelna_diagnoza.split(" ")[0]

    # WIEDZA EBM - WYSWIETLANIE I SORTOWANIE MODELI
    st.divider()
    st.header(f"🧩 Protokoły leczenia dla: {pelna_diagnoza}")
    
    dopasowane_lista = dopasuj_modele(kod_icd, objawy_input if 'objawy_input' in locals() and objawy_input else "")
    
    if dopasowane_lista:
        najlepszy_wynik = dopasowane_lista[0]["punkty"]
        
        for element in dopasowane_lista:
            model = element["model"]
            punkty = element["punkty"]
            
            # Podświetlanie najlepszego wyboru
            if punkty == najlepszy_wynik and punkty > 0:
                st.markdown(f"### ⭐ REKOMENDOWANY: {model['Model']} *(trafność: wysoka)*")
            else:
                st.markdown(f"### 🛠️ {model['Model']}")
                
            st.write(f"**Mechanizm:** {model['Opis']}")
            st.write(f"**Główne interwencje:** {model['Interwencje']}")
            
            if "Wizualizacja" in model:
                with st.expander(f"ZOBACZ SCHEMAT: {model['Model']}"):
                    st.markdown(f"```mermaid\n{model['Wizualizacja']}\n```")
            st.write("---")

    # RESZTA FORMULARZA...
    st.subheader("I.3.1. Lista problemów i cele terapii")
    st.text_area("Lista problemów (w ujęciu poznawczo-behawioralnym)", key="ui_problemy", on_change=sync_fields, height=200)
    st.text_area("Cele terapii (zoperacjonalizowane, mierzalne, SMART)", key="ui_cele", on_change=sync_fields, height=100)
    
    if st.button("💾 Zapisz do Bazy"): st.success("Zapisano (demo)!")

elif menu == "II. Plan i Interwencje":
    st.title("II. Plan terapii i interwencje")
    st.text_input("Sugerowany protokół (EBM):", key="ui_protokol", on_change=sync_fields)
    st.text_area("Uzasadnienie poznawczo-behawioralne:", key="ui_uzasadnienie", on_change=sync_fields, height=150)

elif menu == "III. Podsumowanie":
    st.title("III. Podsumowanie")
    st.text_area("Osiągnięte cele:")

elif menu == "📂 Archiwum":
    st.title("Archiwum pacjentów")
    st.write("Tutaj pojawi się lista pacjentów z możliwością eksportu.")
