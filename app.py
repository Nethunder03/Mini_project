import streamlit as st
from data import load_data, state_coordinates
from filters import apply_filters
from visuals import display_visuals

# Charger les données
data = load_data("donnees_ventes_etudiants.csv")

st.set_page_config(
    page_title="Rock Ferrand",
    layout="wide"
)

# Titre de l'application
st.title("Dashboard de Vente de Produits")
st.sidebar.title("Chose your filter")

# Appliquer les filtres
filtered_data = apply_filters(data)

# # Afficher les visuels
display_visuals(filtered_data, state_coordinates)




