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
            "Interwencje": "Reatrybucja doznań, hiperwentylacja, eliminacja zachowań zabezpieczających.",
            "Wizualizacja": "graph TD\nA[Wewnętrzny wyzwalacz] --> B[Postrzegane zagrożenie]\nB --> C[Lęk / Niepokój]\nC --> D[Doznania somatyczne]\nD --> E{Katastroficzna interpretacja}\nE -- Błędne koło paniki --> B\nstyle E fill:#4d0000,stroke:#ff3333,stroke-width:2px,color:#fff\n"
        }
    ],
    "F32": [
        {
            "Model": "Triada Poznawcza Depresji (A. Beck)",
            "Opis": "Negatywna wizja siebie, świata i przyszłości.",
            "Interwencje": "Tabela Becka, restrukturyzacja poznawcza.",
            "Wizualizacja": "graph TD\nA((Myśli O SOBIE)) <--> B((Myśli O ŚWIECIE))\nB <--> C((Myśli O PRZYSZŁOŚCI))\nC <--> A\nstyle A fill:#002b5e,stroke:#3399ff,color:#fff\n"
        }
    ],
    "F50.2": [
        {
            "Model": "Transdiagnostyczny model zaburzeń odżywiania (C. Fairburn)",
            "Opis": "Nadmierne uzależnienie samooceny od wagi i sylwetki.",
            "Interwencje": "Monitorowanie odżywiania, planowanie posiłków.",
            "Wizualizacja": "graph TD\nA[Koncentracja na sylwetce i wadze] --> B[Restrykcje dietetyczne]\nB --> C[Złamanie zasad / Napięcie]\nC --> D[Napad objadania się]\nD --> E[Zachowania kompensacyjne]\nD --> F[Poczucie winy]\nE --> F\nF --> A\nstyle A fill:#004d40,stroke:#00695c,color:#fff\n"
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
                "icd10": "Stałe zaabsorbowanie jedzeniem i silne pragnienie lub poczucie przymusu jedzenia.",
                "slowa": ["musz", "przymus", "głód", "ochot", "kontro", "obsesj"]
            },
            "Kryterium C: Zachowania kompensacyjne": {
                "icd10": "Pacjent usiłuje przeciwdziałać tuczącym skutkom pokarmów przez wymioty, przeczyszczanie, głodówki, ćwiczenia.",
                "slowa": ["wymiot", "rzyg", "przeczyszcz", "senes", "ćwicz", "siłown", "głodów", "tablet", "kibel"]
            },
            "Kryterium D: Zniekształcona samoocena": {
                "icd10": "Chorobliwa obawa przed otyłością; samoocena nadmiernie wyznaczana przez kształt i masę ciała.",
                "slowa": ["grub", "śmieć", "nienawidz", "brzydz", "wag", "lustr", "schudn", "diet", "wstyd", "wygląd"]
            }
        },
        "cele_smart": "1. Wprowadzenie regularnego planu posiłków.\n2. Zmniejszenie częstotliwości napadów do 1/tydz.",
        "protokol_nazwa": "CBT-E wg C. Fairburna",
        "uzasadnienie_planu": "Psychoedukacja, Dzienniczek myśli i reakcji, Restrukturyzacja poznawcza.",
        "profil_cbt": {
            "SYTUACJA": {"slowa": ["wieczór", "samotn", "stres", "kłótni", "imprez", "lustrz"], "tlumaczenie": "Napięcie emocjonalne, ekspozycja na bodźce (lustro, waga)."},
            "MYŚLI": {"slowa": ["grub", "śmieć", "nienawidz", "brzydz", "wag", "lustr", "schudn", "diet", "nigdy", "zawsze", "muszę"], "tlumaczenie": "Uzależnienie samooceny od wagi, myślenie dychotomiczne."},
            "EMOCJE": {"slowa": ["wstyd", "wyrzut", "win", "lęk", "boję", "stres", "napięc"], "tlumaczenie": "Poczucie winy, wstyd po napadzie, lęk przed przytyciem."},
            "CIAŁO": {"slowa": ["zmęcz", "słab", "mdł", "zimn", "brzuch", "gardł", "opuch"], "tlumaczenie": "Wyczerpanie fizyczne, objawy gastryczne."},
            "ZACHOWANIE": {"slowa": ["napad", "obżarst", "lodówk", "pochłan", "wymiot", "rzyg", "przeczyszcz", "senes", "ćwicz", "głodów"], "tlumaczenie": "Napady objadania się, zachowania kompensacyjne."}
        }
    },
    {
        "diagnoza": "F32 Epizod depresyjny",
        "roznicowa": "ChAD, Dystymia, Niedoczynność tarczycy.",
        "icd10_kryteria": {
            "Kryterium Podstawowe 1: Obniżony nastrój": {
                "icd10": "Obniżony nastrój, utrzymujący się przez większą część dnia, niemal codziennie.",
                "slowa": ["smut", "przygnęb", "płacz", "pust", "dół", "płaka", "źle"]
            },
            "Kryterium Podstawowe 2: Anhedonia": {
                "icd10": "Wyraźna utrata zainteresowań i zdolności odczuwania radości w stosunku do aktywności.",
                "slowa": ["bez sensu", "nic nie czuj", "nie chce mi", "wegetuj", "zaniedb", "obojętn", "nie cieszy"]
            },
            "Kryterium Podstawowe 3: Brak energii": {
                "icd10": "Zmniejszona energia, szybsze męczenie się i spadek aktywności.",
                "slowa": ["zmęcz", "brak sił", "ociężał", "słab", "wyczerp", "leżę"]
            },
            "Kryterium Dodatkowe A: Zaburzenia poznawcze": {
                "icd10": "Spadek zaufania do siebie. Nieracjonalne poczucie winy i bezwartościowości.",
                "slowa": ["beznadziej", "nikim", "ciężar", "nie uda", "głup", "win", "przeze mnie"]
            },
            "Kryterium Dodatkowe B: Zaburzenia snu": {
                "icd10": "Zaburzenia snu wszelkiego typu (najczęściej wczesne wybudzanie).",
                "slowa": ["spać", "sen", "budz", "bezsenn"]
            }
        },
        "cele_smart": "1. Zwiększenie aktywności celowej (min. 3x w tyg).\n2. Zapisywanie myśli w Tabeli Becka.",
        "protokol_nazwa": "Aktywacja Behawioralna / Terapia Poznawcza",
        "uzasadnienie_planu": "Monitorowanie aktywności, testowanie myśli automatycznych.",
        "profil_cbt": {
            "SYTUACJA": {"slowa": ["rano", "wsta", "prac", "obowiąz", "ludz", "problem", "poranek"], "tlumaczenie": "Konieczność podjęcia aktywności, wyzwania dnia codziennego."},
            "MYŚLI": {"slowa": ["beznadziej", "bez sensu", "nikim", "ciężar", "nie uda", "głup", "win", "czarn", "nigdy", "zawsze"], "tlumaczenie": "Negatywna triada Becka, generalizacja, katastrofizacja."},
            "EMOCJE": {"slowa": ["smut", "przygnęb", "płacz", "pust", "nic nie czuj", "znieczul", "płaka"], "tlumaczenie": "Obniżony nastrój, anhedonia, apatia."},
            "CIAŁO": {"slowa": ["spać", "zmęcz", "brak sił", "budzę się", "apetyt", "ociężał"], "tlumaczenie": "Spadek energii, zaburzenia snu i apetytu."},
            "ZACHOWANIE": {"slowa": ["nie chce mi się", "leżę", "wegetuj", "izoluj", "nie wychodz", "zamkn", "zaniedb"], "tlumaczenie": "Wycofanie z relacji społecznych, bierność behawioralna."}
        }
    },
    {
        "diagnoza": "F41.0 Lęk paniczny",
        "roznicowa": "Agorafobia, Zaburzenia kardiologiczne.",
        "icd10_kryteria": {
            "Kryterium A: Nawracające napady paniki": {
                "icd10": "Nawracające napady ciężkiego lęku (paniki), które nie są ograniczone do żadnej szczególnej sytuacji.",
                "slowa": ["panik", "przeraż", "strach", "nagle", "atak"]
            },
            "Kryterium B: Objawy wegetatywne": {
                "icd10": "Nagłe wystąpienie takich objawów jak: palpitacje serca, duszności, zawroty głowy, pocenie się.",
                "slowa": ["serce", "wali", "tchu", "duszno", "kłuci", "drż", "pocę", "miękną"]
            },
            "Kryterium C: Unikanie i lęk przed utratą kontroli": {
                "icd10": "Wtórny lęk przed utratą kontroli nad sobą lub zwariowaniem oraz unikanie sytuacji.",
                "slowa": ["umrę", "uduszę", "zawał", "zwariuję", "kontrol", "zemdlej", "uciekam", "unikam", "karetk", "sor"]
            }
        },
        "cele_smart": "1. Zmniejszenie częstotliwości napadów paniki do 0/miesiąc.\n2. Eliminacja zachowań zabezpieczających.",
        "protokol_nazwa": "Terapia Lęku Panicznego wg D. Clarka",
        "uzasadnienie_planu": "Reatrybucja doznań fizjologicznych, odrzucenie zachowań zabezpieczających.",
        "profil_cbt": {
            "SYTUACJA": {"slowa": ["tłum", "sklep", "kolejk", "autobus", "kawi", "wysił", "zadu", "samochód"], "tlumaczenie": "Miejsca zatłoczone, zamknięte przestrzenie."},
            "MYŚLI": {"slowa": ["umrę", "uduszę", "zawał", "zwariuję", "tracę kontrol", "zemdlej", "to koniec"], "tlumaczenie": "Katastroficzna interpretacja doznań z ciała."},
            "EMOCJE": {"slowa": ["panik", "przeraż", "strach", "lęk"], "tlumaczenie": "Nagły, nieprzewidywalny silny lęk."},
            "CIAŁO": {"slowa": ["serce", "wali", "brakuje mi tchu", "duszno", "kłuci", "drż", "pocę", "miękną nogi"], "tlumaczenie": "Silne pobudzenie wegetatywne."},
            "ZACHOWANIE": {"slowa": ["uciekam", "unikam", "karetk", "sor", "lekarz", "tablet", "muszę usiąść", "woda"], "tlumaczenie": "Ucieczka z sytuacji, zachowania zabezpieczające."}
        }
    }
]

