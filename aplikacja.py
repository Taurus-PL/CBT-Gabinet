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
            "Wizualizacja": "graph TD\nA[Wewnętrzny lub zewn. wyzwalacz] --> B[Postrzegane zagrożenie]\nB --> C[Lęk / Niepokój]\nC --> D[Doznania somatyczne np. serce]\nD --> E{Katastroficzna interpretacja}\nE -- Błędne koło paniki --> B\nstyle E fill:#4d0000,stroke:#ff3333,stroke-width:2px,color:#fff\n"
        }
    ],
    "F32": [
        {
            "Model": "Triada Poznawcza Depresji (A. Beck)",
            "Opis": "Negatywna wizja siebie, świata i przyszłości wynikająca z dysfunkcjonalnych schematów i błędów poznawczych.",
            "Interwencje": "Zapisywanie myśli (Tabela Becka), restrukturyzacja poznawcza, testowanie przekonań.",
            "Wizualizacja": "graph TD\nA((Negatywne myśli O SOBIE)) <--> B((Negatywne myśli O ŚWIECIE))\nB <--> C((Negatywne myśli O PRZYSZŁOŚCI))\nC <--> A\nstyle A fill:#002b5e,stroke:#3399ff,color:#fff\n"
        },
        {
            "Model": "Model Aktywacji Behawioralnej - BA (C. Martell)",
            "Opis": "Depresja jako wynik spadku wzmocnień pozytywnych ze środowiska.",
            "Interwencje": "Monitorowanie aktywności, planowanie aktywności (przyjemność i mistrzostwo).",
            "Wizualizacja": "graph TD\nA[Stresory / Spadek wzmocnień] --> B[Obniżony nastrój / Brak energii]\nB --> C[Wycofanie / Bierność / Ruminacje]\nC --> D[Jeszcze mniej wzmocnień i więcej problemów]\nD -- Błędne koło --> B\nstyle C fill:#333333,stroke:#666666,color:#fff\n"
        }
    ],
    "F50.2": [
        {
            "Model": "Transdiagnostyczny model zaburzeń odżywiania (C. Fairburn)",
            "Opis": "Rdzeniem zaburzenia jest nadmierne uzależnienie samooceny od wagi i sylwetki, co prowadzi do drastycznych restrykcji, napadów objadania się i zachowań kompensacyjnych.",
            "Interwencje": "Monitorowanie odżywiania, planowanie regularnych posiłków, restrukturyzacja przekonań o ciele i wadze.",
            "Wizualizacja": "graph TD\nA[Nadmierna koncentracja na sylwetce i wadze] --> B[Restrykcyjne zasady dietetyczne]\nB --> C[Złamanie zasad / Narastające napięcie]\nC --> D[Napad objadania się]\nD --> E[Zachowania kompensacyjne np. wymioty]\nD --> F[Poczucie winy i lęk przed tyciem]\nE --> F\nF -- Wzmacnia kontrolę --> A\nstyle A fill:#004d40,stroke:#00695c,color:#fff\n"
        }
    ]
}
slownik_modeli["F33"] = slownik_modeli["F32"]
slownik_modeli["F50.0"] = slownik_modeli["F50.2"]

