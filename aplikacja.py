import streamlit as st

# Konfiguracja strony
st.set_page_config(page_title="CBT Gabinet - System Ekspercki", layout="wide")

# Menu boczne do nawigacji między zaburzeniami
st.sidebar.title("🧠 Menu Protokołów CBT")
kategoria = st.sidebar.radio(
    "Wybierz moduł kliniczny:",
    ["Strona Główna", "Lęk Paniczny", "Depresja", "Lęk Społeczny", "OCD", "PTSD"]
)

if kategoria == "Strona Główna":
    st.title("Witaj w Cyfrowym Gabinecie CBT")
    st.write("Wybierz odpowiedni protokół z menu po lewej stronie, aby rozpocząć pracę z pacjentem.")
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Cognitive_behavioral_therapy_explanation.svg/1024px-Cognitive_behavioral_therapy_explanation.svg.png", width=600)

elif kategoria == "Lęk Paniczny":
    st.title("🔴 Protokół: Lęk Paniczny (Model Clarka)")
    st.subheader("Błędne Koło Paniki")
    
    st.info("Praca polega na zmianie katastroficznej interpretacji doznań z ciała.")
    
    with st.expander("Zobacz formularz zapisu myśli"):
        st.write("1. Sytuacja / Doznanie: (np. kołatanie serca)")
        st.write("2. Automatyczna myśl: (np. Zaraz będę mieć zawał)")
        st.write("3. Alternatywna interpretacja: (To tylko adrenalina)")

elif kategoria == "Depresja":
    st.title("🔵 Protokół: Depresja (Aktywacja Behawioralna)")
    [attachment_0](attachment)
    st.subheader("Monitorowanie Aktywności i Nastroju")
    aktywnosc = st.text_input("Jaka aktywność została podjęta?")
    nastroj = st.select_slider("Poziom nastroju po aktywności", options=range(1, 11))
    st.button("Zapisz w dzienniku")

# # --- SEKCJA: LĘK SPOŁECZNY ---
elif kategoria == "Lęk Społeczny":
    st.title("👥 Protokół: Lęk Społeczny (Model Clarka i Wellsa)")
    st.subheader("Model Poznawczy")
    
    st.info("Kluczowym elementem jest skupienie uwagi na sobie i tworzenie negatywnego obrazu siebie w oczach innych.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Zachowania zabezpieczające:**")
        st.write("- Unikanie kontaktu wzrokowego")
        st.write("- Planowanie wypowiedzi")
        st.write("- Ukrywanie rumieńców")
    
    with col2:
        st.write("**Zniekształcenia poznawcze:**")
        st.write("- Czytanie w myślach")
        st.write("- Przepowiadanie przyszłości")
        st.write("- Personalizacja")

    st.subheader("Ćwiczenie: Przenoszenie Uwagi")
    st.write("Skoncentruj się na otoczeniu, a nie na własnych odczuciach z ciała.")
 moduły (OCD, PTSD) będziemy dopisywać w miarę rozwoju aplikacji
with open("protokol_depresja.pdf", "rb") as file:
    st.download_button(
        label="📄 Pobierz pełny protokół leczenia (PDF)",
        data=file,
        file_name="protokol_depresja.pdf",
        mime="application/pdf"
    )
