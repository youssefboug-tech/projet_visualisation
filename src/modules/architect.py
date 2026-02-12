from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List
from .llm_factory import get_llm

# --- STRUCTURE DE DONNÉES ---
class VizSuggestion(BaseModel):
    titre: str = Field(description="Titre métier percutant")
    type_graphique: str = Field(description="Type de graphique (Bar, Scatter, etc.)")
    justification: str = Field(description="Pourquoi ce choix ?")

class VizList(BaseModel):
    propositions: List[VizSuggestion]

# --- LOGIQUE DE L'AGENT ---
def run_architect_agent(df, user_question):
    """
    Rôle : Analyser les données et proposer une stratégie.
    """
    # 1. Instanciation du LLM "Architecte" (Température 0.5 pour la créativité)
    llm = get_llm(temperature=0.5)
    
    schema = df.dtypes.to_string()
    sample = df.head(3).to_string()
    
    parser = PydanticOutputParser(pydantic_object=VizList)

    template = """
    Tu es un Architecte Data Senior.
    
    CONTEXTE :
    - Données : {schema}
    - Aperçu : {sample}
    - Besoin Client : "{question}"
    
    TA MISSION :
    Identifie 3 angles d'analyse pertinents pour répondre au besoin client.
    Pour chaque angle, choisis la visualisation la plus adaptée.
    
    CONTRAINTES :
    - Réponds UNIQUEMENT au format JSON strict.
    - Sois précis sur les types de graphiques.
    
    {format_instructions}
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm | parser
    
    try:
        print("🤖 L'Architecte réfléchit...")
        return chain.invoke({
            "schema": schema,
            "sample": sample, 
            "question": user_question,
            "format_instructions": parser.get_format_instructions()
        }).propositions
    except Exception as e:
        print(f"Erreur Architecte : {e}")
        # Fallback en cas d'erreur de parsing
        return [
            VizSuggestion(titre="Analyse Globale", type_graphique="Bar Chart", justification="Visualisation par défaut (Mode Secours)"),
            VizSuggestion(titre="Distribution", type_graphique="Histogram", justification="Visualisation par défaut (Mode Secours)"),
            VizSuggestion(titre="Tendances", type_graphique="Line Chart", justification="Visualisation par défaut (Mode Secours)")
        ]