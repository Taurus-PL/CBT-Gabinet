import streamlit as st
import pandas as pd
import re
import unicodedata

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Zapis Przebiegu Terapii CBT", layout="wide")


def normalizuj_tekst(tekst):
    tekst = tekst.lower().strip()
    tekst = "".join(
        znak for znak in unicodedata.normalize("NFD", tekst) if unicodedata.category(znak) != "Mn"
    )
    return tekst


def dopasuj_diagnozy(wejscie):
    """Zwraca pozycje bazy pasujące do kodu lub nazwy rozpoznania."""
    zapytanie = normalizuj_tekst(wejscie)
    if len(zapytanie) < 3:
        return []

    # Akceptuj również popularny zapis kodu bez kropki, np. F410.
    zapytanie = re.sub(r"\b([a-z]\d{2})(\d)\b", r"\1.\2", zapytanie)
    dopasowania = []

    for pozycja in baza_modeli_protokolow:
        for fraza in pozycja["frazy"]:
            fraza_norm = normalizuj_tekst(fraza)
            if re.fullmatch(r"[a-z]\d{2}(?:\.\d+)?", fraza_norm):
                pasuje = re.search(rf"(?<!\w){re.escape(fraza_norm)}(?!\w)", zapytanie)
            elif len(fraza_norm) <= 3:
                pasuje = re.search(rf"(?<!\w){re.escape(fraza_norm)}(?!\w)", zapytanie)
            else:
                pasuje = fraza_norm in zapytanie

            if pasuje:
                dopasowania.append(pozycja)
                break

    return dopasowania


