from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from pyzbar.pyzbar import decode
from PIL import Image
import io
from typing import Final
import os
import requests
from telegram.ext import CommandHandler


# Read environment variables
TOKEN: Final = os.getenv('TELEGRAM_TOKEN')
if not TOKEN:
    raise ValueError("Please set the TELEGRAM_TOKEN environment variable.")

BOT_USERNAME: Final = '@TembusuLib_bot'

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    image_bytes = await file.download_as_bytearray()
    
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")  # ensure compatibility
        detected_results = decode(image)
    except Exception as e:
        await update.message.reply_text("⚠️ Could not process the image.")
        return
    
    # ZBar can read multiple codes. If needed, sort by position:
    # sorted(detected_results, key=lambda r: (r.rect.top, r.rect.left))
    # Current code constrained to show only the first result. 

    if detected_results: 
        text = detected_results[0].data.decode()
        code_type = detected_results[0].type
        print(f"Decoded {code_type} Code: {text}")
        await update.message.reply_text(f"📦 {code_type} content: {text}")
    else:
        await update.message.reply_text("❌ No QR code detected in the image.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send me a photo of a QR code or Bar code and I’ll decode it.")



app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
app.run_polling()
