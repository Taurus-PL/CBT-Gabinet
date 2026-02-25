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
            "Opis": "Skupienie na błędnej, katastroficznej interpretacji normalnych doznań z ciała.",
            "Interwencje": "Reatrybucja doznań, eksperymenty, eliminacja zachowań zabezpieczających."
        }
    ],
    "F32": [
        {
            "Model": "Triada Poznawcza Depresji (A. Beck)",
            "Opis": "Negatywna wizja siebie, świata i przyszłości.",
            "Interwencje": "Zapisywanie myśli (Tabela Becka), restrukturyzacja, testowanie przekonań."
        }
    ],
    "F50.2": [
        {
            "Model": "Transdiagnostyczny model zaburzeń odżywiania (C. Fairburn)",
            "Opis": "Uzależnienie samooceny od wagi i sylwetki, prowadzące do restrykcji, napadów i kompensacji.",
            "Interwencje": "Monitorowanie odżywiania, planowanie posiłków, restrukturyzacja przekonań."
        }
    ]
}
slownik_modeli["F33"] = slownik_modeli["F32"]
slownik_modeli["F50.0"] = slownik_modeli["F50.2"]

# --- NOWA BAZA ASYSTENTA DIAGNOZY (MODEL CBT + SYTUACJA) ---
baza_symptomow = [
    {
        "diagnoza": "F50.2 Żarłoczność psychiczna (Bulimia)",
        "roznicowa": "Anoreksja (F50.0), BED, Depresja.",
        "profil_cbt": {
            "SYTUACJA (Wyzwalacz)": {
                "slowa": ["wieczór", "samotn", "stres", "kłótni", "imprez", "restauracj", "sklep", "wadze", "lustrz"],
                "tlumaczenie": "Sytuacje napięcia emocjonalnego (stres, samotność) lub ekspozycja na bodźce związane z jedzeniem/sylwetką."
            },
            "MYŚLI (Sfera poznawcza)": {
                "slowa": ["grub", "śmieć", "nienawidz", "brzydz", "obsesj", "wag", "lustr", "schudn", "diet"],
                "tlumaczenie": "Nadmierne uzależnienie samooceny od wagi/sylwetki, myślenie dychotomiczne ('wszystko albo nic'), silna samokrytyka."
            },
            "EMOCJE (Sfera emocjonalna)": {
                "slowa": ["wstyd", "wyrzut", "win", "lęk", "boję", "stres", "napięc"],
                "tlumaczenie": "Głębokie poczucie winy, wstyd po napadzie objadania, lęk przed przytyciem."
            },
            "CIAŁO (Sfera fizjologiczna)": {
                "slowa": ["zmęcz", "słab", "mdł", "zimn", "brzuch", "gardł", "opuch"],
                "tlumaczenie": "Wyczerpanie, objawy ze strony układu pokarmowego, ryzyko zaburzeń elektrolitowych."
            },
            "ZACHOWANIE (Sfera behawioralna)": {
                "slowa": ["napad", "obżarst", "popłyn", "ciąg", "lodówk", "pochłan", "wymiot", "rzyg", "przeczyszcz", "senes", "ćwicz", "siłown", "głodów"],
                "tlumaczenie": "Napady objadania się (utrata kontroli), restrykcje, zachowania kompensacyjne (wymioty, przeczyszczanie, treningi)."
            }
        },
        "cele_smart": "1. Wprowadzenie regularnego planu posiłków (3 główne, 2 przekąski).\n2. Zmniejszenie częstotliwości napadów/wymiotów do 1/tydz.",
        "protokol_nazwa": "Transdiagnostyczna Terapia CBT Zaburzeń Odżywiania (CBT-E) wg C. Fairburna",
        "uzasadnienie_planu": "1) Psychoedukacja (błędne koło: restrykcje -> głód -> napad -> wymioty).\n2) Bieżące monitorowanie (dzienniczek pacjenta).\n3) Restrukturyzacja poznawcza i poszerzenie bazy samooceny."
    },
    {
        "diagnoza": "F32 Epizod depresyjny",
        "roznicowa": "ChAD, Dystymia, Niedoczynność tarczycy.",
        "profil_cbt": {
            "SYTUACJA (Wyzwalacz)": {
                "slowa": ["rano", "wsta", "prac", "obowiąz", "ludz", "problem", "poranek"],
                "tlumaczenie": "Konieczność podjęcia aktywności, przebudzenie (często gorsze samopoczucie rano), sytuacje wymagające interakcji."
            },
            "MYŚLI (Sfera poznawcza)": {
                "slowa": ["beznadziej", "bez sensu", "nikim", "ciężar", "nie uda", "głup", "win", "czarn"],
                "tlumaczenie": "Negatywna triada Becka (negatywne myśli o sobie, świecie i przyszłości), generalizacja, katastrofizacja."
            },
            "EMOCJE (Sfera emocjonalna)": {
                "slowa": ["smut", "przygnęb", "płacz", "pust", "nic nie czuj", "znieczul"],
                "tlumaczenie": "Obniżony nastrój, anhedonia (brak odczuwania przyjemności), apatia."
            },
            "CIAŁO (Sfera fizjologiczna)": {
                "slowa": ["spać", "zmęcz", "brak sił", "budzę się", "apetyt", "ociężał"],
                "tlumaczenie": "Spadek energii, zaburzenia snu (częste wybudzanie, bezsenność lub hipersomnia), zmiana apetytu."
            },
            "ZACHOWANIE (Sfera behawioralna)": {
                "slowa": ["nie chce mi się", "leżę", "wegetuj", "izoluj", "nie wychodz", "zamkn", "zaniedb"],
                "tlumaczenie": "Wycofanie z relacji społecznych, bierność, spadek wzmocnień pozytywnych ze środowiska."
            }
        },
        "cele_smart": "1. Zwiększenie aktywności celowej i sprawiającej przyjemność do min. 3 razy w tyg.\n2. Zapisywanie min. 2 myśli dziennie w Tabeli Becka.",
        "protokol_nazwa": "Aktywacja Behawioralna (BA) / Terapia Poznawcza Depresji",
        "uzasadnienie_planu": "1) Monitorowanie aktywności.\n2) Planowanie aktywności (przyjemność i mistrzostwo).\n3) Restrukturyzacja poznawcza."
    },
    {
        "diagnoza": "F41.0 Lęk paniczny",
        "roznicowa": "Agorafobia, Zaburzenia kardiologiczne.",
        "profil_cbt": {
            "SYTUACJA (Wyzwalacz)": {
                "slowa": ["tłum", "sklep", "kolejk", "autobus", "kawi", "wysił", "zadu", "samochód"],
                "tlumaczenie": "Miejsca zatłoczone, zamknięte przestrzenie, wysiłek fizyczny lub sytuacje przypominające poprzednie napady."
            },
            "MYŚLI (Sfera poznawcza)": {
                "slowa": ["umrę", "uduszę", "zawał", "zwariuję", "tracę kontrol", "zemdlej", "to koniec"],
                "tlumaczenie": "Katastroficzna interpretacja normalnych doznań płynących z ciała (np. szybkie bicie serca = zawał)."
            },
            "EMOCJE (Sfera emocjonalna)": {
                "slowa": ["panik", "przeraż", "strach", "nagle mnie łapie"],
                "tlumaczenie": "Nagłe, nieprzewidywalne napady silnego lęku/paniki."
            },
            "CIAŁO (Sfera fizjologiczna)": {
                "slowa": ["serce", "wali", "brakuje mi tchu", "duszno", "kłuci", "drż", "pocę", "miękną nogi"],
                "tlumaczenie": "Silne pobudzenie wegetatywne (tachykardia, hiperwentylacja, zawroty głowy)."
            },
            "ZACHOWANIE (Sfera behawioralna)": {
                "slowa": ["uciekam", "unikam", "karetk", "sor", "lekarz", "tablet", "muszę usiąść", "woda"],
                "tlumaczenie": "Ucieczka z sytuacji, unikanie bodźców interoceptywnych, zachowania zabezpieczające (np. noszenie leków, dzwonienie na pogotowie)."
            }
        },
        "cele_smart": "1. Zmniejszenie częstotliwości napadów paniki do 0/miesiąc.\n2. Identyfikacja i eliminacja min. 2 zachowań zabezpieczających.",
        "protokol_nazwa": "Terapia Poznawcza Lęku Panicznego wg D. Clarka",
        "uzasadnienie_planu": "1) Reatrybucja poznawcza doznań z ciała.\n2) Eksperymenty behawioralne (np. hiperwentylacja).\n3) Odrzucenie zachowań zabezpieczających."
    }
]