baza_modeli_protokolow = [
    {
        "diagnoza": "F32/F33 Epizod depresyjny / Zaburzenie depresyjne nawracające (ICD-10), Major Depressive Disorder (DSM-5)",
        "frazy": ["f32", "f33", "depres", "major depressive disorder", "mdd"],
        "modele": [
            "Model poznawczy Becka (triada poznawcza, przekonania kluczowe i pośredniczące).",
            "Model behawioralnej aktywacji (depresja podtrzymywana przez wycofanie i spadek wzmocnień).",
            "Model transdiagnostyczny procesów ruminacyjnych.",
        ],
        "protokoly": [
            "CBT dla depresji wg Becka (Beck, Rush, Shaw, Emery) – protokół o silnym poziomie dowodów z RCT i metaanaliz.",
            "Behavioral Activation (BA; Martell/Jacobson) – skuteczność porównywalna z pełnym CBT w wielu badaniach.",
            "CBASP dla depresji przewlekłej (McCullough) – rekomendowany szczególnie przy przewlekłym przebiegu.",
        ],
    },
    {
        "diagnoza": "F41.0 Lęk paniczny (ICD-10), Panic Disorder (DSM-5)",
        "frazy": ["f41.0", "panic", "lek paniczny", "napady paniki"],
        "modele": [
            "Model paniki Clarka (katastroficzna interpretacja doznań somatycznych).",
            "Model Barlowa (wrażliwość lękowa + unikanie + zachowania zabezpieczające).",
            "Model uczenia i interoceptywnego warunkowania lęku.",
        ],
        "protokoly": [
            "Protokół CBT Clark & Salkovskis dla panic disorder (psychoedukacja, restrukturyzacja, ekspozycja interoceptywna).",
            "Panic Control Treatment (Barlow & Craske) – jeden z najlepiej przebadanych protokołów CBT dla paniki.",
            "Ekspozycja interoceptywna + in vivo w nurcie CBT (potwierdzona skuteczność w wytycznych NICE/APA).",
        ],
    },
    {
        "diagnoza": "F43.1 PTSD (ICD-10), Posttraumatic Stress Disorder (DSM-5)",
        "frazy": ["f43.1", "ptsd", "stres pourazowy", "posttraumatic"],
        "modele": [
            "Model poznawczy PTSD Ehlers i Clark (negatywne znaczenia traumy + utrzymywanie poczucia zagrożenia).",
            "Model przetwarzania emocjonalnego (Foa) i rola unikania.",
            "Model pamięci traumatycznej i integracji wspomnień.",
        ],
        "protokoly": [
            "Trauma-Focused CBT (TF-CBT) – silne potwierdzenie skuteczności, szczególnie dla objawów intruzji i unikania.",
            "Cognitive Processing Therapy (CPT; Resick) – protokół oparty na modyfikacji przekonań potraumatycznych.",
            "Prolonged Exposure (PE; Foa) – złoty standard leczenia PTSD w wielu wytycznych klinicznych.",
        ],
    },
    {
        "diagnoza": "F50.2 Żarłoczność psychiczna (ICD-10), Bulimia Nervosa (DSM-5)",
        "frazy": ["f50.2", "bulim", "zarłocznosc", "bulimia nervosa"],
        "modele": [
            "Transdiagnostyczny model zaburzeń odżywiania Fairburna (nadmierna ocena masy i kształtu ciała).",
            "Model cyklu ograniczanie–napad–kompensacja.",
            "Model regulacji emocji i impulsywności w epizodach objadania.",
        ],
        "protokoly": [
            "CBT-E (Fairburn) – najlepiej przebadany protokół pierwszego wyboru dla bulimii.",
            "Enhanced CBT z modułami perfekcjonizmu, niskiej samooceny i trudności interpersonalnych.",
            "Interpersonal Psychotherapy (IPT-BN) jako alternatywa o potwierdzonej skuteczności (zwykle wolniejszy efekt).",
        ],
    },
    {
        "diagnoza": "F42 Zaburzenie obsesyjno-kompulsyjne (ICD-10), Obsessive-Compulsive Disorder (DSM-5)",
        "frazy": ["f42", "ocd", "obsesyjn", "kompulsyjn"],
        "modele": [
            "Model Salkovskisa (nadodpowiedzialność i katastrofizacja myśli natrętnych).",
            "Model poznawczy OCD (fuzja myśl-działanie, nietolerancja niepewności).",
            "Model behawioralny podtrzymywania kompulsji przez redukcję lęku.",
        ],
        "protokoly": [
            "ERP (Exposure and Response Prevention) – metoda pierwszego wyboru z najsilniejszymi dowodami.",
            "CBT dla OCD z elementami restrukturyzacji poznawczej (szczególnie przy silnych przekonaniach metapoznawczych).",
            "Inferential CBT (I-CBT) – obiecujący protokół dla wybranych profili OCD.",
        ],
    },
]


