import pandas as pd
import numpy as np
import streamlit as st
import pickle
import sklearn
from myfunctions import init_session_men, init_session_sante, set_custom_style, Id_men, Statut_men, load_gb
st.set_page_config(page_title= "Santé", page_icon='💊', layout="centered")


def sante_page():
    #Chargement du modèle
     model_gb = load_gb("XGBoost.pkl")
    # Utilisez les données sauvegardées dans les cookies ou la session pour personnaliser l'évaluation
     # Vérifier si les données sur la santé ont étée sauvégardées une fois
     if 'saved_data' not in st.session_state:
         st.session_state.saved_data = init_session_men('', '', 0,0,0)
     if 'Nb_Consult' not in st.session_state.saved_data :
         st.session_state.saved_data.update(init_session_sante(0,0,0,0,0))
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
     
     
    # Section 3 : Santé
     st.write("")
     sect3 = '<b style="font-family:serif; color:#6082B6; font-size:38px;">💊 Santé</b>'
     st.markdown(sect3, unsafe_allow_html=True)
     st.write("")
     ## Nombre de consultation
     Nb_Consult = st.number_input("# ***💉 Combien de personnes dans le ménage, ont consulté un service de santé au cours des 30 derniers jours ?***" , 0, None, data.get('Nb_Consult'))
     st.write("")
     ## Satisfaction des soins de santé
     if Nb_Consult > 0 :
         Satisfait_y = st.number_input("# ***💉 Parmi les personnes ayant effectuer une consultation, combien sont satisfaits des services sanitaires lors de leur consultations ?***" , 0, None, data.get('Satisfait_y'))
         st.write("")
     else :
         Satisfait_y =0
     ## Couverture maladie
     Couv_Maladi_y = st.number_input("# ***💉 Combien de personnes dans le ménage, disposent d’une assurance maladie ou bénéficient d’une prise en charge particulière ?***" , 0, None, data.get('Couv_Maladi_y'))
     st.write("")
     ## Maladies chroniques
     Chroniq_y = st.number_input("# ***💉 Combien de personnes dans le ménage, souffrent d'une maladie chronique ?***" , 0, None, data.get('Chroniq_y'))
     st.write("")
     ## Indicape
     Handicap_y = st.number_input("# ***💉 Combien de personnes dans le ménage, souffrent d'un handicap physique ou mental ?***" , 0, None, data.get('Handicap_y'))
     st.write("")
    # Enregistrer les données dans les cookies ou la session
     st.session_state.saved_data.update(init_session_sante(Nb_Consult, Satisfait_y, Couv_Maladi_y, Chroniq_y, Handicap_y))
    
    # Satatut du ménage
     sections = {'Alphabet_y' : "Education", 'Nb_Consult' : "Santé", 'FIESE1_1' : "Sécurité alimentaire",'NoEauPotable_1' : 'Conditions de vie du ménage'}
     result =""
     if st.sidebar.button("🖲️ Statut du ménage") :
         Statut_men(data, model_gb)
        
     Id_men(data)            
     st.markdown('<div class="footer"><button>💊 Santé générale du ménage</button></div>', unsafe_allow_html=True)
         
sante_page()   
