from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
# from pyzbar.pyzbar import decode
from PIL import Image
import io
from typing import Final
import os
import requests
from telegram.ext import CommandHandler
from vision_utils import detect_text_from_image

# Read environment variables
TOKEN: Final = os.getenv('TELEGRAM_TOKEN')
if not TOKEN:
    raise ValueError("Please set the TELEGRAM_TOKEN environment variable.")

BOT_USERNAME: Final = '@TembusuLib_bot'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a photo of the book cover!")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_file = await update.message.photo[-1].get_file()
    image_path = "temp.jpg"
    await photo_file.download_to_drive(image_path)

    text = detect_text_from_image(image_path)
    await update.message.reply_text(f"I see:\n{text}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("✅ Telegram bot is running... Press Ctrl+C to stop.")
    print(f"🤖 Bot username: {BOT_USERNAME}")

    app.run_polling()

if __name__ == "__main__":
    main()