# --- BAZA WIEDZY DLA ASYSTENTA (Schowana w tle) ---
baza_symptomow = [
    {
        "diagnoza": "F43.1 Zaburzenie stresowe pourazowe (PTSD)",
        "icd10_kryteria": {
            "Kryterium A: Zdarzenie traumatyczne": {"icd10": "Narażenie na stresujące wydarzenie o wyjątkowo groźnym charakterze.", "slowa": ["wypadek", "śmierć", "gwałt", "napad", "pożar", "wojna", "traum", "zagrożeni", "przetrwać", "system alarmowy", "niebezpieczn", "coś się stanie"]},
            "Kryterium B: Intruzje": {"icd10": "Uporczywe przypominanie sobie traumy, flashbacki, dysocjacja.", "slowa": ["flashback", "koszmar", "wraca", "obraz", "przed oczami", "jakby to", "budzę się", "żywo", "film", "znowu tam", "fragmenty", "odcinam", "wyłączyć", "robot"]},
            "Kryterium C: Unikanie/Pobudzenie": {"icd10": "Unikanie okoliczności, odrętwienie, nadmierne wzbudzenie.", "slowa": ["unikam", "nie chodzę", "nie myśl", "napięt", "czuwam", "wybuch", "zaskoczen", "hałas", "czujność", "skanuję", "wyjście", "odizolow", "płytko", "zamknięte"]}
        }
    },
    {
        "diagnoza": "F50.2 Żarłoczność psychiczna (Bulimia)",
        "icd10_kryteria": {
            "Kryterium A: Epizody przejadania": {"icd10": "Epizody przejadania się dużą ilością jedzenia.", "slowa": ["napad", "obżarst", "popłyn", "ciąg", "lodówk", "pochłan", "zjadł", "żar", "wyjad", "obżar"]},
            "Kryterium B: Przymus jedzenia": {"icd10": "Stałe zaabsorbowanie jedzeniem, przymus jedzenia.", "slowa": ["musz", "przymus", "głód", "ochot", "kontro", "obsesj", "pilnuj"]},
            "Kryterium C: Kompensacje": {"icd10": "Wymioty, przeczyszczanie, głodówki, ćwiczenia.", "slowa": ["wymiot", "rzyg", "przeczyszcz", "senes", "ćwicz", "siłown", "głodów", "tablet", "kibel", "odkręcić"]},
            "Kryterium D: Samoocena": {"icd10": "Samoocena nadmiernie wyznaczana przez kształt i masę ciała.", "slowa": ["grub", "śmieć", "nienawidz", "brzydz", "waga", "wagę", "wagi", "lustr", "schudn", "diet", "wygląd", "ciało", "ocenę"]}
        }
    },
    {
        "diagnoza": "F32 Epizod depresyjny",
        "icd10_kryteria": {
            "Kryterium 1: Obniżony nastrój": {"icd10": "Obniżony nastrój przez większą część dnia.", "slowa": ["smut", "przygnęb", "płacz", "pust", "dół", "płaka", "źle"]},
            "Kryterium 2: Anhedonia": {"icd10": "Utrata zainteresowań i zdolności odczuwania radości.", "slowa": ["bez sensu", "nic nie czuj", "nie chce mi", "wegetuj", "zaniedb", "obojętn", "nie cieszy"]},
            "Kryterium 3: Brak energii": {"icd10": "Zmniejszona energia, szybsze męczenie się.", "slowa": ["zmęcz", "brak sił", "ociężał", "słab", "wyczerp", "leżę"]},
            "Kryterium 4: Zaburzenia poznawcze": {"icd10": "Spadek zaufania do siebie, poczucie winy.", "slowa": ["beznadziej", "nikim", "ciężar", "nie uda", "głup", "win", "przeze mnie"]}
        }
    },
    {
        "diagnoza": "F41.0 Lęk paniczny",
        "icd10_kryteria": {
            "Kryterium A: Napady paniki": {"icd10": "Nawracające napady ciężkiego lęku, nieprzewidywalne.", "slowa": ["panik", "przeraż", "strach", "nagle", "atak"]},
            "Kryterium B: Objawy wegetatywne": {"icd10": "Palpitacje, duszności, zawroty głowy, poty.", "slowa": ["serce", "wali", "tchu", "duszno", "kłuci", "drż", "pocę", "miękną"]},
            "Kryterium C: Wtórny lęk": {"icd10": "Lęk przed śmiercią lub utratą kontroli, unikanie.", "slowa": ["umrę", "uduszę", "zawał", "zwariuję", "kontrol", "zemdlej", "uciekam", "unikam", "karetk", "sor"]}
        }
    }
]

# --- MENU BOCZNE ---
st.sidebar.title("Zapis Przebiegu Terapii (Popiel, Pragłowska 2021)")
menu = st.sidebar.radio("Nawigacja:", [
    "Strona tytułowa i Autorefleksja",
    "I. Pierwszy Etap Terapii",
    "II. Drugi Etap Terapii",
    "III i IV. Trzeci Etap i Wnioski",
    "📂 Archiwum"
])

