import pandas as pd
import numpy as np
import streamlit as st
import pickle
import sklearn

# Chargement du modèle
@st.cache_data
def load_gb(urls) :
    # Chargement du modèle pré-formé
    pickle_in = open(urls, 'rb')
    model_gb = pickle.load(pickle_in)
    return model_gb

# Adress du ménage
@st.cache_data(experimental_allow_widgets=True)
def  Id_men(data) : 
    # Identifiant du ménage       
    sect1 = '<b style="font-family:serif; color:#6082B6; font-size:20px;">🏡 Adresse du ménage</b>'
    st.sidebar.markdown(sect1, unsafe_allow_html=True)
    st.sidebar.write("")
    nom = st.sidebar.text_input("👨 Chef du ménage ",data.get('nom'))
    st.sidebar.write("")
    contact = st.sidebar.text_input("📞 Contact", data.get('contact'))
    st.sidebar.write("")
    data.update({'nom': nom, 'contact':contact})

# Prédire le statut du ménage
sections = {'Alphabet_y' : "Education", 'Nb_Consult' : "Santé", 'FIESE1_1' : "Sécurité alimentaire",'NoEauPotable_1' : 'Conditions de vie du ménage'}

@st.cache_data
def Statut_men(data, _model_gb) :
    for var in sections :
        if var not in data :
            st.sidebar.success(f"Veuillez renseigner la section {sections.get(var)}")
            break
    else :
        if "" in data.values() :
            st.sidebar.success("Certains champs sont non renseignés. Veillez les renseigner par section !!!")
        elif data.get('Taill_men') == 0:
            st.sidebar.success("Dans la section Identifiant du ménage, le ménage doit compter une personne au moins.")
        elif data.get('Age15Plus')==0 and data.get('Age8_14')==0 :
            st.sidebar.success("Dans la section Identifiant du ménage, au moins une personne du ménage doit être âgée de plus de 8 ans")
        elif data.get('Taill_men') < data.get('Age15Plus') + data.get('Age8_14') :
            st.sidebar.success("Dans la section Identifiant du ménage, le nombre total des personnes âgées de 8 à 14 ans et ceux âgées de 15 ans ou plus ne doit pas dépassé la taille du ménage.")
        elif data.get('Alphabet_y') > data.get('Age15Plus') :
            st.sidebar.success(f"Dans la section Education, vous avez renseigné {data.get('Alphabet_y')} personnes âgées de 15 et plus qui savant lire écrire. Or le nombre de personnes âgées de 15 et plus est de {data.get('Age15Plus')}")
        elif data.get('Niveau_Scol_y') > data.get('Age15Plus') :
            st.sidebar.success(f"Dans la section Education, vous avez renseigné {data.get('Niveau_Scol_y')} personnes âgées de 15 et plus qui ont complèté six années d'études . Or le nombre de personnes âgées de 15 et plus est de {data.get('Age15Plus')}")
        elif data.get('Freq_Scolaire_y') > data.get('Age8_14') :
            st.sidebar.success(f"Dans la section Education, vous avez renseigné {data.get('Freq_Scolaire_y')} enfants âgés de 8 à 14 ans qui fréquentent une école . Or le nombre d'enfants âgés de 8 à 14 ans est de {data.get('Age8_14')}")
        elif data.get('Nb_Consult') > data.get('Taill_men') :
            st.sidebar.success(f"Dans la section Santé, vous avez renseigné {data.get('Nb_Consult')} personnes ayant consulté des services de santé. Or le ménage ne compte que {data.get('Taill_men')} personnes")
        elif data.get('Satisfait_y') > data.get('Nb_Consult')  :
            st.sidebar.success(f"Dans la section Santé, vous avez renseigné {data.get('Satisfait_y')} personnes satifaites des services de santée . Or {data.get('Nb_Consult')} personnes en ont consulté.")
        elif data.get('Couv_Maladi_y') > data.get('Taill_men') :
            st.sidebar.success(f"Dans la section Santé, vous avez renseigné {data.get('Couv_Maladi_y')} personnes couvertes par une assurance maladie . Or le ménage ne compte que {data.get('Taill_men')} personnes")
        elif data.get('Chroniq_y') > data.get('Taill_men') :
            st.sidebar.success(f"Dans la section Santé, vous avez renseigné {data.get('Chroniq_y')} personnes souffrant d'une maladie chronique . Or le ménage ne compte que {data.get('Taill_men')} personnes")
        elif data.get('Handicap_y') > data.get('Taill_men') :
            st.sidebar.success(f"Dans la section Santé, vous avez renseigné {data.get('Handicap_y')} personnes souffrant d'un handicap mental ou physique . Or le ménage ne compte que {data.get('Taill_men')} personnes")
        else :
            # Education ---------------------------------------------------------
            if data.get('Age15Plus') != 0 :
                Alphabet_y = data.get('Alphabet_y')/data.get('Age15Plus')
                Niveau_Scol_y = data.get('Niveau_Scol_y')/data.get('Age15Plus')
            else :
                Alphabet_y = 1
                Niveau_Scol_y = 1
                
            if data.get('Age8_14') != 0 :
                Freq_Scolaire_y = data.get('Freq_Scolaire_y')/data.get('Age8_14')
            else :
                Freq_Scolaire_y = 1
            
            # Santé -------------------------------------------------------------
            if data.get('Nb_Consult') !=0 :
                Satisfait_y = data.get('Satisfait_y')/data.get('Nb_Consult')
            else :
                Satisfait_y = 1
            Taill_men = data.get('Taill_men')
            Couv_Maladi_y = data.get('Couv_Maladi_y')/Taill_men
            Chroniq_y = 1-data.get('Chroniq_y')/Taill_men
            Handicap_y = 1-data.get('Handicap_y')/Taill_men
            
            # Sécurité alimentaire--------------------------------------------------
            FIESE1_1 = ["NON", "OUI"].index(data.get('FIESE1_1'))
            FIESE2_1 = ["NON", "OUI"].index(data.get('FIESE2_1'))
            FIESE3_1 = ["NON", "OUI"].index(data.get('FIESE3_1'))
            FIESE4_1 = ["NON", "OUI"].index(data.get('FIESE4_1'))
            FIESE5_1 = ["NON", "OUI"].index(data.get('FIESE5_1'))
            FIESE6_1 = ["NON", "OUI"].index(data.get('FIESE6_1'))
           
            # Conditions de vie-----------------------------------------------------------
            NoEauPotable_1 = ["OUI", "NON"].index(data.get('NoEauPotable_1'))
            Electricite_1 = ["OUI", "NON"].index(data.get('Electricite_1'))
            Combustible_1 = ["OUI", "NON"].index(data.get('Combustible_1'))
            Sanitaire_1 = ["OUI", "NON"].index(data.get('Sanitaire_1'))
            Materio_toit_1 = ["OUI", "NON"].index(data.get('Materio_toit_1'))
            Revet_sol_1 = ["OUI", "NON"].index(data.get('Revet_sol_1'))
            MursExterieur_1 = ["OUI", "NON"].index(data.get('MursExterieur_1'))
            
            # Prédire
            result = _model_gb.predict([[FIESE5_1, FIESE2_1, FIESE1_1, FIESE3_1, Electricite_1, Alphabet_y, Combustible_1, Freq_Scolaire_y, FIESE6_1, Sanitaire_1, Handicap_y, Satisfait_y, FIESE4_1, Chroniq_y, Materio_toit_1, Couv_Maladi_y, Revet_sol_1, MursExterieur_1, NoEauPotable_1, Niveau_Scol_y]])
            if result[0] == 1 : 
                result = "Ménage vulnérable"
            else :
                result = "Ménage non vulnérable"
            st.sidebar.success(result)
    
    
