import streamlit as st
import pandas as pd
import re

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Zapis Przebiegu Terapii CBT", layout="wide")

# --- BAZA WIEDZY I DIAGRAMY MERMAID ---
slownik_modeli = {
    "F41.0": [
        {
            "Model": "Model poznawczy lęku panicznego (D. Clark)",
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
        }
    ],
    "F32": [
        {
            "Model": "Triada Poznawcza Depresji (A. Beck)",
            "Opis": "Negatywna wizja siebie, świata i przyszłości wynikająca z dysfunkcjonalnych schematów i błędów poznawczych.",
            "Interwencje": "Zapisywanie myśli (Tabela Becka), restrukturyzacja poznawcza, testowanie przekonań.",
            "Wizualizacja": (
                "graph TD\n"
                "A((Negatywne myśli O SOBIE)) <--> B((Negatywne myśli O ŚWIECIE))\n"
                "B <--> C((Negatywne myśli O PRZYSZŁOŚCI))\n"
                "C <--> A\n"
                "style A fill:#002b5e,stroke:#3399ff,color:#fff\n"
            )
        },
        {
            "Model": "Model Aktywacji Behawioralnej - BA (C. Martell / P. Lewinsohn)",
            "Opis": "Depresja jako wynik spadku wzmocnień pozytywnych ze środowiska. Obniżony nastrój prowadzi do wycofania.",
            "Interwencje": "Monitorowanie aktywności, planowanie aktywności (przyjemność i mistrzostwo), ocena barier.",
            "Wizualizacja": (
                "graph TD\n"
                "A[Stresory / Spadek wzmocnień] --> B[Obniżony nastrój / Brak energii]\n"
                "B --> C[Wycofanie / Bierność / Ruminacje]\n"
                "C --> D[Jeszcze mniej wzmocnień i więcej problemów]\n"
                "D -- Błędne koło --> B\n"
                "style C fill:#333333,stroke:#666666,color:#fff\n"
            )
        }
    ],
    "F51": [
        {
            "Model": "Model 3P Bezsenności (A. Spielman)",
            "Opis": "Bezsenność pojawia się i utrzymuje przez 3 grupy czynników: Predysponujące, Wyzwalające i Podtrzymujące.",
            "Interwencje": "Restrykcja snu, kontrola bodźców, higiena snu, techniki relaksacyjne.",
            "Wizualizacja": (
                "graph TD\n"
                "A[Czynniki Predysponujące] --> B[Czynniki Wyzwalające]\n"
                "B --> C[Ostra Bezsenność]\n"
                "C --> D[Czynniki Podtrzymujące np. drzemki]\n"
                "D --> E[Przewlekła Bezsenność]\n"
                "E -- Błędne koło --> D\n"
                "style D fill:#1a1a1a,stroke:#4d4d4d,color:#fff\n"
            )
        }
    ],
    "F50.2": [
        {
            "Model": "Transdiagnostyczny model zaburzeń odżywiania (C. Fairburn)",
            "Opis": "Rdzeniem zaburzenia jest nadmierne uzależnienie samooceny od wagi i sylwetki, co prowadzi do drastycznych restrykcji, napadów objadania się i zachowań kompensacyjnych.",
            "Interwencje": "Monitorowanie odżywiania, planowanie regularnych posiłków, restrukturyzacja przekonań o ciele i wadze.",
            "Wizualizacja": (
                "graph TD\n"
                "A[Nadmierna koncentracja na sylwetce i wadze] --> B[Restrykcyjne zasady dietetyczne]\n"
                "B --> C[Złamanie zasad / Narastające napięcie]\n"
                "C --> D[Napad objadania się]\n"
                "D --> E[Zachowania kompensacyjne np. wymioty]\n"
                "D --> F[Poczucie winy i lęk przed tyciem]\n"
                "E --> F\n"
                "F -- Wzmacnia kontrolę --> A\n"
                "style A fill:#004d40,stroke:#00695c,color:#fff\n"
            )
        }
    ]
}
slownik_modeli["F33"] = slownik_modeli["F32"]
slownik_modeli["F50.0"] = slownik_modeli["F50.2"]