with st.sidebar.expander("🤖 Asystent Diagnozy (Opcjonalnie)"):
    st.write("Skorzystaj, jeśli potrzebujesz pomocy w dopasowaniu słów pacjenta do ICD-10.")
    asystent_input = st.text_area("Słowa-klucze ze skargi pacjenta:")
    if st.button("Sprawdź kryteria"):
        if asystent_input:
            zdania = [z.strip() for z in re.split(r'[.,;!|\n]+', asystent_input) if len(z.strip()) > 1]
            najlepsze = None
            max_wynik = 0
            raport = ""
            for choroba in baza_symptomow:
                wynik = 0
                temp_raport = f"**{choroba['diagnoza']}**\n"
                for nazwa, dane in choroba["icd10_kryteria"].items():
                    znalezione = [z for z in zdania if any(r.lower() in z.lower() for r in dane["slowa"])]
                    if znalezione:
                        wynik += len(znalezione)
                        temp_raport += f"- ✅ {nazwa} (Znaleziono: '{znalezione[0]}...')\n"
                    else:
                        temp_raport += f"- ❌ {nazwa} (Brak danych)\n"
                if wynik > max_wynik:
                    max_wynik = wynik
                    najlepsze = choroba
                    raport = temp_raport
            if max_wynik > 0:
                st.success("Sugerowana diagnoza:")
                st.markdown(raport)
            else:
                st.info("Brak wystarczających słów kluczowych.")

# ==========================================================
# STRONA TYTUŁOWA I AUTOREFLEKSJA
# ==========================================================
if menu == "Strona tytułowa i Autorefleksja":
    st.title("ZAPIS PRZEBIEGU TERAPII POZNAWCZO-BEHAWIORALNEJ")
    st.caption("A. Popiel, E. Pragłowska 2009, 2013, 2021")

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Dane ogólne")
        st.text_input("Pacjent (inicjały lub pseudonim):")
        st.text_input("Wiek:")
        st.text_input("Data rozpoczęcia terapii:")
    with col2:
        st.subheader("Dane terapeuty")
        st.text_input("Nazwisko i imię terapeuty:")
        st.text_input("Nazwa i adres ośrodka:")

    st.divider()
    st.subheader("Autorefleksja terapeuty")
    st.text_area("Refleksja terapeuty przed rozpoczęciem terapii:", height=200)

