import fitz
import json
import os
from mistralai import Mistral

# Initialisation du client Mistral
client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

async def extract_text(file_bytes: bytes) -> str:
    """extrait le texte brut du fichier PDF."""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def analyze_with_llm(text: str) -> dict:
    """envoie le texte à Mistral et retourne le JSON structuré."""
    text_chunk = text[:6000] # limitation des tokens pour éviter les erreurs de dépassement de capacité du modèle
    
    prompt = f"""
    Analyse le texte suivant extrait d'un PDF et retourne UNIQUEMENT un objet JSON valide avec cette structure exacte :
    {{
        "titre": "Titre du document ou titre suggéré",
        "resume": "Résumé du contenu en 2-3 phrases",
        "mots_cles": ["mot1", "mot2", "mot3"],
        "type_document": "facture | contrat | article | rapport | cv | autre",
        "langue": "fr | en | autre"
    }}
    
    Texte à analyser :
    {text_chunk}
    """

    # appel à l'API Mistral avec le mode JSON
    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": prompt}],
        response_format={ "type": "json_object" }
    )
    
    # parse la réponse
    return json.loads(response.choices[0].message.content)