# --- NOWA BAZA ASYSTENTA (ZGODNA Z ARKUSZEM PSYCHOLOGY TOOLS) ---
baza_symptomow = [
    {
        "diagnoza": "F50.2 Żarłoczność psychiczna (Bulimia)",
        "roznicowa": "Anoreksja (F50.0), BED, Depresja.",
        "profil_cbt": {
            "SYTUACJA (Co działo się? Gdzie? Kiedy? Z kim?)": {
                "slowa": ["wieczór", "samotn", "stres", "kłótni", "imprez", "restauracj", "sklep", "wadze", "lustrz"],
                "tlumaczenie": "Sytuacje napięcia emocjonalnego (stres, samotność) lub ekspozycja na bodźce związane z jedzeniem/sylwetką."
            },
            "MYŚLI (Co przyszło do głowy? Myśli, obrazy, wspomnienia)": {
                "slowa": ["grub", "śmieć", "nienawidz", "brzydz", "obsesj", "wag", "lustr", "schudn", "diet", "nigdy", "zawsze", "muszę", "nie dam rady"],
                "tlumaczenie": "Nadmierne uzależnienie samooceny od wagi/sylwetki, myślenie dychotomiczne ('wszystko albo nic'), silna samokrytyka."
            },
            "EMOCJE I OBJAWY FIZYCZNE (Co czułeś? Jak silne to było?)": {
                "slowa": ["wstyd", "wyrzut", "win", "lęk", "boję", "stres", "napięc", "zmęcz", "słab", "mdł", "zimn", "brzuch", "gardł", "opuch"],
                "tlumaczenie": "Głębokie poczucie winy, wstyd po napadzie, lęk przed przytyciem. Wyczerpanie fizyczne i objawy ze strony układu pokarmowego."
            },
            "REAKCJE I KONSEKWENCJE (Co zrobiłeś? Jak sobie poradziłeś?)": {
                "slowa": ["napad", "obżarst", "popłyn", "ciąg", "lodówk", "pochłan", "wymiot", "rzyg", "przeczyszcz", "senes", "ćwicz", "siłown", "głodów", "ulga"],
                "tlumaczenie": "Napady objadania się (utrata kontroli), po których następują zachowania kompensacyjne. Krótkotrwała ulga prowadząca do poczucia winy."
            }
        },
        "cele_smart": "1. Wprowadzenie regularnego planu posiłków (3 główne, 2 przekąski).\n2. Zmniejszenie częstotliwości napadów/wymiotów do 1/tydz.",
        "protokol_nazwa": "CBT-E wg C. Fairburna",
        "uzasadnienie_planu": "1) Psychoedukacja (błędne koło). 2) Dzienniczek myśli i reakcji. 3) Restrukturyzacja poznawcza."
    },
    {
        "diagnoza": "F32 Epizod depresyjny",
        "roznicowa": "ChAD, Dystymia, Niedoczynność tarczycy.",
        "profil_cbt": {
            "SYTUACJA (Co działo się? Gdzie? Kiedy? Z kim?)": {
                "slowa": ["rano", "wsta", "prac", "obowiąz", "ludz", "problem", "poranek"],
                "tlumaczenie": "Konieczność podjęcia aktywności, przebudzenie (często gorsze samopoczucie rano), sytuacje wymagające interakcji."
            },
            "MYŚLI (Co przyszło do głowy? Myśli, obrazy, wspomnienia)": {
                "slowa": ["beznadziej", "bez sensu", "nikim", "ciężar", "nie uda", "głup", "win", "czarn", "nigdy", "zawsze"],
                "tlumaczenie": "Negatywna triada Becka (negatywne myśli o sobie, świecie i przyszłości), generalizacja, katastrofizacja."
            },
            "EMOCJE I OBJAWY FIZYCZNE (Co czułeś? Jak silne to było?)": {
                "slowa": ["smut", "przygnęb", "płacz", "pust", "nic nie czuj", "znieczul", "spać", "zmęcz", "brak sił", "budzę się", "apetyt", "ociężał"],
                "tlumaczenie": "Obniżony nastrój, anhedonia, apatia. Spadek energii, zaburzenia snu i apetytu."
            },
            "REAKCJE I KONSEKWENCJE (Co zrobiłeś? Jak sobie poradziłeś?)": {
                "slowa": ["nie chce mi się", "leżę", "wegetuj", "izoluj", "nie wychodz", "zamkn", "zaniedb"],
                "tlumaczenie": "Wycofanie z relacji społecznych, bierność, spadek wzmocnień pozytywnych ze środowiska. Pogłębienie izolacji."
            }
        },
        "cele_smart": "1. Zwiększenie aktywności celowej.\n2. Zapisywanie myśli w arkuszu samooceny.",
        "protokol_nazwa": "Aktywacja Behawioralna / Terapia Poznawcza Depresji",
        "uzasadnienie_planu": "Monitorowanie aktywności i nastroju, testowanie myśli automatycznych."
    },
    {
        "diagnoza": "F41.0 Lęk paniczny",
        "roznicowa": "Agorafobia, Zaburzenia kardiologiczne.",
        "profil_cbt": {
            "SYTUACJA (Co działo się? Gdzie? Kiedy? Z kim?)": {
                "slowa": ["tłum", "sklep", "kolejk", "autobus", "kawi", "wysił", "zadu", "samochód"],
                "tlumaczenie": "Miejsca zatłoczone, zamknięte przestrzenie, wysiłek fizyczny lub sytuacje przypominające poprzednie napady."
            },
            "MYŚLI (Co przyszło do głowy? Myśli, obrazy, wspomnienia)": {
                "slowa": ["umrę", "uduszę", "zawał", "zwariuję", "tracę kontrol", "zemdlej", "to koniec"],
                "tlumaczenie": "Katastroficzna interpretacja normalnych doznań płynących z ciała (np. bicie serca = zawał)."
            },
            "EMOCJE I OBJAWY FIZYCZNE (Co czułeś? Jak silne to było?)": {
                "slowa": ["panik", "przeraż", "strach", "serce", "wali", "brakuje mi tchu", "duszno", "kłuci", "drż", "pocę", "miękną nogi"],
                "tlumaczenie": "Nagły, nieprzewidywalny silny lęk z towarzyszącym silnym pobudzeniem wegetatywnym (tachykardia, duszności)."
            },
            "REAKCJE I KONSEKWENCJE (Co zrobiłeś? Jak sobie poradziłeś?)": {
                "slowa": ["uciekam", "unikam", "karetk", "sor", "lekarz", "tablet", "muszę usiąść", "woda"],
                "tlumaczenie": "Ucieczka, unikanie bodźców. Stosowanie zachowań zabezpieczających, co w konsekwencji podtrzymuje wiarę w objaw."
            }
        },
        "cele_smart": "1. Zmniejszenie częstotliwości napadów paniki do 0/miesiąc.\n2. Eliminacja min. 2 zachowań zabezpieczających.",
        "protokol_nazwa": "Terapia Lęku Panicznego wg D. Clarka",
        "uzasadnienie_planu": "Reatrybucja doznań fizjologicznych, odrzucenie zachowań zabezpieczających."
    }
]

