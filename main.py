from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import PyPDF2
import io
import os
from datetime import datetime

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create output directory if it doesn't exist
if not os.path.exists("output"):
    os.makedirs("output")


def extract_text_from_pdf(file_content: bytes) -> str:
    """
    Estrae il testo da un file PDF.
    """
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Errore nell'estrazione del testo dal PDF: {str(e)}")


def extract_text_from_txt(file_content: bytes) -> str:
    """
    Estrae il testo da un file TXT.
    """
    try:
        return file_content.decode("utf-8")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Errore nella lettura del file TXT: {str(e)}")


def generate_summary(text: str) -> str:
    """
    Genera un riassunto del testo fornito.
    
    NOTA: Questa è una funzione placeholder. Per l'integrazione con OpenAI API,
    sostituire questa implementazione con:
    
    import openai
    openai.api_key = "YOUR_API_KEY"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Sei un assistente che crea riassunti concisi di documenti."},
            {"role": "user", "content": f"Riassumi il seguente testo in modo conciso:\n\n{text}"}
        ],
        max_tokens=500,
        temperature=0.7
    )
    
    return response.choices[0].message.content
    """
    # Implementazione semplificata per demo
    words = text.split()
    if len(words) <= 100:
        return text
    
    # Prende le prime 100 parole come riassunto di base
    summary = " ".join(words[:100]) + "..."
    return f"RIASSUNTO AUTOMATICO:\n\n{summary}\n\n[Nota: Questa è una versione demo. Integrare OpenAI API per riassunti avanzati.]"


@app.get("/")
async def read_root():
    """
    Serve la pagina principale.
    """
    from fastapi.responses import FileResponse
    return FileResponse("templates/index.html")


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Endpoint per il caricamento e l'elaborazione dei file.
    """
    # Verifica l'estensione del file
    file_extension = file.filename.split(".")[-1].lower()
    if file_extension not in ["pdf", "txt"]:
        raise HTTPException(
            status_code=400,
            detail="Formato file non supportato. Utilizzare file .pdf o .txt"
        )
    
    # Leggi il contenuto del file
    file_content = await file.read()
    
    # Estrai il testo in base al tipo di file
    if file_extension == "pdf":
        text = extract_text_from_pdf(file_content)
    else:
        text = extract_text_from_txt(file_content)
    
    if not text or len(text.strip()) == 0:
        raise HTTPException(
            status_code=400,
            detail="Il file non contiene testo leggibile"
        )
    
    # Genera il riassunto
    summary = generate_summary(text)
    
    # Salva il riassunto in un file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"riassunto_{timestamp}.txt"
    output_path = os.path.join("output", output_filename)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(summary)
    
    return JSONResponse({
        "success": True,
        "summary": summary,
        "filename": output_filename,
        "original_filename": file.filename
    })


@app.get("/download/{filename}")
async def download_file(filename: str):
    """
    Endpoint per il download del riassunto generato.
    """
    file_path = os.path.join("output", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File non trovato")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="text/plain"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
