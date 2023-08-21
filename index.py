import logging
import asyncio
import hypercorn.asyncio

from quart import Quart, request
from pyngrok import ngrok
from models import Update
from config import Config
from telegram_bot import TelegramBotBuilder
from openai_helper import OpenAiHelper



#inizializzo Logging
logging.basicConfig(filename='test.log', level=logging.ERROR)
logger = logging.getLogger("bot")

#Inizializzo Quart
app = Quart(__name__)

# Empty webserver index, return nothing, just http 200
@app.route('/', methods=["GET", "POST"])
async def handle_webhook():
    try:
        json_data = await request.json
        logger.info(f"Handling a webhook: {json_data}")
        update = Update(**json_data)
        chat_id = update.message.chat.id
    
    #process start command
        if update.message.text.startswith("/start"):
            response = "Ciao oggi ti guiderò in questa mostra, chiedimi quello che vuoi sapere."
        else:
            #response =update.message.text + " ho aggiunto una stringa boia"
            response = app.openai_helper.get_response(update.message.text)

        app.bot.send_message(chat_id, response)
        return "OK", 200
    
    except Exception as e:
        logger.error(f"Something went wrong while handling a request: {e}")
        return "Something went worng", 500

def run_ngrok(port=8000):
    logger.info(f"Starting ngrok tunnel at port {port}")
    http_tunnel = ngrok.connect(port)
    return http_tunnel.public_url

@app.before_serving
async def startup():
    host = run_ngrok(Config.PORT)
    bot_builder = TelegramBotBuilder(Config.TELEGRAM_TOKEN).with_webhook(host).with_core_api(Config.TELEGRAM_CORE_API_ID, Config.TELEGRAM_CORE_API_HASH)
    
    app.bot = bot_builder.get_bot()
    app.openai_helper = OpenAiHelper(Config.OPENAI_TOKEN)
    if app.bot.core_api_client:
        await app.bot.core_api_client.connect()
        await app.bot.core_api_client.start()
        
async def main():
    quart_cfg = hypercorn.Config()
    quart_cfg.bind = [f"127.0.0.1:{Config.PORT}"]
    logger.info("Starting the application")
    await hypercorn.asyncio.serve(app, quart_cfg)

if __name__ == "__main__":
    asyncio.run(main())