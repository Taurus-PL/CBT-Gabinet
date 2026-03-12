import streamlit as st
import pandas as pd
import re

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Zapis Przebiegu Terapii CBT", layout="wide")

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
        st.text_input("Terapeuta")
        st.text_input("Pacjent (inicjały lub imię)")
        st.radio("Płeć", ["K", "M"], horizontal=True)
    with col2:
        st.number_input("Wiek", min_value=0, max_value=120, step=1)
        st.date_input("Czas terapii od")
        st.date_input("do")
    
    col3, col4 = st.columns(2)
    with col3:
        st.number_input("Liczba odbytych sesji", min_value=0, step=1)
    with col4:
        st.radio("Terapia:", ["zakończona", "w trakcie", "przerwana"], horizontal=True)
        
    st.text_area("Uwagi: (np. pytania do superwizji, informacje o załączonych nagraniach sesji)")
    
    st.header("Autorefleksja przed superwizją:")
    st.text_area("Co jest problemem w pracy z tym pacjentem - na jakie pytania chciał/a/bym uzyskać odpowiedź?")
    st.text_area("Jeśli został sformułowany problem pacjenta (diagnoza kliniczna – czy przejrzałam/em materiały dotyczące terapii poznawczo-behawioralnej w tym problemie – literatura, materiały z zajęć?)")
    st.text_area("Czy pacjent jest bezpieczny – czy mam dane dotyczące ryzyka samobójstwa, zachowań ryzykownych?")
    st.text_area("Czy znam model teoretyczny najlepiej opisujący problem pacjenta?")
    st.text_area("Czy w konceptualizacji uwzględniłam/em mechanizmy - procesy podtrzymujące problem pacjenta?")
    st.text_area("Na którą z moich interwencji pacjent zareagował najlepiej? Czy mam pomysł dlaczego?")
    st.text_area("Na którą z moich interwencji pacjent zareagował najgorzej? Czy mam pomysł dlaczego?")
    st.text_area("Jak oceniam relację terapeutyczną i z jakimi zjawiskami w tej relacji mam trudność?")
    st.text_area("Jak wygląda moje własne ABC na myśl o (superwizji) terapii tego pacjenta?")

# ==========================================================
# I. PIERWSZY ETAP TERAPII
# ==========================================================
elif menu == "I. Pierwszy Etap Terapii":
    st.title("I. PIERWSZY ETAP TERAPII")
    
    st.header("I.1. OGÓLNA DIAGNOZA KLINICZNA:")
    st.text_area("Zgłaszane problemy, powód przyjścia", help="[Jest to miejsce na krótki opis powodu zgłoszenia się do terapii, tak jak podaje go pacjent. Warto opisać sformułowaną przez pacjenta skargę...]")
    st.text_area("Informacje ogólne (dane z wywiadu: wykształcenie, sytuacja zawodowa, rodzinna, materialna, prawna, historia leczenia)", help="[Należy podać informacje uzyskane podczas wywiadu klinicznego...]")
    st.text_area("Badanie stanu psychicznego, diagnoza nozologiczna", help="[W tym miejscu powinien się znaleźć zapis badania stanu psychicznego...]")
    
    st.subheader("Diagnoza wstępna [według ICD lub DSM]:")
    st.text_input("Zaburzenie dominujące w obrazie klinicznym")
    st.text_input("Zaburzenia współwystępujące")
    st.text_input("Zaburzenia osobowości")
    st.text_input("Choroby somatyczne")
    
    st.write("Ogólne funkcjonowanie w sferze:")
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1: st.text_input("‒ rodzinnej (relacje z bliskimi)")
    with col_f2: st.text_input("‒ zawodowej/ szkolnej")
    with col_f3: st.text_input("‒ społecznej")
    
    st.text_area("Uwaga: jeśli w trakcie terapii w wyniku uzyskania nowych danych rozpoznanie zostało zmienione lub uzupełnione, należy to opisać.")
    
    st.divider()
    st.header("I.2. WYODRĘBNIENIE PROBLEMÓW DO TERAPII")
    st.text_area("Typowe aktualne problemy i trudne sytuacje (lista problemów)", help="[Przy każdym z problemów warto podać jego nasilenie – np. dyskomfort na skali 0-10 lub 0-100]")
    st.caption("[Pytania pomocnicze: czy lista problemów odzwierciedla objawy z kryteriów diagnostycznych? Czy coś się nie zgadza? Co należy uwzględnić w diagnozie różnicowej?]")
    
    st.text_area("PROBLEM DOMINUJĄCY WYBRANY DO KONCEPTUALIZACJI", help="[należy zwrócić uwagę i przeanalizować ewentualne niespójności...]")
    st.text_input("[Pytanie pomocnicze 1: Co byłoby MIARĄ rozwiązania/ustąpienia problemu?]")
    st.text_area("[Pytanie pomocnicze 2: Jakie sytuacje w ciągu ubiegłego tygodnia stanowią najlepszą ilustrację PROBLEMU?]")
    st.text_area("[Pytanie pomocnicze 3: Której z tych sytuacji pacjent chciałby się przyjrzeć bliżej z powodu „C”...]")

    st.divider()
    st.header("I.3. KONCEPTUALIZACJA")
    st.subheader("Model poznawczy i/lub behawioralny problemu pacjenta")
    st.caption("[Konceptualizacja – tworzenie modelu rozumienia problemu pacjenta... Poniższy zapis uwzględnia niezbędne składowe...]")
    
    st.write("**PIERWSZY POZIOM KONCEPTUALIZACJI POZNAWCZO-BEHAWIORALNEJ: ABC**")
    st.caption("Automatyczne myśli, emocje i zachowania przedstawione na konkretnym przykładzie...")
    
    st.text_input("Sytuacja ilustrująca problem:")
    st.text_input("A - Czynnik wyzwalający:")
    st.text_area("B - Automatyczne myśli:")
    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1: st.text_area("C - Emocje:")
    with col_c2: st.text_area("C - Objawy fizjologiczne:")
    with col_c3: st.text_area("C - Zachowanie:")
    
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
    st.header("I.4 Cele terapii") # Poprawiłem numerację zgodnie z sensem formularza (w oryginale błędne I.2)
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
    with col_c1: st.text_area("Według pacjenta:")
    with col_c2: st.text_area("Według terapeuty:")
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
