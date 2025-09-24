# test_concurrent_users.py
import asyncio, json
from pathlib import Path
from pyrogram import Client
from flows.borrow_return_flow import run_borrow_return

BOT_USERNAME = "TembusuLib_bot"

with open(Path(__file__).parent / "credentials" / "tester.json") as f:
    USER_CONFIGS = json.load(f)

async def simulate_user(config):
    client = Client(config["session_name"], api_id=config["api_id"], api_hash=config["api_hash"])
    async with client:
        await run_borrow_return(
            client,
            BOT_USERNAME,
            Path(__file__).parent / config["book_qr"],     # book QR
            Path(__file__).parent / config["location_qr"],  # location QR
            iterations=2
        )

async def main():
    tasks = [simulate_user(c) for c in USER_CONFIGS]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
