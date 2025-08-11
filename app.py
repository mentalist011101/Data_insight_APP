import streamlit as st
import pandas as pd
from utils.data_cleaner import DataCleaner
from utils.viz_helper import generate_plot
import duckdb

# Configuration de la page
st.set_page_config(
    page_title="DataInsight",
    page_icon="📊",
    layout="wide"
)

# Injection CSS personnalisé
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# State management simplifié
if "df" not in st.session_state:
    st.session_state.df = None
if "steps" not in st.session_state:
    st.session_state.steps = []

# Sidebar avec étapes
with st.sidebar:
    st.header("Workflow")
    st.write("1. Upload → 2. Nettoyer → 3. Visualiser")

# Page Upload
def upload_section():
    st.title("📤 Importer vos données")
    file = st.file_uploader("Déposez un fichier CSV/Excel", type=["csv", "xlsx"])
    
    if file:
        try:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
            
            st.session_state.df = df
            st.success(f"Fichier chargé ({len(df)} lignes)")
            st.dataframe(df.head(3))
            
        except Exception as e:
            st.error(f"Erreur : {str(e)}")

# Page Nettoyage
def clean_section():
    st.title("🧹 Nettoyage des données")
    
    if st.session_state.df is None:
        st.warning("Importez d'abord un fichier")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Commandes rapides")
        if st.button("Supprimer les doublons"):
            cleaner = DataCleaner(st.session_state.df)
            st.session_state.df = cleaner.remove_duplicates()
            st.session_state.steps.append("Suppression doublons")
            
        if st.button("Remplir valeurs manquantes"):
            cleaner = DataCleaner(st.session_state.df)
            st.session_state.df = cleaner.fill_missing()
            st.session_state.steps.append("Remplissage NA")
    
    with col2:
        st.subheader("Commande personnalisée")
        user_cmd = st.text_input("Que faire ? (ex: 'convertir dates en YYYY-MM-DD')")
        if user_cmd:
            cleaner = DataCleaner(st.session_state.df)
            result = cleaner.execute_command(user_cmd)
            if result is not None:
                st.session_state.df = result
                st.session_state.steps.append(f"Commande: {user_cmd}")
    
    st.dataframe(st.session_state.df.head(3))

# Page Visualisation
def visualize_section():
    st.title("📈 Visualisation")
    
    if st.session_state.df is None:
        st.warning("Importez et nettoyez d'abord les données")
        return
    
    col_types = {
        col: "Numérique" if pd.api.types.is_numeric_dtype(st.session_state.df[col]) 
        else "Catégoriel" 
        for col in st.session_state.df.columns
    }
    
    with st.expander("Configuration du graphique"):
        col1, col2 = st.columns(2)
        with col1:
            chart_type = st.selectbox("Type", ["Barre", "Ligne", "Histogramme", "Nuage de points"])
        with col2:
            x_axis = st.selectbox("Axe X", st.session_state.df.columns)
    
    if st.button("Générer le graphique"):
        fig = generate_plot(
            df=st.session_state.df,
            chart_type=chart_type.lower(),
            x_col=x_axis,
            y_col=None
        )
        st.plotly_chart(fig, use_container_width=True)

# Navigation
pages = {
    "Importer": upload_section,
    "Nettoyer": clean_section,
    "Visualiser": visualize_section
}

selected_page = st.sidebar.radio("Navigation", list(pages.keys()))
pages[selected_page]()