# --- DOKŁADNE KRYTERIA ICD-10 + SŁOWNIKI ---
baza_symptomow = [
    {
        "diagnoza": "F50.2 Żarłoczność psychiczna (Bulimia)",
        "roznicowa": "Anoreksja (F50.0), BED, Depresja nietypowa.",
        "icd10_kryteria": {
            "Kryterium A: Epizody przejadania się": {
                "icd10": "Występują powtarzające się epizody przejadania się (spożywanie obiektywnie dużych ilości jedzenia w krótkim czasie).",
                "slowa": ["napad", "obżarst", "popłyn", "ciąg", "lodówk", "pochłan", "zjadł", "żar", "wyjad", "obżar"]
            },
            "Kryterium B: Przymus jedzenia": {
                "icd10": "Stałe zaabsorbowanie jedzeniem i silne pragnienie lub poczucie przymusu jedzenia (niemożność powstrzymania się).",
                "slowa": ["musz", "przymus", "głód", "ochot", "kontro", "obsesj"]
            },
            "Kryterium C: Zachowania kompensacyjne": {
                "icd10": "Pacjent usiłuje przeciwdziałać tuczącym skutkom pokarmów stosując co najmniej jedną z metod: prowokowanie wymiotów, nadużywanie leków przeczyszczających, głodówki, wyczerpujące ćwiczenia fizyczne.",
                "slowa": ["wymiot", "rzyg", "przeczyszcz", "senes", "ćwicz", "siłown", "głodów", "tablet", "kibel"]
            },
            "Kryterium D: Zniekształcona samoocena": {
                "icd10": "Chorobliwa obawa przed otyłością; pacjent określa nieprzekraczalne granice swojej masy ciała, a samoocena jest nadmiernie wyznaczana przez kształt i masę ciała.",
                "slowa": ["grub", "śmieć", "nienawidz", "brzydz", "wag", "lustr", "schudn", "diet", "wstyd", "wygląd"]
            }
        },
        "cele_smart": "1. Wprowadzenie regularnego planu posiłków (3 główne, 2 przekąski).\n2. Zmniejszenie częstotliwości napadów/wymiotów do 1/tydz.",
        "protokol_nazwa": "CBT-E wg C. Fairburna",
        "uzasadnienie_planu": "1) Psychoedukacja (błędne koło). 2) Dzienniczek myśli i reakcji. 3) Restrukturyzacja poznawcza i zmiana bazy samooceny.",
        "profil_cbt": {
            "SYTUACJA": {"slowa": ["wieczór", "samotn", "stres", "kłótni", "imprez", "restauracj", "sklep", "wadze", "lustrz"], "tlumaczenie": "Sytuacje napięcia emocjonalnego (stres, samotność) lub ekspozycja na bodźce (lustro, waga)."},
            "MYŚLI": {"slowa": ["grub", "śmieć", "nienawidz", "brzydz", "obsesj", "wag", "lustr", "schudn", "diet", "nigdy", "zawsze", "muszę", "nie dam rady"], "tlumaczenie": "Nadmierne uzależnienie samooceny od wagi/sylwetki, myślenie dychotomiczne ('wszystko albo nic')."},
            "EMOCJE": {"slowa": ["wstyd", "wyrzut", "win", "lęk", "boję", "stres", "napięc"], "tlumaczenie": "Głębokie poczucie winy, wstyd po napadzie, silny lęk przed przytyciem."},
            "CIAŁO": {"slowa": ["zmęcz", "słab", "mdł", "zimn", "brzuch", "gardł", "opuch"], "tlumaczenie": "Wyczerpanie fizyczne, uczucie przepełnienia, możliwe powikłania gastryczne."},
            "ZACHOWANIE": {"slowa": ["napad", "obżarst", "popłyn", "ciąg", "lodówk", "pochłan", "wymiot", "rzyg", "przeczyszcz", "senes", "ćwicz", "siłown", "głodów"], "tlumaczenie": "Napady objadania się (utrata kontroli), po których następują zachowania kompensacyjne."}
        }
    },
    {
        "diagnoza": "F32 Epizod depresyjny",
        "roznicowa": "ChAD, Dystymia, Niedoczynność tarczycy.",
        "icd10_kryteria": {
            "Kryterium Podstawowe 1: Obniżony nastrój": {
                "icd10": "Obniżony nastrój, utrzymujący się przez większą część dnia, niemal codziennie, niepodlegający wpływowi wydarzeń zewnętrznych.",
                "slowa": ["smut", "przygnęb", "płacz", "pust", "dół", "płaka", "źle"]
            },
            "Kryterium Podstawowe 2: Anhedonia": {
                "icd10": "Wyraźna utrata zainteresowań i zdolności odczuwania radości w stosunku do aktywności, które zwykle sprawiały przyjemność.",
                "slowa": ["bez sensu", "nic nie czuj", "nie chce mi", "wegetuj", "zaniedb", "obojętn", "nie cieszy"]
            },
            "Kryterium Podstawowe 3: Brak energii": {
                "icd10": "Zmniejszona energia, szybsze męczenie się i spadek aktywności. Wzmożona męczliwość po minimalnym wysiłku.",
                "slowa": ["zmęcz", "brak sił", "ociężał", "słab", "wyczerp", "leżę", "spać"]
            },
            "Kryterium Dodatkowe A: Zaburzenia poznawcze (Samoocena)": {
                "icd10": "Spadek zaufania do siebie oraz szacunku do siebie. Nieracjonalne poczucie winy i bezwartościowości.",
                "slowa": ["beznadziej", "nikim", "ciężar", "nie uda", "głup", "win", "przeze mnie"]
            },
            "Kryterium Dodatkowe B: Objawy somatyczne (Sen)": {
                "icd10": "Zaburzenia snu wszelkiego typu (najczęściej wczesne wybudzanie).",
                "slowa": ["spać", "sen", "budz", "bezsenn"]
            }
        },
        "cele_smart": "1. Zwiększenie aktywności celowej (min. 3x w tyg).\n2. Zapisywanie myśli w arkuszu samooceny (Tabela Becka).",
        "protokol_nazwa": "Aktywacja Behawioralna / Terapia Poznawcza Depresji",
        "uzasadnienie_planu": "Monitorowanie aktywności i nastroju, planowanie dnia (mistrzostwo i przyjemność), testowanie myśli automatycznych.",
        "profil_cbt": {
            "SYTUACJA": {"slowa": ["rano", "wsta", "prac", "obowiąz", "ludz", "problem", "poranek"], "tlumaczenie": "Konieczność podjęcia aktywności, wyzwania dnia codziennego."},
            "MYŚLI": {"slowa": ["beznadziej", "bez sensu", "nikim", "ciężar", "nie uda", "głup", "win", "czarn", "nigdy", "zawsze"], "tlumaczenie": "Negatywna triada Becka, generalizacja, katastrofizacja."},
            "EMOCJE": {"slowa": ["smut", "przygnęb", "płacz", "pust", "nic nie czuj", "znieczul", "płaka"], "tlumaczenie": "Obniżony nastrój, anhedonia, apatia, znieczulenie emocjonalne."},
            "CIAŁO": {"slowa": ["spać", "zmęcz", "brak sił", "budzę się", "apetyt", "ociężał"], "tlumaczenie": "Spadek energii, zaburzenia snu i apetytu, spowolnienie psychoruchowe."},
            "ZACHOWANIE": {"slowa": ["nie chce mi się", "leżę", "wegetuj", "izoluj", "nie wychodz", "zamkn", "zaniedb"], "tlumaczenie": "Wycofanie z relacji społecznych, bierność behawioralna, pogłębienie izolacji."}
        }
    },
    {
        "diagnoza": "F41.0 Lęk paniczny",
        "roznicowa": "Agorafobia, Zaburzenia kardiologiczne.",
        "icd10_kryteria": {
            "Kryterium A: Nawracające napady paniki": {
                "icd10": "Nawracające napady ciężkiego lęku (paniki), które nie są ograniczone do żadnej szczególnej sytuacji, w związku z czym są nieprzewidywalne.",
                "slowa": ["panik", "przeraż", "strach", "nagle", "atak"]
            },
            "Kryterium B: Objawy wegetatywne": {
                "icd10": "Nagłe wystąpienie takich objawów jak: palpitacje serca, bóle w klatce piersiowej, uczucie duszności, zawroty głowy, pocenie się.",
                "slowa": ["serce", "wali", "tchu", "duszno", "kłuci", "drż", "pocę", "miękną"]
            },
            "Kryterium C: Wtórne objawy poznawcze/behawioralne": {
                "icd10": "Wtórny lęk przed śmiercią, utratą kontroli nad sobą lub zwariowaniem oraz unikanie sytuacji (zachowania zabezpieczające).",
                "slowa": ["umrę", "uduszę", "zawał", "zwariuję", "kontrol", "zemdlej", "uciekam", "unikam", "karetk", "sor"]
            }
        },
        "cele_smart": "1. Zmniejszenie częstotliwości napadów paniki do 0 w skali miesiąca.\n2. Rozpoznanie i eliminacja min. 2 głównych zachowań zabezpieczających.",
        "protokol_nazwa": "Terapia Lęku Panicznego wg D. Clarka",
        "uzasadnienie_planu": "Reatrybucja doznań fizjologicznych (eksperymenty behawioralne np. hiperwentylacja), odrzucenie zachowań zabezpieczających.",
        "profil_cbt": {
            "SYTUACJA": {"slowa": ["tłum", "sklep", "kolejk", "autobus", "kawi", "wysił", "zadu", "samochód"], "tlumaczenie": "Miejsca zatłoczone, zamknięte przestrzenie, wysiłek fizyczny."},
            "MYŚLI": {"slowa": ["umrę", "uduszę", "zawał", "zwariuję", "tracę kontrol", "zemdlej", "to koniec"], "tlumaczenie": "Katastroficzna interpretacja normalnych doznań płynących z ciała."},
            "EMOCJE": {"slowa": ["panik", "przeraż", "strach", "lęk"], "tlumaczenie": "Nagły, nieprzewidywalny silny lęk, przerażenie."},
            "CIAŁO": {"slowa": ["serce", "wali", "brakuje mi tchu", "duszno", "kłuci", "drż", "pocę", "miękną nogi"], "tlumaczenie": "Silne pobudzenie wegetatywne (tachykardia, duszności, zawroty głowy)."},
            "ZACHOWANIE": {"slowa": ["uciekam", "unikam", "karetk", "sor", "lekarz", "tablet", "muszę usiąść", "woda"], "tlumaczenie": "Ucieczka z sytuacji, unikanie bodźców interoceptywnych, stosowanie zachowań zabezpieczających."}
        }
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
if 'ui_problemy_html' not in st.session_state: st.session_state.ui_problemy_html = ""
if 'ui_cele' not in st.session_state: st.session_state.ui_cele = ""
if 'ui_protokol' not in st.session_state: st.session_state.ui_protokol = ""
if 'ui_uzasadnienie' not in st.session_state: st.session_state.ui_uzasadnienie = ""

# ZMIENNE DLA SEKCJI I.3.2
for key in ['ui_sytuacja', 'ui_mysli', 'ui_emocje', 'ui_cialo', 'ui_zachowanie']:
    if key not in st.session_state: st.session_state[key] = ""

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

    with st.expander("🤖 Asystent Diagnozy (Tłumacz na Kryteria ICD-10)", expanded=True):
        st.write("Wpisz swobodną wypowiedź. Algorytm pociąnie ją na zdania i dopasuje jako 'materiał dowodowy' do urzędowych kryteriów ICD-10.")
        objawy_input = st.text_area("Cytaty pacjenta / Skarga główna:")
        
        if st.button("🔍 Przetłumacz na kryteria kliniczne"):
            if objawy_input:
                input_lower = objawy_input.lower()
                
                # Ulepszony podział na pełne zdania, by wyciągać kontekst pacjenta
                zdania_pacjenta = [z.strip() + "." for z in re.split(r'[.!?\n]+', objawy_input) if len(z.strip()) > 2]
                
                najlepsze_dopasowanie = None
                najwyzszy_wynik = 0
                najlepszy_html = ""
                
                temp_sytuacja, temp_mysli, temp_emocje, temp_cialo, temp_zachowanie = "", "", "", "", ""
                
                for choroba in baza_symptomow:
                    wynik_choroby = 0
                    
                    # --- 1. SPRAWDZANIE KRYTERIÓW ICD-10 ---
                    html_raport = "<h4 style='color: #2c3e50;'>Analiza kryteriów diagnostycznych (ICD-10):</h4>"
                    
                    for nazwa_kryterium, dane_kryterium in choroba["icd10_kryteria"].items():
                        znalezione_dowody = [] 
                        
                        for rdzen in dane_kryterium["slowa"]:
                            for zdanie in zdania_pacjenta:
                                if rdzen.lower() in zdanie.lower() and zdanie not in znalezione_dowody:
                                    znalezione_dowody.append(zdanie)
                        
                        if znalezione_dowody:
                            wynik_choroby += len(znalezione_dowody) * 2 # Punktujemy mocniej pełne kryteria
                            dowody_html = "<br>".join([f"👉 <i>„{d}”</i>" for d in znalezione_dowody])
                            
                            html_raport += f"""
                            <div style='border-left: 5px solid #28a745; padding: 12px; background-color: #f0fdf4; margin-bottom: 15px; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);'>
                                <h5 style='color: #155724; margin-top: 0;'>✅ SPEŁNIONE: {nazwa_kryterium}</h5>
                                <p style='font-size: 0.9em; color: #333; margin-bottom: 8px;'><b>Definicja ICD-10:</b> {dane_kryterium['icd10']}</p>
                                <div style='padding: 8px; background-color: #d1e7dd; border-radius: 4px; color: #0f5132;'>
                                    <b>Materiał dowodowy z wywiadu:</b><br>{dowody_html}
                                </div>
                            </div>
                            """
                        else:
                            html_raport += f"""
                            <div style='border-left: 5px solid #dc3545; padding: 12px; background-color: #fdf2f2; margin-bottom: 15px; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);'>
                                <h5 style='color: #721c24; margin-top: 0;'>❌ BRAK DANYCH: {nazwa_kryterium}</h5>
                                <p style='font-size: 0.9em; color: #333; margin-bottom: 8px;'><b>Definicja ICD-10:</b> {dane_kryterium['icd10']}</p>
                                <div style='padding: 8px; background-color: #f8d7da; border-radius: 4px; color: #842029;'>
                                    <i>Kryterium nieobecne w skardze. Wymaga dopytania podczas wywiadu (badanie różnicowe).</i>
                                </div>
                            </div>
                            """

                    # --- 2. WYPEŁNIANIE MODELU CBT (Słowa do I.3.2) ---
                    slowa_z_tekstu = re.findall(r'\b\w+\b', input_lower)
                    for sfera, dane_sfery in choroba["profil_cbt"].items():
                        znalezione_slowa = []
                        for rdzen in dane_sfery["slowa"]:
                            for s in slowa_z_tekstu:
                                if rdzen in s and s not in znalezione_slowa: znalezione_slowa.append(s)
                        if znalezione_slowa:
                            format_tekstu = f"Wykryto słowa: {', '.join(znalezione_slowa)}\n[Znaczenie CBT: {dane_sfery['tlumaczenie']}]"
                            if sfera == "SYTUACJA": temp_sytuacja = format_tekstu
                            elif sfera == "MYŚLI": temp_mysli = format_tekstu
                            elif sfera == "EMOCJE": temp_emocje = format_tekstu
                            elif sfera == "CIAŁO": temp_cialo = format_tekstu
                            elif sfera == "ZACHOWANIE": temp_zachowanie = format_tekstu
                            wynik_choroby += 1

                    if wynik_choroby > najwyzszy_wynik:
                        najwyzszy_wynik = wynik_choroby
                        najlepsze_dopasowanie = choroba
                        najlepszy_html = html_raport

                # --- ZAPIS STANÓW ---
                if najlepsze_dopasowanie:
                    st.success(f"🎯 Zidentyfikowano ścieżkę kliniczną: {najlepsze_dopasowanie['diagnoza']}")
                    st.warning(f"⚖️ Diagnoza różnicowa (do wykluczenia): {najlepsze_dopasowanie['roznicowa']}")
                    st.session_state.ui_problemy_html = najlepszy_html
                    st.session_state.ui_cele = najlepsze_dopasowanie['cele_smart']
                    st.session_state.ui_protokol = najlepsze_dopasowanie['protokol_nazwa']
                    st.session_state.ui_uzasadnienie = najlepsze_dopasowanie['uzasadnienie_planu']
                    
                    st.session_state.ui_sytuacja = temp_sytuacja if temp_sytuacja else "Brak wyraźnego wyzwalacza."
                    st.session_state.ui_mysli = temp_mysli if temp_mysli else "Brak zidentyfikowanych myśli automatycznych."
                    st.session_state.ui_emocje = temp_emocje if temp_emocje else "Brak zidentyfikowanych emocji."
                    st.session_state.ui_cialo = temp_cialo if temp_cialo else "Brak zidentyfikowanych doznań somatycznych."
                    st.session_state.ui_zachowanie = temp_zachowanie if temp_zachowanie else "Brak zidentyfikowanych zachowań."
                else:
                    st.info("Brak wystarczających danych diagnostycznych.")
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

    st.divider()
    st.header("I.3. Konceptualizacja problemu")
    
    st.subheader("I.3.1. Raport diagnostyczny (Kryteria ICD-10)")
    
    # Renderowanie pięknego HTML-a z listą problemów
    if st.session_state.ui_problemy_html:
        st.markdown(st.session_state.ui_problemy_html, unsafe_allow_html=True)
    else:
        st.text_area("Lista problemów (Czeka na analizę...)", disabled=True)

    st.text_area("Cele terapii (SMART)", key="ui_cele", on_change=sync_cele, height=100)

    st.subheader("I.3.2. Poziom pierwszy (Sytuacja bieżąca - przekrój poprzeczny)")
    
    st.text_area("Sytuacja (Wyzwalacz)", key="ui_sytuacja")
    c3, c4 = st.columns(2)
    with c3:
        st.text_area("Myśli automatyczne / Obrazy", key="ui_mysli")
        st.text_area("Emocje", key="ui_emocje")
    with c4:
        st.text_area("Ciało (Objawy fizjologiczne)", key="ui_cialo")
        st.text_area("Zachowanie", key="ui_zachowanie")

    st.subheader("I.3.3. Poziom drugi (Mechanizmy podtrzymujące i Przekonania)")
    st.text_area("Przekonania kluczowe (o sobie, innych, świecie)")
    st.text_area("Przekonania warunkowe (Założenia / Zasady / Postawy)")
    st.text_area("Strategie radzenia sobie (kompensacyjne)")

    st.subheader("I.3.4. Historia uczenia się (Profil rozwojowy)")
    st.text_area("Wydarzenia z przeszłości i wczesne doświadczenia")
    st.text_area("Zdarzenia wyzwalające (Czynniki spustowe)")

    st.divider()
    st.header("I.4. Zasoby pacjenta")
    st.text_area("Mocne strony, wsparcie społeczne, umiejętności itp.")

    if st.button("💾 Zapisz Diagnozę do Archiwum"):
        st.session_state.baza_terapii.append({"Pacjent": imie, "Wiek": wiek, "Kod ICD": kod_icd, "Diagnoza": pelna_diagnoza})
        st.success("Zapisano do bazy!")

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
    with col1: st.text_area("Według pacjenta")
    with col2: st.text_area("Według terapeuty")
    st.header("III.2. Zidentyfikowane mechanizmy zmiany")
    st.text_area("Co dokładnie pomogło pacjentowi?")
    st.header("III.3. Zapobieganie nawrotom")
    st.text_area("Sygnały ostrzegawcze i plan radzenia sobie")
    st.header("III.4. Literatura")
    st.text_area("Materiały, protokoły wykorzystane do pracy")

# ==========================================================
# MODUŁ IV: ARCHIWUM DIAGNOZ
# ==========================================================
elif menu == "📂 Archiwum Diagnoz":
    st.title("Baza Terapii")
    if not st.session_state.baza_terapii:
        st.warning("Baza jest pusta. Dodaj pacjenta w zakładce I.")
    else:
        df = pd.DataFrame(st.session_state.baza_terapii)
        st.dataframe(df, use_container_width=True)
