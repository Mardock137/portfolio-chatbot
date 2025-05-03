from langdetect import detect
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import cohere
import os
from dotenv import load_dotenv

# Carica le variabili da .env
load_dotenv()

# Inizializza FastAPI
app = FastAPI()

# Abilita CORS per chiamate da frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puoi sostituire con "http://localhost:5500" per sicurezza
    allow_methods=["*"],
    allow_headers=["*"],
)

# Schema della richiesta
class ChatRequest(BaseModel):
    message: str

# Inizializza client Cohere
cohere_api_key = os.getenv("COHERE_API_KEY")
co = cohere.Client(cohere_api_key)

# Endpoint di chat
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    user_message = request.message
    print("Utente ha scritto:", user_message)

    try:
        # Rileva la lingua del messaggio
        lang = detect(user_message)
        print("Lingua rilevata:", lang)

        if lang == 'it':
            preamble = (
                "Sei un simulatore di un assistente virtuale integrato in un sito web. "
                "Il tuo scopo è mostrare come potrebbe funzionare un chatbot su un sito aziendale. "
                "Parla in modo informale, diretto e simpatico. "
                "Dai risposte brevi ma utili. Se l'utente fa domande strane, rispondi con ironia."
            )
        else:
            preamble = (
                "You are simulating a virtual assistant integrated into a company website. "
                "Your purpose is to demonstrate how a chatbot could work in a modern web environment. "
                "Speak in a friendly, informal, and helpful tone. "
                "Keep responses short, clear, and fun. If users ask weird things, reply with light sarcasm."
            )

        response = co.chat(message=user_message, preamble=preamble)
        bot_reply = response.text

    except Exception as e:
        import traceback
        traceback.print_exc()
        bot_reply = "Oops! Something went wrong with my AI brain 🤯"

    return {"response": bot_reply}
