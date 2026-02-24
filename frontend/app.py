import os
import streamlit as st
import requests

# url du backend pour docker
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

st.set_page_config(page_title="Analyseur PDF", layout="centered")

st.title("Extracteur & Analyseur PDF")
st.write("Uploade un document pour extraire son contenu et générer une analyse structurée via IA.")

uploaded_file = st.file_uploader("Glisse ton fichier PDF ici", type="pdf")

if uploaded_file is not None:
    if st.button("Lancer l'analyse"):
        with st.spinner("Analyse du document en cours..."):
            try:
                # envoi du fichier au backend via api
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                response = requests.post(f"{BACKEND_URL}/analyze", files=files)
                
                if response.status_code == 200:
                    data = response.json()
                    st.success("Analyse terminée avec succès !")
                
                    st.header(data.get("titre", "Titre non identifié"))
                    
                    # résultats clés affichés côte à côte
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric(label="Type de document", value=str(data.get("type_document", "N/A")).capitalize())
                    with col2:
                        st.metric(label="Langue", value=str(data.get("langue", "N/A")).upper())
                        
                    st.divider()
                    
                    st.subheader("Résumé")
                    st.write(data.get("resume", "Aucun résumé généré."))
                    
                    # afficher les mots clès sous forme de tags
                    st.subheader("Mots-clés")
                    mots_cles = data.get("mots_cles", [])
                    if mots_cles:
                        # utiliser du html pour du styme 
                        tags = "".join([f"<span style='background-color: #0f0f0f; padding: 4px 8px; border-radius: 4px; margin-right: 5px;'>{mot}</span>" for mot in mots_cles])
                        st.markdown(tags, unsafe_allow_html=True)
                    else:
                        st.write("Aucun mot-clé trouvé.")
                        
                else:
                    st.error(f"Erreur lors de l'analyse : {response.json().get('detail', 'Erreur inconnue')}")
                    
            except requests.exceptions.ConnectionError:
                st.error("Impossible de se connecter au backend. Vérifie que le conteneur backend est bien lancé.")