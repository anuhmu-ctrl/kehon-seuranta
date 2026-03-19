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

# Alustetaan tiedostot
for f in [TIEDOSTO, TAVOITE_TIEDOSTO]:
    if not os.path.exists(f):
        pd.DataFrame(columns=sarakkeet).to_csv(f, index=False)

st.title("⚖️ Kehon mittausseuranta")

# --- SIVUPALKKI ---
st.sidebar.header("👤 Käyttäjäprofiili")
pituus = st.sidebar.number_input("Pituus (cm)", value=170, min_value=100)
ika = st.sidebar.number_input("Ikä", value=20)
sukupuoli = st.sidebar.selectbox("Sukupuoli", ["Mies", "Nainen", "Muu"])

# --- VÄLILEHDET ---
tab_lisaa, tab_trendit, tab_tavoitteet = st.tabs(["📥 Lisää mittaukset", "📈 Trendikäyrät", "🎯 Aseta tavoitteet"])

# 1. LISÄÄ MITTAUKSET
with tab_lisaa:
    valittu_paiva = st.date_input("Valitse päivämäärä (PP.KK.VVVV)", date.today())
    
    st.subheader("🧬 Kehon koostumus")
    c1, c2, c3 = st.columns(3)
    with c1:
        paino = st.number_input("Paino (kg)", format="%.1f", value=70.0)
        rasva = st.number_input("Rasvaprosentti (%)", format="%.1f")
    with c2:
        lihas = st.number_input("Lihasmassaprosentti (%)", format="%.1f")
        rm = st.number_input("RM (kcal)", step=10)
    with c3:
        viskeraali = st.number_input("Viskeraalinen rasva", step=1)
        bmi = paino / ((pituus/100)**2)
        st.metric("Laskettu BMI", f"{bmi:.1f}")

    st.markdown("---")
    st.subheader("📏 Ympärysmitta (cm)")
    
    col_yla1, col_yla2 = st.columns(2)
    with col_yla1:
        hartia = st.number_input("Hartiaympärys")
        rinta = st.number_input("Rinnanympärys")
        kasi_v = st.number_input("Käsivarsi (V)")
        kasi_o = st.number_input("Käsivarsi (O)")
    with col_yla2:
        yla_vatsa = st.number_input("Ylävatsa")
        vatsa = st.number_input("Vatsa (napa)")
        ala_vatsa = st.number_input("Alavatsa")
        lantio = st.number_input("Lantio (levein kohta)")

    st.info("💡 Mittaa alaraajat jalan ollessa 90° kulmassa parhaan tarkkuuden saamiseksi.")
    
    
    col_ala1, col_ala2 = st.columns(2)
    with col_ala1:
        ry_v = st.number_input("Reisi yläosa 90° (V)")
        rp_v = st.number_input("Reisi puoliväli 90° (V)")
        pol_v = st.number_input("Polven päältä 90° (V)")
        poh_v = st.number_input("Pohje, levein kohta (V)")
    with col_ala2:
        ry_o = st.number_input("Reisi yläosa 90° (O)")
        rp_o = st.number_input("Reisi puoliväli 90° (O)")
        pol_o = st.number_input("Polven päältä 90° (O)")
        poh_o = st.number_input("Pohje, levein kohta (O)")

    if st.button("TALLENNA KAIKKI MITTAUKSET"):
        uudet = [
            valittu_paiva, paino, round(bmi, 2), rasva, lihas, rm, viskeraali,
            hartia, rinta, kasi_v, kasi_o, yla_vatsa, vatsa, ala_vatsa, lantio,
            ry_v, ry_o, rp_v, rp_o, pol_v, pol_o, poh_v, poh_o
        ]
        df_old = pd.read_csv(TIEDOSTO)
        pd.concat([df_old, pd.DataFrame([uudet], columns=sarakkeet)]).to_csv(TIEDOSTO, index=False)
        st.success("Mittaukset tallennettu onnistuneesti!")
        st.balloons()

# 2. ASETA TAVOITTEET
with tab_tavoitteet:
    st.subheader("Aseta tavoitearvosi seurattaville mitoille")
    # Luodaan syöttökentät tavoitteille (oletusarvot ladataan jos olemassa)
    t_vals = {}
    cols = st.columns(3)
    for i, m in enumerate(["Paino", "Rasva_%", "Lihasmassa_%", "Vatsa_napa", "Hartia", "Lantio"]):
        with cols[i % 3]:
            t_vals[m] = st.number_input(f"Tavoite: {m}", value=0.0)

    if st.button("TALLENNA TAVOITTEET"):
        t_df = pd.DataFrame([t_vals])
        t_df.to_csv(TAVOITE_TIEDOSTO, index=False)
        st.success("Tavoitteet päivitetty!")

# 3. TRENDIKÄYRÄT
with tab_trendit:
    df_p = pd.read_csv(TIEDOSTO)
    if not df_p.empty:
        df_p["Päivämäärä"] = pd.to_datetime(df_p["Päivämäärä"])
        df_p = df_p.sort_values("Päivämäärä")
        
        mittari = st.selectbox("Valitse seurattava mitta", sarakkeet[1:])
        
        plot_df = df_p.set_index("Päivämäärä")[[mittari]].copy()
        
        # Lisätään tavoiteviiva jos se on asetettu
        if os.path.exists(TAVOITE_TIEDOSTO):
            df_t = pd.read_csv(TAVOITE_TIEDOSTO)
            if mittari in df_t.columns and df_t[mittari].iloc[0] > 0:
                plot_df["Tavoite"] = df_t[mittari].iloc[0]
        
        st.line_chart(plot_df)
        st.dataframe(df_p.sort_values("Päivämäärä", ascending=False))
    else:
        st.warning("Ei dataa näytettäväksi. Lisää mittauksia ensimmäisellä välilehdellä.")
