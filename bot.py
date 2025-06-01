import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(env_path)

from pyrogram import Client, filters, enums
from pyrogram.handlers import BusinessMessageHandler, CallbackQueryHandler

import MessageHandler

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')

# Initialize the Telegram client
app = Client(
    name="mrs012_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    parse_mode=enums.ParseMode.HTML
)


app.add_handler(BusinessMessageHandler(MessageHandler.handle_message))
app.add_handler(CallbackQueryHandler(callback=MessageHandler.handle_callback_query, filters=filters.regex(r"^send_message_(\d+)$")))

if __name__ == "__main__":
    app.run()
