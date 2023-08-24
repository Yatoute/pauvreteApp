import pandas as pd
import numpy as np
import streamlit as st
import pickle
import sklearn
from myfunctions import init_session_men, init_session_vie, set_custom_style, Id_men, Statut_men, load_gb

st.set_page_config(page_title= "Conditions de vie", page_icon='🏕️', layout="centered")


def vie_page():
     
     # Chargement du modèle
     model_gb = load_gb("XGBoost.pkl")
    # Utilisez les données sauvegardées dans les cookies ou la session pour personnaliser l'évaluation
     # Vérifier si les données sur la santé ont étée sauvégardées une fois
     if 'saved_data' not in st.session_state:
         st.session_state.saved_data = init_session_men('', '', 0,0,0)

     if 'NoEauPotable_1' not in st.session_state.saved_data :
         st.session_state.saved_data.update(init_session_vie('','','','','','',''))
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
     
     
     # Section 5 : Conditions de vie
     st.write("")
     sect5 = '<b style="font-family:serif; color:#6082B6; font-size:38px;">🏕️ Conditions de vie du ménage</b>'
     st.markdown(sect5, unsafe_allow_html=True)
     st.write("")
     ## Accès à l'eau potable
     NoEauPotable_1 = st.selectbox("# ***🏷️ Le ménage a t-il accès à une eau potable buvable ?***", ["OUI", "NON", ''], ["OUI", "NON", ''].index(data.get('NoEauPotable_1')))
     st.write("")
     ## Accès à l'électricité
     Electricite_1 = st.selectbox("# ***🏷️ Le ménage a t-il accès à l'électricité ?***", ["OUI", "NON", ''], ["OUI", "NON", ''].index(data.get('Electricite_1')))
     st.write("")
     ## Utilisation du combustible pour cuisson
     Combustible_1 = st.selectbox("# ***🏷️ Le ménage dispose t-il un combustible pour cuisson approprié(gaz, électricité, pétrole ou huile) ?***", ["OUI", "NON", ''], ["OUI", "NON", ''].index(data.get('Combustible_1')))
     st.write("")
     ## Sanitaire
     Sanitaire_1 =  st.selectbox("# ***🏷️ le ménage dispose t-il des toilettes avec chasse d’eau et des latrines améliorées ?***", ["OUI", "NON", ''], ["OUI", "NON", ''].index(data.get('Sanitaire_1')))
     st.write("")
     ## Materiaux du toit
     Materio_toit_1 = st.selectbox("# ***🏷️ Le principal matériel du toi du ménage est-il appropiré (tôle, tuile ou dalle en ciment ) ?***", ["OUI", "NON", ''], ["OUI", "NON", ''].index(data.get('Materio_toit_1')))
     st.write("")
     ## Revêtement du sol
     Revet_sol_1 = st.selectbox("# ***🏷️ le sol du logement est-il approprié (fait du ciment ou carrelage) ?***", ["OUI", "NON", ''], ["OUI", "NON", ''].index(data.get('Revet_sol_1')))
     st.write("")
     ## Matériaux de construction des murs extérieurs : les matériaux de constructions des murs extérieurs sont 
     MursExterieur_1 = st.selectbox("# ***🏷️ les matériaux de constructions des murs extérieurs sont-ils appropriés (en ciment, béton, pierres, briques cuites, bac alu, vitres ou banco amélioré) ?***", ["OUI", "NON", ''], ["OUI", "NON", ''].index(data.get('MursExterieur_1')))
     st.write("")
    # Enregistrer les données dans les cookies ou la session
     st.session_state.saved_data.update(init_session_vie(NoEauPotable_1, Electricite_1, Combustible_1, Sanitaire_1, Materio_toit_1, Revet_sol_1, MursExterieur_1))
     
     # Statut du ménage
     sections = {'Alphabet_y' : "Education", 'Nb_Consult' : "Santé", 'FIESE1_1' : "Sécurité alimentaire",'NoEauPotable_1' : 'Conditions de vie du ménage'}
     result =""
     if st.sidebar.button("🖲️ Statut du ménage") :
         Statut_men(data, model_gb)
        
     Id_men(data)
     st.markdown('<div class="footer"><button>🏕️ Conditions de vie du ménage</button></div>', unsafe_allow_html=True)
         
vie_page()   
