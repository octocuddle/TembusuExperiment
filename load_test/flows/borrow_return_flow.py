# flows/borrow_return_flow.py

import asyncio
import time
from pathlib import Path
from pyrogram.types import Message
from pyrogram import filters
from pyrogram.handlers import MessageHandler

# --- Helper 1: wait for bot message containing text (Corrected Version) ---
async def wait_for_bot_message(client, bot_username, keywords, timeout=20):
    """
    Waits for a bot message containing specific keywords using an event handler.
    This is the efficient way that avoids FloodWait errors.
    """
    # Future is an object that will eventually hold our result (the message).
    future = asyncio.get_event_loop().create_future()

    # This handler will be called for every new message from the target bot.
    async def handler(_, message):
        text = (message.text or message.caption or "").lower()
        # If the message contains any of our keywords...
        if any(k.lower() in text for k in keywords):
            if not future.done():
                # ...set the message as the result of our future.
                future.set_result(message)

    # Add the handler to the client. We specify the chat filter.
    # Group number -1 makes it a high-priority handler.
    handler_obj = MessageHandler(handler, filters.chat(bot_username))
    client.add_handler(handler_obj, group=-1)

    try:
        # Now, wait for the future to be completed by the handler.
        # If it's not completed within the timeout, it will raise an error.
        return await asyncio.wait_for(future, timeout=timeout)
    except asyncio.TimeoutError:
        raise TimeoutError(f"Timeout waiting for bot message with keywords: {keywords}")
    finally:
        # Crucially, always remove the handler when we're done.
        # This prevents it from firing on later, unrelated messages.
        client.remove_handler(handler_obj, group=-1)


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
async def run_borrow_return(client, bot_username, book_qr, location_qr, iterations=3, log_func=print):
    for i in range(iterations):
        t0 = time.time()
        log_func(f"\n[{client.name}] >>> Starting iteration {i+1}/{iterations}")

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
        log_func(f"[{client.name}] Iteration {i+1} done in {latency:.2f} sec")
