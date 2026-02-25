import streamlit as st
import pandas as pd
import re

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Zapis Przebiegu Terapii CBT", layout="wide")

# --- BAZA WIEDZY I DIAGRAMY ---
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
            "Opis": "Negatywna wizja siebie, świata i przyszłości.",
            "Interwencje": "Zapisywanie myśli (Tabela Becka), restrukturyzacja poznawcza, testowanie przekonań.",
            "Wizualizacja": "graph TD\nA((Negatywne myśli O SOBIE)) <--> B((Negatywne myśli O ŚWIECIE))\nB <--> C((Negatywne myśli O PRZYSZŁOŚCI))\nC <--> A\nstyle A fill:#002b5e,stroke:#3399ff,color:#fff\n"
        }
    ],
    "F50.2": [
        {
            "Model": "Transdiagnostyczny model zaburzeń odżywiania (C. Fairburn)",
            "Opis": "Nadmierne uzależnienie samooceny od wagi i sylwetki, prowadzące do restrykcji, napadów objadania się i zachowań kompensacyjnych.",
            "Interwencje": "Monitorowanie odżywiania, planowanie regularnych posiłków, restrukturyzacja przekonań o ciele i wadze.",
            "Wizualizacja": "graph TD\nA[Koncentracja na sylwetce i wadze] --> B[Restrykcje dietetyczne]\nB --> C[Złamanie zasad / Narastające napięcie]\nC --> D[Napad objadania się]\nD --> E[Zachowania kompensacyjne np. wymioty]\nD --> F[Poczucie winy i lęk przed tyciem]\nE --> F\nF -- Wzmacnia kontrolę --> A\nstyle A fill:#004d40,stroke:#00695c,color:#fff\n"
        }
    ]
}
slownik_modeli["F33"] = slownik_modeli["F32"]
slownik_modeli["F50.0"] = slownik_modeli["F50.2"]

