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
            "Wizualizacja": "graph TD\nA((Myśli O SOBIE)) <--> B((Myśli O ŚWIECIE))\nB <--> C((Myśli O PRZYSZŁOŚCI))\nC <--> A\nstyle A fill:#002b5e,stroke:#3399ff,color:#fff\n"
        },
        {
            "Model": "Model Aktywacji Behawioralnej - BA",
            "Opis": "Depresja jako wynik spadku wzmocnień pozytywnych ze środowiska.",
            "Interwencje": "Monitorowanie aktywności, planowanie aktywności (przyjemność i mistrzostwo).",
            "Wizualizacja": "graph TD\nA[Stresory / Spadek wzmocnień] --> B[Obniżony nastrój / Brak energii]\nB --> C[Wycofanie / Bierność / Ruminacje]\nC --> D[Jeszcze mniej wzmocnień i więcej problemów]\nD -- Błędne koło --> B\nstyle C fill:#333333,stroke:#666666,color:#fff\n"
        }
    ],
    "F50.2": [
        {
            "Model": "Transdiagnostyczny model zaburzeń odżywiania (C. Fairburn)",
            "Opis": "Rdzeniem zaburzenia jest nadmierne uzależnienie samooceny od wagi i sylwetki, co prowadzi do restrykcji, napadów i kompensacji.",
            "Interwencje": "Monitorowanie odżywiania, planowanie regularnych posiłków, restrukturyzacja przekonań o ciele i wadze.",
            "Wizualizacja": "graph TD\nA[Koncentracja na sylwetce i wadze] --> B[Restrykcje dietetyczne]\nB --> C[Złamanie zasad / Narastające napięcie]\nC --> D[Napad objadania się]\nD --> E[Zachowania kompensacyjne np. wymioty]\nD --> F[Poczucie winy i lęk przed tyciem]\nE --> F\nF -- Wzmacnia kontrolę --> A\nstyle A fill:#004d40,stroke:#00695c,color:#fff\n"
        }
    ],
    "F40.1": [
        {
            "Model": "Model poznawczy fobii społecznej (Clark i Wells)",
            "Opis": "Lęk przed negatywną oceną prowadzi do skupienia uwagi na sobie (self-focus) i stosowania zachowań zabezpieczających.",
            "Interwencje": "Przenoszenie uwagi na zewnątrz, eksperymenty behawioralne, rezygnacja z zachowań zabezpieczających.",
            "Wizualizacja": "graph TD\nA[Sytuacja społeczna] --> B[Aktywacja założeń 'Wyśmieją mnie']\nB --> C[Postrzegane niebezpieczeństwo społeczne]\nC --> D[Skupienie uwagi na sobie]\nC --> E[Objawy somatyczne np. czerwienienie się]\nC --> F[Zachowania zabezpieczające]\nD --> C\nE --> C\nF --> C\nstyle C fill:#4d0000,stroke:#ff3333,stroke-width:2px,color:#fff\n"
        }
    ],
    "F42": [
        {
            "Model": "Model poznawczy OCD (P. Salkovskis)",
            "Opis": "Kluczem nie jest myśl intruzowa, ale nadanie jej katastroficznego znaczenia (hiperodpowiedzialność).",
            "Interwencje": "Ekspozycja z powstrzymaniem reakcji (ERP), praca z fuzją myśli-działanie.",
            "Wizualizacja": "graph TD\nA[Myśl intruzowa / Wyobrażenie] --> B[Błędna interpretacja / Hiperodpowiedzialność]\nB --> C[Silny Lęk / Dyskomfort]\nC --> D[Kompulsje / Rytuały / Unikanie]\nD -- Przynosi krótką ulgę i podtrzymuje lęk --> A\nstyle B fill:#004d40,stroke:#00695c,color:#fff\n"
        }
    ],
    "F43.1": [
        {
            "Model": "Model poznawczy PTSD (Ehlers i Clark)",
            "Opis": "Utrzymujące się poczucie aktualnego zagrożenia wynika z negatywnej oceny traumy i niezintegrowanej pamięci o zdarzeniu.",
            "Interwencje": "Przedłużona ekspozycja (PE), praca z punktami węzłowymi traumy, restrukturyzacja znaczenia traumy.",
            "Wizualizacja": "graph TD\nA[Traumatyczne zdarzenie] --> B[Niezintegrowana pamięć o traumie]\nA --> C[Negatywna ocena traumy np. 'To moja wina']\nB --> D[Poczucie AKTUALNEGO zagrożenia]\nC --> D\nD --> E[Intruzje / Pobudzenie]\nD --> F[Strategie radzenia sobie / Unikanie]\nF -- Uniemożliwia przetwarzanie --> B\nF -- Wzmacnia oceny --> C\nstyle D fill:#4d0000,stroke:#ff3333,color:#fff\n"
        }
    ],
    "F51": [
        {
            "Model": "Model 3P Bezsenności (A. Spielman)",
            "Opis": "Bezsenność jest wynikiem 3 czynników: Predysponujących, Wyzwalających i Podtrzymujących.",
            "Interwencje": "CBT-I: Restrykcja czasu snu, kontrola bodźców (łóżko=sen), higiena snu.",
            "Wizualizacja": "graph TD\nA[Czynniki Predysponujące] --> B[Czynniki Wyzwalające np. stres]\nB --> C[Ostra bezsenność]\nC --> D[Czynniki Podtrzymujące np. leżenie w łóżku]\nD --> E[Przewlekła bezsenność]\nE -- Lęk przed nocą --> D\nstyle D fill:#002b5e,stroke:#3399ff,color:#fff\n"
        }
    ]
}