# --- PEŁNA BAZA ICD-10 ---
icd10_full = {
    "F00-F09 Zab. psychiczne organiczne": ["F00 Otępienie w ch. Alzheimera", "F01 Otępienie naczyniowe", "F06 Inne zab. wskutek uszkodzenia mózgu", "F07 Zaburzenia osobowości wskutek choroby mózgu"],
    "F10-F19 Zab. spowodowane substancjami": ["F10 Zab. spowodowane alkoholem", "F11 Zab. spowodowane opioidami", "F12 Zab. spowodowane kanabinoidami", "F13 Leki uspokajające i nasenne", "F17 Palenie tytoniu"],
    "F20-F29 Schizofrenia i urojeniowe": ["F20 Schizofrenia", "F21 Zaburzenie schizotypowe", "F22 Uporczywe zaburzenia urojeniowe", "F23 Ostre zaburzenia psychotyczne", "F25 Zaburzenia schizoafektywne"],
    "F30-F39 Zaburzenia nastroju (afektywne)": ["F30 Epizod maniakalny", "F31 ChAD", "F32 Epizod depresyjny", "F33 Zaburzenia depresyjne nawracające", "F34 Uporczywe zaburzenia nastroju (Dystymia)"],
    "F40-F48 Zaburzenia nerwicowe i lękowe": ["F40.0 Agorafobia", "F40.1 Fobie społeczne", "F40.2 Specyficzne fobie", "F41.0 Zaburzenie lękowe z napadami lęku", "F41.1 Zaburzenie lękowe uogólnione (GAD)", "F41.2 Zab. lękowo-depresyjne mieszane", "F42 Zaburzenie obsesyjno-kompulsyjne (OCD)", "F43.0 Ostra reakcja na stres", "F43.1 Zaburzenie stresowe pourazowe (PTSD)", "F43.2 Zaburzenia adaptacyjne", "F44 Zaburzenia dysocjacyjne", "F45 Zaburzenia pod postacią somatyczną (np. Hipochondria)"],
    "F50-F59 Zespoły behawioralne": ["F50.0 Jadłowstręt psychiczny (Anoreksja)", "F50.2 Żarłoczność psychiczna (Bulimia)", "F51 Nieorganiczne zaburzenia snu", "F52 Dysfunkcje seksualne"],
    "F60-F69 Zaburzenia osobowości": ["F60.0 Osobowość paranoiczna", "F60.1 Osobowość schizoidalna", "F60.2 Osobowość dyssocjalna", "F60.30 Os. chwiejna emocjonalnie typ impulsywny", "F60.31 Os. chwiejna emocjonalnie typ borderline", "F60.4 Os. histrioniczna", "F60.5 Os. anankastyczna (OCPD)", "F60.6 Os. lękliwa (unikająca)", "F60.7 Os. zależna", "F61 Mieszane zab. osobowości"],
    "F90-F98 Zaburzenia wieku dziecięcego": ["F90 Zaburzenia hiperkinetyczne (ADHD)", "F91 Zaburzenia zachowania", "F95 Tiki"]
}

