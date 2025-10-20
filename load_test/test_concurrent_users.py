import asyncio, json, time
from datetime import datetime
from pathlib import Path
from pyrogram import Client
from flows.borrow_return_flow import run_borrow_return


BOT_USERNAME = "TembusuLib_bot"
LOG_FILE = Path(__file__).parent / "load_test_log.txt"

# --- Helper: log to file (append mode) ---
def append_log(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(message)

# --- Main test logic ---
with open(Path(__file__).parent / "credentials" / "tester.json") as f:
    USER_CONFIGS = json.load(f)

async def simulate_user(config):
    client = Client(config["session_name"], api_id=config["api_id"], api_hash=config["api_hash"])
    async with client:
        # IMPORTANT: Set the iterations for a single burst here
        await run_borrow_return(
            client,
            BOT_USERNAME,
            Path(__file__).parent / config["book_qr"],
            Path(__file__).parent / config["location_qr"],
            iterations=10,  # <-- This is for one cycle
            log_func=append_log,
        )

async def main():
    append_log("=== New test session started at " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " ===")
    tasks = [simulate_user(c) for c in USER_CONFIGS]
    await asyncio.gather(*tasks)
    append_log("=== Test session ended ===\n")

async def run_test_cycles():
    """
    Manages the overall test, running multiple cycles with a rest
    period in between.
    """
    num_cycles = 4
    rest_time_seconds = 1800

    for i in range(num_cycles):
        append_log(f"======= Starting Test Cycle {i + 1}/{num_cycles} =======")
        await main()  # Run one full test session (2 users x 10 iterations)
        append_log(f"======= Test Cycle {i + 1} Finished =======")

        # Don't rest after the very last cycle
        if i < num_cycles - 1:
            append_log(f"--- Resting for {rest_time_seconds} seconds ---")
            await asyncio.sleep(rest_time_seconds)

if __name__ == "__main__":
    # Instead of running main() directly, run the new cycle manager
    asyncio.run(run_test_cycles())