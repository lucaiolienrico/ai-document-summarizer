# 🤖 AI Document Summarizer

**Web App di Riassunto Documenti AI** con Python FastAPI e Modern Web Design

Una web app minimalista e moderna che permette di caricare documenti (PDF o TXT) e ottenere riassunti automatici in tempo reale.

## ✨ Caratteristiche

- 📝 **Supporto multipli formati**: PDF e TXT
- ⚡ **Elaborazione in tempo reale**: Riassunto istantaneo senza ricaricare la pagina
- 🎨 **Design moderno**: Interfaccia pulita con TailwindCSS
- ⬇️ **Download immediato**: Scarica il riassunto in formato TXT
- 🔌 **API Ready**: Predisposto per l'integrazione con OpenAI API

## 🛠️ Stack Tecnologico

- **Backend**: Python 3.8+ con FastAPI
- **Frontend**: HTML5, JavaScript Vanilla, TailwindCSS (via CDN)
- **Processing**: PyPDF2 per l'estrazione testo da PDF
- **Server**: Uvicorn ASGI

## 🚀 Installazione Rapida

### Prerequisiti

- Python 3.8 o superiore
- pip (package manager Python)

### Passo 1: Clona il Repository

```bash
git clone https://github.com/lucaiolienrico/ai-document-summarizer.git
cd ai-document-summarizer
```

### Passo 2: Crea un Virtual Environment (Opzionale ma Raccomandato)

```bash
python -m venv venv

# Su Windows
venv\Scripts\activate

# Su macOS/Linux
source venv/bin/activate
```

### Passo 3: Installa le Dipendenze

```bash
pip install -r requirements.txt
```

### Passo 4: Avvia il Server

```bash
python main.py
```

Oppure usando uvicorn direttamente:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Passo 5: Apri l'App nel Browser

Apri il browser e vai su:

```
http://localhost:8000
```

## 📚 Struttura del Progetto

```
ai-document-summarizer/
│
├── main.py                 # Backend FastAPI con logica di processing
├── requirements.txt        # Dipendenze Python
├── README.md               # Documentazione
├── templates/
│   └── index.html          # Frontend con JavaScript integrato
└── output/                 # Cartella per i riassunti generati (auto-creata)
```

## 🧩 Integrazione OpenAI API (Opzionale)

Per utilizzare l'AI di OpenAI per riassunti avanzati:

1. Ottieni una API key da [OpenAI Platform](https://platform.openai.com/)

2. Installa la libreria OpenAI:

```bash
pip install openai
```

3. Modifica la funzione `generate_summary()` in `main.py`:

```python
import openai

def generate_summary(text: str) -> str:
    openai.api_key = "YOUR_API_KEY_HERE"
    
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
```

## 📦 API Endpoints

### `GET /`
Serve la pagina principale dell'applicazione.

### `POST /upload`
Carica e processa un documento.

**Request:**
- `file`: File multipart (.pdf o .txt)

**Response:**
```json
{
    "success": true,
    "summary": "Riassunto del documento...",
    "filename": "riassunto_20231120_153045.txt",
    "original_filename": "documento.pdf"
}
```

### `GET /download/{filename}`
Scarica il riassunto generato.

## 🔧 Utilizzo

1. Apri l'app nel browser
2. Clicca su "Carica File" o trascina un file PDF/TXT
3. Clicca su "Carica e Analizza"
4. Attendi l'elaborazione (visualizzerai uno spinner)
5. Leggi il riassunto generato
6. Clicca su "Scarica Riassunto (.txt)" per salvare il file

## 🐛 Troubleshooting

### Errore: "ModuleNotFoundError"

Assicurati di aver installato tutte le dipendenze:

```bash
pip install -r requirements.txt
```

### Errore: "Port already in use"

Cambia la porta nel comando di avvio:

```bash
uvicorn main:app --reload --port 8080
```

### Il PDF non viene letto correttamente

Alcuni PDF potrebbero essere scansioni di immagini senza testo estraibile. In questo caso, considera l'uso di OCR (Optical Character Recognition).

## 📝 Licenza

MIT License - Sentiti libero di utilizzare questo progetto per scopi personali o commerciali.

## 👥 Autore

Creato da **Enrico Lucaioli** - [GitHub Profile](https://github.com/lucaiolienrico)

## 🌟 Contributi

I contributi sono benvenuti! Sentiti libero di aprire issue o pull request.

---

**Happy Coding! 🚀**