# Fonction pour initialiser les données de session de ménage
@st.cache_data
def init_session_men(nom, contact, Taill_men, Age15Plus, Age8_14):
    return {
       'nom' : nom,
       'contact' : contact,
       'Taill_men' : Taill_men,
       'Age15Plus' : Age15Plus,
       'Age8_14' : Age8_14
    }

# Fonction pour initialiser les données de session éducation
@st.cache_data
def init_session_educ(Alphabet_y,Niveau_Scol_y,Freq_Scolaire_y):
    return {
       'Alphabet_y' : Alphabet_y,
       'Niveau_Scol_y' : Niveau_Scol_y,
       'Freq_Scolaire_y' : Freq_Scolaire_y,
    }

# Fonction pour initialiser les données de la session Santé
@st.cache_data
def init_session_sante(Nb_Consult, Satisfait_y, Couv_Maladi_y, Chroniq_y, Handicap_y):
    return {
       'Nb_Consult' : Nb_Consult,
       'Satisfait_y' : Satisfait_y,
       'Couv_Maladi_y' : Couv_Maladi_y,
       'Chroniq_y' : Chroniq_y,
       'Handicap_y' : Handicap_y
    }

# Session Sécurité alimentaire
@st.cache_data
def init_session_aliment(FIESE1_1, FIESE2_1, FIESE3_1, FIESE4_1, FIESE5_1, FIESE6_1) :
    return {
       'FIESE1_1' : FIESE1_1,
       'FIESE2_1' : FIESE2_1,
       'FIESE3_1' : FIESE3_1,
       'FIESE4_1' : FIESE4_1,
       'FIESE5_1' : FIESE5_1,
       'FIESE6_1' : FIESE6_1
    }

# Conditions de vie
@st.cache_data
def init_session_vie(NoEauPotable_1, Electricite_1, Combustible_1, Sanitaire_1, Materio_toit_1, Revet_sol_1, MursExterieur_1) :
    return {
       'NoEauPotable_1' : NoEauPotable_1,
       'Electricite_1' : Electricite_1,
       'Combustible_1' : Combustible_1,
       'Sanitaire_1' : Sanitaire_1,
       'Materio_toit_1' : Materio_toit_1,
       'Revet_sol_1' : Revet_sol_1,
       'MursExterieur_1': MursExterieur_1
    }
    

# Définir les styles de l'application

def set_custom_style():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #E3EFEF; 
            font-family: 'serif';
        }
        .stMarkdown {
            background-color: #f0f0f0; 
            font-family: 'serif';
        }
        p { 
            text-align: justify;
            font-weight: bold;
            
        }
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #f0f0f0;
            padding: 10px;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