# ==========================================================
# I. PIERWSZY ETAP TERAPII
# ==========================================================
elif menu == "I. Pierwszy Etap Terapii":
    st.title("I. PIERWSZY ETAP TERAPII")

    st.header("I.1 Problem")
    st.text_area("Główne skargi i problemy pacjenta:", height=100)

    st.header("I.2 Lista problemów")
    st.text_area("Szczegółowa lista problemów (z punktu widzenia pacjenta i terapeuty):", height=120)

    st.header("I.3 Konceptualizacja")
    st.write("**PIERWSZY POZIOM KONCEPTUALIZACJI.**")
    st.caption("Objawy, automatyczne myśli, emocje, reakcje fizjologiczne, zachowania i ich konsekwencje")

    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        st.text_area("A - Sytuacja:")
    with col_c2:
        st.text_area("B - Automatyczne myśli:")
    with col_c3:
        st.text_area("C - Emocje:")

    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        st.text_area("C - Objawy fizjologiczne:")
    with col_c2:
        st.text_area("C - Zachowanie:")
    with col_c3:
        st.text_area("Konsekwencje:")

    st.text_area("Typowe automatyczne myśli [występujące w podobnych sytuacjach ilustrujących PROBLEM]:")
    st.text_area("Typowe emocje [występujące w podobnych sytuacjach ilustrujących PROBLEM]:")
    st.text_area("Reakcje fizjologiczne [występujące w podobnych sytuacjach ilustrujących PROBLEM]:")
    st.text_area("Podstawowe strategie behawioralne (w tym zachowania zabezpieczające) [występujące w podobnych sytuacjach ilustrujących PROBLEM]:")
    st.text_area("Konsekwencje zachowań [np. wzmocnienia pozytywne i negatywne]:")
    st.text_area("Analiza funkcjonalna A-B-C sytuacji problemowej (analiza łańcuchowa) [jeśli jest wykonana]:")

    st.divider()
    st.write("**DRUGI POZIOM KONCEPTUALIZACJI.**")
    st.caption("Schematy poznawcze, typowe wzorce reagowania w przeszłości i ich uwarunkowania. Czynniki wyzwalające i odpornościowe")

    st.text_area("Przekonania kluczowe [schematy poznawcze]:")
    st.text_area("Przekonania warunkowe, pośredniczące [zasady]:")
    st.text_area("Zniekształcenia i ograniczenia poznawcze [należy uwzględnić ewentualne wnioski z przeprowadzonych testów diagnostycznych]:")
    st.text_area("Typowe emocje:")
    st.text_area("Podstawowe strategie behawioralne stosowane przez pacjenta i ich rola w powstaniu lub podtrzymywaniu problemu [analiza w kontekście wzmocnień]:")

    st.write("Zidentyfikowane procesy transdiagnostyczne podtrzymujące problem:")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.text_input("Unikanie poznawcze:")
        st.text_input("Zamartwianie, ruminacje:")
        st.text_input("Historia uczenia/wzmocnienia:")
    with col_t2:
        st.text_input("Perfekcjonizm:")
        st.text_input("Monitorowanie zagrożenia (ukierunkowanie uwagi):")
        st.text_input("Inne:")

    st.text_area("Profil rozwojowy - Przeszłość i związki z innymi (rodzice, rodzeństwo, rówieśnicy, autorytety, ważne osoby, historia leczenia, problemów.)", help="[Ten fragment konceptualizacji uwzględnia... perspektywę historii uczenia się...]")
    st.text_area("Istotne wydarzenia i przeżycia traumatyczne [i ich związek z obecnymi problemami]:")
    st.text_area("Czynniki wyzwalające obecne zaburzenie [i uwzględnienie mechanizmu, w jakim dany bodziec zadziałał]:")
    st.text_area("Czynniki, które mogą negatywnie wpływać na przebieg terapii:")
    st.text_area("Zasoby, rezyliencja ‒ czynniki, które mogą pozytywnie wpływać na przebieg terapii:")
    st.text_area("Dodatkowe informacje, zastosowane narzędzia diagnostyczne, wyniki badań:")

    st.text_area("Podsumowanie konceptualizacji", help="[Jest to synteza wiedzy na temat czynników i mechanizmów... Podsumowanie stanowi podstawę do określenia celów...]", height=200)

    st.divider()
    st.header("I.4 Cele terapii")
    st.text_area("[Powinny być uzgodnione wspólnie z pacjentem, spójne z listą problemów i diagnozą oraz wynikać z podsumowania konceptualizacji]:")