# --- PEŁNA BAZA ICD-10 ---
icd10_full = {
    "F30-F39 Zaburzenia nastroju": ["F32 Epizod depresyjny", "F33 Zaburzenia depresyjne nawracające", "F31 ChAD"],
    "F40-F48 Zaburzenia lękowe": ["F41.0 Lęk paniczny", "F40.1 Fobia społeczna", "F41.1 GAD", "F42 OCD", "F43.1 PTSD"],
    "F50-F59 Zespoły behawioralne": ["F50.0 Anoreksja", "F50.2 Bulimia", "F51 Bezsenność"]
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
menu = st.sidebar.radio("Spis treści:", ["I. Diagnoza i Konceptualizacja", "II. Plan i Interwencje", "III. Podsumowanie", "📂 Archiwum Diagnoz"])
st.sidebar.divider()

if menu == "I. Diagnoza i Konceptualizacja":
    st.title("I. Diagnoza i konceptualizacja zjawiska")
    
    st.header("I.1. Metryczka")
    col1, col2 = st.columns(2)
    imie = col1.text_input("Pacjent (inicjały/kod)")
    wiek = col2.number_input("Wiek", 0, 110)
    
    st.divider()
    st.header("I.2. Diagnoza kliniczna")

    with st.expander("🤖 Asystent Diagnozy (Analiza Kryteriów ICD-10)", expanded=True):
        st.write("Wpisz skargę pacjenta. Algorytm wygeneruje kolorowy raport ICD-10 oparty na cytatach z wywiadu.")
        objawy_input = st.text_area("Wpisz swobodną skargę pacjenta:")
        
        if st.button("🔍 Przetłumacz na kryteria kliniczne"):
            if objawy_input:
                input_lower = objawy_input.lower()
                
                # Podział na zdania
                zdania_pacjenta = [z.strip() + "." for z in re.split(r'[.!?\n]+', objawy_input) if len(z.strip()) > 2]
                
                najlepsze_dopasowanie = None
                najwyzszy_wynik = 0
                najlepszy_html = ""
                
                # Globalne zmienne, do których zapiszemy wynik tylko TEJ WYGRANEJ choroby
                final_sytuacja = final_mysli = final_emocje = final_cialo = final_zachowanie = ""
                
                for choroba in baza_symptomow:
                    wynik_choroby = 0
                    
                    # 1. SPRAWDZANIE KRYTERIÓW ICD-10
                    html_raport = f"<h4 style='color: #2c3e50;'>Analiza dla: {choroba['diagnoza']}</h4>"
                    
                    for nazwa_kryterium, dane_kryterium in choroba["icd10_kryteria"].items():
                        znalezione_dowody = [] 
                        
                        for rdzen in dane_kryterium["slowa"]:
                            for zdanie in zdania_pacjenta:
                                # Używamy \b (Word Boundary), aby np. "waga" nie łapała się na "uwaga"
                                # ani "sen" na "bez sensu"
                                if re.search(r'\b' + rdzen.lower(), zdanie.lower()) and zdanie not in znalezione_dowody:
                                    znalezione_dowody.append(zdanie)
                        
                        if znalezione_dowody:
                            wynik_choroby += len(znalezione_dowody) * 3  # Mocno punktujemy kryteria główne
                            dowody_html = "<br>".join([f"👉 <i>„{d}”</i>" for d in znalezione_dowody])
                            
                            html_raport += f"""
                            <div style='border-left: 5px solid #28a745; padding: 12px; background-color: #f0fdf4; margin-bottom: 15px; border-radius: 4px;'>
                                <h5 style='color: #155724; margin-top: 0;'>✅ SPEŁNIONE: {nazwa_kryterium}</h5>
                                <p style='font-size: 0.9em; color: #333;'><b>Definicja ICD-10:</b> {dane_kryterium['icd10']}</p>
                                <div style='padding: 8px; background-color: #d1e7dd; border-radius: 4px; color: #0f5132;'>
                                    <b>Materiał dowodowy:</b><br>{dowody_html}
                                </div>
                            </div>
                            """
                        else:
                            html_raport += f"""
                            <div style='border-left: 5px solid #dc3545; padding: 12px; background-color: #fdf2f2; margin-bottom: 15px; border-radius: 4px;'>
                                <h5 style='color: #721c24; margin-top: 0;'>❌ BRAK DANYCH: {nazwa_kryterium}</h5>
                                <p style='font-size: 0.9em; color: #333;'><b>Definicja ICD-10:</b> {dane_kryterium['icd10']}</p>
                                <div style='padding: 8px; background-color: #f8d7da; border-radius: 4px; color: #842029;'>
                                    <i>Wymaga dopytania podczas wywiadu.</i>
                                </div>
                            </div>
                            """

                    # 2. WYPEŁNIANIE MODELU CBT (Słowa do okienek)
                    # Zmienne TYMCZASOWE tylko dla analizowanej w tej pętli choroby
                    temp_sytuacja = temp_mysli = temp_emocje = temp_cialo = temp_zachowanie = ""
                    
                    slowa_z_tekstu = re.findall(r'\b\w+\b', input_lower)
                    for sfera, dane_sfery in choroba["profil_cbt"].items():
                        znalezione_slowa = []
                        for rdzen in dane_sfery["slowa"]:
                            for s in slowa_z_tekstu:
                                if re.search(r'\b' + rdzen.lower(), s) and s not in znalezione_slowa: 
                                    znalezione_slowa.append(s)
                                    
                        if znalezione_slowa:
                            wynik_choroby += 1
                            format_tekstu = f"Wykryte słowa pacjenta: {', '.join(znalezione_slowa)}\n[Znaczenie CBT: {dane_sfery['tlumaczenie']}]"
                            if sfera == "SYTUACJA": temp_sytuacja = format_tekstu
                            elif sfera == "MYŚLI": temp_mysli = format_tekstu
                            elif sfera == "EMOCJE": temp_emocje = format_tekstu
                            elif sfera == "CIAŁO": temp_cialo = format_tekstu
                            elif sfera == "ZACHOWANIE": temp_zachowanie = format_tekstu

                    # Zapisujemy, jeśli to najlepszy dotychczasowy wynik
                    if wynik_choroby > najwyzszy_wynik:
                        najwyzszy_wynik = wynik_choroby
                        najlepsze_dopasowanie = choroba
                        najlepszy_html = html_raport
                        # Przepisujemy temp do finalnych zmiennych!
                        final_sytuacja = temp_sytuacja
                        final_mysli = temp_mysli
                        final_emocje = temp_emocje
                        final_cialo = temp_cialo
                        final_zachowanie = temp_zachowanie

                # --- AKTUALIZACJA INTERFEJSU ---
                if najlepsze_dopasowanie and najwyzszy_wynik > 0:
                    st.success(f"🎯 Zidentyfikowano profil kliniczny: {najlepsze_dopasowanie['diagnoza']}")
                    
                    st.session_state.ui_problemy_html = najlepszy_html
                    st.session_state.ui_cele = najlepsze_dopasowanie['cele_smart']
                    st.session_state.ui_protokol = najlepsze_dopasowanie['protokol_nazwa']
                    st.session_state.ui_uzasadnienie = najlepsze_dopasowanie['uzasadnienie_planu']
                    
                    st.session_state.ui_sytuacja = final_sytuacja
                    st.session_state.ui_mysli = final_mysli
                    st.session_state.ui_emocje = final_emocje
                    st.session_state.ui_cialo = final_cialo
                    st.session_state.ui_zachowanie = final_zachowanie
                else:
                    st.info("Algorytm nie wykrył żadnych specyficznych słów klinicznych.")
            else:
                st.warning("Najpierw wpisz wypowiedź pacjenta!")

    c1, c2 = st.columns(2)
    kat_wybrana = c1.selectbox("Grupa ICD-10:", list(icd10_full.keys()))
    pelna_diagnoza = c2.selectbox("Rozpoznanie główne:", icd10_full[kat_wybrana])

    st.divider()
    st.header("I.3. Konceptualizacja problemu")
    
    st.subheader("I.3.1. Raport diagnostyczny (Kryteria ICD-10)")
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

    st.subheader("I.3.3. Poziom drugi (Mechanizmy podtrzymujące)")
    st.text_area("Przekonania kluczowe (o sobie, innych, świecie)")
    st.text_area("Strategie radzenia sobie (kompensacyjne)")

    st.divider()
    if st.button("💾 Zapisz Diagnozę do Archiwum"):
        st.session_state.baza_terapii.append({"Pacjent": imie, "Wiek": wiek, "Diagnoza": pelna_diagnoza})
        st.success("Zapisano!")

elif menu == "II. Plan i Interwencje":
    st.title("II. Plan terapii")
    st.text_input("Protokół (EBM):", key="ui_protokol", on_change=sync_protokol)
    st.text_area("Uzasadnienie interwencji:", key="ui_uzasadnienie", on_change=sync_uzasadnienie, height=150)

elif menu == "III. Podsumowanie":
    st.title("III. Podsumowanie i Ewaluacja")
    st.text_area("Co dokładnie pomogło pacjentowi?")

elif menu == "📂 Archiwum Diagnoz":
    st.title("Baza Terapii")
    if not st.session_state.baza_terapii:
        st.warning("Baza jest pusta.")
    else:
        st.dataframe(pd.DataFrame(st.session_state.baza_terapii), use_container_width=True)
