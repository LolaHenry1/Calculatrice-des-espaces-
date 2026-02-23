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
# PIÈCES / VIENNOISERIES
# -------------------------------
if format_event in ["Cocktail déjeunatoire", "Cocktail dinatoire"]:
    st.header("🍢 Quantité de pièces par personne")
    with st.container(border=True):
        pieces_pp = st.slider("Nombre de pièces par personne", min_value=4, max_value=24, value=12)

        st.markdown("#### Répartition des pièces")
        col1, col2, col3 = st.columns(3)
        with col1:
            pct_froid = st.slider("Froid (%)", 0, 100, 40)
        with col2:
            pct_chaud = st.slider("Chaud (%)", 0, 100, 40)
        with col3:
            pct_sucre = st.slider("Sucré (%)", 0, 100, 20)

    # Ajustement si somme ≠ 100
    total_pct = pct_froid + pct_chaud + pct_sucre
    if total_pct != 100:
        pct_froid = round(100 * pct_froid / total_pct)
        pct_chaud = round(100 * pct_chaud / total_pct)
        pct_sucre = 100 - pct_froid - pct_chaud
        st.warning("Les pourcentages ont été ajustés pour totaliser 100 %.")

elif format_event == "Accueil café":
    st.header("🥐 Quantité de viennoiseries par personne")
    with st.container(border=True):
        st.write("Mini-viennoiseries (croissant, pain au chocolat, etc.)")
        pieces_pp = st.number_input("Quantité", min_value=1, max_value=5, value=2, step=1)

elif format_event == "Pause café":
    st.header("☕ Quantité de viennoiseries par personne")
    with st.container(border=True):
        st.write("Souvent reprise du matin")
        pieces_pp = st.number_input("Quantité", min_value=0, max_value=3, value=1, step=1)

elif format_event == "Journée complète":
    st.header("🕓 Journée complète (Accueil + Cocktail)")
    with st.container(border=True):
        st.write("Inclut un accueil café et un cocktail déjeunatoire")
        pieces_pp = st.slider("Nombre total de pièces par personne", 8, 24, 14)

# -------------------------------
# BOISSONS
# -------------------------------
st.header("🥤 Boissons")
with st.container(border=True):
    st.write("Ratios par défaut : Softs 1/6 pers · Vin 1/10 pers · Champagne 1/9 pers")

    include_softs = True
    include_vin = False
    include_champagne = False

    if format_event in ["Cocktail déjeunatoire", "Cocktail dinatoire", "Journée complète"]:
        col1, col2, col3 = st.columns(3)
        with col1:
            include_softs = st.checkbox("Softs", True)
        with col2:
            include_vin = st.checkbox("Vin", True)
        with col3:
            include_champagne = st.checkbox("Champagne", False)
    else:
        include_softs = st.checkbox("Softs", True, disabled=True)
        include_vin = st.checkbox("Vin", False, disabled=True)
        include_champagne = st.checkbox("Champagne", False, disabled=True)

# -------------------------------
# RATIOS BOISSONS
# -------------------------------
ratio_soft = 6
ratio_vin = 10
ratio_champagne = 9

nb_softs = math.ceil(nb_pers / ratio_soft) if include_softs else 0
nb_vin = math.ceil(nb_pers / ratio_vin) if include_vin else 0
nb_champagne = math.ceil(nb_pers / ratio_champagne) if include_champagne else 0

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
    nb_sucre = total_pieces - nb_froid - nb_chaud

# -------------------------------
# RÉSULTATS
# -------------------------------
st.divider()
st.header("📊 Résultats chiffrés")

colA, colB = st.columns(2)
with colA:
    st.subheader("🍢 Pièces")
    st.write(f"Froid : {nb_froid}")
    st.write(f"Chaud : {nb_chaud}")
    st.write(f"Sucré : {nb_sucre}")
    st.write(f"**Total pièces : {total_pieces}**")

with colB:
    st.subheader("🍾 Boissons (bouteilles)")
    if include_softs: st.write(f"Softs : {nb_softs}")
    if include_vin: st.write(f"Vin : {nb_vin}")
    if include_champagne: st.write(f"Champagne : {nb_champagne}")

# -------------------------------
# RÉSUMÉ GLOBAL
# -------------------------------
st.divider()
st.header("📈 Résumé global")
total_boissons = nb_softs + nb_vin + nb_champagne
st.write(f"Nombre total de convives : {nb_pers}")
st.write(f"Total pièces : {total_pieces}")
st.write(f"Total boissons : {total_boissons}")
