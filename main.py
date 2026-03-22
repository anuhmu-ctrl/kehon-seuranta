import streamlit as st
import pandas as pd
from datetime import date
import os

# 1. ASETUKSET
st.set_page_config(page_title="Kehon mittausseuranta", layout="wide")
TIEDOSTO = "kehon_mitat.csv"
TAVOITE_TIEDOSTO = "tavoitteet.csv"

# Kaikki speksatut sarakkeet
sarakkeet = [
    "Päivämäärä", "Paino", "BMI", "Rasva_%", "Lihasmassa_%", "RM_kcal", "Viskeraalinen_rasva",
    "Hartia", "Rinta", "Käsivarsi_V", "Käsivarsi_O", 
    "Ylävatsa", "Vatsa_napa", "Alavatsa", "Lantio",
    "Reisi_ylä_V_90", "Reisi_ylä_O_90", "Reisi_puoli_V_90", "Reisi_puoli_O_90",
    "Polvi_V_90", "Polvi_O_90", "Pohje_V", "Pohje_O"
]

# Alustetaan tiedostot jos niitä ei ole
if not os.path.exists(TIEDOSTO):
    pd.DataFrame(columns=sarakkeet).to_csv(TIEDOSTO, index=False)
if not os.path.exists(TAVOITE_TIEDOSTO):
    # Luodaan tavoitteille oma rakenne, joka vastaa mittareita
    pd.DataFrame(columns=sarakkeet[1:]).to_csv(TAVOITE_TIEDOSTO, index=False)

# --- APUFUNKTIO: Turvallinen arvojen haku ---
def hae_viimeisimmat():
    if os.path.exists(TIEDOSTO):
        try:
            df = pd.read_csv(TIEDOSTO)
            if not df.empty:
                return df.iloc[-1].to_dict()
        except:
            pass
    return {}

v = hae_viimeisimmat()

st.title("⚖️ Kehon mittausseuranta")

# --- SIVUPALKKI ---
st.sidebar.header("👤 Käyttäjäprofiili")
pituus = st.sidebar.number_input("Pituus (cm)", value=175, min_value=100)
ika = st.sidebar.number_input("Ikä", value=25)
sukupuoli = st.sidebar.selectbox("Sukupuoli", ["Mies", "Nainen", "Muu"])

# --- VÄLILEHDET ---
tab_lisaa, tab_trendit, tab_tavoitteet = st.tabs(["📥 Lisää mittaukset", "📈 Trendikäyrät", "🎯 Aseta tavoitteet"])

# 1. LISÄÄ MITTAUKSET
with tab_lisaa:
    valittu_paiva = st.date_input("Valitse päivämäärä", date.today())
    
    st.subheader("🧬 Kehon koostumus")
    c1, c2, c3 = st.columns(3)
    with c1:
        paino = st.number_input("Paino (kg)", format="%.1f", value=float(v.get("Paino", 75.0)))
        rasva = st.number_input("Rasvaprosentti (%)", format="%.1f", value=float(v.get("Rasva_%", 20.0)))
    with c2:
        lihas = st.number_input("Lihasmassaprosentti (%)", format="%.1f", value=float(v.get("Lihasmassa_%", 35.0)))
        rm = st.number_input("RM (kcal)", step=10, value=int(v.get("RM_kcal", 1700)))
    with c3:
        viskeraali = st.number_input("Viskeraalinen rasva", step=1, value=int(v.get("Viskeraalinen_rasva", 5)))
        bmi = paino / ((pituus/100)**2)
        st.metric("Laskettu BMI", f"{bmi:.1f}")

    st.markdown("---")
    st.subheader("📏 Ympärysmitta (cm)")
    
    col_yla1, col_yla2 = st.columns(2)
    with col_yla1:
        hartia = st.number_input("Hartiaympärys", value=float(v.get("Hartia", 0.0)))
        kasi_v = st.number_input("Käsivarsi (V)", value=float(v.get("Käsivarsi_V", 0.0)))
        vatsa = st.number_input("Vatsa (napa)", value=float(v.get("Vatsa_napa", 0.0)))
    with col_yla2:
        rinta = st.number_input("Rinnanympärys", value=float(v.get("Rinta", 0.0)))
        kasi_o = st.number_input("Käsivarsi (O)", value=float(v.get("Käsivarsi_O", 0.0)))
        lantio = st.number_input("Lantio", value=float(v.get("Lantio", 0.0)))

    st.info("💡 Muista: Mittaa alaraajat (reidet/polvet) 90° kulmassa.")
    
    col_ala1, col_ala2 = st.columns(2)
    with col_ala1:
        ry_v = st.number_input("Reisi ylä 90° (V)", value=float(v.get("Reisi_ylä_V_90", 0.0)))
    rp_v = st.number_input("Reisi puoliväli 90° (V)", value=float(v.get("Reisi_puoli_V_90", 0.0)))
