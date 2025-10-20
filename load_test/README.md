## Chatbot Load Test

This project contains a set of Python scripts designed to run a concurrent load test against a Telegram bot. It simulates multiple users performing a defined workflow and measures the end-to-end latency for each transaction.

-----

## ⚙️ Configuration

Before running the test, you need to configure the user accounts and test parameters.

### 1\. Configure User Credentials

The test script loads user session details from a JSON file. This file is ignored by Git to protect sensitive credentials.

1.  Create a `credentials` directory if it doesn't exist.
2.  Inside `credentials`, create a file named `tester.json`.
3.  Populate `tester.json` with the configuration for each user you want to simulate. Each user is an object in a JSON array.

**File:** `credentials/tester.json`

```json
[
  {
    "session_name": "user1_session",
    "api_id": xxxxxxx,
    "api_hash": "your_api_hash_for_user1",
    "book_qr": "testdata/book1.png",
    "location_qr": "testdata/location1.png"
  },
  {
    "session_name": "user2_session",
    "api_id": xxxxxx,
    "api_hash": "your_api_hash_for_user2",
    "book_qr": "testdata/book2.png",
    "location_qr": "testdata/location1.png"
  }
]
```

  * **`session_name`**: A unique name for the Pyrogram session file (`.session`).
  * **`api_id` / `api_hash`**: Your Telegram API credentials.
  * **`book_qr` / `location_qr`**: The file paths to the QR code images needed for the test flow.

The number of objects in this array determines the number of **concurrent users** in the test.

### 2\. Configure Test Iterations

The number of times each user will repeat the test workflow is defined directly in the main script.

**File:** `test_concurrent_users.py`

In the `simulate_user` function call, modify the `iterations` argument:

```python
# ... inside the simulate_user function ...
await run_borrow_return(
    client,
    BOT_USERNAME,
    Path(__file__).parent / config["book_qr"],
    Path(__file__).parent / config["location_qr"],
    iterations=2,  # <-- CHANGE THIS VALUE
    log_func=append_log,
)
```

-----

## 🔬 Test Scenario

The test executes a fixed conversation flow for each simulated user:

1.  **Start Conversation**: Sends `/start`.
2.  **Borrow Flow**:
      * Clicks the "📚 Borrow" button.
      * Sends a book QR code photo.
      * Clicks the "✅ Yes" button to confirm.
3.  **Return Flow**:
      * Sends `/start` again.
      * Clicks the "⏪️ Return" button.
      * Sends the book QR code photo.
      * Sends a location QR code photo.

A single **iteration** consists of one complete borrow-and-return cycle. The script logs the total time taken for each iteration per user.

-----

## ▶️ Running the Test

1.  **Create and activate a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  **Install dependencies (assuming a `requirements.txt` file exists):**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Execute the main test script:**

    ```bash
    python test_concurrent_users.py
    ```

Test progress and timing results will be printed to the console and appended to **`load_test_log.txt`**.