# --- NOWA BAZA: JĘZYK KLINICZNY + ROZBICIE NA I.3.2. ---
baza_symptomow = [
    {
        "diagnoza": "F50.2 Żarłoczność psychiczna (Bulimia)",
        "roznicowa": "Anoreksja (F50.0), BED, Depresja nietypowa.",
        "problemy_kliniczne": "KLINICZNA LISTA PROBLEMÓW (Kryteria Diagnostyczne CBT):\n1. Nawracające epizody przejadania się (spożywanie obiektywnie dużej ilości jedzenia z poczuciem utraty kontroli).\n2. Powtarzające się, nieodpowiednie zachowania kompensacyjne w celu zapobieżenia przyrostowi masy ciała (np. prowokowanie wymiotów, nadużywanie leków przeczyszczających, intensywne ćwiczenia fizyczne).\n3. Samoocena nadmiernie wyznaczana przez kształt i masę ciała (współwystępujące zniekształcenia poznawcze).\n4. Błędne koło restrykcji i objadania się prowadzące do wyczerpania fizjologicznego i chwiejności afektu.",
        "cele_smart": "1. Wprowadzenie regularnego planu posiłków (3 główne, 2 przekąski).\n2. Zmniejszenie częstotliwości napadów/wymiotów do 1/tydz w ciągu miesiąca.",
        "protokol_nazwa": "CBT-E wg C. Fairburna",
        "uzasadnienie_planu": "1) Psychoedukacja (błędne koło). 2) Dzienniczek myśli i reakcji. 3) Restrukturyzacja poznawcza i zmiana oceny własnej wartości.",
        "profil_cbt": {
            "SYTUACJA": {"slowa": ["wieczór", "samotn", "stres", "kłótni", "imprez", "restauracj", "sklep", "wadze", "lustrz"], "tlumaczenie": "Sytuacje napięcia emocjonalnego (stres, samotność) lub ekspozycja na bodźce (lustro, waga)."},
            "MYŚLI": {"slowa": ["grub", "śmieć", "nienawidz", "brzydz", "obsesj", "wag", "lustr", "schudn", "diet", "nigdy", "zawsze", "muszę", "nie dam rady"], "tlumaczenie": "Nadmierne uzależnienie samooceny od wagi/sylwetki, myślenie dychotomiczne, silna samokrytyka."},
            "EMOCJE": {"slowa": ["wstyd", "wyrzut", "win", "lęk", "boję", "stres", "napięc"], "tlumaczenie": "Głębokie poczucie winy, wstyd po napadzie, silny lęk przed przytyciem."},
            "CIAŁO": {"slowa": ["zmęcz", "słab", "mdł", "zimn", "brzuch", "gardł", "opuch"], "tlumaczenie": "Wyczerpanie fizyczne, uczucie przepełnienia, możliwe powikłania gastryczne."},
            "ZACHOWANIE": {"slowa": ["napad", "obżarst", "popłyn", "ciąg", "lodówk", "pochłan", "wymiot", "rzyg", "przeczyszcz", "senes", "ćwicz", "siłown", "głodów"], "tlumaczenie": "Napady objadania się (utrata kontroli), po których następują zachowania kompensacyjne."}
        }
    },
    {
        "diagnoza": "F32 Epizod depresyjny",
        "roznicowa": "ChAD, Dystymia, Niedoczynność tarczycy.",
        "problemy_kliniczne": "KLINICZNA LISTA PROBLEMÓW (Kryteria Diagnostyczne CBT):\n1. Obniżony nastrój występujący przez większą część dnia, niemal codziennie.\n2. Wyraźna utrata zainteresowań i odczuwania przyjemności we wszystkich lub prawie wszystkich aktywnościach (anhedonia).\n3. Spadek energii i wzmożona męczliwość.\n4. Deficyty poznawcze: negatywna triada Becka (negatywne postrzeganie siebie, świata i przyszłości).\n5. Wycofanie społeczne i bierność behawioralna prowadząca do drastycznego spadku wzmocnień pozytywnych ze środowiska.",
        "cele_smart": "1. Zwiększenie aktywności celowej (min. 3x w tyg).\n2. Zapisywanie myśli w arkuszu samooceny (Tabela Becka).",
        "protokol_nazwa": "Aktywacja Behawioralna / Terapia Poznawcza Depresji",
        "uzasadnienie_planu": "Monitorowanie aktywności i nastroju, planowanie dnia (mistrzostwo i przyjemność), testowanie myśli automatycznych.",
        "profil_cbt": {
            "SYTUACJA": {"slowa": ["rano", "wsta", "prac", "obowiąz", "ludz", "problem", "poranek"], "tlumaczenie": "Konieczność podjęcia aktywności, wyzwania dnia codziennego."},
            "MYŚLI": {"slowa": ["beznadziej", "bez sensu", "nikim", "ciężar", "nie uda", "głup", "win", "czarn", "nigdy", "zawsze"], "tlumaczenie": "Negatywna triada Becka, generalizacja, katastrofizacja."},
            "EMOCJE": {"slowa": ["smut", "przygnęb", "płacz", "pust", "nic nie czuj", "znieczul"], "tlumaczenie": "Obniżony nastrój, anhedonia, apatia, znieczulenie emocjonalne."},
            "CIAŁO": {"slowa": ["spać", "zmęcz", "brak sił", "budzę się", "apetyt", "ociężał"], "tlumaczenie": "Spadek energii, zaburzenia snu i apetytu, spowolnienie psychoruchowe."},
            "ZACHOWANIE": {"slowa": ["nie chce mi się", "leżę", "wegetuj", "izoluj", "nie wychodz", "zamkn", "zaniedb"], "tlumaczenie": "Wycofanie z relacji społecznych, bierność behawioralna, pogłębienie izolacji."}
        }
    },
    {
        "diagnoza": "F41.0 Lęk paniczny",
        "roznicowa": "Agorafobia, Zaburzenia kardiologiczne.",
        "problemy_kliniczne": "KLINICZNA LISTA PROBLEMÓW (Kryteria Diagnostyczne CBT):\n1. Nawracające, nieoczekiwane napady paniki z silnym pobudzeniem autonomicznym i somatycznym.\n2. Katastroficzna interpretacja normalnych doznań płynących z ciała (np. szybkie bicie serca interpretowane jako zawał).\n3. Uporczywa obawa przed wystąpieniem kolejnych napadów (lęk antycypacyjny) trwająca min. 1 miesiąc.\n4. Istotna, niekorzystna zmiana zachowania związana z napadami, w tym stosowanie zachowań zabezpieczających i unikanie wysiłku fizycznego.",
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

# --- ICD-10 ---
icd10_full = {
    "F30-F39 Zaburzenia nastroju": ["F32 Epizod depresyjny", "F33 Zaburzenia depresyjne nawracające"],
    "F40-F48 Zaburzenia lękowe": ["F41.0 Lęk paniczny"],
    "F50-F59 Zespoły behawioralne": ["F50.2 Bulimia"]
}

# --- STANY APLIKACJI W PAMIĘCI ---
if 'baza_terapii' not in st.session_state: st.session_state.baza_terapii = []
if 'ui_problemy' not in st.session_state: st.session_state.ui_problemy = ""
if 'ui_cele' not in st.session_state: st.session_state.ui_cele = ""
if 'ui_protokol' not in st.session_state: st.session_state.ui_protokol = ""
if 'ui_uzasadnienie' not in st.session_state: st.session_state.ui_uzasadnienie = ""

# ZMIENNE DLA SEKCJI I.3.2
if 'ui_sytuacja' not in st.session_state: st.session_state.ui_sytuacja = ""
if 'ui_mysli' not in st.session_state: st.session_state.ui_mysli = ""
if 'ui_emocje' not in st.session_state: st.session_state.ui_emocje = ""
if 'ui_cialo' not in st.session_state: st.session_state.ui_cialo = ""
if 'ui_zachowanie' not in st.session_state: st.session_state.ui_zachowanie = ""

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
    terapeuta = col1.text_input("Terapeuta")
    superwizor = col2.text_input("Superwizor")
    st.checkbox("Czy pacjent jest bezpieczny? (ryzyko samobójstwa / heteroagresji)")

    st.divider()
    st.header("I.2. Diagnoza kliniczna")

    with st.expander("🤖 Asystent Diagnozy (Analiza potocznej wypowiedzi pacjenta)", expanded=True):
        st.write("Wpisz skargę pacjenta. Algorytm wygeneruje kliniczną Listę Problemów, a słowa pacjenta rozdzieli do odpowiednich okienek w sekcji I.3.2. (Przekrój poprzeczny).")
        objawy_input = st.text_area("Wpisz swobodną skargę pacjenta:")
        
        if st.button("🔍 Analizuj i przetwórz do formularza"):
            if objawy_input:
                input_do_analizy = objawy_input.lower()
                slowa_z_tekstu = re.findall(r'\b\w+\b', input_do_analizy)
                
                najlepsze_dopasowanie = None
                najwyzszy_wynik = 0
                
                # Zmienne tymczasowe dla I.3.2
                temp_sytuacja = ""
                temp_mysli = ""
                temp_emocje = ""
                temp_cialo = ""
                temp_zachowanie = ""
                
                for choroba in baza_symptomow:
                    wynik_choroby = 0
                    
                    # Sprawdzanie poszczególnych sfer w modelu 5 elementów
                    for sfera, dane_sfery in choroba["profil_cbt"].items():
                        znalezione_slowa = []
                        for rdzen in dane_sfery["slowa"]:
                            for slowo_pacjenta in slowa_z_tekstu:
                                if rdzen in slowo_pacjenta and slowo_pacjenta not in znalezione_slowa:
                                    znalezione_slowa.append(slowo_pacjenta)
                        
                        if znalezione_slowa:
                            wynik_choroby += len(znalezione_slowa)
                            format_tekstu = f"Wypowiedź: \"{', '.join(znalezione_slowa)}\"\n[Klinicznie: {dane_sfery['tlumaczenie']}]"
                            
                            if sfera == "SYTUACJA": temp_sytuacja = format_tekstu
                            elif sfera == "MYŚLI": temp_mysli = format_tekstu
                            elif sfera == "EMOCJE": temp_emocje = format_tekstu
                            elif sfera == "CIAŁO": temp_cialo = format_tekstu
                            elif sfera == "ZACHOWANIE": temp_zachowanie = format_tekstu
                    
                    if wynik_choroby > najwyzszy_wynik:
                        najwyzszy_wynik = wynik_choroby
                        najlepsze_dopasowanie = choroba

                if najlepsze_dopasowanie:
                    st.success(f"🎯 Rozpoznano: {najlepsze_dopasowanie['diagnoza']}")
                    
                    # Wypełniamy listę problemów językiem KLINICZNYM
                    st.session_state.ui_problemy = najlepsze_dopasowanie['problemy_kliniczne']
                    st.session_state.ui_cele = najlepsze_dopasowanie['cele_smart']
                    st.session_state.ui_protokol = najlepsze_dopasowanie['protokol_nazwa']
                    st.session_state.ui_uzasadnienie = najlepsze_dopasowanie['uzasadnienie_planu']
                    
                    # Rozdzielamy słowa pacjenta do sekcji I.3.2
                    st.session_state.ui_sytuacja = temp_sytuacja if temp_sytuacja else "Brak wyraźnego wyzwalacza w wypowiedzi pacjenta."
                    st.session_state.ui_mysli = temp_mysli if temp_mysli else "Brak zidentyfikowanych myśli automatycznych."
                    st.session_state.ui_emocje = temp_emocje if temp_emocje else "Brak zidentyfikowanych emocji."
                    st.session_state.ui_cialo = temp_cialo if temp_cialo else "Brak zidentyfikowanych doznań somatycznych."
                    st.session_state.ui_zachowanie = temp_zachowanie if temp_zachowanie else "Brak zidentyfikowanych zachowań."
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

    st.divider()
    st.header("I.3. Konceptualizacja problemu")
    
    st.subheader("I.3.1. Lista problemów i cele terapii")
    st.text_area("Lista problemów (Kliniczne Kryteria Diagnostyczne CBT)", key="ui_problemy", height=200)
    st.text_area("Cele terapii (SMART)", key="ui_cele", height=100)

    st.subheader("I.3.2. Poziom pierwszy (Sytuacja bieżąca - przekrój poprzeczny)")
    st.info("Poniższe pola zostały automatycznie uzupełnione potocznym językiem pacjenta wyodrębnionym ze skargi głównej.")
    
    st.text_area("Sytuacja (typowa sytuacja ilustrująca problem)", key="ui_sytuacja")
    c3, c4 = st.columns(2)
    with c3:
        st.text_area("Myśli automatyczne / Obrazy", key="ui_mysli")
        st.text_area("Emocje (rodzaj i nasilenie)", key="ui_emocje")
    with c4:
        st.text_area("Doznania z ciała (fizjologiczne)", key="ui_cialo")
        st.text_area("Zachowanie (w tym zabezpieczające/unikające)", key="ui_zachowanie")

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
        st.success("Zapisano!")

elif menu == "II. Plan i Interwencje":
    st.title("II. Plan terapii i interwencje")
    st.header("II.1. Plan terapii (Uzasadnienie EBM)")
    st.text_input("Protokół (EBM):", key="ui_protokol")
    st.text_area("Uzasadnienie interwencji:", key="ui_uzasadnienie", height=150)
    st.divider()
    st.header("II.2. Zapis przebiegu poszczególnych sesji")
    st.text_area("Rejestr sesji (np. Sesja 1 [Data] - Psychoedukacja i BA...)", height=300)

elif menu == "III. Podsumowanie":
    st.title("III. Podsumowanie i Ewaluacja")
    st.header("III.1. Osiągnięte cele terapii")
    col1, col2 = st.columns(2)
    with col1: st.text_area("Według pacjenta")
    with col2: st.text_area("Według terapeuty")
    st.header("III.2. Zidentyfikowane mechanizmy zmiany")
    st.text_area("Co dokładnie pomogło pacjentowi?")

elif menu == "📂 Archiwum Diagnoz":
    st.title("Baza Terapii")
    if not st.session_state.baza_terapii:
        st.warning("Baza jest pusta. Dodaj pacjenta w zakładce I.")
    else:
        df = pd.DataFrame(st.session_state.baza_terapii)
        st.dataframe(df, use_container_width=True)