slownik_modeli["F33"] = slownik_modeli["F32"]
slownik_modeli["F50.0"] = slownik_modeli["F50.2"]

# --- DOKŁADNE KRYTERIA ICD-10 + SŁOWNIKI KLINICZNE ---
baza_symptomow = [
    {
        "diagnoza": "F43.1 Zaburzenie stresowe pourazowe (PTSD)",
        "roznicowa": "Ostra reakcja na stres, Zaburzenia adaptacyjne, Fobia społeczna, Depresja.",
        "icd10_kryteria": {
            "Kryterium A: Poczucie zagrożenia / Zdarzenie traumatyczne": {
                "icd10": "Narażenie na stresujące wydarzenie o wyjątkowo groźnym charakterze lub trwające poczucie bezpośredniego zagrożenia.",
                "slowa": ["wypadek", "śmierć", "gwałt", "napad", "pożar", "wojna", "traum", "zagrożeni", "przetrwać", "system alarmowy", "niebezpieczn", "coś się stanie"]
            },
            "Kryterium B: Intruzje i Flashbacki (Ponowne przeżywanie)": {
                "icd10": "Uporczywe przypominanie sobie traumy w postaci natrętnych wspomnień (flashbacków), poczucia że trauma dzieje się znów lub dysocjacji.",
                "slowa": ["flashback", "koszmar", "wraca", "obraz", "przed oczami", "jakby to", "budzę się", "żywo", "film", "znowu tam", "fragmenty", "odcinam", "wyłączyć", "robot"]
            },
            "Kryterium C: Unikanie i Pobudzenie (Hiperarousal)": {
                "icd10": "Faktyczne unikanie okoliczności przypominających stresor, odrętwienie emocjonalne oraz objawy nadmiernego wzbudzenia (wzmożona czujność).",
                "slowa": ["unikam", "nie chodzę", "nie myśl", "napięt", "czuwam", "wybuch", "zaskoczen", "hałas", "czujność", "skanuję", "wyjście", "odizolow", "płytko", "zamknięte"]
            }
        },
        "cele_smart": "1. Zmniejszenie częstotliwości intruzji/flashbacków.\n2. Przerwanie zachowań unikowych i ekspozycja na bodźce (in vivo).",
        "protokol_nazwa": "Przedłużona Ekspozycja (PE) lub Trauma-Focused CBT (Ehlers/Clark)",
        "uzasadnienie_planu": "Ekspozycja wyobrażeniowa (praca z pamięcią) i ekspozycja in vivo (przełamanie unikania i hiperczujności).",
        "profil_cbt": {
            "SYTUACJA": {"slowa": ["hałas", "zapach", "tłum", "samochód", "noc", "miejsce", "dźwięk", "głos"], "tlumaczenie": "Bodźce (triggery), które wyzwalają reakcję alarmową."},
            "MYŚLI": {"slowa": ["świat", "niebezpiecz", "nie ufam", "znowu", "nie dam rady", "zniszczon", "wina", "słab", "normaln", "coś się stanie"], "tlumaczenie": "Poczucie zagrożenia, negatywne oceny siebie i świata."},
            "EMOCJE": {"slowa": ["przeraż", "złość", "gniew", "wina", "wstyd", "odrętwien", "pustka", "bezradność"], "tlumaczenie": "Lęk, gniew, wstyd, dysocjacja (odcięcie)."},
            "CIAŁO": {"slowa": ["napięt", "skaczę", "serce", "pot", "bezdech", "spięt", "reakcj", "zimno", "spinają"], "tlumaczenie": "Wzbudzenie fizjologiczne, odruch zaskoczenia, zamrożenie (freeze)."},
            "ZACHOWANIE": {"slowa": ["unikam", "izoluj", "piję", "nie rozmaw", "sprawdzam", "chowam", "robot"], "tlumaczenie": "Unikanie sytuacji i myśli, hiperczujność, odcięcie emocjonalne."}
        }
    },
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
                "slowa": ["musz", "przymus", "głód", "ochot", "kontro", "obsesj", "pilnuj"]
            },
            "Kryterium C: Zachowania kompensacyjne": {
                "icd10": "Pacjent usiłuje przeciwdziałać tuczącym skutkom pokarmów przez wymioty, przeczyszczanie, głodówki, ćwiczenia.",
                "slowa": ["wymiot", "rzyg", "przeczyszcz", "senes", "ćwicz", "siłown", "głodów", "tablet", "kibel", "odkręcić"]
            },
            "Kryterium D: Zniekształcona samoocena": {
                "icd10": "Chorobliwa obawa przed otyłością; samoocena nadmiernie wyznaczana przez kształt i masę ciała.",
                "slowa": ["grub", "śmieć", "nienawidz", "brzydz", "waga", "wagę", "wagi", "lustr", "schudn", "diet", "wygląd", "ciało", "ocenę"]
            }
        },
        "cele_smart": "1. Wprowadzenie regularnego planu posiłków.\n2. Zmniejszenie częstotliwości napadów/wymiotów do 1/tydz.",
        "protokol_nazwa": "CBT-E wg C. Fairburna",
        "uzasadnienie_planu": "Psychoedukacja, dzienniczek myśli i reakcji, restrukturyzacja poznawcza i zmiana bazy samooceny.",
        "profil_cbt": {
            "SYTUACJA": {"slowa": ["wieczór", "samotn", "stres", "kłótni", "imprez", "lustrz"], "tlumaczenie": "Napięcie emocjonalne lub ekspozycja na bodźce (lustro, waga)."},
            "MYŚLI": {"slowa": ["grub", "śmieć", "nienawidz", "waga", "lustr", "schudn", "diet", "nigdy", "muszę", "zasady"], "tlumaczenie": "Uzależnienie samooceny od wagi, myślenie dychotomiczne."},
            "EMOCJE": {"slowa": ["wstyd", "wyrzut", "win", "lęk", "boję", "stres", "napięc"], "tlumaczenie": "Poczucie winy, wstyd po napadzie, silny lęk przed przytyciem."},
            "CIAŁO": {"slowa": ["zmęcz", "słab", "mdł", "zimn", "brzuch", "opuch"], "tlumaczenie": "Wyczerpanie fizyczne, dolegliwości gastryczne."},
            "ZACHOWANIE": {"slowa": ["napad", "obżarst", "lodówk", "pochłan", "wymiot", "rzyg", "przeczyszcz", "senes", "ćwicz", "głodów", "ograniczam"], "tlumaczenie": "Napady objadania się i zachowania kompensacyjne."}
        }
    },
    {
        "diagnoza": "F32 Epizod depresyjny",
        "roznicowa": "ChAD, Dystymia, Niedoczynność tarczycy.",
        "icd10_kryteria": {
            "Kryterium 1: Obniżony nastrój": {
                "icd10": "Obniżony nastrój, utrzymujący się przez większą część dnia, niemal codziennie, niepodlegający wpływowi wydarzeń zewnętrznych.",
                "slowa": ["smut", "przygnęb", "płacz", "pust", "dół", "płaka", "źle"]
            },
            "Kryterium 2: Anhedonia": {
                "icd10": "Wyraźna utrata zainteresowań i zdolności odczuwania radości w stosunku do aktywności, które zwykle sprawiały przyjemność.",
                "slowa": ["bez sensu", "nic nie czuj", "nie chce mi", "wegetuj", "zaniedb", "obojętn", "nie cieszy"]
            },
            "Kryterium 3: Brak energii": {
                "icd10": "Zmniejszona energia, szybsze męczenie się i spadek aktywności.",
                "slowa": ["zmęcz", "brak sił", "ociężał", "słab", "wyczerp", "leżę"]
            },
            "Kryterium 4: Zaburzenia poznawcze": {
                "icd10": "Spadek zaufania do siebie. Nieracjonalne poczucie winy i bezwartościowości.",
                "slowa": ["beznadziej", "nikim", "ciężar", "nie uda", "głup", "win", "przeze mnie"]
            },
            "Kryterium 5: Objawy somatyczne": {
                "icd10": "Zaburzenia snu wszelkiego typu (najczęściej wczesne wybudzanie) lub zmiany apetytu.",
                "slowa": [" spię", " śpię", " spać", " sen", " snu", "budz", "bezsenn", "apetyt"]
            }
        },
        "cele_smart": "1. Zwiększenie aktywności celowej (min. 3x w tyg).\n2. Zapisywanie myśli w Tabeli Becka.",
        "protokol_nazwa": "Aktywacja Behawioralna / Terapia Poznawcza Depresji",
        "uzasadnienie_planu": "Monitorowanie aktywności, testowanie myśli automatycznych.",
        "profil_cbt": {
            "SYTUACJA": {"slowa": ["rano", "wsta", "prac", "obowiąz", "problem", "poranek"], "tlumaczenie": "Konieczność podjęcia aktywności, wyzwania dnia codziennego."},
            "MYŚLI": {"slowa": ["beznadziej", "bez sensu", "nikim", "ciężar", "głup", "win", "czarn", "nigdy", "zawsze"], "tlumaczenie": "Negatywna triada Becka, generalizacja."},
            "EMOCJE": {"slowa": ["smut", "przygnęb", "płacz", "pust", "nic nie czuj", "znieczul", "płaka"], "tlumaczenie": "Obniżony nastrój, anhedonia, apatia."},
            "CIAŁO": {"slowa": [" spać", "zmęcz", "brak sił", "budzę", "apetyt", "ociężał"], "tlumaczenie": "Spadek energii, zaburzenia snu/apetytu."},
            "ZACHOWANIE": {"slowa": ["nie chce mi", "leżę", "wegetuj", "izoluj", "nie wychodz", "zaniedb"], "tlumaczenie": "Wycofanie, bierność behawioralna."}
        }
    },
    {
        "diagnoza": "F41.0 Lęk paniczny",
        "roznicowa": "Agorafobia, Zaburzenia kardiologiczne.",
        "icd10_kryteria": {
            "Kryterium A: Napady paniki": {
                "icd10": "Nawracające napady ciężkiego lęku (paniki), nieprzewidywalne.",
                "slowa": ["panik", "przeraż", "strach", "nagle", "atak"]
            },
            "Kryterium B: Objawy wegetatywne": {
                "icd10": "Nagłe wystąpienie objawów: palpitacje, duszności, zawroty głowy, poty.",
                "slowa": ["serce", "wali", "tchu", "duszno", "kłuci", "drż", "pocę", "miękną"]
            },
            "Kryterium C: Wtórny lęk": {
                "icd10": "Wtórny lęk przed śmiercią lub utratą kontroli nad sobą oraz unikanie sytuacji.",
                "slowa": ["umrę", "uduszę", "zawał", "zwariuję", "kontrol", "zemdlej", "uciekam", "unikam", "karetk", "sor"]
            }
        },
        "cele_smart": "1. Zmniejszenie częstotliwości napadów paniki do 0/m-c.\n2. Eliminacja zachowań zabezpieczających.",
        "protokol_nazwa": "Terapia Lęku Panicznego wg D. Clarka",
        "uzasadnienie_planu": "Reatrybucja doznań fizjologicznych, ekspozycja, eliminacja zachowań zabezpieczających.",
        "profil_cbt": {
            "SYTUACJA": {"slowa": ["tłum", "sklep", "kolejk", "autobus", "wysił", "samochód"], "tlumaczenie": "Miejsca zatłoczone, zamknięte przestrzenie."},
            "MYŚLI": {"slowa": ["umrę", "uduszę", "zawał", "zwariuję", "tracę kontrol", "zemdlej"], "tlumaczenie": "Katastroficzna interpretacja doznań z ciała."},
            "EMOCJE": {"slowa": ["panik", "przeraż", "strach", "lęk"], "tlumaczenie": "Nagły, silny lęk."},
            "CIAŁO": {"slowa": ["serce", "wali", "tchu", "duszno", "kłuci", "drż", "pocę", "miękną"], "tlumaczenie": "Silne pobudzenie wegetatywne."},
            "ZACHOWANIE": {"slowa": ["uciekam", "unikam", "karetk", "sor", "lekarz", "tablet", "woda"], "tlumaczenie": "Ucieczka z sytuacji, zachowania zabezpieczające."}
        }
    },
    {
        "diagnoza": "F40.1 Fobia społeczna",
        "roznicowa": "Lęk paniczny, Unikające zaburzenie osobowości, PTSD.",
        "icd10_kryteria": {
            "Kryterium A: Lęk przed oceną": {
                "icd10": "Wyraźna obawa przed znalezieniem się w centrum uwagi lub strach przed kompromitującym zachowaniem.",
                "slowa": ["oceni", "wyśmiej", "głupio", "patrzą", "krytyk", "zbłaźn", "kompromit", "uwagi"]
            },
            "Kryterium B: Unikanie sytuacji": {
                "icd10": "Unikanie sytuacji ekspozycji społecznej (np. jedzenie, przemawianie, spotkania towarzyskie).",
                "slowa": ["imprez", "spotkań", "ludzi", "wyjści", "wystąpień", "nie chodz", "odwoł"]
            },
            "Kryterium C: Objawy lęku w sytuacjach społ.": {
                "icd10": "Pojawienie się objawów lęku w obawianych sytuacjach, często zaczerwienienie twarzy, drżenie.",
                "slowa": ["czerwieni", "drż", "jąka", "pocę", "głos", "gorąc"]
            }
        },
        "cele_smart": "1. Rezygnacja z zachowań zabezpieczających podczas rozmowy.\n2. Wykonanie 3 eksperymentów behawioralnych (ekspozycji).",
        "protokol_nazwa": "Terapia Poznawcza Fobii Społecznej wg Clarka i Wellsa",
        "uzasadnienie_planu": "Przenoszenie uwagi z wewnątrz na zewnątrz, eksperymenty, restrukturyzacja założeń.",
        "profil_cbt": {
            "SYTUACJA": {"slowa": ["imprez", "ludzi", "spotka", "wystąp", "rozmow", "prezentacj"], "tlumaczenie": "Sytuacje ekspozycji na ocenę innych."},
            "MYŚLI": {"slowa": ["oceni", "wyśmiej", "głupio", "nudn", "dziwn", "zbłaźnię", "widzą", "zauważ"], "tlumaczenie": "Antycypacja negatywnej oceny, czytanie w myślach."},
            "EMOCJE": {"slowa": ["lęk", "wstyd", "stres", "spięt", "niepokój"], "tlumaczenie": "Lęk społeczny, zakłopotanie."},
            "CIAŁO": {"slowa": ["czerwieni", "drż", "pocę", "gorąc", "jąka", "głos"], "tlumaczenie": "Pobudzenie współczulne, widoczne objawy lęku."},
            "ZACHOWANIE": {"slowa": ["unikam", "odwoł", "nie odzyw", "telefon", "patrzę w dół"], "tlumaczenie": "Unikanie, zachowania zabezpieczające."}
        }
    },
    {
        "diagnoza": "F42 Zaburzenie obsesyjno-kompulsyjne (OCD)",
        "roznicowa": "Zaburzenia lękowe uogólnione, Schizofrenia, PTSD.",
        "icd10_kryteria": {
            "Kryterium A: Obsesje (myśli intruzowe)": {
                "icd10": "Występowanie obsesji (nawracających, nieprzyjemnych myśli, wyobrażeń), które są uznawane za własne, ale przeszkadzające.",
                "slowa": ["myśli", "obraz", "narzuc", "wbrew", "głowie", "zaraz", "brud", "zrobię krzywdę", "bluźnier"]
            },
            "Kryterium B: Kompulsje (czynności natrętne)": {
                "icd10": "Obecność kompulsji (rytuałów) - stereotypowych, wielokrotnie powtarzanych zachowań lub czynności umysłowych.",
                "slowa": ["myję", "sprawdz", "liczę", "rytuał", "muszę", "powtarz", "układ", "kilka razy"]
            },
            "Kryterium C: Redukcja napięcia": {
                "icd10": "Wykonywanie kompulsji służy zapobieżeniu mało prawdopodobnemu wydarzeniu lub redukcji lęku.",
                "slowa": ["ulg", "spokój", "przesta", "żeby nic", "zabezpiecz", "obaw", "inaczej"]
            }
        },
        "cele_smart": "1. Ograniczenie czasu rytuałów do X minut dziennie.\n2. Wykonanie ekspozycji bez reakcji zabezpieczającej.",
        "protokol_nazwa": "Ekspozycja z Powstrzymaniem Reakcji (ERP) / Model Salkovskisa",
        "uzasadnienie_planu": "ERP, edukacja o powszechności myśli intruzowych, praca z nadmierną odpowiedzialnością.",
        "profil_cbt": {
            "SYTUACJA": {"slowa": ["klamk", "brud", "nóż", "kuchn", "wyjści", "zamk", "gaz"], "tlumaczenie": "Wyzwalacze intruzji (brud, niebezpieczne przedmioty, wątpliwości)."},
            "MYŚLI": {"slowa": ["co jeśli", "zaraz", "zabiję", "może", "nie sprawdz", "wina", "odpowiedzial", "przeze mnie"], "tlumaczenie": "Fuzja myśli z działaniem, hiperodpowiedzialność."},
            "EMOCJE": {"slowa": ["lęk", "panik", "napięc", "wstręt", "obrzydzen", "niepokój"], "tlumaczenie": "Silny lęk i dyskomfort wywołany obsesją."},
            "CIAŁO": {"slowa": ["spięt", "napięt", "serce", "ból", "żołądek"], "tlumaczenie": "Pobudzenie z lęku."},
            "ZACHOWANIE": {"slowa": ["sprawdz", "myję", "liczę", "wracam", "pytam", "upewniam", "powtarz"], "tlumaczenie": "Rytuały jawne (mycie, sprawdzanie) i ukryte (liczenie w myślach)."}
        }
    },
    {
        "diagnoza": "F51 Nieorganiczna bezsenność",
        "roznicowa": "Bezsenność wtórna (depresja, lęk, PTSD), Zespół bezdechu sennego.",
        "icd10_kryteria": {
            "Kryterium A: Problemy ze snem": {
                "icd10": "Trudności w zasypianiu, utrzymaniu snu lub sen jest złej jakości (nie dający odpoczynku).",
                "slowa": ["zasnąć", "budzę", "sen", "zła jakość", "płytki", "wybudz"]
            },
            "Kryterium B: Częstotliwość": {
                "icd10": "Zaburzenia snu występują co najmniej 3 razy w tygodniu przez co najmniej 1 miesiąc.",
                "slowa": ["znowu", "często", "codzien", "tygodni", "miesiąc", "ciągle", "każdej nocy"]
            },
            "Kryterium C: Zaabsorbowanie i Lęk": {
                "icd10": "Nadmierne zaabsorbowanie bezsennością, lęk przed niemożnością zaśnięcia i jej skutkami w ciągu dnia.",
                "slowa": ["boję się że nie zasnę", "patrzę w sufit", "przewraca", "znowu nie", "jutro", "zmęczon", "tablet"]
            }
        },
        "cele_smart": "1. Zwiększenie wydajności snu powyżej 85%.\n2. Skrócenie czasu zasypiania do max 30 minut.",
        "protokol_nazwa": "Poznawczo-Behawioralna Terapia Bezsenności (CBT-I)",
        "uzasadnienie_planu": "Dzienniczek snu, Restrykcja snu, Kontrola bodźców, Restrukturyzacja poznawcza.",
        "profil_cbt": {
            "SYTUACJA": {"slowa": ["noc", "łóżk", "sypialn", "wieczór", "godzin", "ciemn"], "tlumaczenie": "Sytuacja kładzenia się do łóżka lub przebudzenie w nocy."},
            "MYŚLI": {"slowa": ["nie zasnę", "jutro", "masakr", "muszę spać", "ile godzin", "zniszczy"], "tlumaczenie": "Lęk antycypacyjny, wymuszanie snu, katastrofizowanie skutków niewyspania."},
            "EMOCJE": {"slowa": ["lęk", "stres", "frustracj", "złość", "bezradn"], "tlumaczenie": "Frustracja łóżkowa, niepokój."},
            "CIAŁO": {"slowa": ["rozbudzon", "gorąc", "zmęczon", "przebudz"], "tlumaczenie": "Hiperwzbudzenie somatyczne, brak naturalnej senności."},
            "ZACHOWANIE": {"slowa": ["przewracam", "patrzę w sufit", "telefon", "zegar", "drzemk", "leżę"], "tlumaczenie": "Leżenie w łóżku bez snu, zerkanie na zegarek, odesypianie (drzemki)."}
        }
    }
]

