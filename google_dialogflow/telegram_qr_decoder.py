from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from PIL import Image
from pyzbar.pyzbar import decode
import io
import os
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = 'https://0c7a-119-74-64-53.ngrok-free.app/webhook'    # remember to update this if URL changes

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    photo = update.message.photo[-1]  # highest resolution
    file = await context.bot.get_file(photo.file_id)
    image_bytes = await file.download_as_bytearray()

    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        decoded = decode(image)
        if decoded:
            qr_value = decoded[0].data.decode()
            print(f"✅ QR decoded: {qr_value}")
            await update.message.reply_text(f"✅ QR code decoded: {qr_value}")

            # Send to webhook
            requests.post(WEBHOOK_URL, json={
                "session": f"projects/tembusulib/agent/sessions/{user_id}",
                "queryResult": {
                    "intent": {"displayName": "borrow - authentication - qr"},
                    "parameters": {
                        "QRcode": qr_value
                    }
                }
            })

        else:
            await update.message.reply_text("❌ No QR code detected. Try again.")
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("⚠️ Error processing the image.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.run_polling()
