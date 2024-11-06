import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def display_visuals(filtered_data, state_coordinates):
    # Vérifier si les données sont filtrées
    if filtered_data.empty:
        st.write("Aucune donnée disponible pour afficher.")
        return

    # Calcul des KPI
    total_sales = filtered_data['total'].sum()
    distinct_customers = filtered_data['cust_id'].nunique()
    total_orders = filtered_data['order_id'].nunique()

    # Afficher les résultats
    st.write("### KPIs")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"<h3 style='font-size:20px;'>Total des ventes</h3>", unsafe_allow_html=True)
        st.metric(label="", value=f"{total_sales:.2f}")

    with col2:
        st.markdown(f"<h3 style='font-size:20px;'>Clients distincts</h3>", unsafe_allow_html=True)
        st.metric(label="", value=distinct_customers)

    with col3:
        st.markdown(f"<h3 style='font-size:20px;'>Total des commandes</h3>", unsafe_allow_html=True)
        st.metric(label="", value=total_orders)


    # Graphiques sur une autre ligne
    st.write("### Visualisations")

    col4, col5 = st.columns(2)

    with col4:
        # Diagramme en barres par catégorie
        category_sales = filtered_data.groupby('category')['total'].sum().reset_index()
        fig = px.bar(category_sales, x='category', y='total',
                      title='Total des ventes par catégorie',
                      labels={'category': 'Catégorie', 'total': 'Total des ventes'},
                      color='total',
                      color_continuous_scale='Blues',
                      text='total')
        
        fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig.update_layout(yaxis_title='Total des ventes', xaxis_title='Catégorie')
        st.plotly_chart(fig)

    with col5:
        # Diagramme circulaire par région
        region_sales = filtered_data.groupby('Region')['total'].sum().reset_index()

        # Créer le graphique donut
        fig_donut = px.pie(region_sales, 
                        names='Region', 
                        values='total', 
                        title='Pourcentage des ventes par région',
                        color='Region',
                        color_discrete_sequence=px.colors.qualitative.Set3,
                        hole=0.4)

        # Personnaliser le texte
        fig_donut.update_traces(textinfo='percent+label',
                                textfont_size=14)

        # Personnaliser la mise en page
        fig_donut.update_layout(title_font_size=20,
                                margin=dict(l=20, r=20, t=50, b=20),
                                showlegend=True)

        # Afficher le graphique
        st.plotly_chart(fig_donut)


    
    st.write("### Top 10 des meilleurs clients")
    # Calculer le total des ventes par client
    top_customers = filtered_data.groupby('full_name')['total'].sum().reset_index()
    
    # Trier les clients par total des ventes et prendre les 10 meilleurs
    top_customers = top_customers.sort_values(by='total', ascending=False).head(10)

    # Créer le diagramme en barres
    fig_bar = px.bar(top_customers, 
                     x='full_name', 
                     y='total', 
                     title='Top 10 des meilleurs clients',
                     labels={'full_name': 'Nom du client', 'total': 'Total des ventes'},
                     color='total',
                     color_continuous_scale=px.colors.sequential.Blues)  # Palette de couleurs

    # Mettre à jour les traces pour afficher les valeurs sur les barres
    fig_bar.update_traces(texttemplate='%{y:.2f}', textposition='outside')
    fig_bar.update_layout(yaxis_title='Total des ventes', 
                          xaxis_title='Nom du client',
                          title_font_size=20)

    # Afficher le graphique
    st.plotly_chart(fig_bar)


    col6, col7 = st.columns(2)

    with col6:
        fig_age = px.histogram(filtered_data, 
                            x='age', 
                            title='Répartition de l\'âge des clients',
                            labels={'age': 'Âge'},
                            nbins=30,  # Nombre de bins
                            color_discrete_sequence=['lightblue'])  # Couleur de l'histogramme

        fig_age.update_layout(title_font_size=20, 
                            xaxis_title='Âge',
                            yaxis_title='Nombre de clients',
                            margin=dict(l=20, r=20, t=50, b=20))

        # Afficher l'histogramme
        st.plotly_chart(fig_age)

    with col7:
        # Compter le nombre d'hommes et de femmes
        gender_counts = filtered_data['Gender'].value_counts().reset_index()
        gender_counts.columns = ['Gender', 'Count']

        # Créer le diagramme en barres
        fig_gender = px.bar(gender_counts, 
                            x='Gender', 
                            y='Count', 
                            title='Nombre d\'hommes et de femmes',
                            labels={'Gender': 'Genre', 'Count': 'Nombre'},
                            color='Gender', 
                            color_discrete_sequence=['blue', 'pink'])  # Couleurs pour hommes et femmes

        # Calculer le pourcentage sur la base des comptes
        total_count = gender_counts['Count'].sum()
        gender_counts['Percentage'] = (gender_counts['Count'] / total_count) * 100

        # Mettre à jour les traces pour afficher le nombre et le pourcentage
        fig_gender.update_traces(texttemplate='%{y} (<br>%{customdata:.1f}%)',
                                customdata=gender_counts['Percentage'],
                                textposition='outside')

        # Mettre à jour la mise en page
        fig_gender.update_layout(title_font_size=20, 
                                xaxis_title='Genre', 
                                yaxis_title='Nombre',
                                margin=dict(l=20, r=20, t=50, b=20))

        # Afficher le diagramme en barres
        st.plotly_chart(fig_gender)



    # Grouper par mois-année et calculer le total des ventes
    monthly_sales = (filtered_data
                     .groupby(filtered_data['order_date'].dt.to_period('M'))['total']
                     .sum()
                     .reset_index())
    
    # Convertir 'order_date' en format datetime pour le tracé
    monthly_sales['order_date'] = monthly_sales['order_date'].dt.to_timestamp()

    # Créer la courbe
    fig_monthly_sales = px.line(monthly_sales, 
                                 x='order_date', 
                                 y='total', 
                                 title='Total des ventes par mois',
                                 labels={'order_date': 'Mois', 'total': 'Total des ventes'},
                                 markers=True)

    # Mettre à jour la mise en page
    fig_monthly_sales.update_layout(title_font_size=20, 
                                     xaxis_title='Mois', 
                                     yaxis_title='Total des ventes',
                                     margin=dict(l=20, r=20, t=50, b=20))

    # Afficher la courbe
    st.plotly_chart(fig_monthly_sales)


     # Ajouter les colonnes de latitude et longitude
    filtered_data['Latitude'] = filtered_data['State'].map(lambda x: state_coordinates[x][0] if x in state_coordinates else None)
    filtered_data['Longitude'] = filtered_data['State'].map(lambda x: state_coordinates[x][1] if x in state_coordinates else None)

    # Calculer le total des ventes par État
    sales_by_state = (filtered_data
                      .groupby('State')
                      .agg({'total': 'sum', 'Latitude': 'first', 'Longitude': 'first'})
                      .reset_index())
    
    fig = px.scatter_geo(sales_by_state,
                         lat='Latitude',
                         lon='Longitude',
                         size='total',
                         hover_name='State',
                         title='Total des ventes par État',
                         size_max=20,
                         template='plotly')

    # Mettre à jour la mise en page
    fig.update_layout(title_font_size=20)

    # Afficher la carte
    st.plotly_chart(fig)