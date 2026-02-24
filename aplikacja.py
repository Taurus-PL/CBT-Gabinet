import streamlit as st
import pandas as pd

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Zapis Przebiegu Terapii CBT", layout="wide")

# --- BAZA WIEDZY I DIAGRAMY MERMAID ---
slownik_modeli = {
    "F41.0": {
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
    },
    "F32": {
        "Model": "Triada Poznawcza Becka / Model Aktywacji Behawioralnej (Martell)",
        "Opis": "Negatywna wizja siebie, świata i przyszłości. Spadek wzmocnień pozytywnych z otoczenia.",
        "Interwencje": "Monitorowanie aktywności, Aktywacja behawioralna (BA), restrukturyzacja myśli.",
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
    "F40.1": {
        "Model": "Model Lęku Społecznego (Clark i Wells)",
        "Opis": "Koncentracja uwagi na sobie, tworzenie negatywnego obrazu siebie, silne zachowania zabezpieczające.",
        "Interwencje": "Trening uwagi na zewnątrz (task-concentration), wideo-feedback, eksperymenty.",
        "Wizualizacja": (
            "graph TD\n"
            "A[Sytuacja społeczna] --> B[Zagrożenie społeczne]\n"
            "B --> C[Skupienie uwagi na sobie]\n"
            "C <--> D[Objawy somatyczne i poznawcze]\n"
            "C <--> E[Zachowania zabezpieczające]\n"
            "D <--> E\n"
            "style C fill:#663300,stroke:#ff9900,color:#fff\n"
        )
    },
    "F42": {
        "Model": "Model poznawczy OCD (P. Salkovskis)",
        "Opis": "Przesadne poczucie odpowiedzialności (TAF). Myśl natrętna jest interpretowana jako realne zagrożenie.",
        "Interwencje": "ERP (Ekspozycja z powstrzymaniem reakcji), restrukturyzacja przekonań o odpowiedzialności.",
        "Wizualizacja": (
            "graph TD\n"
            "A[Sytuacja wyzwalająca] --> B[Natrętna myśl / Obraz]\n"
            "B --> C{Zagrożenie / Odpowiedzialność}\n"
            "C --> D[Lęk i Dyskomfort]\n"
            "D --> E[Kompulsje i Rytuały]\n"
            "E --> F[Chwilowa ulga]\n"
            "F -. Wzmocnienie .-> B\n"
            "style C fill:#4d004d,stroke:#cc00cc,color:#fff\n"
        )
    },
    "F41.1": {
        "Model": "Model Nietolerancji Niepewności (Dugas) / Metapoznawczy (Wells)",
        "Opis": "Zamartwianie się jako unikający styl radzenia sobie z lękiem oraz metaprzekonania.",
        "Interwencje": "Trening rozwiązywania problemów, ekspozycja na wyobrażenia, zmiana metaprzekonań.",
        "Wizualizacja": (
            "graph TD\n"
            "A[Sytuacja niepewna] --> B[Nietolerancja niepewności]\n"
            "B --> C[Pozytywne przekonania o martwieniu]\n"
            "C --> D[ZAMARTWIANIE SIĘ]\n"
            "D --> E[Negatywne przekonania / Lęk przed martwieniem]\n"
            "D --> F[Nieskuteczne unikanie]\n"
            "style D fill:#4d4d00,stroke:#cccc00,color:#fff\n"
        )
    },
    "F43.1": {
        "Model": "Model poznawczy PTSD (Ehlers i Clark)",
        "Opis": "Poczucie aktualnego zagrożenia wynikające z negatywnej oceny traumy i zaburzeń pamięci autobiograficznej.",
        "Interwencje": "Przedłużona ekspozycja (PE), restrukturyzacja punktów zapalnych, zmiana zachowań zabezpieczających.",
        "Wizualizacja": (
            "graph TD\n"
            "A[Wyzwalacze traumy] --> B[Wrażenie: To dzieje się teraz]\n"
            "B --> C[Silny lęk i emocje]\n"
            "C --> D[Unikanie i dysocjacja]\n"
            "D -. Brak przetworzenia traumy .-> B\n"
            "style C fill:#004d4d,stroke:#00cccc,color:#fff\n"
        )
    }
}
slownik_modeli["F33"] = slownik_modeli["F32"]

# --- BAZA ASYSTENTA DIAGNOZY (Słownik NLP + Profil CBT + Cele SMART + Protokoły EBM) ---
baza_symptomow = [
    {
        "slowa_kluczowe": ["serce mi wali", "zaraz umrę", "uduszę się", "brakuje mi tchu", "zawał", "tracę kontrolę", "zwariuję", "kłucie w klatce", "duszno", "miękną mi nogi", "nagle mnie łapie", "atak paniki", "myślałem że to zawał", "nogi z waty", "zaraz zemdleję", "ścisk w gardle", "jakbym był obok siebie", "odrealnienie", "nagle robi mi się słabo", "uderzenie gorąca"], 
        "diagnoza": "F41.0 Zaburzenie lękowe z napadami lęku (Lęk paniczny)", 
        "roznicowa": "Agorafobia (F40.0), PTSD (F43.1), Zaburzenia kardiologiczne, Nadczynność tarczycy.",
        "cbt_problemy": "LĘK PANICZNY:\n- Poznawcze: Katastroficzna interpretacja normalnych doznań płynących z ciała (np. 'mam zawał', 'uduszę się', 'zwariuję').\n- Emocjonalne: Napady nagłego, obezwładniającego lęku (panika).\n- Fizjologiczne: Silne pobudzenie wegetatywne (tachykardia, duszności, zawroty głowy, hiperwentylacja).\n- Behawioralne: Unikanie sytuacji wyzwalających, stosowanie zachowań zabezpieczających (np. noszenie leków, ciągłe sprawdzanie pulsu).",
        "cele_smart": "1. Zmniejszenie częstotliwości napadów paniki do 0 w skali miesiąca.\n2. Identyfikacja i eliminacja min. 2 głównych zachowań zabezpieczających (np. noszenie przy sobie wody/leków uspokajających) w ciągu 4 tygodni.\n3. Obniżenie subiektywnego poziomu lęku przed objawami somatycznymi (np. kołatanie serca) z 9/10 do 3/10 w sytuacjach spoczynkowych.",
        "protokol_nazwa": "Terapia Poznawcza lęku panicznego wg D. Clarka / Panic Control Treatment (PCT) D. Barlowa",
        "uzasadnienie_planu": "Cele będą osiągane przez:\n1) Psychoedukację dot. błędnego koła paniki w celu redukcji początkowego lęku przed objawami.\n2) Reatrybucję poznawczą doznań z ciała wspartą eksperymentami behawioralnymi (np. celowa hiperwentylacja), aby dowieść, że doznania nie prowadzą do zawału/uduszenia.\n3) Ekspozycję na bodźce interoceptywne przy jednoczesnej stopniowej eliminacji zachowań zabezpieczających."
    },
    {
        "slowa_kluczowe": ["nie mam siły", "nic mnie nie cieszy", "nie chce mi się żyć", "budzę się w nocy", "płaczę bez powodu", "jestem beznadziejny", "nie mam apetytu", "wszystko jest bez sensu", "ciągle chce mi się spać", "zmuszam się do", "nic nie ma sensu", "poczucie winy", "smutek", "zrezygnowany", "przytłumione", "po co w ogóle wstawać", "ciało jest ciężkie", "mokry koc", "ponad siły", "jestem do niczego", "zawsze tak będzie", "radość gdzieś za szybą", "nie mam energii udawać", "rozsypuje się", "wegetuję", "czarna dziura", "pustka", "robię minimum"], 
        "diagnoza": "F32 Epizod depresyjny / F33 Zab. depresyjne nawracające", 
        "roznicowa": "ChAD - epizod depresyjny (F31), Dystymia (F34.1), Niedoczynność tarczycy.",
        "cbt_problemy": "ZESPÓŁ DEPRESYJNY:\n- Poznawcze: Negatywna triada Becka (pesymistyczne przekonania o sobie: 'jestem do niczego', o świecie: 'nikt mnie nie rozumie' i o przyszłości: 'zawsze tak będzie'), nadmierne ruminacje.\n- Emocjonalne: Utrzymujący się obniżony nastrój, anhedonia (brak zdolności odczuwania radości), poczucie winy, odrętwienie.\n- Fizjologiczne: Wyraźny spadek energii ('ciało jak mokry koc'), zaburzenia snu (np. wczesne wybudzanie), zmiany apetytu, ociężałość psychomotoryczna.\n- Behawioralne: Zaniechanie aktywności celowej, wycofanie z relacji społecznych, bierność (pozostawanie w łóżku/domu).",
        "cele_smart": "1. Zwiększenie aktywności celowej i sprawiającej przyjemność (np. spacer, hobby) z 0 do min. 3 razy w tygodniu (czas trwania: 30 min).\n2. Redukcja czasu spędzanego bezproduktywnie w łóżku w ciągu dnia z [aktualna ilość] do max. 1 godziny na dobę.\n3. Identyfikacja i zapisywanie min. 2 negatywnych myśli automatycznych dziennie w dzienniku myśli (Tabela Becka) przez najbliższe 2 tygodnie.",
        "protokol_nazwa": "Aktywacja Behawioralna (BA) wg C. Martella / Terapia Poznawcza Depresji A. Becka",
        "uzasadnienie_planu": "Cele będą osiągane przez:\n1) Monitorowanie aktywności i nastroju, co pozwoli zidentyfikować deficyt wzmocnień pozytywnych w środowisku.\n2) Planowanie aktywności z naciskiem na działania dające poczucie przyjemności i mistrzostwa (przerwanie cyklu 'działanie na podstawie obniżonego nastroju').\n3) Restrukturyzację poznawczą: wyłapywanie NMA i błędów poznawczych w celu podważenia pesymistycznej triady Becka."
    },
    {
        "slowa_kluczowe": ["muszę to sprawdzić", "ciągle myję", "głupie myśli", "nie mogę przestać o tym myśleć", "muszę policzyć", "mam wrażenie że coś się stanie", "natrętne", "rytuał", "robię to żeby nie zapeszyć", "ciągle wraca ta myśl", "czuję brud", "układam", "muszę ułożyć", "inaczej zwariuję", "zarazki", "coś złego się stanie jak", "odliczam w myślach", "magiczne myślenie", "czuję że muszę", "chore myśli", "muszę mieć pewność"], 
        "diagnoza": "F42 Zaburzenie obsesyjno-kompulsyjne (OCD)", 
        "roznicowa": "Osobowość anankastyczna (F60.5), Schizofrenia (F20), Tiki (F95).",
        "cbt_problemy": "ZABURZENIE OBSESYJNO-KOMPULSYJNE:\n- Poznawcze: Występowanie myśli/obrazów natrętnych (obsesji), fuzja myśli z działaniem (TAF), wyolbrzymione poczucie odpowiedzialności za zapobieganie szkodzie.\n- Emocjonalne: Silny lęk i napięcie po pojawieniu się intruzji, poczucie winy, czasem obrzydzenie.\n- Fizjologiczne: Pobudzenie wegetatywne będące reakcją na wyzwalacz/obsesję.\n- Behawioralne: Rytuały jawne i ukryte (kompulsje) mające na celu redukcję lęku, ciągłe poszukiwanie zapewnień ze strony innych, unikanie bodźców.",
        "cele_smart": "1. Stopniowe wydłużanie czasu powstrzymywania się od rytuału (kompulsji) po wystąpieniu intruzji z 0 do min. 30 minut w ciągu 2 tygodni.\n2. Całkowita redukcja zachowań upewniających się (pytanie bliskich 'czy na pewno nic się nie stało?') do zera w perspektywie miesiąca.\n3. Przeprowadzenie 3 udanych eksperymentów ERP (Ekspozycja i Powstrzymanie Reakcji) w tygodniu z zapisanym spadkiem lęku na skali SUDs.",
        "protokol_nazwa": "Ekspozycja z Powstrzymaniem Reakcji (ERP) z elementami poznawczymi wg P. Salkovskisa",
        "uzasadnienie_planu": "Cele będą osiągane przez:\n1) Stworzenie hierarchii lęku i stopniową, zaplanowaną ekspozycję na bodźce wyzwalające intruzje/obsesje.\n2) Konsekwentne powstrzymywanie reakcji kompulsywnych (rytuałów i uników), co pozwoli na habituację lęku i zerwanie sprzężenia zwrotnego.\n3) Restrukturyzację poznawczą ukierunkowaną na zniekształcenia takie jak fuzja myśl-działanie (TAF) i nadmierna odpowiedzialność."
    },
    {
        "slowa_kluczowe": ["boję się odezwać", "wszyscy na mnie patrzą", "spalę się ze wstydu", "wyśmieją mnie", "robię się czerwony", "boję się ludzi", "trzęsą mi się ręce jak", "kompromitacja", "boję się co pomyślą", "wypaść głupio", "wzrok innych", "wystąpienia publiczne", "zrobię z siebie pośmiewisko", "zablokuje mnie", "pustka w głowie jak", "nie wiem gdzie podziać ręce", "boję się oceny", "wymsknie mi się coś głupiego", "głos mi drży", "czuję że mnie oceniają"], 
        "diagnoza": "F40.1 Fobia społeczna", 
        "roznicowa": "Osobowość unikająca (F60.6), Agorafobia (F40.0).",
        "cbt_problemy": "LĘK SPOŁECZNY:\n- Poznawcze: Skupienie uwagi na sobie (tworzenie i monitorowanie negatywnego obrazu własnego 'ja'), przewidywanie negatywnej oceny przez otoczenie ('wyśmieją mnie').\n- Emocjonalne: Ostry lęk przed i w trakcie ekspozycji społecznej, poczucie wstydu i zakłopotania.\n- Fizjologiczne: Czerwienienie się, drżenie rąk/głosu, nadmierna potliwość, suchość w ustach, tachykardia.\n- Behawioralne: Unikanie (izolacja) lub znoszenie z silnym lękiem sytuacji społecznych, zachowania zabezpieczające (np. brak kontaktu wzrokowego, zaciskanie rąk, chowanie się w tle).",
        "cele_smart": "1. Inicjowanie krótkiej (min. 2 minuty) rozmowy na tematy codzienne z wybraną osobą min. 2x w tygodniu.\n2. Świadome porzucenie 1 zachowania zabezpieczającego (np. ciągłego sprawdzania telefonu w sytuacjach społecznych) w trakcie ekspozycji.\n3. Przeniesienie uwagi z analizowania siebie na bodźce zewnętrzne (trening koncentracji zadaniowej) w 3 trudnych sytuacjach w tygodniu.",
        "protokol_nazwa": "Terapia Poznawcza Lęku Społecznego wg Clarka i Wellsa",
        "uzasadnienie_planu": "Cele będą osiągane przez:\n1) Trening przesunięcia uwagi (Task Concentration Training) z bolesnej samoobserwacji na otoczenie zewnętrzne.\n2) Eksperymenty behawioralne w sytuacjach społecznych (z porzuceniem zachowań zabezpieczających), mające na celu falsyfikację przekonań o kompromitacji.\n3) Zastosowanie wideo-feedbacku w celu urealnienia wewnętrznego, wyolbrzymionego obrazu własnego lęku (np. nagranie wystąpienia i obiektywna ocena widoczności objawów)."
    },
    {
        "slowa_kluczowe": ["ciągle się martwię", "co będzie jak", "nie mogę się rozluźnić", "mam spięte mięśnie", "najgorsze scenariusze", "a co jeśli", "boli mnie kark", "niepokój", "czuję takie napięcie", "nie umiem przestać myśleć o problemach", "martwię się o zdrowie", "martwię się o bliskich", "czarne scenariusze", "nie potrafię odpuścić", "ścisk w żołądku ze stresu", "głowa mi pęka od myślenia", "myśli krążą", "zawsze muszę być przygotowany", "wieczne napięcie", "jak na szpilkach", "natłok myśli"], 
        "diagnoza": "F41.1 Zaburzenie lękowe uogólnione (GAD)", 
        "roznicowa": "Lęk paniczny (F41.0), Fobia społeczna (F40.1), Hipochondria (F45.2).",
        "cbt_problemy": "LĘK UOGÓLNIONY (ZAMARTWIANIE SIĘ):\n- Poznawcze: Chroniczne zamartwianie się ('a co jeśli...'), nietolerancja niepewności, tworzenie czarnych scenariuszy, dodatnie i ujemne przekonania o martwieniu się.\n- Emocjonalne: Wolnopłynący lęk, chroniczne poczucie niepokoju, drażliwość.\n- Fizjologiczne: Uporczywe napięcie mięśniowe (np. bóle karku), uczucie 'bycia na krawędzi', ścisk w żołądku, trudności z koncentracją i snem.\n- Behawioralne: Nadmierne poszukiwanie informacji/zapewnień, overplanning (przesadne planowanie w celu redukcji niepewności), unikanie delegowania zadań innym.",
        "cele_smart": "1. Ograniczenie martwienia się do wyznaczonego „czasu na martwienie” (max 20 minut dziennie o stałej porze) przy użyciu techniki odraczania.\n2. Zmniejszenie uśrednionego poziomu napięcia wolnopłynącego z 8/10 do 4/10 w skali tygodnia poprzez trening relaksacji mięśniowej (PMR).\n3. Rezygnacja z pytania bliskich o zdanie (poszukiwanie upewnień) przy podejmowaniu 3 codziennych, drobnych decyzji w tygodniu.",
        "protokol_nazwa": "Protokół Nietolerancji Niepewności (M. Dugas) / Terapia Metapoznawcza (MCT) A. Wellsa",
        "uzasadnienie_planu": "Cele będą osiągane przez:\n1) Trening odraczania martwienia się w celu odzyskania poczucia kontroli nad tym procesem.\n2) Restrukturyzację poznawczą metaprzekonań na temat martwienia się (zarówno dodatnich, np. 'martwienie mnie chroni', jak i ujemnych, np. 'od tego zwariuję').\n3) Ekspozycję wyobrażeniową na najgorsze scenariusze (rozwijanie skryptów) oraz trening rozwiązywania realnych problemów."
    },
    {
        "slowa_kluczowe": ["ciągle mi się to śni", "wspomnienia wracają", "mam przed oczami", "unikam miejsc", "budzę się z krzykiem", "odkąd zdarzył się ten wypadek", "flashbacki", "czuję jakby to działo się znowu", "od tamtej pory", "trauma", "wraca jak bumerang", "koszmary z tamtego", "wystarczy jeden dźwięk", "ciągle na krawędzi", "unikam wszystkiego co", "nie czuję się już bezpiecznie", "odrętwienie", "czuję że to znowu się dzieje"], 
        "diagnoza": "F43.1 Zaburzenie stresowe pourazowe (PTSD)", 
        "roznicowa": "Ostra reakcja na stres (F43.0), Zaburzenia adaptacyjne (F43.2).",
        "cbt_problemy": "ZABURZENIE POTRAUMATYCZNE:\n- Poznawcze: Poczucie ciągłego, aktualnego zagrożenia pomimo ustania bodźca, natrętne wspomnienia (intruzje/flashbacki), negatywne przekonania o świecie i własnej skuteczności.\n- Emocjonalne: Przerażenie w reakcji na triggery, silny gniew, poczucie winy, odrętwienie emocjonalne.\n- Fizjologiczne: Chroniczna hiperreaktywność, wzmożony odruch orientacyjny, zaburzenia snu i koszmary.\n- Behawioralne: Unikanie myśli, emocji i rozmów związanych z traumą, unikanie zewnętrznych wyzwalaczy (ludzi, miejsc, dźwięków), nadmierna czujność.",
        "cele_smart": "1. Odtworzenie pełnej narracji traumatycznej i codzienne jej odsłuchiwanie/czytanie (Ekspozycja Wyobrażeniowa) aż do spadku lęku poniżej 4/10.\n2. Odwiedzenie 2 obiektywnie bezpiecznych, a dotąd unikanych miejsc (związanych z wydarzeniem) w ciągu miesiąca.\n3. Urealnienie min. 1 skrajnego przekonania wygenerowanego przez traumę (np. 'nigdzie nie jestem bezpieczny') na bardziej wyważone.",
        "protokol_nazwa": "Przedłużona Ekspozycja (PE) E. Foa / Model Ehlers i Clarka",
        "uzasadnienie_planu": "Cele będą osiągane przez:\n1) Przeprowadzenie ekspozycji wyobrażeniowej (relacjonowanie traumy w czasie teraźniejszym), co doprowadzi do habituacji i przetworzenia śladów pamięciowych.\n2) Zaplanowaną ekspozycję in vivo na bezpieczne, ale unikane dotąd bodźce, miejsca i sytuacje (wygaszanie reakcji warunkowej).\n3) Restrukturyzację poznawczą 'punktów zapalnych' traumy i zmianę negatywnych przekonań utrzymujących poczucie aktualnego zagrożenia."
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

# --- BAZA DANYCH W PAMIĘCI I STAN APLIKACJI ---
if 'baza_terapii' not in st.session_state:
    st.session_state.baza_terapii = []
if 'lista_problemow' not in st.session_state:
    st.session_state.lista_problemow = ""
if 'cele_terapii' not in st.session_state:
    st.session_state.cele_terapii = ""
if 'wybrany_protokol' not in st.session_state:
    st.session_state.wybrany_protokol = ""
if 'uzasadnienie_planu' not in st.session_state:
    st.session_state.uzasadnienie_planu = ""
if 'wykryte_kody' not in st.session_state:
    st.session_state.wykryte_kody = []

# --- MENU BOCZNE ---
st.sidebar.title("🛡️ Zapis Terapii CBT")
menu = st.sidebar.radio("Spis treści:", [
    "I. Diagnoza i Konceptualizacja", 
    "II. Plan i Interwencje", 
    "III. Podsumowanie",
    "📂 Archiwum Diagnoz"
])
st.sidebar.divider()
st.sidebar.caption("Oparte na: Zapis przebiegu terapii CBT")

# ==========================================================
# MODUŁ I: DIAGNOZA I KONCEPTUALIZACJA ZJAWISKA
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
    
    # ASYSTENT DIAGNOZY
    with st.expander("🤖 Asystent Diagnozy (NLP)", expanded=True):
        st.write("Wpisz objawy językiem pacjenta. System wypełni: Listę Problemów, Cele SMART oraz protokoły EBM w zakładce II.")
        objawy_input = st.text_area("Cytaty pacjenta / Skarga główna:")
        
        if st.button("🔍 Analizuj i przygotuj dokumentację"):
            st.session_state.wykryte_kody = []
            wykryte_problemy_cbt = []
            wykryte_cele = []
            wykryte_protokoly_nazwy = []
            wykryte_uzasadnienia = []
            
            if objawy_input:
                znaleziono = False
                input_do_analizy = objawy_input.lower()
                
                for el in baza_symptomow:
                    if any(fraza in input_do_analizy for fraza in el["slowa_kluczowe"]):
                        kod_glowny = el['diagnoza'].split(" ")[0]
                        st.session_state.wykryte_kody.append(kod_glowny)
                        wykryte_problemy_cbt.append(el['cbt_problemy'])
                        wykryte_cele.append(el['cele_smart'])
                        wykryte_protokoly_nazwy.append(el['protokol_nazwa'])
                        wykryte_uzasadnienia.append(el['uzasadnienie_planu'])
                        
                        st.success(f"🎯 **Wykryto element:** {el['diagnoza']}")
                        st.warning(f"⚖️ **Diagnoza różnicowa:** {el['roznicowa']}")
                        znaleziono = True
                        
                if znaleziono:
                    st.session_state.lista_problemow = "\n\n".join(wykryte_problemy_cbt)
                    st.session_state.cele_terapii = "\n\n".join(wykryte_cele)
                    st.session_state.wybrany_protokol = " + ".join(wykryte_protokoly_nazwy)
                    st.session_state.uzasadnienie_planu = "\n\n".join(wykryte_uzasadnienia)
                else:
                    st.info("Brak oczywistych dopasowań. Puste szablony wygenerowane.")
                    st.session_state.lista_problemow = "OBSZAR POZNAWCZY:\n- \n\nOBSZAR EMOCJONALNY:\n- \n\nOBSZAR FIZJOLOGICZNY:\n- \n\nOBSZAR BEHAWIORALNY:\n- "
                    st.session_state.cele_terapii = "1. [Wpisz cel SMART - co? o ile? w jakim czasie?]\n2. [Wpisz cel SMART]"
                    st.session_state.wybrany_protokol = "[Wpisz nazwę protokołu, np. Terapia Poznawcza Becka]"
                    st.session_state.uzasadnienie_planu = "1) [Wpisz interwencję nr 1...]\n2) [Wpisz interwencję nr 2...]"
            else:
                st.warning("Wpisz najpierw to, co zgłasza pacjent!")

    c1, c2 = st.columns(2)
    kat_wybrana = c1.selectbox("Grupa ICD-10:", list(icd10_full.keys()))
    pelna_diagnoza = c2.selectbox("Rozpoznanie główne potwierdzone ręcznie:", icd10_full[kat_wybrana])
    kod_icd = pelna_diagnoza.split(" ")[0]
    inne_rozpoznania = st.text_input("Inne rozpoznania (np. somatyczne, psychiatryczne współwystępujące):")

    # WIEDZA EBM I ŁĄCZENIE MODELI CBT
    st.divider()
    st.header("🧩 Modułowe łączenie modeli CBT")
    
    lista_wszystkich_modeli = [dane["Model"] for dane in slownik_modeli.values()]
    kody_do_nazw = {kod: dane["Model"] for kod, dane in slownik_modeli.items()}
    nazwy_do_kodow = {dane["Model"]: kod for kod, dane in slownik_modeli.items()}
    
    kody_sugerowane = set(st.session_state.wykryte_kody)
    if kod_icd in slownik_modeli:
        kody_sugerowane.add(kod_icd)
        
    modele_sugerowane = [kody_do_nazw[k] for k in kody_sugerowane if k in kody_do_nazw]

    wybrane_modele = st.multiselect(
        "Wybierz modele do uwzględnienia w konceptualizacji:",
        options=list(set(lista_wszystkich_modeli)),
        default=modele_sugerowane
    )
    
    if wybrane_modele:
        for nazwa_modelu in wybrane_modele:
            kod = nazwy_do_kodow[nazwa_modelu]
            dane = slownik_modeli[kod]
            
            st.markdown(f"### 🛠️ {nazwa_modelu}")
            st.write(f"**Mechanizm:** {dane['Opis']}")
            st.write(f"**Główne interwencje:** {dane['Interwencje']}")
            
            if "Wizualizacja" in dane:
                with st.expander(f"ZOBACZ SCHEMAT: {nazwa_modelu}"):
                    st.markdown(f"```mermaid\n{dane['Wizualizacja']}\n```")

    st.divider()
    st.header("I.3. Konceptualizacja problemu")
    
    st.subheader("I.3.1. Lista problemów i cele terapii")
    st.text_area("Lista problemów (w ujęciu poznawczo-behawioralnym)", key="lista_problemow", height=250)
    st.text_area("Cele terapii (zoperacjonalizowane, mierzalne, SMART)", key="cele_terapii", height=150)

    # NOWOŚĆ: Wyświetlanie sugerowanego protokołu od razu pod celami!
    if st.session_state.wybrany_protokol:
        st.success(f"📚 **Sugerowany protokół leczenia w oparciu o który będzie prowadzona praca nad realizacją celów:**\n\n**{st.session_state.wybrany_protokol}**\n\n*(Pełne uzasadnienie i plan interwencji zostały automatycznie przeniesione do zakładki 'II. Plan i Interwencje' w menu bocznym).*")

    st.subheader("I.3.2. Poziom pierwszy (Sytuacja bieżąca - przekrój poprzeczny)")
    st.text_area("Sytuacja (typowa sytuacja ilustrująca problem)")
    c3, c4 = st.columns(2)
    with c3:
        st.text_area("Myśli automatyczne / Obrazy")
        st.text_area("Emocje (rodzaj i nasilenie)")
    with c4:
        st.text_area("Doznania z ciała (fizjologiczne)")
        st.text_area("Zachowanie (w tym zachowania zabezpieczające/unikające)")

    st.subheader("I.3.3. Poziom drugi (Mechanizmy podtrzymujące i Przekonania)")
    st.text_area("Przekonania kluczowe (o sobie, innych, świecie)")
    st.text_area("Przekonania warunkowe (Założenia / Zasady / Postawy)")
    st.text_area("Strategie radzenia sobie (kompensacyjne)")

    st.subheader("I.3.4. Historia uczenia się (Profil rozwojowy)")
    st.text_area("Wydarzenia z przeszłości i wczesne doświadczenia kształtujące schematy")
    st.text_area("Zdarzenia wyzwalające (Czynniki spustowe wystąpienia obecnego epizodu)")

    st.divider()
    st.header("I.4. Zasoby pacjenta")
    st.text_area("Mocne strony, wsparcie społeczne, umiejętności, inteligencja, motywacja itp.")

    if st.button("💾 Zapisz Diagnozę i Konceptualizację"):
        st.session_state.baza_terapii.append({"Pacjent": imie, "Wiek": wiek, "Kod ICD": kod_icd, "Diagnoza": pelna_diagnoza})
        st.success("Zapisano do Archiwum!")

# ==========================================================
# MODUŁ II: PLAN TERAPII I INTERWENCJE
# ==========================================================
elif menu == "II. Plan i Interwencje":
    st.title("II. Plan terapii i interwencje")
    
    st.header("II.1. Plan terapii (Uzasadnienie EBM)")
    
    st.text_input(
        "Sugerowany protokół oparty na dowodach naukowych (EBM) do pracy nad realizacją celów:", 
        key="wybrany_protokol"
    )
    
    st.text_area(
        "Uzasadnienie poznawczo-behawioralne (w jaki sposób wybrane interwencje zrealizują postawione cele):", 
        key="uzasadnienie_planu", 
        height=150
    )
    
    st.divider()
    st.header("II.2. Zapis przebiegu poszczególnych sesji")
    st.info("Tutaj dokumentuj krótko kolejne spotkania: datę, główne interwencje, zadania domowe i wnioski.")
    st.text_area("Rejestr sesji (np. Sesja 1 [Data] - Psychoedukacja i BA...)", height=300)

# ==========================================================
# MODUŁ III: PODSUMOWANIE I EWALUACJA
# ==========================================================
elif menu == "III. Podsumowanie":
    st.title("III. Podsumowanie i Ewaluacja Terapii")
    
    st.header("III.1. Osiągnięte cele terapii")
    col1, col2 = st.columns(2)
    with col1:
        st.text_area("Według pacjenta")
    with col2:
        st.text_area("Według terapeuty (odniesienie do celów z I.3.1)")

    st.header("III.2. Zidentyfikowane mechanizmy zmiany")
    st.text_area("Co dokładnie pomogło pacjentowi? (np. zmiana przekonania X, zaprzestanie unikania Y)")

    st.header("III.3. Zapobieganie nawrotom")
    st.text_area("Sygnały ostrzegawcze i plan radzenia sobie z nawrotem objawów")

    st.header("III.4. Literatura")
    st.text_area("Materiały, protokoły i książki wykorzystane do pracy z pacjentem")

# ==========================================================
# MODUŁ IV: ARCHIWUM
# ==========================================================
elif menu == "📂 Archiwum Diagnoz":
    st.title("Baza Terapii i Filtrowanie")
    
    if not st.session_state.baza_terapii:
        st.warning("Baza jest pusta. Dodaj pacjenta w zakładce I.")
    else:
        df = pd.DataFrame(st.session_state.baza_terapii)
        lista_diagnoz = ["Wszystkie"] + list(df['Kod ICD'].unique())
        wybrany_kod = st.selectbox("Filtruj bazę według diagnozy:", lista_diagnoz)
        
        if wybrany_kod != "Wszystkie":
            df = df[df['Kod ICD'] == wybrany_kod]
            
        st.dataframe(df, use_container_width=True)
