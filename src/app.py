import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dotenv import load_dotenv
import sys
import os

# Imports de nos nouveaux modules
from modules.architect import run_architect_agent
from modules.engineer import run_engineer_agent
from utils.data_loader import load_csv_file, load_hf_dataset

# Chargement de la configuration
load_dotenv()
st.set_page_config(page_title="AI DataViz - Architecture Multi-LLM", page_icon="🏗️", layout="wide")

st.title("🏗️ Assistant DataViz (Architecture Scaffolding)")
st.markdown("---")

# --- 1. CHARGEMENT DES DONNÉES ---
with st.sidebar:
    st.header("1. Données")
    source = st.radio("Source :", ["Exemples", "Upload CSV"])
    
    df = None
    if source == "Upload CSV":
        up_file = st.file_uploader("Fichier CSV", type="csv")
        if up_file:
            df = load_csv_file(up_file)
    else:
        ds_name = st.selectbox("Dataset", ["Titanic", "Tips", "Iris"])
        if st.button("Charger"):
            df = load_hf_dataset(ds_name)
            st.session_state['df'] = df

    # Persistance
    if 'df' in st.session_state and df is None:
        df = st.session_state['df']

# --- 2. INTERFACE PRINCIPALE ---
if df is not None:
    st.write("### Aperçu", df.head(3))
    
    # Zone de saisie
    with st.container():
        st.header("2. Problématique")
        question = st.text_input("Quelle analyse souhaitez-vous ?", placeholder="Ex: Montre l'impact de la classe sur la survie")
        
        if st.button("🚀 Lancer l'Architecte (Agent 1)"):
            with st.spinner("L'Architecte analyse le schéma et élabore une stratégie..."):
                # APPEL AGENT 1
                propositions = run_architect_agent(df, question)
                st.session_state['propositions'] = propositions
                st.session_state['question'] = question

    # Affichage des cartes (Résultat Agent 1)
    if 'propositions' in st.session_state:
        st.divider()
        st.header("3. Stratégie proposée")
        cols = st.columns(3)
        
        for i, prop in enumerate(st.session_state['propositions']):
            with cols[i]:
                st.info(f"**{prop.titre}**")
                st.caption(prop.type_graphique)
                st.write(f"_{prop.justification}_")
                
                if st.button(f"Générer ce graphe", key=f"btn_{i}"):
                    st.session_state['selected_plan'] = prop
                    st.rerun()

    # Génération finale (Appel Agent 2)
    if 'selected_plan' in st.session_state:
        plan = st.session_state['selected_plan']
        st.divider()
        st.header(f"4. Résultat : {plan.titre}")
        
        with st.spinner("L'Ingénieur écrit le code Python..."):
            # APPEL AGENT 2
            code = run_engineer_agent(df, st.session_state['question'], plan)
            
            with st.expander("Voir le code généré par l'Ingénieur"):
                st.code(code, language='python')
            
            # Exécution
            ldict = {"df": df, "px": px, "go": go, "make_subplots": make_subplots}
            try:
                exec(code, globals(), ldict)
                if "generate_plot" in ldict:
                    fig = ldict["generate_plot"](df)
                    
                    # Bouton natif pour l'export
                    fig.update_layout(modebar_add=["toImage"], modebar_orientation="h")
                    
                    st.plotly_chart(fig, use_container_width=True)
                    st.success("Visualisation générée avec succès par l'architecture Multi-LLM.")
                else:
                    st.error("Erreur : Fonction introuvable.")
            except Exception as e:
                st.error(f"Erreur d'exécution : {e}")

else:
    st.info("👈 Veuillez charger des données pour commencer.")