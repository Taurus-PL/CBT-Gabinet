import streamlit as st
import pandas as pd

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
                "style B fill:#002b5e,stroke:#3399ff,color:#fff\n"
                "style C fill:#002b5e,stroke:#3399ff,color:#fff\n"
            )
        },
        {
            "Model": "Model Aktywacji Behawioralnej - BA (C. Martell / P. Lewinsohn)",
            "Opis": "Depresja jako wynik spadku wzmocnień pozytywnych ze środowiska. Obniżony nastrój prowadzi do wycofania, co pogłębia brak wzmocnień.",
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
    "F40.1": [
        {
            "Model": "Model Lęku Społecznego (Clark i Wells)",
            "Opis": "Koncentracja uwagi na sobie, tworzenie negatywnego obrazu siebie jako obiektu społecznego, silne zachowania zabezpieczające.",
            "Interwencje": "Trening uwagi na zewnątrz (task-concentration), wideo-feedback, eksperymenty ze zrzucaniem zachowań zabezpieczających.",
            "Wizualizacja": (
                "graph TD\n"
                "A[Sytuacja społeczna] --> B[Zagrożenie społeczzne]\n"
                "B --> C[Skupienie uwagi na sobie]\n"
                "C <--> D[Objawy somatyczne i poznawcze]\n"
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
            "Interwencje": "Restrukturyzacja przekonań o odpowiedzialności, ciasto odpowiedzialności, edukacja o naturze myśli.",
            "Wizualizacja": (
                "graph TD\n"
                "A[Wyzwalacz] --> B[Natrętna myśl / Obraz]\n"
                "B --> C{Nadmierna Odpowiedzialność}\n"
                "C --> D[Silny Lęk i Poczucie Winy]\n"
                "D --> E[Kompulsje i Unikanie]\n"
                "E --> F[Chwilowa ulga]\n"
                "F -. Wzmocnia wiarę w odpowiedzialność .-> C\n"
                "style C fill:#4d004d,stroke:#cc00cc,color:#fff\n"
            )
        }
    ],
    "F41.1": [
        {
            "Model": "Model Nietolerancji Niepewności (M. Dugas)",
            "Opis": "Zamartwianie się jako unikający styl radzenia sobie z lękiem. Pacjent uważa, że niepewność jest nie do zniesienia.",
            "Interwencje": "Trening rozwiązywania problemów, ekspozycja na wyobrażenia, rozwój tolerancji na niepewność.",
            "Wizualizacja": (
                "graph TD\n"
                "A[Sytuacja o niepewnym wyniku] --> B{Nietolerancja Niepewności}\n"
                "B --> C[Zamartwianie się - próba zyskania pewności]\n"
                "C --> D[Iluzja kontroli]\n"
                "C --> E[Spadek umiejętności rozwiązywania problemów]\n"
                "style B fill:#4d4d00,stroke:#cccc00,color:#fff\n"
            )
        }
    ],
    "F43.1": [
        {
            "Model": "Przedłużona Ekspozycja - PE (E. Foa)",
            "Opis": "PTSD wynika z niepełnego przetworzenia wspomnień traumatycznych z powodu silnego unikania.",
            "Interwencje": "Ekspozycja wyobrażeniowa (nagrywanie i słuchanie), ekspozycja in vivo na unikane obiekty.",
            "Wizualizacja": (
                "graph TD\n"
                "A[Doświadczenie Traumatyczne] --> B[Silny Lęk warunkowy]\n"
                "B --> C[Unikanie bodźców i wspomnień]\n"
                "C --> D[Brak przetwarzania emocjonalnego]\n"
                "D -- Podtrzymanie lęku --> B\n"
                "style C fill:#003366,stroke:#006699,color:#fff\n"
            )
        }
    ],
    "F45.2": [
        {
            "Model": "Poznawczy model lęku o zdrowie (Salkovskis i Warwick)",
            "Opis": "Błędna interpretacja łagodnych, normalnych objawów płynących z ciała jako bezspornego dowodu na poważną, zagrażającą życiu chorobę.",
            "Interwencje": "Reatrybucja poznawcza, eksperymenty ze skanowaniem ciała, powstrzymanie poszukiwania zapewnień (np. u lekarzy, w internecie).",
            "Wizualizacja": (
                "graph TD\n"
                "A[Wyzwalacz np. informacja / doznanie] --> B[Zauważenie objawu z ciała]\n"
                "B --> C{Katastroficzna interpretacja: To rak!}\n"
                "C --> D[Silny lęk o własne życie i zdrowie]\n"
                "D --> E[Skanowanie ciała / Dr Google / Lekarze]\n"
                "E --> F[Chwilowa ulga i upewnienie]\n"
                "F -. Zwiększa czujność i lęk .-> B\n"
                "style C fill:#800040,stroke:#cc0066,color:#fff\n"
            )
        }
    ],
    "F51": [
        {
            "Model": "Model 3P Bezsenności (A. Spielman)",
            "Opis": "Bezsenność pojawia się i utrzymuje przez 3 grupy czynników: Predysponujące (np. lękowa osobowość), Wyzwalające (stres) i Podtrzymujące (złe nawyki senne).",
            "Interwencje": "Restrykcja snu, kontrola bodźców, higiena snu, techniki relaksacyjne.",
            "Wizualizacja": (
                "graph TD\n"
                "A[Czynniki Predysponujące np. geny, skłonność do lęku] --> B[Czynniki Wyzwalające np. stres w pracy]\n"
                "B --> C[Ostra Bezsenność]\n"
                "C --> D[Czynniki Podtrzymujące np. drzemki, leżenie w łóżku bez snu, zamartwianie się]\n"
                "D --> E[Przewlekła Bezsenność]\n"
                "E -- Błędne koło --> D\n"
                "style D fill:#1a1a1a,stroke:#4d4d4d,color:#fff\n"
            )
        }
    ],
    "F50.2": [
        {
            "Model": "Transdiagnostyczny model zaburzeń odżywiania (C. Fairburn)",
            "Opis": "Rdzeniem zaburzenia jest nadmierne uzależnienie samooceny od wagi i sylwetki, co prowadzi do drastycznych restrykcji, a w konsekwencji do napadów objadania się i zachowań kompensacyjnych.",
            "Interwencje": "Monitorowanie odżywiania, planowanie regularnych posiłków, restrukturyzacja przekonań o ciele i wadze, praca nad samooceną.",
            "Wizualizacja": (
                "graph TD\n"
                "A[Nadmierna koncentracja na sylwetce i wadze] --> B[Restrykcyjne zasady dietetyczne]\n"
                "B --> C[Złamanie zasad / Narastające napięcie]\n"
                "C --> D[Napad objadania się]\n"
                "D --> E[Zachowania kompensacyjne np. wymioty, przeczyszczanie]\n"
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

# --- BAZA ASYSTENTA DIAGNOZY ---
baza_symptomow = [
    {
        "slowa_kluczowe": ["serce mi wali", "zaraz umrę", "uduszę", "brakuje mi tchu", "zawał", "tracę kontrolę", "zwariuję", "kłuci", "duszno", "miękną", "nagle mnie łapie", "paniki", "zawał"], 
        "diagnoza": "F41.0 Zaburzenie lękowe z napadami lęku (Lęk paniczny)", 
        "roznicowa": "Agorafobia (F40.0), PTSD (F43.1), Zaburzenia kardiologiczne.",
        "cbt_problemy": "LĘK PANICZNY:\n- Poznawcze: Katastroficzna interpretacja normalnych doznań płynących z ciała.\n- Emocjonalne: Napady nagłego lęku.\n- Fizjologiczne: Silne pobudzenie wegetatywne.\n- Behawioralne: Unikanie sytuacji wyzwalających.",
        "cele_smart": "1. Zmniejszenie częstotliwości napadów paniki do 0 w skali miesiąca.\n2. Identyfikacja i eliminacja min. 2 głównych zachowań zabezpieczających.",
        "protokol_nazwa": "Terapia Poznawcza lęku panicznego wg D. Clarka",
        "uzasadnienie_planu": "Cele będą osiągane przez:\n1) Psychoedukację.\n2) Reatrybucję poznawczą doznań z ciała (eksperymenty behawioralne).\n3) Ekspozycję na bodźce interoceptywne."
    },
    {
        "slowa_kluczowe": ["nie mam siły", "nie ciesz", "nie chce mi się żyć", "budzę się w nocy", "płacz", "beznadziej", "apetyt", "bez sensu", "spać", "wegetuj", "czarna dziura", "smut", "przygnęb"], 
        "diagnoza": "F32 Epizod depresyjny / F33 Zab. depresyjne nawracające", 
        "roznicowa": "ChAD - epizod depresyjny (F31), Dystymia (F34.1), Niedoczynność tarczycy.",
        "cbt_problemy": "ZESPÓŁ DEPRESYJNY:\n- Poznawcze: Negatywna triada Becka.\n- Emocjonalne: Obniżony nastrój, anhedonia.\n- Fizjologiczne: Spadek energii, zaburzenia snu.\n- Behawioralne: Wycofanie z relacji społecznych, bierność.",
        "cele_smart": "1. Zwiększenie aktywności celowej i sprawiającej przyjemność do min. 3 razy w tygodniu.\n2. Zapisywanie min. 2 myśli dziennie w Tabeli Becka.",
        "protokol_nazwa": "Aktywacja Behawioralna (BA) / Terapia Poznawcza Depresji A. Becka",
        "uzasadnienie_planu": "Cele będą osiągane przez:\n1) Monitorowanie aktywności.\n2) Planowanie aktywności (przyjemność i mistrzostwo).\n3) Restrukturyzację poznawczą."
    },
    {
        "slowa_kluczowe": ["sprawdz", "myję", "głupie myśli", "nie mogę przestać", "policz", "coś się stanie", "rytuał", "zapesz", "natrętn"], 
        "diagnoza": "F42 Zaburzenie obsesyjno-kompulsyjne (OCD)", 
        "roznicowa": "Osobowość anankastyczna (F60.5), Schizofrenia (F20).",
        "cbt_problemy": "ZABURZENIE OBSESYJNO-KOMPULSYJNE:\n- Poznawcze: Myśli natrętne, fuzja myśli z działaniem (TAF).\n- Emocjonalne: Silny lęk po intruzji.\n- Fizjologiczne: Napięcie.\n- Behawioralne: Rytuały (kompulsje).",
        "cele_smart": "1. Stopniowe wydłużanie czasu powstrzymywania się od rytuału po wystąpieniu intruzji.\n2. Przeprowadzenie 3 eksperymentów ERP w tygodniu.",
        "protokol_nazwa": "Ekspozycja z Powstrzymaniem Reakcji (ERP)",
        "uzasadnienie_planu": "Cele będą osiągane przez:\n1) Hierarchię lęku i ekspozycję.\n2) Powstrzymywanie reakcji kompulsywnych.\n3) Restrukturyzację poznawczą."
    },
    {
        "slowa_kluczowe": ["odezwa", "patrzą", "wstyd", "wyśmiej", "czerwon", "ludzi", "kompromit", "ocen", "zbłaźni"], 
        "diagnoza": "F40.1 Fobia społeczna", 
        "roznicowa": "Osobowość unikająca (F60.6).",
        "cbt_problemy": "LĘK SPOŁECZNY:\n- Poznawcze: Skupienie uwagi na sobie.\n- Emocjonalne: Ostry lęk przed i w trakcie ekspozycji.\n- Fizjologiczne: Czerwienienie się, drżenie.\n- Behawioralne: Unikanie lub znoszenie z lękiem sytuacji społecznych.",
        "cele_smart": "1. Inicjowanie krótkiej rozmowy min. 2x w tygodniu.\n2. Porzucenie 1 zachowania zabezpieczającego.",
        "protokol_nazwa": "Terapia Poznawcza Lęku Społecznego wg Clarka i Wellsa",
        "uzasadnienie_planu": "Cele będą osiągane przez:\n1) Trening koncentracji zadaniowej.\n2) Eksperymenty behawioralne.\n3) Wideo-feedback."
    },
    {
        "slowa_kluczowe": ["martwi", "co będzie jak", "rozluźni", "napię", "scenariusz", "a co jeśli", "kark", "stres"], 
        "diagnoza": "F41.1 Zaburzenie lękowe uogólnione (GAD)", 
        "roznicowa": "Lęk paniczny (F41.0), Fobia społeczna (F40.1).",
        "cbt_problemy": "LĘK UOGÓLNIONY (ZAMARTWIANIE SIĘ):\n- Poznawcze: Nietolerancja niepewności, czarne scenariusze.\n- Emocjonalne: Wolnopłynący lęk.\n- Fizjologiczne: Uporczywe napięcie mięśniowe.\n- Behawioralne: Poszukiwanie zapewnień, overplanning.",
        "cele_smart": "1. Ograniczenie martwienia się do czasu na martwienie (max 20 min dziennie).\n2. Zmniejszenie uśrednionego napięcia poprzez relaksację.",
        "protokol_nazwa": "Protokół Nietolerancji Niepewności / MCT",
        "uzasadnienie_planu": "Cele będą osiągane przez:\n1) Trening odraczania martwienia się.\n2) Zmianę przekonań na temat martwienia.\n3) Rozwiązywanie problemów."
    },
    {
        "slowa_kluczowe": ["śni", "wspomnien", "przed oczami", "unikam", "krzyk", "flashback", "traum", "wypad", "gwałt"], 
        "diagnoza": "F43.1 Zaburzenie stresowe pourazowe (PTSD)", 
        "roznicowa": "Ostra reakcja na stres (F43.0).",
        "cbt_problemy": "ZABURZENIE POTRAUMATYCZNE:\n- Poznawcze: Poczucie aktualnego zagrożenia.\n- Emocjonalne: Przerażenie, odrętwienie.\n- Fizjologiczne: Chroniczna hiperreaktywność.\n- Behawioralne: Unikanie myśli, emocji i wyzwalaczy.",
        "cele_smart": "1. Odsłuchiwanie narracji traumatycznej aż do spadku lęku.\n2. Odwiedzenie 2 unikanych, bezpiecznych miejsc w ciągu miesiąca.",
        "protokol_nazwa": "Przedłużona Ekspozycja (PE)",
        "uzasadnienie_planu": "Cele będą osiągane przez:\n1) Ekspozycję wyobrażeniową.\n2) Ekspozycję in vivo.\n3) Restrukturyzację punktów zapalnych."
    },
    {
        "slowa_kluczowe": ["badam", "internet", "lekarz", "rak", "dr google", "zachoruj", "guz", "chorob"],
        "diagnoza": "F45.2 Hipochondria (Zaburzenie z lękiem o zdrowie)",
        "roznicowa": "Lęk paniczny (F41.0), Zaburzenia somatyzacyjne (F45.0).",
        "cbt_problemy": "LĘK O ZDROWIE:\n- Poznawcze: Katastroficzna interpretacja normalnych sygnałów z ciała.\n- Emocjonalne: Lęk, frustracja.\n- Fizjologiczne: Objawy somatyczne nasilone przez stres.\n- Behawioralne: Skanowanie ciała, poszukiwanie zapewnień u lekarzy.",
        "cele_smart": "1. Całkowite powstrzymanie się od sprawdzania objawów w internecie.\n2. Zmniejszenie skanowania ciała do 2x dziennie.",
        "protokol_nazwa": "CBT Lęku o Zdrowie wg Salkovskisa",
        "uzasadnienie_planu": "Cele będą osiągane przez:\n1) Eksperymenty behawioralne ze skanowaniem.\n2) Zablokowanie zachowań zabezpieczających.\n3) Restrukturyzację poznawczą."
    },
    {
        "slowa_kluczowe": ["nie mogę spać", "budzę się", "leżę i myślę", "płytki sen", "wybudzam", "zasnąć", "zmęczeni", "drzemk", "sufit", "tabletki nasenne", "bezsen"],
        "diagnoza": "F51 Nieorganiczne zaburzenia snu (Bezsenność)",
        "roznicowa": "Depresja (F32), GAD (F41.1), Bezsenność organiczna, Bezdech senny.",
        "cbt_problemy": "BEZSENNOŚĆ:\n- Poznawcze: Lęk przed bezsennością ('jak nie zasnę, to jutro zawalę w pracy'), ciągłe monitorowanie snu.\n- Emocjonalne: Frustracja, złość, lęk związany ze zbliżającą się porą snu.\n- Fizjologiczne: Zmęczenie, brak koncentracji w ciągu dnia, nadmierne wzbudzenie układu nerwowego wieczorem.\n- Behawioralne: Spędzanie nadmiernej ilości czasu w łóżku, drzemki w ciągu dnia, używanie łóżka do innych aktywności (TV, praca).",
        "cele_smart": "1. Zwiększenie wydajności snu (Sleep Efficiency) do min. 85% w ciągu 4 tygodni.\n2. Zmniejszenie czasu zasypiania (SOL) do poniżej 30 minut.\n3. Eliminacja drzemek w ciągu dnia całkowicie w ciągu 1 tygodnia.",
        "protokol_nazwa": "Poznawczo-Behawioralna Terapia Bezsenności (CBT-I)",
        "uzasadnienie_planu": "Cele będą osiągane przez:\n1) Zastosowanie techniki restrykcji snu (skrócenie czasu spędzanego w łóżku do faktycznego czasu snu).\n2) Kontrolę bodźców (łóżko służy tylko do snu i seksu, wstawanie z łóżka w przypadku braku snu przez 20 min).\n3) Restrukturyzację poznawczą dysfunkcjonalnych przekonań dotyczących snu i jego braku."
    },
    {
        "slowa_kluczowe": [
            "napad", "obżarst", "popłyn", "ciąg", "lodówk", 
            "pochłan", "kontrol", "zajad", "wilcz", 
            "wymiot", "rzyg", "zwraca", "wyrzuc", 
            "gardł", "przeczyszcz", "tablet", 
            "senes", "ćwicz", "siłown", "głodów",
            "grub", "nienawidz", "brzydz", 
            "śmieć", "wstyd", "wyrzut", 
            "przyty", "obsesj", "wag", 
            "lustr", "schudn", "jedzen"
        ],
        "diagnoza": "F50.2 Żarłoczność psychiczna (Bulimia)",
        "roznicowa": "Anoreksja z napadami objadania (F50.0), Zaburzenie z napadami objadania się (BED), Depresja nietypowa.",
        "cbt_problemy": "ZABURZENIA ODŻYWIANIA:\n- Poznawcze: Uzależnienie samooceny od wagi i sylwetki, myślenie dychotomiczne ('wszystko albo nic' w diecie).\n- Emocjonalne: Wstyd, poczucie winy, lęk przed przytyciem, obrzydzenie do siebie.\n- Fizjologiczne: Zaburzenia elektrolitowe, wahania wagi, uszkodzenia szkliwa (przy wymiotach), wyczerpanie.\n- Behawioralne: Restrykcje dietetyczne, napady objadania się (utrata kontroli), zachowania kompensacyjne (wymioty, środki przeczyszczające, intensywne ćwiczenia).",
        "cele_smart": "1. Wprowadzenie regularnego planu posiłków (3 główne, 2 przekąski) od najbliższego tygodnia.\n2. Zmniejszenie częstotliwości napadów objadania się i wymiotów do 1 na tydzień w ciągu pierwszego miesiąca.\n3. Ograniczenie ważenia się do maksymalnie 1 razu w tygodniu.",
        "protokol_nazwa": "Transdiagnostyczna Terapia CBT Zaburzeń Odżywiania (CBT-E) wg C. Fairburna",
        "uzasadnienie_planu": "Cele będą osiągane przez:\n1) Psychoedukację na temat fizjologicznych skutków restrykcji (błędne koło: restrykcje -> głód -> napad -> wymioty).\n2) Bieżące monitorowanie spożywanych posiłków, napadów i zachowań kompensacyjnych (dzienniczek pacjenta).\n3) Restrukturyzację poznawczą nakierowaną na poszerzenie bazy do budowania samooceny (oderwanie jej wyłącznie od wagi/sylwetki)."
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

# --- INICJALIZACJA KLUCZY UI ---
if 'ui_problemy' not in st.session_state:
    st.session_state.ui_problemy = ""
if 'ui_cele' not in st.session_state:
    st.session_state.ui_cele = ""
if 'ui_protokol' not in st.session_state:
    st.session_state.ui_protokol = ""
if 'ui_uzasadnienie' not in st.session_state:
    st.session_state.ui_uzasadnienie = ""

# --- FUNKCJE SYNCHRONIZUJĄCE INTERFEJS Z PAMIĘCIĄ ---
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
                
                st.session_state.ui_problemy = st.session_state.lista_problemow
                st.session_state.ui_cele = st.session_state.cele_terapii
                st.session_state.ui_protokol = st.session_state.wybrany_protokol
                st.session_state.ui_uzasadnienie = st.session_state.uzasadnienie_planu
            else:
                st.warning("Wpisz najpierw to, co zgłasza pacjent!")

    c1, c2 = st.columns(2)
    kat_wybrana = c1.selectbox("Grupa ICD-10:", list(icd10_full.keys()))
    pelna_diagnoza = c2.selectbox("Rozpoznanie główne potwierdzone ręcznie:", icd10_full[kat_wybrana])
    kod_icd = pelna_diagnoza.split(" ")[0]
    inne_rozpoznania = st.text_input("Inne rozpoznania (np. somatyczne, psychiatryczne współwystępujące):")

    # WIEDZA EBM I MODELE CBT
    st.divider()
    st.header(f"🧩 Poznawczo-behawioralne modele: {pelna_diagnoza}")
    
    if kod_icd in slownik_modeli:
        modele = slownik_modeli[kod_icd]
        st.info(f"Znaleziono {len(modele)} kluczowe, oparte na dowodach (EBM) modele dla tego zaburzenia.")
        
        for dane in modele:
            nazwa_modelu = dane["Model"]
            st.markdown(f"### 🛠️ {nazwa_modelu}")
            st.write(f"**Mechanizm:** {dane['Opis']}")
            st.write(f"**Główne interwencje:** {dane['Interwencje']}")
            
            if "Wizualizacja" in dane:
                with st.expander(f"ZOBACZ SCHEMAT: {nazwa_modelu}"):
                    st.markdown(f"```mermaid\n{dane['Wizualizacja']}\n```")
    else:
        st.info("Brak szczegółowego modelu CBT w podręcznej bazie dla wybranego rozpoznania. Możesz oprzeć się na ogólnym protokole poznawczo-behawioralnym.")

    st.divider()
    st.header("I.3. Konceptualizacja problemu")
    
    st.subheader("I.3.1. Lista problemów i cele terapii")
    st.text_area(
        "Lista problemów (w ujęciu poznawczo-behawioralnym)", 
        key="ui_problemy", 
        on_change=sync_problemy, 
        height=250
    )
    st.text_area(
        "Cele terapii (zoperacjonalizowane, mierzalne, SMART)", 
        key="ui_cele", 
        on_change=sync_cele, 
        height=150
    )

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
        key="ui_protokol",
        on_change=sync_protokol
    )
    
    st.text_area(
        "Uzasadnienie poznawczo-behawioralne (w jaki sposób wybrane interwencje zrealizują postawione cele):", 
        key="ui_uzasadnienie",
        on_change=sync_uzasadnienie,
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
