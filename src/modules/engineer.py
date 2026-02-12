from langchain_core.prompts import ChatPromptTemplate
from .llm_factory import get_llm

def run_engineer_agent(df, user_question, viz_plan):
    """
    Rôle : Produire du code Python avec une INTELLIGENCE STATISTIQUE GÉNÉRALISÉE.
    Stratégie : Détecter l'intention (Agrégation vs Brut) sans dépendre du nom du dataset.
    """
    # Température à 0 pour une rigueur de code absolue
    llm = get_llm(temperature=0.0)
    
    schema = df.dtypes.to_string()
    
    template = """
    Tu es un Expert Data Visualization (Python/Plotly) doté d'une logique statistique impeccable.
    
    CONTEXTE :
    - Données : {schema}
    - Question Utilisateur : "{question}"
    - Intention de l'Architecte : "{titre}" ({type_graph})
    
    RÈGLES D'INTELLIGENCE STATISTIQUE (ABSTRAITES & UNIVERSELLES) :
    
    1. **LOGIQUE D'AGRÉGATION (Moyenne/Taux)** :
       - Si la question implique un **"Taux"**, une **"Chance"**, un **"Pourcentage"** ou une **"Moyenne"** (surtout si la colonne cible est binaire 0/1 ou numérique) :
       - -> **IMPÉRATIF** : Tu DOIS faire un `groupby(Var_Explicative)[Var_Cible].mean().reset_index()` AVANT de tracer.
       - *Pourquoi ?* Tracer des points bruts (0 et 1) pour une probabilité est une erreur de débutant. On veut voir des barres de moyenne.
    
    2. **LOGIQUE DE RELATION (Corrélation/Influence)** :
       - Si la question cherche un **"Lien"**, une **"Influence"**, ou une **"Relation"** entre deux variables numériques :
       - -> Utilise **`px.scatter`** sur les données BRUTES.
       - -> Si la question mentionne **"Colorie"** ou **"Selon [Groupe]"**, map l'argument `color='Nom_Colonne'`.
       - -> Ajoute une **Trendline** (`trendline="ols"`) pour matérialiser l'influence (avec sécurité `try/except`).
    
    3. **LOGIQUE DE DISTRIBUTION (Comparaison)** :
       - Si la question demande la **"Distribution"**, la **"Répartition"** ou l'**"Étalement"** :
       - -> NE FAIS PAS d'agrégation. Garde toutes les lignes.
       - -> Utilise **`px.box`** (Boîte à moustaches) ou **`px.histogram`**. C'est le seul moyen de voir la variance.
    
    4. **SÉCURITÉ & ROBUSTESSE (ANTI-CRASH)** :
       - Signature fonction : `def generate_plot(df):` (Strictement).
       - Statsmodels : L'argument `trendline="ols"` doit TOUJOURS être protégé par un `try/except ImportError`.
       - Design : `template="plotly_white"`, titre centré (`title_x=0.5`).
    
    EXEMPLE DE STRUCTURE DE CODE ATTENDUE :
    ```python
    def generate_plot(df):
        # 1. DÉCISION : AGRÉGER OU PAS ?
        # Si Taux/Moyenne demandé -> on agrège
        # df_plot = df.groupby('categorie')['valeur'].mean().reset_index()
        
        # Si Distribution ou Relation brute demandée -> on garde tout
        # df_plot = df
        
        # 2. SÉCURITÉ TRENDLINE (Uniquement pour Scatter)
        trend_kwargs = {{}}
        if "{type_graph}" == "Scatter Plot":
            try:
                import statsmodels
                trend_kwargs = {{"trendline": "ols"}}
            except ImportError:
                pass # On continue sans planter
        
        # 3. CRÉATION DU GRAPHIQUE
        # fig = px.bar(df_plot, x='...', y='...', title="{titre}")
        # OU
        # fig = px.scatter(df_plot, x='...', y='...', color='...', **trend_kwargs)
        # OU
        # fig = px.box(df_plot, x='...', y='...')
        
        # 4. DESIGN
        fig.update_layout(template="plotly_white", title_x=0.5)
        return fig
    ```
    
    TACHE : Écris UNIQUEMENT le code de la fonction `generate_plot(df)` pour répondre à la question posée.
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm
    
    print(f"🔧 L'Ingénieur Statistique (Mode Généraliste) code pour : {viz_plan.titre}...")
    
    code = chain.invoke({
        "schema": schema, 
        "titre": viz_plan.titre, 
        "type_graph": viz_plan.type_graphique, 
        "question": user_question
    }).content
    
    return code.replace("```python", "").replace("```", "").strip()