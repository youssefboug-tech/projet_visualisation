from langchain_google_genai import ChatGoogleGenerativeAI
import os

# On utilise le modèle Lite validé pour ton compte
MODEL_NAME = "gemini-2.0-flash-lite-001"

def get_llm(temperature=0.0):
    """
    Fabrique une instance de LLM configurée.
    temperature: 0.0 pour le code (précis), 0.7 pour les idées (créatif).
    """
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("Clé API manquante dans le fichier .env")
        
    return ChatGoogleGenerativeAI(
        model=MODEL_NAME,
        temperature=temperature,
        max_retries=3
    )