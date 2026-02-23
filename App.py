import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="Simulateur Cocktail & Buffet", layout="centered")

st.title("🍽️ Simulateur de réception / cocktail")

# --- Données de base ----
BAREME = {
    "Cocktail déjeunatoire": {"min": 8, "max": 14, "default": 10},
    "Cocktail dinatoire": {"min": 10, "max": 18, "default": 13},
    "Cocktail de clôture": {"min": 4, "max": 8, "default": 6},
    "Petit déjeuner": {"min": 2, "max": 4, "default": 2.5},
    "Déjeuner assis": {"min": 3, "max": 3, "default": 3},
    "Journée complète": {"min": 20, "max": 30, "default": 25},
}

# --- Interface utilisateur ----
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

alcool = st.radio("Boissons alcoolisées ?", ["Oui", "Non"], horizontal=True)
option_style = st.selectbox(
    "Style de service",
    ["Classique", "Copieux", "Léger"]
)

# --- Définition des répartitions pièces ----
# Ratios de base, que tu pourras affiner ensuite
if "cocktail" in type_event.lower():
    ratio_chaud = 0.4
    ratio_froid = 0.4
    ratio_sucre = 0.2
elif type_event == "Journée complète":
    ratio_chaud, ratio_froid, ratio_sucre = 0.45, 0.35, 0.20
elif type_event == "Petit déjeuner":
    ratio_chaud, ratio_froid, ratio_sucre = 0, 0, 1
elif type_event == "Déjeuner assis":
    ratio_chaud, ratio_froid, ratio_sucre = 0.5, 0.3, 0.2
else:
    ratio_chaud, ratio_froid, ratio_sucre = 0.4, 0.4, 0.2

# Ajustement “intensité”
multiplier = {"Léger": 0.9, "Classique": 1.0, "Copieux": 1.2}[option_style]

pieces_total = nb_pers * pieces_slider * multiplier
chaudes_total = pieces_total * ratio_chaud
froides_total = pieces_total * ratio_froid
sucrees_total = pieces_total * ratio_sucre

# --- Boissons ----
# Hypothèses standards
softs_btl_pour = 5
alcool_btl_pour = 6

softs_btl = math.ceil(nb_pers / softs_btl_pour)
alcool_btl = math.ceil(nb_pers / alcool_btl_pour) if alcool == "Oui" else 0

# --- Affichage ----
st.markdown("---")
st.subheader("📊 Résumé")

data = {
    "Éléments": [
        "Participants",
        "Pièces totales",
        "Pièces chaudes",
        "Pièces froides",
        "Pièces sucrées",
        "Bouteilles softs (1 L)",
        "Bouteilles alcoolisées (vin/champagne)",
    ],
    "Valeurs": [
        f"{nb_pers}",
        f"{pieces_total:.0f}",
        f"{chaudes_total:.0f}",
        f"{froides_total:.0f}",
        f"{sucrees_total:.0f}",
        f"{softs_btl}",
        f"{alcool_btl}" if alcool == "Oui" else "–",
    ],
}

df = pd.DataFrame(data)
st.table(df)

st.markdown("---")
st.caption(
    "Les ratios et répartitions sont basés sur une moyenne professionnelle (cocktails traiteur 2024). "
    "Tous les paramètres sont ajustables."
)
