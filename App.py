import streamlit as st
import math

st.set_page_config(page_title="Calculateur Traiteur – V4 Pro", layout="centered")

st.title("🍽️ Calculateur Traiteur – Version 4 Pro")

st.header("👥 Paramètres invités")
nb_pers = st.number_input("Nombre de convives", min_value=1, value=50, step=1)

st.header("🥂 Format de l'événement")
format_event = st.radio(
    "Type de prestation",
    ["Cocktail déjeunatoire", "Cocktail dinatoire"],
    index=0,
)

st.header("🍢 Quantité de pièces par personne")
pieces_pp = st.slider("Nombre de pièces par personne", min_value=4, max_value=24, value=12)

st.header("🥶 Répartition des pièces")
col1, col2, col3 = st.columns(3)
with col1:
    pct_froid = st.slider("Froid (%)", 0, 100, 40)
with col2:
    pct_chaud = st.slider("Chaud (%)", 0, 100, 40)
with col3:
    pct_sucre = st.slider("Sucré (%)", 0, 100, 20)

# Normalisation si la somme dépasse 100
total_pct = pct_froid + pct_chaud + pct_sucre
if total_pct != 100:
    pct_froid = round(100 * pct_froid / total_pct)
    pct_chaud = round(100 * pct_chaud / total_pct)
    pct_sucre = 100 - pct_froid - pct_chaud
    st.warning("Les pourcentages ont été ajustés pour totaliser 100 %.")

st.divider()

st.header("📊 Résultats chiffrés")

# Calculs des pièces
total_pieces = nb_pers * pieces_pp

nb_froid = math.ceil(total_pieces * pct_froid / 100)
nb_chaud = math.ceil(total_pieces * pct_chaud / 100)
nb_sucre = math.ceil(total_pieces * pct_sucre / 100)

# Calcul des boissons selon ratios validés
# Softs : 1 bouteille / 6 pers
# Vin : 1 bouteille / 10 pers
# Champagne : 1 bouteille / 9 pers
nb_softs = math.ceil(nb_pers / 6)
nb_vin = math.ceil(nb_pers / 10)
nb_champagne = math.ceil(nb_pers / 9)

colA, colB = st.columns(2)

with colA:
    st.subheader("🍢 Pièces")
    st.write(f"Froid : {nb_froid}")
    st.write(f"Chaud : {nb_chaud}")
    st.write(f"Sucré : {nb_sucre}")
    st.write(f"**Total pièces : {total_pieces}**")

with colB:
    st.subheader("🍾 Boissons (bouteilles)")
    st.write(f"Softs : {nb_softs}")
    st.write(f"Vin : {nb_vin}")
    st.write(f"Champagne : {nb_champagne}")

# Résumé global
st.divider()
st.header("📈 Résumé global")
total_boissons = nb_softs + nb_vin + nb_champagne
st.write(f"Nombre total de convives : {nb_pers}")
st.write(f"Total pièces : {total_pieces}")
st.write(f"Total boissons (toutes catégories) : {total_boissons}")