# --- PEŁNA BAZA ICD-10 ---
icd10_full = {
    "F00-F09 Zab. psychiczne organiczne": ["F00 Otępienie", "F01 Otępienie naczyniowe", "F06 Inne zab. wskutek uszkodzenia mózgu", "F07 Zaburzenia osobowości wskutek choroby mózgu"],
    "F10-F19 Zab. spowodowane substancjami": ["F10 Alkohol", "F11 Opioidy", "F12 Kanabinoidy", "F13 Leki uspokajające i nasenne", "F17 Palenie tytoniu"],
    "F20-F29 Schizofrenia i urojeniowe": ["F20 Schizofrenia", "F21 Zaburzenie schizotypowe", "F22 Zaburzenia urojeniowe", "F25 Zaburzenia schizoafektywne"],
    "F30-F39 Zaburzenia nastroju (afektywne)": ["F30 Epizod maniakalny", "F31 ChAD", "F32 Epizod depresyjny", "F33 Zab. depresyjne nawracające", "F34 Dystymia"],
    "F40-F48 Zaburzenia nerwicowe i lękowe": ["F40.0 Agorafobia", "F40.1 Fobia społeczna", "F40.2 Specyficzne fobie", "F41.0 Lęk paniczny", "F41.1 GAD", "F42 OCD", "F43.0 Ostra reakcja na stres", "F43.1 PTSD", "F43.2 Zab. adaptacyjne", "F44 Zaburzenia dysocjacyjne", "F45 Somatyzacyjne"],
    "F50-F59 Zespoły behawioralne": ["F50.0 Anoreksja", "F50.2 Bulimia", "F51 Nieorganiczna bezsenność", "F52 Dysfunkcje seksualne"],
    "F60-F69 Zaburzenia osobowości": ["F60.0 Paranoiczna", "F60.1 Schizoidalna", "F60.2 Dyssocjalna", "F60.30 Impulsywna", "F60.31 Borderline", "F60.4 Histrioniczna", "F60.5 Anankastyczna", "F60.6 Lękliwa (unikająca)", "F60.7 Zależna"],
    "F90-F98 Zaburzenia wieku dziecięcego": ["F90 ADHD", "F91 Zaburzenia zachowania", "F95 Tiki"]
}

