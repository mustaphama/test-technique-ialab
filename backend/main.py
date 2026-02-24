from fastapi import FastAPI, UploadFile, File, HTTPException
from processor import extract_text, analyze_with_llm

app = FastAPI()

@app.post("/analyze")
async def analyze_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Le fichier doit être un PDF")
    
    try:
        # lecture du fichier depuis la requête
        content = await file.read()
        
        # extraction du texte du PDF
        text = await extract_text(content)
        if not text.strip():
            raise HTTPException(status_code=400, detail="PDF vide ou illisible.")

        # analyse avec le llm
        result = analyze_with_llm(text)
        
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))