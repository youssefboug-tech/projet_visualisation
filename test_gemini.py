import pandas as pd
from src.llm_logic import analyze_and_suggest
from dotenv import load_dotenv

load_dotenv()
# Création d'un petit DF de test
data = {'Mois': ['Jan', 'Feb'], 'Ventes': [100, 150]}
df = pd.DataFrame(data)

print("Test de la logique LLM...")
try:
    res = analyze_and_suggest(df, "Quelle est l'évolution des ventes ?")
    print("✅ Succès ! L'IA a proposé :")
    for s in res:
        print(f"- {s.titre} ({s.type_graphique})")
except Exception as e:
    print(f"❌ Erreur : {e}")