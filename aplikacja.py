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

# Dalsze moduły (OCD, PTSD) będziemy dopisywać w miarę rozwoju aplikacji
