import pandas as pd
import numpy as np
import streamlit as st
import pickle
import sklearn
from myfunctions import init_session_men, init_session_aliment, set_custom_style, Id_men, Statut_men, load_gb

st.set_page_config(page_title= "Sécurité alimentaire", page_icon='🧆', layout="centered")


def aliment_page():
     
     # Chargement du modèle
     model_gb = load_gb("XGBoost.pkl")
    
    # Utilisez les données sauvegardées dans les cookies ou la session pour personnaliser l'évaluation
     # Vérifier si les données sur la santé ont étée sauvégardées une fois
     if 'saved_data' not in st.session_state:
         st.session_state.saved_data = init_session_men('', '', 0,0,0)

     if 'FIESE1_1' not in st.session_state.saved_data :
         st.session_state.saved_data.update(init_session_aliment('','','','','',''))
     data = st.session_state.saved_data

    # la police et la couleur de fond, le padding et le texte à afficher
     
     set_custom_style()
     html_temp = """
     <div style ="background-color:#31333F ; padding:12px">
     <h1 style ="font-family:serif;color:#6082B6;text-align:center;">💡💡💡💡💡💡💡💡 <br>Evaluation de la vulnérabilité <br>des ménages </h1>
     </div>
     """
 
     # Titre
     st.markdown(html_temp, unsafe_allow_html=True)
     
     
     # Section 4 : Sécurité alimentaire
     st.write("")
     sect4 = '<b style="font-family:serif; color:#6082B6; font-size:38px;">🧆 Sécurité alimentaire</b>'
     st.markdown(sect4, unsafe_allow_html=True)
     st.write("")
     ## FIESE1
     FIESE1_1 = st.selectbox("🏷️ Au cours des 12 derniers mois, vous ou d'autres membres de votre ménage avez été inquiet(s) de ne pas avoir suffisamment de nourriture par manque d’argent ou d’autres ressources ?", ["NON", "OUI", ''], ["NON", "OUI", ''].index(data.get('FIESE1_1')))
     st.write("")
     ## FIESE2
     FIESE2_1 = st.selectbox("🏷️ Au cours des 12 derniers mois, vous ou d'autres membres de votre ménage n'avez pas pu manger une nourriture saine et nutritive par manque d’argent ou d’autres ressources ?", ["NON", "OUI", ''], ["NON", "OUI", ''].index(data.get('FIESE2_1')))
     st.write("")
     ## FIESE3
     FIESE3_1 = st.selectbox("🏷️ Au cours des 12 derniers mois, vous ou d'autres membres de votre ménage avez mangé une nourriture peu variée par manque d’argent ou d’autres ressources ?" , ["NON", "OUI", ''], ["NON", "OUI", ''].index(data.get('FIESE3_1')))
     st.write("")
     ## FIESE4
     FIESE4_1 = st.selectbox("🏷️ Au cours des 12 derniers mois, vous ou d'autres membres de votre ménage avez dû sauter un repas parce qu’il n’y avait pas assez d’argent ou d’autres ressources pour se procurer à manger ?", ["NON", "OUI", ''], ["NON", "OUI", ''].index(data.get('FIESE4_1')))
     st.write("")
     ## FIESE5
     FIESE5_1 = st.selectbox("🏷️ Au cours des 12 derniers mois, vous ou d'autres membres de votre ménage avez mangé moins que ce que vous pensiez que vous auriez dû manger à cause d’un manque d’argent ou d’autres ressources ?", ["NON", "OUI", ''], ["NON", "OUI", ''].index(data.get('FIESE5_1')))
     st.write("")
     ## FIESE6
     FIESE6_1 = st.selectbox("🏷️ Au cours des 12 derniers mois, votre ménage n'avait de nourriture parce qu’il n’y avait plus assez d’argent ou d’autres ressources ?", ["NON", "OUI", ''], ["NON", "OUI", ''].index(data.get('FIESE6_1')))
     st.write("")
    # Enregistrer les données dans les cookies ou la session
     st.session_state.saved_data.update(init_session_aliment(FIESE1_1, FIESE2_1, FIESE3_1, FIESE4_1, FIESE5_1, FIESE6_1))
     
     # Statut du ménage
     sections = {'Alphabet_y' : "Education", 'Nb_Consult' : "Santé", 'FIESE1_1' : "Sécurité alimentaire",'NoEauPotable_1' : 'Conditions de vie du ménage'}
     result =""
     if st.sidebar.button("🖲️ Statut du ménage") :
         Statut_men(data, model_gb)

     Id_men(data)           
     st.markdown('<div class="footer"><button>Evaluation de la vulnérabilité des ménages</button></div>', unsafe_allow_html=True)
         
aliment_page()   
