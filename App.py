import streamlit as st
import math

st.set_page_config(page_title="Calculateur Traiteur – V4 Pro étendu", layout="centered")
st.title("🍽️ Calculateur Traiteur – Version 4 Pro étendu")

# -------------------------------
# PARAMÈTRES INVITÉS
# -------------------------------
st.header("👥 Paramètres invités")
nb_pers = st.number_input("Nombre de convives", min_value=1, value=50, step=1)

# -------------------------------
# FORMAT DE L'ÉVÉNEMENT
# -------------------------------
st.header("🥂 Format de l'événement")
format_event = st.radio(
    "Type de prestation",
    [
        "Accueil café",
        "Pause café",
        "Cocktail déjeunatoire",
        "Cocktail dinatoire",
        "Journée complète"
    ],
    index=0,
)

# -------------------------------
# QUANTITÉS DE BASE PAR FORMAT
# -------------------------------
if format_event in ["Cocktail déjeunatoire", "Cocktail dinatoire"]:
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

# Ajustement automatique si somme != 100
    total_pct = pct_froid + pct_chaud + pct_sucre
    if total_pct != 100:
        pct_froid = round(100 * pct_froid / total_pct)
        pct_chaud = round(100 * pct_chaud / total_pct)
        pct_sucre = 100 - pct_froid - pct_chaud
        st.warning("Les pourcentages ont été ajustés pour totaliser 100 %.")

elif format_event in ["Accueil café"]:
    st.header("🥐 Quantité de viennoiseries par personne")
    pieces_pp = 2  # Selon devis : 2 mini-viennoiseries par pers.

elif format_event in ["Pause café"]:
    st.header("☕ Pause – consommations")
    pieces_pp = 1  # En général : reprise des viennoiseries du matin.

elif format_event in ["Journée complète"]:
    st.header("🕓 Journée complète")
    st.info("Inclusion d’un accueil café le matin et d’un cocktail déjeunatoire (à paramétrer ci-dessous).")
    pieces_pp = 14  # Moyenne journée complète (accueil + cocktail)

# -------------------------------
# RATIOS BOISSONS
# -------------------------------
st.divider()
st.header("🥤 Boissons")

# Ratios standard
ratio_soft = 6  # 1 bouteille / 6 pers
ratio_vin = 10  # 1 bouteille / 10 pers
ratio_champagne = 9  # 1 bouteille / 9 pers

nb_softs = math.ceil(nb_pers / ratio_soft)
nb_vin = math.ceil(nb_pers / ratio_vin)
nb_champagne = math.ceil(nb_pers / ratio_champagne)

# -------------------------------
# CALCULS DES PIÈCES
# -------------------------------
if format_event in ["Cocktail déjeunatoire", "Cocktail dinatoire"]:
    total_pieces = nb_pers * pieces_pp
    nb_froid = math.ceil(total_pieces * pct_froid / 100)
    nb_chaud = math.ceil(total_pieces * pct_chaud / 100)
    nb_sucre = math.ceil(total_pieces * pct_sucre / 100)

elif format_event == "Accueil café":
    total_pieces = nb_pers * pieces_pp
    nb_froid = nb_chaud = 0
    nb_sucre = total_pieces

elif format_event == "Pause café":
    total_pieces = nb_pers * pieces_pp
    nb_froid = nb_chaud = 0
    nb_sucre = total_pieces

elif format_event == "Journée complète":
    total_pieces = nb_pers * pieces_pp
    nb_froid = math.ceil(total_pieces * 0.4)
    nb_chaud = math.ceil(total_pieces * 0.4)
    nb_sucre = math.ceil(total_pieces * 0.2)

# -------------------------------
# AFFICHAGE DES RÉSULTATS
# -------------------------------
st.divider()
st.header("📊 Résultats chiffrés")

colA, colB = st.columns(2)

with colA:
    st.subheader("🍢 Pièces")
    st.write(f"Froid : {nb_froid}")
    st.write(f"Chaud : {nb_chaud}")
    st.write(f"Sucré : {nb_sucre}")
    st.write(f"**Total pieces : {total_pieces}**")

with colB:
    st.subheader("🍾 Boissons (bouteilles)")
    if format_event in ["Accueil café", "Pause café", "Journée complète"]:
        st.write(f"Softs : {nb_softs}")
    if format_event in ["Cocktail déjeunatoire", "Cocktail dinatoire", "Journée complète"]:
        st.write(f"Vin : {nb_vin}")
        st.write(f"Champagne : {nb_champagne}")

# -------------------------------
# RÉSUMÉ GLOBAL FINAL
# -------------------------------
st.divider()
st.header("📈 Résumé global")

if format_event in ["Cocktail déjeunatoire", "Cocktail dinatoire", "Journée complète"]:
    total_boissons = nb_softs + nb_vin + nb_champagne
else:
    total_boissons = nb_softs

st.write(f"Nombre total de convives : {nb_pers}")
st.write(f"Total pièces : {total_pieces}")
st.write(f"Total boissons (toutes catégories) : {total_boissons}")
