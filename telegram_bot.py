import logging
import requests
from telethon import TelegramClient
from config import Config

logger = logging.getLogger("mybot.log")
logger.setLevel("ERROR")

class TelegramBotBuilder:
    def __init__(self, token):
        logger.info("Building a new BOT")
        self.bot = TelegramBot(token)
    
    def with_webhook(self, host):
        self.bot.set_webhook(host)
        return self
    
    def with_core_api(self, api_id, api_hash):
        client = TelegramClient('mymuseum', api_id, api_hash)
        self.bot.core_api_client = client
        return self

    def get_bot(self):
        return self.bot

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.bot_api_url = f"{Config.TELEGRAM_API}/bot{self.token}"
        self.core_api_client = None

    def set_webhook(self, host):
        try:
            host = host.replace("http", "http")
            logger.info(f"Setting webhook for url: {host}")
            set_webhook_url = f"{self.bot_api_url}/setWebhook?url={host}"

            response = requests.get(set_webhook_url)
            response.raise_for_status()
            logger.info(f"Got response: {response.json()}")
        except Exception as e:
            logger.error(f"Failed to set webhook: {e}")

    def send_message(self, chat_id, message):
        try:
            logger.info(f"Sending message to chat #{chat_id}")
            send_message_url = f"{self.bot_api_url}/sendMessage"
            response = requests.post(send_message_url, json={"chat_id": chat_id, "text": message})
            response.raise_for_status()
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            raise