# --- PEŁNA BAZA ICD-10 ---
icd10_full = {
    "F30-F39 Zaburzenia nastroju": ["F32 Epizod depresyjny", "F33 Zaburzenia depresyjne nawracające", "F31 ChAD"],
    "F40-F48 Zaburzenia lękowe": ["F41.0 Lęk paniczny", "F40.1 Fobia społeczna", "F41.1 GAD", "F42 OCD", "F43.1 PTSD"],
    "F50-F59 Zespoły behawioralne": ["F50.0 Anoreksja", "F50.2 Bulimia", "F51 Bezsenność"]
}

# --- BAZA DANYCH W PAMIĘCI ---
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
menu = st.sidebar.radio("Spis treści:", ["I. Diagnoza i Konceptualizacja", "II. Plan i Interwencje", "III. Podsumowanie"])
st.sidebar.divider()

# ==========================================================
# MODUŁ I: DIAGNOZA I KONCEPTUALIZACJA ZJAWISKA
# ==========================================================
if menu == "I. Diagnoza i Konceptualizacja":
    st.title("I. Diagnoza i konceptualizacja zjawiska")
    
    with st.expander("🤖 Asystent Diagnozy CBT (Model 5 Elementów)", expanded=True):
        st.write("Wpisz swobodną wypowiedź pacjenta. Algorytm wychwyci słowa-klucze, przetłumaczy je na język poznawczo-behawioralny i stworzy listę problemów.")
        objawy_input = st.text_area("Cytaty pacjenta / Skarga główna:")
        
        if st.button("🔍 Analizuj i przygotuj konceptualizację CBT"):
            if objawy_input:
                input_do_analizy = objawy_input.lower()
                # Wyciągamy listę wszystkich pełnych słów pacjenta (bez kropek i przecinków)
                slowa_z_tekstu = re.findall(r'\b\w+\b', input_do_analizy)
                
                najlepsze_dopasowanie = None
                najwyzszy_wynik = 0
                wygenerowana_lista_problemow = ""
                
                # Algorytm sprawdzający model CBT dla każdej diagnozy
                for choroba in baza_symptomow:
                    wynik_choroby = 0
                    tymczasowa_lista = f"WSTĘPNA KONCEPTUALIZACJA ({choroba['diagnoza']}):\n"
                    
                    # Dzięki użyciu .items(), słowniki Pythona zachowają kolejność:
                    # 1. Sytuacja, 2. Myśli, 3. Emocje, 4. Ciało, 5. Zachowanie
                    for sfera, dane_sfery in choroba["profil_cbt"].items():
                        znalezione_pelne_slowa = []
                        # Szukamy, czy rdzenie ukrywają się w pełnych słowach pacjenta
                        for rdzen in dane_sfery["slowa"]:
                            for slowo_pacjenta in slowa_z_tekstu:
                                if rdzen in slowo_pacjenta and slowo_pacjenta not in znalezione_pelne_slowa:
                                    znalezione_pelne_slowa.append(slowo_pacjenta)
                        
                        if znalezione_pelne_slowa:
                            wynik_choroby += len(znalezione_pelne_slowa)
                            tymczasowa_lista += f"\n👉 {sfera}:\n- Język pacjenta: '{', '.join(znalezione_pelne_slowa)}'\n- Tłumaczenie CBT: {dane_sfery['tlumaczenie']}\n"
                    
                    if wynik_choroby > najwyzszy_wynik:
                        najwyzszy_wynik = wynik_choroby
                        najlepsze_dopasowanie = choroba
                        wygenerowana_lista_problemow = tymczasowa_lista

                if najlepsze_dopasowanie:
                    st.success(f"🎯 **Rozpoznano profil:** {najlepsze_dopasowanie['diagnoza']}")
                    st.warning(f"⚖️ **Diagnoza różnicowa:** {najlepsze_dopasowanie['roznicowa']}")
                    
                    st.session_state.ui_problemy = wygenerowana_lista_problemow
                    st.session_state.ui_cele = najlepsze_dopasowanie['cele_smart']
                    st.session_state.ui_protokol = najlepsze_dopasowanie['protokol_nazwa']
                    st.session_state.ui_uzasadnienie = najlepsze_dopasowanie['uzasadnienie_planu']
                else:
                    st.info("Brak wystarczających danych do stworzenia modelu. Wpisz więcej objawów.")
            else:
                st.warning("Wpisz najpierw to, co zgłasza pacjent!")

    c1, c2 = st.columns(2)
    kat_wybrana = c1.selectbox("Grupa ICD-10:", list(icd10_full.keys()))
    pelna_diagnoza = c2.selectbox("Rozpoznanie główne:", icd10_full[kat_wybrana])

    st.divider()
    st.header("I.3. Konceptualizacja problemu")
    
    st.text_area("Lista problemów (Tłumaczenie na model CBT)", key="ui_problemy", on_change=sync_problemy, height=350)
    st.text_area("Cele terapii (SMART)", key="ui_cele", on_change=sync_cele, height=150)
    
    if st.session_state.ui_protokol:
        st.success(f"📚 **Sugerowany protokół:** {st.session_state.ui_protokol}")

# ==========================================================
# MODUŁ II: PLAN TERAPII I INTERWENCJE
# ==========================================================
elif menu == "II. Plan i Interwencje":
    st.title("II. Plan terapii i interwencje")
    st.text_input("Protokół (EBM):", key="ui_protokol", on_change=sync_protokol)
    st.text_area("Uzasadnienie interwencji:", key="ui_uzasadnienie", on_change=sync_uzasadnienie, height=150)

# ==========================================================
# MODUŁ III: PODSUMOWANIE
# ==========================================================
elif menu == "III. Podsumowanie":
    st.title("III. Podsumowanie")
    st.write("Miejsce na notatki końcowe.")
