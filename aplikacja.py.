import streamlit as st
import docx
from io import BytesIO

# Konfiguracja głównego okna
st.set_page_config(page_title="Zapis Przebiegu Terapii CBT", page_icon="📝", layout="wide")

# ==========================================
# FUNKCJA GENERUJĄCA DOKUMENT WORD
# ==========================================
def generuj_word():
    doc = docx.Document()
    doc.add_heading('ZAPIS PRZEBIEGU TERAPII POZNAWCZO-BEHAWIORALNEJ', 0)
    
    doc.add_heading('0. Autorefleksja przed superwizją', level=1)
    doc.add_paragraph("Problem w pracy z pacjentem / Pytania:")
    doc.add_paragraph(st.session_state.get('auto_problem', '- brak wpisu -'))
    
    doc.add_heading('I. Diagnoza i Problemy', level=1)
    doc.add_paragraph("Zgłaszane problemy, powód przyjścia:")
    doc.add_paragraph(st.session_state.get('diag_problemy', '- brak wpisu -'))
    doc.add_paragraph("Diagnoza wstępna (ICD/DSM):")
    doc.add_paragraph(st.session_state.get('diag_wstepna', '- brak wpisu -'))
    
    doc.add_heading('I.3. Konceptualizacja (Model ABC)', level=1)
    doc.add_paragraph(f"Wyzwalacz (A): {st.session_state.get('konc_a', '')}")
    doc.add_paragraph(f"Myśli (B): {st.session_state.get('konc_b', '')}")
    doc.add_paragraph(f"Emocje/Ciało (C): {st.session_state.get('konc_c_emocje', '')}")
    doc.add_paragraph(f"Zachowanie (C): {st.session_state.get('konc_c_zachowanie', '')}")
    
    doc.add_heading('Podsumowanie i Plan Terapii', level=1)
    doc.add_paragraph(st.session_state.get('plan_terapii', '- brak wpisu -'))

    # Zapisywanie pliku do pamięci, aby Streamlit mógł go pobrać
    bio = BytesIO()
    doc.save(bio)
    return bio.getvalue()

# ==========================================
# PASEK BOCZNY - NAWIGACJA I EKSPORT
# ==========================================
st.sidebar.title("📝 Karta Pacjenta CBT")
zakladka = st.sidebar.radio(
    "WYBIERZ ETAP:",
    [
        "0. Autorefleksja (Superwizja)",
        "I. Diagnoza i Problemy",
        "I. Konceptualizacja (Poz. I i II)",
        "II. Plan i Przebieg Terapii"
    ]
)

st.sidebar.divider()
st.sidebar.subheader("🖨️ Eksport do druku")
st.sidebar.write("Pobierz wypełniony formularz:")

# Przycisk pobierania pliku Word
gotowy_plik_word = generuj_word()
st.sidebar.download_button(
    label="Pobierz plik Word (.docx)",
    data=gotowy_plik_word,
    file_name="Zapis_Terapii_CBT.docx",
    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
)

st.sidebar.divider()

# ==========================================
# WIDOKI ZAKŁADEK (Z PAMIĘCIĄ SESJI - key)
# ==========================================
if zakladka == "0. Autorefleksja (Superwizja)":
    st.header("Autorefleksja przed superwizją")
    st.text_area("Co jest problemem w pracy z tym pacjentem?", key="auto_problem")
    st.text_area("Moje własne ABC na myśl o superwizji:", key="auto_abc")

elif zakladka == "I. Diagnoza i Problemy":
    st.header("I. Pierwszy Etap Terapii - Diagnoza")
    st.text_area("Zgłaszane problemy, powód przyjścia:", key="diag_problemy")
    st.text_area("Informacje ogólne (wywiad):", key="diag_wywiad")
    st.text_input("Diagnoza wstępna (ICD/DSM) - Zaburzenie dominujące:", key="diag_wstepna")
    st.text_area("Lista problemów z oceną dyskomfortu (0-100):", key="diag_lista")

elif zakladka == "I. Konceptualizacja (Poz. I i II)":
    st.header("I.3. Konceptualizacja")
    st.subheader("Poziom I: Model ABC")
    st.text_input("Sytuacja ilustrująca problem (A):", key="konc_a")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text_area("Automatyczne myśli (B):", key="konc_b")
    with col2:
        st.text_area("Emocje i Objawy fizjologiczne (C):", key="konc_c_emocje")
    with col3:
        st.text_area("Zachowanie (w tym strategie zabezpieczające) (C):", key="konc_c_zachowanie")
        
    st.subheader("Poziom II: Schematy")
    st.text_area("Przekonania kluczowe:", key="konc_kluczowe")

elif zakladka == "II. Plan i Przebieg Terapii":
    st.header("II. Drugi Etap Terapii")
    st.text_area("Plan terapii (uzasadnienie EBP):", key="plan_terapii")
    st.text_area("Notatki z sesji (chronologicznie):", height=300, key="plan_notatki")
