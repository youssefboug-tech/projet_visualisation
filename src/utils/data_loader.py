import pandas as pd
import streamlit as st
from datasets import load_dataset

def load_csv_file(uploaded_file):
    """Charge un CSV en gérant les séparateurs (, ou ;)"""
    try:
        # On se remet au début du fichier
        uploaded_file.seek(0)
        
        # Tentative 1 : lecture standard (virgule)
        df = pd.read_csv(uploaded_file)
        
        # Si le fichier a une seule colonne, c'est suspect -> on tente le point-virgule
        if len(df.columns) <= 1:
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, sep=';')
            
        return df
        
    except Exception as e:
        st.error(f"Erreur de lecture du fichier CSV : {e}")
        return None

def load_hf_dataset(dataset_name):
    """Charge un dataset depuis une URL stable (GitHub Seaborn Data)"""
    # Dictionnaire des URLs brutes (plus stable que load_dataset pour la démo)
    DATASETS = {
        "Titanic": "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv",
        "Tips": "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv",
        "Iris": "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
    }
    
    try:
        url = DATASETS.get(dataset_name)
        if url:
            return pd.read_csv(url)
        else:
            st.error("Dataset non trouvé dans la liste.")
            return None
            
    except Exception as e:
        st.error(f"Erreur de chargement du dataset : {e}")
        return None