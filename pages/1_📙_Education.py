import pandas as pd
import numpy as np
import streamlit as st
import pickle
import sklearn
from myfunctions import init_session_men, init_session_educ, set_custom_style, Id_men, Statut_men, load_gb
st.set_page_config(page_title= "Education", page_icon='📙', layout="centered")



def education_page():
    
     # Chargement du modèle
     model_gb = load_gb("XGBoost.pkl")
     
    # Utilisez les données sauvegardées dans les cookies ou la session pour personnaliser l'évaluation
     # Vérifier si les données sur l'éducation ont étée sauvégardées une fois
     if 'saved_data' not in st.session_state:
         st.session_state.saved_data = init_session_men('', '', 0,0,0)

     if 'Alphabet_y' not in st.session_state.saved_data :
         st.session_state.saved_data.update(init_session_educ(0,0,0))
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
     
     # Section 2 : Education
     
     
     st.write("")
     st.write("")
     sect2 = '<b style="font-family:serif; color:#6082B6; font-size:38px;">📙 Education</b>'
     st.markdown(sect2, unsafe_allow_html=True)
     st.write("")
    ## Alphabétisation
     Alphabet_y = st.number_input("# ***🏷️ Parmi les personnes âgées de 15 ans ou plus dans le ménage, combien savent lire et écrire ?***" , 0, None, data.get('Alphabet_y'))
     st.write("")
    ## Niveau de scolarisation
     Niveau_Scol_y = st.number_input("# ***🏷️ Parmi les personnes âgées de 15 ans ou plus dans le ménage, combien ont pu complèté six années d'études ?***" , 0, None, data.get('Niveau_Scol_y'))
     st.write("")
     if data.get('Age8_14') > 0 :
         ## Fréquentation scolaire
         Freq_Scolaire_y = st.number_input("# ***🏷️ Parmi les enfants de 8 à 14 ans dans le ménage, combien fréquentent une école ?***" , 0, None, data.get('Freq_Scolaire_y'))
         st.write("")
        #
     else :
         Freq_Scolaire_y = 0
    # Enrégistré les données
    # Enregistrer les données dans les cookies ou la session
     st.session_state.saved_data.update(init_session_educ(Alphabet_y,Niveau_Scol_y,Freq_Scolaire_y))
     
     # Prédire
     sections = {'Alphabet_y' : "Education", 'Nb_Consult' : "Santé", 'FIESE1_1' : "Sécurité alimentaire",'NoEauPotable_1' : 'Conditions de vie du ménage'}
     result =""
     
     if st.sidebar.button("🖲️ Statut du ménage") :
         Statut_men(data, model_gb)
    
     Id_men(data)
     
     st.markdown('<div class="footer"><button>Evaluation de la vulnérabilité des ménages</button></div>', unsafe_allow_html=True)
     
         
education_page()   
