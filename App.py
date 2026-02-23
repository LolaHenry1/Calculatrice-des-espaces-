import streamlit as st
import pandas as pd

st.set_page_config(page_title="Simulateur Cocktail & Buffet", layout="centered")

st.title("🥂 Simulateur de pièces et boissons")
st.markdown("Calcule automatiquement la quantité de pièces et de boissons selon le type d’événement.")

# --- 🔹 Barème de base issu du devis analysé ----
BAREME = {
    "Petit déjeuner": {
        "duree": "0h30–1h",
        "pieces_par_pers": 2.5,
        "salées": 0,
        "sucrées": 2.5,
        "boissons_soft_L": 0.2,
        "boissons_alcool_btl_pour": None,
    },
    "Cocktail déjeunatoire": {
        "duree": "1h",
        "pieces_par_pers": 9,
        "salées": 6,
        "sucrées": 3,
        "boissons_soft_L": 0.2,
        "boissons_alcool_btl_pour": 6,
    },
    "Cocktail dinatoire": {
        "duree": "2h",
        "pieces_par_pers": 13,
        "salées": 9,
        "sucrées": 4,
        "boissons_soft_L": 0.3,
        "boissons_alcool_btl_pour": 5,
    },
    "Cocktail de clôture": {
        "duree": "1h",
        "pieces_par_pers": 6,
        "salées": 4,
        "sucrées": 2,
        "boissons_soft_L": 0.2,
        "boissons_alcool_btl_pour": 6,
    },
    "Déjeuner assis": {
        "duree": "1h30-2h",
        "pieces_par_pers": 3,  # entrée, plat, dessert
        "salées": 2,
        "sucrées": 1,
        "boissons_soft_L": 0.1,
        "boissons_alcool_btl_pour": 6,
    },
    "Journée complète": {
        "duree": "12h",
        "pieces_par_pers": 25,
        "salées": 14,
        "sucrées": 11,
        "boissons_soft_L": 0.8,
        "boissons_alcool_btl_pour": 6,
    },
}

# --- 🔹 Interface utilisateu.r
col1, col2 = st.columns(2)
with col1:
    type_event = st.selectbox("Type d’événement", list(BAREME.keys()))
with col2:
    nb_pers = st.number_input("Nombre de participants", min_value=5, step=5, value=100)

alcool = st.radio("Boissons alcoolisées ?", ["Oui", "Non"], horizontal=True)

# --- 🔹 Calculs simples selon barème ----
params = BAREME[type_event]

pieces_tot = nb_pers * params["pieces_par_pers"]
salees_tot = nb_pers * params["salées"]
sucrees_tot = nb_pers * params["sucrées"]
softs_L = nb_pers * params["boissons_soft_L"]

if params["boissons_alcool_btl_pour"] and alcool == "Oui":
    bouteilles_alcool = nb_pers / params["boissons_alcool_btl_pour"]
else:
    bouteilles_alcool = 0

# --- 🔹 Résumé et tableau ----
st.subheader("📊 Résumé de l’estimation")
data = {
    "Éléments": [
        "Durée",
        "Pièces totales",
        "Salées totales",
        "Sucrées totales",
        "Boissons sans alcool (L)",
        "Bouteilles alcoolisées",
    ],
    "Valeurs": [
        params["duree"],
        f"{pieces_tot:.0f}",
        f"{salees_tot:.0f}",
        f"{sucrees_tot:.0f}",
        f"{softs_L:.1f} L",
        f"{bouteilles_alcool:.1f}" if alcool == "Oui" else "–",
    ],
}

df = pd.DataFrame(data)
st.table(df)

st.markdown("---")
st.markdown(
    "*Ces ratios proviennent de moyennes réelles issues d’un devis professionnel (Inédit Réceptions, 100 pers, 2024).*"
)
