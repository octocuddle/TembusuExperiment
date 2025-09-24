# flows/borrow_return_flow.py
import asyncio, time
from pathlib import Path
from pyrogram.types import Message


# --- Helper 1: wait for bot message containing text ---
async def wait_for_bot_message(client, bot_username, keywords, timeout=10):
    """
    Wait until the bot sends a message containing one of the keywords.
    """
    start = time.time()
    while time.time() - start < timeout:
        async for msg in client.get_chat_history(bot_username, limit=1):
            if any(k.lower() in (msg.text or "").lower() for k in keywords):
                return msg
        await asyncio.sleep(0.5)
    raise TimeoutError(f"Timeout waiting for bot message with {keywords}")


# --- Helper 2: click a button by text ---
async def click_button_from_message(client, msg: Message, button_text: str):
    """
    Click a button from a given bot message.
    """
    if not msg.reply_markup:
        print(f"[{client.name}] No buttons in this message.")
        return False

    for y, row in enumerate(msg.reply_markup.inline_keyboard):
        for x, btn in enumerate(row):
            if btn.text.strip() == button_text.strip():
                await msg.click(x, y)
                print(f"[{client.name}] Clicked '{button_text}'")
                return True
    
    print(f"[{client.name}] Button '{button_text}' not found in this message.")
    return False


# --- Main flow: borrow → return ---
async def run_borrow_return(client, bot_username, book_qr, location_qr, iterations=3):
    for i in range(iterations):
        t0 = time.time()
        print(f"\n[{client.name}] >>> Starting iteration {i+1}/{iterations}")

        # --- Step 1: Start ---
        await client.send_message(bot_username, "/start")
        msg = await wait_for_bot_message(client, bot_username, ["welcome to", "what would you like to do"])

        # --- Step 2: Click Borrow ---
        await click_button_from_message(client, msg, "📚 Borrow")
        msg = await wait_for_bot_message(client, bot_username, ["please submit a photo", "qr code"])

        # --- Step 3: Send book QR ---
        await client.send_photo(bot_username, book_qr)
        msg = await wait_for_bot_message(client, bot_username, ["do you want to borrow"])

        # --- Step 4: Confirm borrow (Yes) ---
        await click_button_from_message(client, msg, "✅ Yes")
        msg = await wait_for_bot_message(client, bot_username, ["successfully borrowed", "due date"])

        # --- Step 5: Start again for Return ---
        await client.send_message(bot_username, "/start")
        msg = await wait_for_bot_message(client, bot_username, ["welcome to", "what would you like to do"])

        # --- Step 6: Click Return ---
        await click_button_from_message(client, msg, "⏪️ Return")
        msg = await wait_for_bot_message(client, bot_username, ["submit a photo", "qr code"])

        # --- Step 7: Send book QR again ---
        await client.send_photo(bot_username, book_qr)
        msg = await wait_for_bot_message(client, bot_username, ["location qr", "shelf"])

        # --- Step 8: Send location QR ---
        await client.send_photo(bot_username, location_qr)
        msg = await wait_for_bot_message(client, bot_username, ["book returned successfully"])

        # --- Log this iteration ---
        latency = time.time() - t0
        print(f"[{client.name}] Iteration {i+1} done in {latency:.2f} sec")
