import streamlit as st
import pandas as pd

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Zapis Przebiegu Terapii CBT - System Pro", layout="wide")

# --- BAZA WIEDZY I DIAGRAMY MERMAID ---
slownik_modeli = {
    "F41.0": {
        "Model": "Model poznawczy lęku panicznego (D. Clark, 1986)",
        "Opis": "Skupienie na błędnej, katastroficznej interpretacji normalnych doznań z ciała (np. kołatanie serca = zawał).",
        "Interwencje": "Reatrybucja doznań, hiperwentylacja (eksperyment), eliminacja zachowań zabezpieczających.",
        "Wizualizacja": """
```mermaid
graph TD
    A[Wewnętrzny lub zewnętrzny wyzwalacz] --> B[Postrzegane zagrożenie]
    B --> C[Lęk / Niepokój]
    C --> D[Doznania somatyczne np. kołatanie serca]
    D --> E{Katastroficzna interpretacja}
    E -- Błędne koło paniki --> B
    
    style E fill:#ffcccc,stroke:#ff0000,stroke-width:2px
