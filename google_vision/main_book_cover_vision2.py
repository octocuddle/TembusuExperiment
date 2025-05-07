from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
# from pyzbar.pyzbar import decode
from PIL import Image
import io
from typing import Final
import os
import requests
import re
from telegram.ext import CommandHandler
from vision_utils import detect_text_from_image

# Read environment variables
TOKEN: Final = os.getenv('TELEGRAM_TOKEN')
if not TOKEN:
    raise ValueError("Please set the TELEGRAM_TOKEN environment variable.")

BOT_USERNAME: Final = '@TembusuLib_bot'

def looks_like_isbn(query):
    cleaned = query.replace("-", "").replace(" ", "")
    return re.fullmatch(r"\d{10}|\d{13}", cleaned)

def search_google_books(query):
    url = "https://www.googleapis.com/books/v1/volumes"
    q = f"isbn:{query.replace('-', '').replace(' ', '')}" if looks_like_isbn(query) else query

    params = {
        "q": q,
        "maxResults": 10,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    results = []
    for item in data.get("items", []):
        volume_info = item.get("volumeInfo", {})
        identifiers = volume_info.get("industryIdentifiers", [])
        isbn_10 = isbn_13 = ""
        for id_obj in identifiers:
            if id_obj["type"] == "ISBN_10":
                isbn_10 = id_obj["identifier"]
            elif id_obj["type"] == "ISBN_13":
                isbn_13 = id_obj["identifier"]

        results.append({
            "title": volume_info.get("title", ""),
            "authors": ", ".join(volume_info.get("authors", [])),
            "publisher": volume_info.get("publisher", ""),
            "publishedDate": volume_info.get("publishedDate", ""),
            "description": volume_info.get("description", ""),
            "pageCount": volume_info.get("pageCount", ""),
            "isbn_10": isbn_10,
            "isbn_13": isbn_13,
        })

    return results


async def handle_google_books_search(query, update):
    await update.message.reply_text("🔍 Please wait while we retrieve relevant book information...")
    results = search_google_books(query)

    if not results:
        await update.message.reply_text("❌ No books found.")
        return

    for i, book in enumerate(results, start=1):
        message = f"""📘 Result {i}:
Title       : {book.get('title', '')}
Author(s)   : {book.get('authors', '')}
Publisher   : {book.get('publisher', '')}
Published   : {book.get('publishedDate', '')}
ISBN-10     : {book.get('isbn_10', '')}
ISBN-13     : {book.get('isbn_13', '')}
Page Count  : {book.get('pageCount', '')}
Description : {book.get('description', '')[:30]}{"..." if len(book.get('description', '')) > 30 else ""}
\n----------------------------------------
"""
        await update.message.reply_text(message)



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a photo of the book cover!")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_file = await update.message.photo[-1].get_file()
    image_path = "temp.jpg"
    await photo_file.download_to_drive(image_path)

    text = detect_text_from_image(image_path)
    await update.message.reply_text(f"I see:\n{text}")

    await handle_google_books_search(text, update)




def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("✅ Telegram bot is running... Press Ctrl+C to stop.")
    print(f"🤖 Bot username: {BOT_USERNAME}")

    app.run_polling()

if __name__ == "__main__":
    main()
