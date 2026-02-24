# ==========================================================
# MODUŁ II: PLAN TERAPII I INTERWENCJE
# ==========================================================
elif menu == "II. Plan i Interwencje":
    st.title("II. Plan terapii i interwencje")
    
    st.header("II.1. Plan terapii (Uzasadnienie EBM)")
    
    # Jasne wskazanie sugerowanego protokołu do realizacji celów
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
