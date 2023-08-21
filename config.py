import os
from dotenv import load_dotenv

#Carico le variabili d'ambiente
load_dotenv()

class Config:
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
    PORT = os.getenv("TELEGRAM_BOT_PORT", 5002)
    TELEGRAM_API = "https://api.telegram.org"
    OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")
    TELEGRAM_CORE_API_HASH = os.getenv("TELEGRAM_CORE_API_HASH")
    TELEGRAM_CORE_API_ID = os.getenv("TELEGRAM_CORE_API_ID")