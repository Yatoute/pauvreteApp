import pandas as pd
import numpy as np
import streamlit as st
import pickle
import sklearn
from myfunctions import init_session_men, set_custom_style, Id_men, Statut_men, load_gb



# 📦 🔄 🚀 💡 🖲️


# Page d'accueil
def welcome_page(saved_data):
    # Configuration de la page
    if saved_data not in st.session_state :
        # Afficher la barre latérale pour chaque nouvelle session
        st.set_page_config(page_title= "Identifiants du ménage", page_icon='🏡', layout="centered", initial_sidebar_state ="expanded")
        st.session_state.saved_data = init_session_men('', '', 0,0,0)
    else : 
        st.set_page_config(page_title= "Identifiants du ménage", page_icon='🏡', layout="centered", initial_sidebar_state ="auto")
    
        
    # Chargement du modèle
    model_gb = load_gb("XGBoost.pkl")
        
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
    sect1 = '<b style="font-family:serif; color:#6082B6; font-size:30px;">🏡 Identifiants du ménage</b>'
    st.markdown(sect1, unsafe_allow_html=True)
    st.write("")
    st.write("")
    nom = st.text_input("# ***👨 Nom et prénom du chef de ménage***",data.get('nom'))
    st.write("")
    contact = st.text_input("# ***📞 Contact du ménage***", data.get('contact'))
    st.write("")
    Taill_men = st.number_input("# ***🏷️ Le ménage compte combien de personnes ?***", 0,100, data.get('Taill_men'))
    st.write("")
    Age15Plus = st.number_input("# ***🏷️ Combien sont âgés de 15 ans ou plus ?***" , 0, None, data.get('Age15Plus'))
    st.write("")
    Age8_14 = st.number_input("# ***🏷️ Combien sont âgés de 8 à 14 ans ?***" , 0, None, data.get('Age8_14'))
    st.write("")
    # Enregistrer les données dans les cookies ou la session
    st.session_state.saved_data.update(init_session_men(nom, contact, Taill_men, Age15Plus, Age8_14))
    
    # Statut du ménage
    sections = {'Alphabet_y' : "Education", 'Nb_Consult' : "Santé", 'FIESE1_1' : "Sécurité alimentaire",'NoEauPotable_1' : 'Conditions de vie du ménage'}
    result =""
    if st.sidebar.button("🖲️ Statut du ménage") :
        Statut_men(data, model_gb)
    text = """
       <b style="font-family:algerian; text-align: center; background-color: #e3efef; color:#6082B6; font-size:35px;">OEVM</b>
       <div style="padding: 15px; border: 2px solid #333;"><p>L'outil d'évaluation de la vulnérabilité des ménages (OEVM) vise à évaluer de manière régulière l’impact des politiques de réductions mise en place au Sénégal. Cette application opère au moyen d’un formulaire au sein duquel sont recueillies certaines informations  spécifiques au ménage, minutieusement réparties en cinq sections, à savoir : « Identifiants du ménage », « Éducation », « Santé », « Sécurité alimentaire » et « Conditions de vie du ménage ». Ces informations peuvent être renseigné en plus ou moins 10 minutes. Après avoir renseigner toutes les sections, l’utilisateur clique sur le bouton « Statut du ménage » pour voCette application opère au moyen d’un formulaire au sein duquel sont recueillies certaines informations  spécifiques au ménage, minutieusement réparties en cinq sections, à savoir : « Identifiants du ménage », « Éducation », « Santé », « Sécurité alimentaire » et « Conditions de vie du ménage ». Ces informations peuvent être renseigné en plus ou moins 10 minutes. Après avoir renseigner toutes les sections, l’utilisateur clique sur le bouton « Statut du ménage » pour voir le statut de vulnérabilité de son ménage.</p></div>
       """
    st.sidebar.markdown(text, unsafe_allow_html=True)  
    
    st.markdown('<div class="footer"><button>🏡 Identifiants du ménage</button></div>', unsafe_allow_html=True)
        
if __name__=='__main__':
    welcome_page('saved_data')