# --- STANY APLIKACJI W PAMIĘCI ---
if 'baza_terapii' not in st.session_state: st.session_state.baza_terapii = []
if 'ui_problemy_html' not in st.session_state: st.session_state.ui_problemy_html = ""
if 'ui_cele' not in st.session_state: st.session_state.ui_cele = ""
if 'ui_protokol' not in st.session_state: st.session_state.ui_protokol = ""
if 'ui_uzasadnienie' not in st.session_state: st.session_state.ui_uzasadnienie = ""

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
                
                final_sytuacja = final_mysli = final_emocje = final_cialo = final_zachowanie = ""
                
                for choroba in baza_symptomow:
                    wynik_choroby = 0
                    
                    html_raport = f"<h4 style='color: #2c3e50;'>Analiza dla: {choroba['diagnoza']}</h4>\n"
                    
                    for nazwa_kryterium, dane_kryterium in choroba["icd10_kryteria"].items():
                        znalezione_dowody = [] 
                        
                        for rdzen in dane_kryterium["slowa"]:
                            for zdanie in zdania_pacjenta:
                                if rdzen.lower() in zdanie.lower() and zdanie not in znalezione_dowody:
                                    znalezione_dowody.append(zdanie)
                        
                        if znalezione_dowody:
                            wynik_choroby += len(znalezione_dowody) * 3 
                            dowody_html = "<br>".join([f"👉 <i>„{d}”</i>" for d in znalezione_dowody])
                            
                            html_raport += "<div style='border-left: 5px solid #28a745; padding: 12px; background-color: #f0fdf4; margin-bottom: 15px; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);'>\n"
                            html_raport += f"<h5 style='color: #155724; margin-top: 0;'>✅ SPEŁNIONE: {nazwa_kryterium}</h5>\n"
                            html_raport += f"<p style='font-size: 0.9em; color: #333; margin-bottom: 8px;'><b>Definicja ICD-10:</b> {dane_kryterium['icd10']}</p>\n"
                            html_raport += "<div style='padding: 8px; background-color: #d1e7dd; border-radius: 4px; color: #0f5132;'>\n"
                            html_raport += f"<b>Materiał dowodowy z wywiadu:</b><br>{dowody_html}\n"
                            html_raport += "</div></div>\n"
                        else:
                            html_raport += "<div style='border-left: 5px solid #dc3545; padding: 12px; background-color: #fdf2f2; margin-bottom: 15px; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);'>\n"
                            html_raport += f"<h5 style='color: #721c24; margin-top: 0;'>❌ BRAK DANYCH: {nazwa_kryterium}</h5>\n"
                            html_raport += f"<p style='font-size: 0.9em; color: #333; margin-bottom: 8px;'><b>Definicja ICD-10:</b> {dane_kryterium['icd10']}</p>\n"
                            html_raport += "<div style='padding: 8px; background-color: #f8d7da; border-radius: 4px; color: #842029;'>\n"
                            html_raport += "<i>Kryterium nieobecne w skardze. Wymaga dopytania podczas wywiadu.</i>\n"
                            html_raport += "</div></div>\n"

                    temp_sytuacja = temp_mysli = temp_emocje = temp_cialo = temp_zachowanie = ""
                    
                    slowa_z_tekstu = re.findall(r'\b\w+\b', input_lower)
                    for sfera, dane_sfery in choroba["profil_cbt"].items():
                        znalezione_slowa = []
                        for rdzen in dane_sfery["slowa"]:
                            for s in slowa_z_tekstu:
                                if rdzen.lower() in s.lower() and s not in znalezione_slowa: 
                                    znalezione_slowa.append(s)
                                    
                        if znalezione_slowa:
                            wynik_choroby += 1
                            format_tekstu = f"Wykryte słowa pacjenta: {', '.join(znalezione_slowa)}\n[Znaczenie CBT: {dane_sfery['tlumaczenie']}]"
                            if sfera == "SYTUACJA": temp_sytuacja = format_tekstu
                            elif sfera == "MYŚLI": temp_mysli = format_tekstu
                            elif sfera == "EMOCJE": temp_emocje = format_tekstu
                            elif sfera == "CIAŁO": temp_cialo = format_tekstu
                            elif sfera == "ZACHOWANIE": temp_zachowanie = format_tekstu

                    if wynik_choroby > najwyzszy_wynik:
                        najwyzszy_wynik = wynik_choroby
                        najlepsze_dopasowanie = choroba
                        najlepszy_html = html_raport
                        
                        final_sytuacja = temp_sytuacja
                        final_mysli = temp_mysli
                        final_emocje = temp_emocje
                        final_cialo = temp_cialo
                        final_zachowanie = temp_zachowanie

                if najlepsze_dopasowanie and najwyzszy_wynik > 0:
                    st.success(f"🎯 Zidentyfikowano profil kliniczny: {najlepsze_dopasowanie['diagnoza']}")
                    st.warning(f"⚖️ Diagnoza różnicowa (do wykluczenia): {najlepsze_dopasowanie['roznicowa']}")
                    
                    st.session_state.ui_problemy_html = najlepszy_html
                    st.session_state.ui_cele = najlepsze_dopasowanie['cele_smart']
                    st.session_state.ui_protokol = najlepsze_dopasowanie['protokol_nazwa']
                    st.session_state.ui_uzasadnienie = najlepsze_dopasowanie['uzasadnienie_planu']
                    
                    st.session_state.ui_sytuacja = final_sytuacja if final_sytuacja else "Brak wyraźnego wyzwalacza."
                    st.session_state.ui_mysli = final_mysli if final_mysli else "Brak zidentyfikowanych myśli automatycznych."
                    st.session_state.ui_emocje = final_emocje if final_emocje else "Brak zidentyfikowanych emocji."
                    st.session_state.ui_cialo = final_cialo if final_cialo else "Brak zidentyfikowanych doznań somatycznych."
                    st.session_state.ui_zachowanie = final_zachowanie if final_zachowanie else "Brak zidentyfikowanych zachowań."
                else:
                    st.info("Algorytm nie wykrył żadnych specyficznych słów klinicznych.")
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
        st.session_state.baza_terapii.append({
            "Pacjent": imie, 
            "Wiek": wiek, 
            "Kod ICD": kod_icd,
            "Diagnoza": pelna_diagnoza
        })
        st.success("Zapisano do bazy!")

elif menu == "II. Plan i Interwencje":
    st.title("II. Plan terapii i interwencje")
    st.header("II.1. Plan terapii (Uzasadnienie EBM)")
    st.text_input("Protokół (EBM):", key="ui_protokol", on_change=sync_protokol)
    st.text_area("Uzasadnienie interwencji:", key="ui_uzasadnienie", on_change=sync_uzasadnienie, height=150)
    st.divider()
    st.header("II.2. Zapis przebiegu poszczególnych sesji")
    st.text_area("Rejestr sesji (np. Sesja 1 [Data] - Psychoedukacja i BA...)", height=300)

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

elif menu == "📂 Archiwum Diagnoz":
    st.title("Baza Terapii")
    if not st.session_state.baza_terapii:
        st.warning("Baza jest pusta. Dodaj pacjenta w zakładce I.")
    else:
        df = pd.DataFrame(st.session_state.baza_terapii)
        st.dataframe(df, use_container_width=True)