# --- STANY APLIKACJI W PAMIĘCI ---
if 'baza_terapii' not in st.session_state: st.session_state.baza_terapii = []
if 'ui_problemy' not in st.session_state: st.session_state.ui_problemy = ""
if 'ui_cele' not in st.session_state: st.session_state.ui_cele = ""
if 'ui_protokol' not in st.session_state: st.session_state.ui_protokol = ""
if 'ui_uzasadnienie' not in st.session_state: st.session_state.ui_uzasadnienie = ""

def sync_problemy(): st.session_state.lista_problemow = st.session_state.ui_problemy
def sync_cele(): st.session_state.cele_terapii = st.session_state.ui_cele
def sync_protokol(): st.session_state.wybrany_protokol = st.session_state.ui_protokol
def sync_uzasadnienie(): st.session_state.uzasadnienie_planu = st.session_state.ui_uzasadnienie

# --- MENU BOCZNE ---
st.sidebar.title("🛡️ Zapis Terapii CBT")
menu = st.sidebar.radio("Spis treści:", [
    "I. Diagnoza i Konceptualizacja", 
    "II. Plan i Interwencje", 
    "III. Podsumowanie",
    "📂 Archiwum Diagnoz"
])
st.sidebar.divider()

# ==========================================================
# MODUŁ I: DIAGNOZA I KONCEPTUALIZACJA
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

    with st.expander("🤖 Asystent Diagnozy (Wg Arkusza Psychology Tools)", expanded=True):
        objawy_input = st.text_area("Wpisz swobodną skargę pacjenta:")
        
        if st.button("🔍 Analizuj wypowiedź"):
            if objawy_input:
                input_do_analizy = objawy_input.lower()
                slowa_z_tekstu = re.findall(r'\b\w+\b', input_do_analizy)
                
                najlepsze_dopasowanie = None
                najwyzszy_wynik = 0
                wygenerowana_lista_problemow = ""
                
                for choroba in baza_symptomow:
                    wynik_choroby = 0
                    tymczasowa_lista = f"WSTĘPNA ANALIZA ({choroba['diagnoza']}):\n"
                    
                    for sfera, dane_sfery in choroba["profil_cbt"].items():
                        znalezione_pelne_slowa = []
                        for rdzen in dane_sfery["slowa"]:
                            for slowo_pacjenta in slowa_z_tekstu:
                                if rdzen in slowo_pacjenta and slowo_pacjenta not in znalezione_pelne_slowa:
                                    znalezione_pelne_slowa.append(slowo_pacjenta)
                        
                        if znalezione_pelne_slowa:
                            wynik_choroby += len(znalezione_pelne_slowa)
                            tymczasowa_lista += f"\n📌 {sfera}:\n- Język pacjenta: '{', '.join(znalezione_pelne_slowa)}'\n- Znaczenie kliniczne: {dane_sfery['tlumaczenie']}\n"
                    
                    if wynik_choroby > najwyzszy_wynik:
                        najwyzszy_wynik = wynik_choroby
                        najlepsze_dopasowanie = choroba
                        wygenerowana_lista_problemow = tymczasowa_lista

                if najlepsze_dopasowanie:
                    st.success(f"🎯 Rozpoznano wzorzec: {najlepsze_dopasowanie['diagnoza']}")
                    st.warning(f"⚖️ Diagnoza różnicowa: {najlepsze_dopasowanie['roznicowa']}")
                    st.session_state.ui_problemy = wygenerowana_lista_problemow
                    st.session_state.ui_cele = najlepsze_dopasowanie['cele_smart']
                    st.session_state.ui_protokol = najlepsze_dopasowanie['protokol_nazwa']
                    st.session_state.ui_uzasadnienie = najlepsze_dopasowanie['uzasadnienie_planu']
                else:
                    st.info("Za mało danych. Wpisz więcej szczegółów zgłaszanych przez pacjenta.")
            else:
                st.warning("Najpierw wpisz wypowiedź pacjenta!")

    c1, c2 = st.columns(2)
    kat_wybrana = c1.selectbox("Grupa ICD-10:", list(icd10_full.keys()))
    pelna_diagnoza = c2.selectbox("Rozpoznanie główne:", icd10_full[kat_wybrana])
    kod_icd = pelna_diagnoza.split(" ")[0]
    inne_rozpoznania = st.text_input("Inne rozpoznania (np. somatyczne, współwystępujące):")

    st.divider()
    st.header(f"🧩 Modele CBT: {pelna_diagnoza}")
    if kod_icd in slownik_modeli:
        for dane in slownik_modeli[kod_icd]:
            st.markdown(f"### 🛠️ {dane['Model']}")
            st.write(f"**Mechanizm:** {dane['Opis']}")
            st.write(f"**Interwencje:** {dane['Interwencje']}")
            if "Wizualizacja" in dane:
                with st.expander(f"ZOBACZ SCHEMAT: {dane['Model']}"):
                    st.markdown(f"```mermaid\n{dane['Wizualizacja']}\n```")
    else:
        st.info("Brak szczegółowego modelu CBT w bazie dla wybranego rozpoznania.")

    st.divider()
    st.header("I.3. Konceptualizacja problemu")
    
    st.subheader("I.3.1. Lista problemów i cele terapii")
    st.text_area("Pogrupowana Lista Problemów (wg arkusza)", key="ui_problemy", on_change=sync_problemy, height=450)
    st.text_area("Cele terapii (SMART)", key="ui_cele", on_change=sync_cele, height=150)

    st.subheader("I.3.2. Poziom pierwszy (Sytuacja bieżąca - przekrój poprzeczny)")
    st.text_area("Sytuacja (typowa sytuacja ilustrująca problem)")
    c3, c4 = st.columns(2)
    with c3:
        st.text_area("Myśli automatyczne / Obrazy")
        st.text_area("Emocje (rodzaj i nasilenie)")
    with c4:
        st.text_area("Doznania z ciała (fizjologiczne)")
        st.text_area("Zachowanie (w tym zabezpieczające/unikające)")

    st.subheader("I.3.3. Poziom drugi (Mechanizmy podtrzymujące i Przekonania)")
    st.text_area("Przekonania kluczowe (o sobie, innych, świecie)")
    st.text_area("Przekonania warunkowe (Założenia / Zasady / Postawy)")
    st.text_area("Strategie radzenia sobie (kompensacyjne)")

    st.subheader("I.3.4. Historia uczenia się (Profil rozwojowy)")
    st.text_area("Wydarzenia z przeszłości i wczesne doświadczenia")
    st.text_area("Zdarzenia wyzwalające (Czynniki spustowe)")

    st.divider()
    st.header("I.4. Zasoby pacjenta")
    st.text_area("Mocne strony, wsparcie społeczne, umiejętności, inteligencja, motywacja itp.")

    if st.button("💾 Zapisz Diagnozę do Archiwum"):
        st.session_state.baza_terapii.append({"Pacjent": imie, "Wiek": wiek, "Kod ICD": kod_icd, "Diagnoza": pelna_diagnoza})
        st.success("Zapisano!")

