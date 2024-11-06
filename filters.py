import streamlit as st
import pandas as pd

def apply_filters(data):
    # Calendrier pour la période de vente
    min_date = data['order_date'].min()
    max_date = data['order_date'].max()
    col1, col2 = st.columns(2)

    with col1:
        st.header("Date de début")
        start_date = st.date_input("Date de début", min_value=min_date.date(), max_value=max_date.date())

    with col2:
        st.header("Date de fin")
        end_date = st.date_input("Date de fin", min_value=min_date.date(), max_value=max_date.date())

    # Filtrer les données par dates
    filtered_data = data[(data['order_date'] >= pd.to_datetime(start_date)) & 
                         (data['order_date'] <= pd.to_datetime(end_date))]

    # Filtres
    regions = st.sidebar.multiselect("Choisir la Région", data['Region'].unique())
    if regions:
        filtered_data = filtered_data[filtered_data['Region'].isin(regions)]

    states = st.sidebar.multiselect("Choisir l'État", filtered_data['State Complet'].unique())
    if states:
        filtered_data = filtered_data[filtered_data['State Complet'].isin(states)]

    countries = st.sidebar.multiselect("Choisir le Pays", filtered_data['Country'].unique())
    if countries:
        filtered_data = filtered_data[filtered_data['Country'].isin(countries)]

    cities = st.sidebar.multiselect("Choisir la Ville", filtered_data['City'].unique())
    if cities:
        filtered_data = filtered_data[filtered_data['City'].isin(cities)]

    # Filtre pour le statut de la commande
    order_status = st.sidebar.multiselect("Choisir le statut de la commande", data['status'].unique())
    if order_status:
        filtered_data = filtered_data[filtered_data['status'].isin(order_status)]

    return filtered_data
