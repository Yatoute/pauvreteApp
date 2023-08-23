import pandas as pd
import numpy as np
import streamlit as st
import pickle
import sklearn
from myfunctions import init_session_men, set_custom_style, Id_men, Statut_men, load_gb

# Définir le titre et la largeur de la page en mode large
st.set_page_config(page_title= "Identifiants du ménage", page_icon='🏠', layout="centered")

# 📦 🔄 🚀 💡 🖲️




# Page d'accueil
def welcome_page(): 
    
    # Chargement du modèle
    model_gb = load_gb("XGBoost.pkl")
    
    # Charger les données sauvegardées dans les cookies ou la session
    if 'saved_data' not in st.session_state :
        st.session_state.saved_data = init_session_men('', '', 0,0,0)

    data = st.session_state.saved_data
    
    # Style
    set_custom_style()
    html_temp = """
    <div style ="background-color:#31333F ; padding:12px">
    <h1 style ="font-family:serif;color:#6082B6;text-align:center;">💡💡💡💡💡💡💡💡 <br>Evaluation de la vulnérabilité <br>des ménages </h1>
    </div>
    """
    # Titre
    st.markdown(html_temp, unsafe_allow_html=True)

    # Identifiants du ménage
 
    st.write("")
    sect1 = '<b style="font-family:serif; color:#6082B6; font-size:30px;">📦 Identifiant du ménage</b>'
    st.markdown(sect1, unsafe_allow_html=True)
    st.write("")
    st.write("")
    nom = st.text_input("➡️ Nom et prénom du chef de ménage",data.get('nom'))
    st.write("")
    contact = st.text_input("➡️ Contact du ménage", data.get('contact'))
    st.write("")
    Taill_men = st.number_input("➡️ Le ménage compte combien de personnes ?", 0,100, data.get('Taill_men'))
    st.write("")
    Age15Plus = st.number_input("➡️ Combien sont âgés de 15 ans ou plus ?" , 0, None, data.get('Age15Plus'))
    st.write("")
    Age8_14 = st.number_input("➡️ Combien sont âgés de 8 à 14 ans ?" , 0, None, data.get('Age8_14'))
    st.write("")
    # Enregistrer les données dans les cookies ou la session
    st.session_state.saved_data.update(init_session_men(nom, contact, Taill_men, Age15Plus, Age8_14))
    
    # Statut du ménage
    sections = {'Alphabet_y' : "Education", 'Nb_Consult' : "Santé", 'FIESE1_1' : "Sécurité alimentaire",'NoEauPotable_1' : 'Conditions de vie du ménage'}
    result =""
    if st.sidebar.button("🖲️ Statut du ménage") :
        Statut_men(data, model_gb)
        
    Id_men(data)   
    st.markdown('<div class="footer"><button>Evaluation de la vulnérabilité des ménages</button></div>', unsafe_allow_html=True)


        
if __name__=='__main__':
        welcome_page()