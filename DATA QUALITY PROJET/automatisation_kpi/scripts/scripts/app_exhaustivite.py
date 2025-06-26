import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO

# Configuration de la page
st.set_page_config(page_title="Calculateur d'Exhaustivité")
st.title("Calculateur d'Exhaustivité")
st.markdown("Calculs terminés avec succès.")

# Lecture des fichiers CSV
try:
    df_mensuel = pd.read_csv("trafic_data_monthly.csv")
    df_otari = pd.read_csv("trafic_otari.csv")

    # Nettoyage des colonnes
    df_mensuel['total_brouille'] = df_mensuel['total_brouille'].astype(str).str.replace(",", ".").astype(float)
    df_otari['volume'] = df_otari['volume'].astype(str).str.replace(",", ".").astype(float)

    # Calculs
    somme_mensuel = df_mensuel['total_brouille'].sum()
    somme_otari = df_otari['volume'].sum()
    diff = abs(somme_mensuel - somme_otari)
    exhaustivite = (min(somme_mensuel, somme_otari) / max(somme_mensuel, somme_otari)) * 100

    # Affichage des résultats dans l'application
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Fichier Mensuel", f"{somme_mensuel:,.2f}", delta=f"{len(df_mensuel)} lignes")
    with col2:
        st.metric("Fichier OTARI", f"{somme_otari:,.2f}", delta=f"{len(df_otari)} lignes")

    col3, col4 = st.columns(2)
    with col3:
        st.metric("Différence Absolue", f"{diff:,.2f}")
    with col4:
        st.metric("Exhaustivité", f"{exhaustivite:.4f}%", delta="Taux de couverture des données")

    # Génération du rapport texte
    rapport = StringIO()
    rapport.write("RÉSULTATS DU CALCUL D'EXHAUSTIVITÉ\n")
    rapport.write("=" * 50 + "\n\n")
    rapport.write(f"Somme Mensuel       : {somme_mensuel:,.2f}\n")
    rapport.write(f"Somme OTARI         : {somme_otari:,.2f}\n")
    rapport.write(f"Différence Absolue  : {diff:,.2f}\n")
    rapport.write(f"Taux d'exhaustivité : {exhaustivite:.4f}%\n")

    # Bouton de téléchargement
    st.download_button(
        label="Télécharger les résultats",
        data=rapport.getvalue(),
        file_name="resultats_exhaustivite.txt",
        mime="text/plain"
    )

except FileNotFoundError as e:
    st.error(f"Fichier introuvable : {e.filename}")
    st.stop()

except Exception as e:
    st.error(f"Une erreur est survenue : {str(e)}")
    st.stop()