# ==========================================================
# II. DRUGI ETAP TERAPII
# ==========================================================
elif menu == "II. Drugi Etap Terapii":
    st.title("II. DRUGI ETAP TERAPII")

    st.header("II. 1 Plan terapii")
    st.text_area("(jakie modele zaburzenia, jaki protokół terapeutyczny stanowią podstawę planu terapii, uzasadnienie wyboru metody)", help="[W tym miejscu należy odpowiedzieć sobie na pytania: Co wiadomo na temat leczenia... Czy istnieją protokoły...]", height=200)
    st.text_area("Narzędzia oceny stanu psychicznego (i/lub opis sposobu monitorowania zmian zachodzących podczas terapii):")

    st.divider()
    st.subheader("🧠 Asystent modeli CBT i protokołów (DSM-5 / ICD-10)")
    st.caption("Wpisz kod (np. F41.0, F32) albo nazwę diagnozy DSM-5/ICD-10, aby zobaczyć dostępne modele poznawczo-behawioralne i rekomendowane protokoły.")

    st.info(
        "Wyniki mają charakter pomocniczy. Wybór modelu i protokołu wymaga "
        "konceptualizacji przypadku, diagnozy różnicowej oraz oceny ryzyka i przeciwwskazań."
    )
    diagnoza_wejscie = st.text_input("Diagnoza terapeuty:", placeholder="np. F43.1, PTSD, OCD, Major Depressive Disorder")
    if diagnoza_wejscie:
        dopasowania = dopasuj_diagnozy(diagnoza_wejscie)

        if not normalizuj_tekst(diagnoza_wejscie):
            st.warning("Wpisz kod lub nazwę diagnozy.")
        elif len(normalizuj_tekst(diagnoza_wejscie)) < 3:
            st.warning("Zapytanie jest zbyt krótkie. Wpisz pełny kod lub nazwę diagnozy.")
        elif dopasowania:
            st.success(f"Znaleziono {len(dopasowania)} dopasowanie(a) diagnostyczne.")
            for wpis in dopasowania:
                with st.expander(f"📌 {wpis['diagnoza']}", expanded=True):
                    st.markdown("**Dostępne modele poznawczo-behawioralne:**")
                    for model in wpis["modele"]:
                        st.markdown(f"- {model}")

                    st.markdown("**Gotowe protokoły terapeutyczne (potwierdzone naukowo):**")
                    for protokol in wpis["protokoly"]:
                        st.markdown(f"- {protokol}")
        else:
            st.warning("Brak dopasowania w aktualnej bazie. Spróbuj kodu ICD-10 (np. F42) lub nazwy DSM-5/ICD-10.")

    st.divider()
    st.header("II.2 REALIZACJA PLANU – OPIS KOLEJNYCH SESJI, ZASTOSOWANYCH INTERWENCJI")
    st.caption("[Opis przeprowadzonej terapii powinien być syntetyczny... powinny znaleźć się: plan sesji, co zrobiono, jakimi metodami, wnioski, praca osobista pacjenta. Refleksje terapeuty.]")
    st.text_area("Zapis sesji:", height=400)

# ==========================================================
# III. TRZECI ETAP TERAPII i IV. PODSUMOWANIE
# ==========================================================
elif menu == "III i IV. Trzeci Etap i Wnioski":
    st.title("III. TRZECI ETAP TERAPII")

    st.subheader("OSIĄGNIĘTE CELE")
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.text_area("Według pacjenta:")
    with col_c2:
        st.text_area("Według terapeuty:")
    st.text_area("Według narzędzi oceny: [wskazane zamieszczenie wartości przed terapią i po jej zakończeniu lub wykres zmian z sesji na sesję]")

    st.subheader("ZMIANY, KTÓRE PODCZAS TERAPII ZASZŁY W ZAKRESIE:")
    st.text_area("Funkcjonowania poznawczego pacjenta:")
    st.text_area("Emocji:")
    st.text_area("Zachowań:")

    st.subheader("MECHANIZMY ZMIAN (LUB BRAKU ZMIAN):")
    st.text_area("Według pacjenta:")
    st.text_area("Według terapeuty [z odniesieniem do konceptualizacji problemu pacjenta]:")

    st.text_area("Zastosowane strategie „zapobiegania nawrotom” i zalecenia dla pacjenta:")
    st.text_area("TRUDNOŚCI, KTÓRE WYSTĄPIŁY PODCZAS TERAPII [z odniesieniem do konceptualizacji problemu pacjenta]:")
    st.text_area("RELACJA TERAPEUTYCZNA [ocena czynników wpływających na jej jakość występujących zarówno ze strony pacjenta jak i terapeuty]:")

    st.divider()
    st.title("IV. PODSUMOWANIE TERAPII – WNIOSKI")
    st.text_area("[Podsumowanie całości procesu diagnostycznego i terapeutycznego może stanowić zapis terapii...]", height=200)
    st.text_area("LITERATURA [z jakich materiałów teoretycznych korzystałam/em planując i prowadząc terapię tego pacjenta]:")

# ==========================================================
# ARCHIWUM
# ==========================================================
elif menu == "📂 Archiwum":
    st.title("Baza Terapii")
    st.info("Tutaj pojawią się zapisani pacjenci. (Funkcja wymaga bazy danych).")