# ==========================================================
# MODUŁ II: PLAN TERAPII I INTERWENCJE
# ==========================================================
elif menu == "II. Plan i Interwencje":
    st.title("II. Plan terapii i interwencje")
    st.header("II.1. Plan terapii (Uzasadnienie EBM)")
    st.text_input("Protokół (EBM):", key="ui_protokol", on_change=sync_protokol)
    st.text_area("Uzasadnienie interwencji:", key="ui_uzasadnienie", on_change=sync_uzasadnienie, height=150)
    st.divider()
    st.header("II.2. Zapis przebiegu poszczególnych sesji")
    st.text_area("Rejestr sesji (np. Sesja 1 [Data] - Psychoedukacja i BA...)", height=300)

# ==========================================================
# MODUŁ III: PODSUMOWANIE
# ==========================================================
elif menu == "III. Podsumowanie":
    st.title("III. Podsumowanie i Ewaluacja")
    st.header("III.1. Osiągnięte cele terapii")
    col1, col2 = st.columns(2)
    with col1:
        st.text_area("Według pacjenta")
    with col2:
        st.text_area("Według terapeuty")
    st.header("III.2. Zidentyfikowane mechanizmy zmiany")
    st.text_area("Co dokładnie pomogło pacjentowi?")
    st.header("III.3. Zapobieganie nawrotom")
    st.text_area("Sygnały ostrzegawcze i plan radzenia sobie")
    st.header("III.4. Literatura")
    st.text_area("Materiały, protokoły wykorzystane do pracy")

# ==========================================================
# MODUŁ IV: ARCHIWUM
# ==========================================================
elif menu == "📂 Archiwum Diagnoz":
    st.title("Baza Terapii")
    if not st.session_state.baza_terapii:
        st.warning("Baza jest pusta. Dodaj pacjenta w zakładce I.")
    else:
        df = pd.DataFrame(st.session_state.baza_terapii)
        lista_diagnoz = ["Wszystkie"] + list(df['Kod ICD'].unique())
        wybrany_kod = st.selectbox("Filtruj bazę według diagnozy:", lista_diagnoz)
        if wybrany_kod != "Wszystkie":
            df = df[df['Kod ICD'] == wybrany_kod]
        st.dataframe(df, use_container_width=True)
