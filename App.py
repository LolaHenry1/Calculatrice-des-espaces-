import streamlit as st
import math

st.set_page_config(page_title="Simulateur Cocktail & Buffet", layout="centered")

st.title("🍽️ Simulateur de Réception / Cocktail - V3")

# === Paramètres de base ===
BAREME = {
    "Cocktail déjeunatoire": {"min": 8, "max": 14, "default": 10},
    "Cocktail dinatoire": {"min": 10, "max": 18, "default": 13},
    "Cocktail de clôture": {"min": 4, "max": 8, "default": 6},
    "Petit déjeuner": {"min": 2, "max": 4, "default": 2.5},
    "Déjeuner assis": {"min": 3, "max": 3, "default": 3},
    "Journée complète": {"min": 20, "max": 30, "default": 25},
}

# === Entrées utilisateur ===
col1, col2 = st.columns(2)
with col1:
    type_event = st.selectbox("Type d’événement", list(BAREME.keys()))
with col2:
    nb_pers = st.number_input("Nombre de participants", min_value=5, step=5, value=100)

pieces_slider = st.slider(
    f"Nombre de pièces par personne ({type_event})",
    min_value=int(BAREME[type_event]["min"]),
    max_value=int(BAREME[type_event]["max"]),
    value=int(BAREME[type_event]["default"]),
)

style = st.selectbox("Style de service", ["Léger", "Classique", "Copieux"])
multiplier = {"Léger": 0.9, "Classique": 1.0, "Copieux": 1.2}[style]

st.subheader("🥂 Sélection des boissons")
colb1, colb2, colb3 = st.columns(3)
with colb1:
    inclure_softs = st.checkbox("Softs / sans alcool", value=True)
with colb2:
    inclure_vin = st.checkbox("Vin (rouge/blanc)")
with colb3:
    inclure_champagne = st.checkbox("Champagne")

# === Ratios chaud/froid/sucré ===
st.markdown("### 🍢 Répartition des pièces (ajustable)")

r_col1, r_col2, r_col3 = st.columns(3)
with r_col1:
    ratio_froid = st.slider("Froid %", 0, 100, 40)
with r_col2:
    ratio_chaud = st.slider("Chaud %", 0, 100, 40)
with r_col3:
    ratio_sucre = st.slider("Sucré %", 0, 100, 20)

total_ratio = ratio_froid + ratio_chaud + ratio_sucre
if total_ratio != 100:
    st.error("⚠️ Le total doit être égal à 100 %. Ajuste les curseurs.")
    st.stop()

# === Calculs ===
pieces_total = nb_pers * pieces_slider * multiplier
froid_total = pieces_total * (ratio_froid / 100)
chaud_total = pieces_total * (ratio_chaud / 100)
sucre_total = pieces_total * (ratio_sucre / 100)

# === Boissons ===
softs_btl_pour = 5
vin_btl_pour = 6
champ_btl_pour = 6

softs_btl = math.ceil(nb_pers / softs_btl_pour) if inclure_softs else 0
vin_btl = math.ceil(nb_pers / vin_btl_pour) if inclure_vin else 0
champ_btl = math.ceil(nb_pers / champ_btl_pour) if inclure_champagne else 0

# === Résumé ===
st.markdown("---")
st.markdown(f"## 📋 Fiche de synthèse – {type_event}")

st.markdown(
    f"""
### 👥 Participants
**{nb_pers} personnes**  
Style : **{style}**

### 🍴 Pièces prévues
- Total : **{pieces_total:,.0f} pièces**  
- Froides : **{froid_total:,.0f}**  
- Chaudes : **{chaud_total:,.0f}**  
- Sucrées : **{sucre_total:,.0f}**

### 🍹 Boissons
"""
)

if inclure_softs or inclure_vin or inclure_champagne:
    if inclure_softs:
        st.write(f"• **Softs / sans alcool** : {softs_btl} bouteilles (1 L)")
    if inclure_vin:
        st.write(f"• **Vin (rouge / blanc)** : {vin_btl} bouteilles")
    if inclure_champagne:
        st.write(f"• **Champagne** : {champ_btl} bouteilles")
else:
    st.write("_Aucune boisson sélectionnée._")

# Résumé des totaux rapides (pour affichage visuel)
st.markdown("---")
col_r1, col_r2, col_r3 = st.columns(3)
col_r1.metric("🥶 Froides", f"{int(froid_total)}")
col_r2.metric("🔥 Chaudes", f"{int(chaud_total)}")
col_r3.metric("🍰 Sucrées", f"{int(sucre_total)}")

st.markdown("---")
st.caption(
    "💡 Les ratios et volumes sont calculés sur des moyennes standards traiteur 2024. "
    "Ajuste les curseurs et options selon ton besoin."
)
