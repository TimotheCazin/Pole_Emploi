import streamlit as st
import pandas as pd
import altair as alt
import requests

st.title("Salaires checker France Travail")

url = "https://salaires-417017.ew.r.appspot.com/predict"

url_or_id = st.text_input('URL or ID de l\'offre')
if len(url_or_id) != 0:
    data = {"url_or_id": url_or_id}
    try:
        salaire_pred = requests.post(url, json=data).json()['prediction']
        st.write('Le salaire estimé est de', round(salaire_pred), '€ mensuel brut.')
    except Exception as e:
        st.error("Erreur dans l'url ou l'id.")
        salaire_pred = 0
else:
    salaire_pred = 0

st.write("")  # Espacement

bin_pred = int(salaire_pred/100)*100

df_model = pd.read_csv('df_model.csv')

intervalles = list(range(0, int(df_model['salaires_final'].max()) + 100, 100))

# Création des bins pour l'histogramme
intervalles_label = [intervalle for intervalle in intervalles[:-1]]
df_model['salaires_bins'] = pd.cut(df_model['salaires_final'], bins=intervalles, labels=intervalles_label, right=False)

# Création de l'histogramme avec Altair
histogram = alt.Chart(df_model).mark_bar().encode(
    x=alt.X('salaires_bins:O', axis=alt.Axis(title='Salaires')),
    y=alt.Y('count()', axis=alt.Axis(title='Nombre de salariés')),
    color=alt.condition(
        alt.datum.salaires_bins == bin_pred,  # Condition pour la couleur rouge
        alt.value('red'),  # Si la condition est vraie
        alt.value('steelblue')  # Si la condition est fausse
    )
).properties(
    title="Répartition des salaires"
)

st.altair_chart(histogram, use_container_width=True)