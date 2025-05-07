# About this code

This `qr_reader_prototype.py` is renamed to `code_reader_prototype.py` and modified to read **both QR code and bar code**.

Run `qr_reader_prototype.py`, then go to telegram **/start** for test.

# Dependencies

## System Dependencies

This project requires the ZBar library to be installed on your system:

- On macOS: `brew install zbar`
- On Ubuntu/Debian: `sudo apt install libzbar0`

## Python Dependencies 
- telegram
- pyzbar
- Pillow
- io
- Final
- os
- requests


---

# 📦 About `pyzbar` and `zbar`

This project uses the [`pyzbar`](https://github.com/NaturalHistoryMuseum/pyzbar) Python package to **decode QR codes from images**, such as those sent via Telegram.

However, `pyzbar` is only a **wrapper** — it **depends on the native `zbar` library** installed on your system to do the actual decoding work.

---

## 🖥️ MacOS Setup

On macOS, you must install the native `zbar` library using [Homebrew](https://brew.sh):

```bash
brew install zbar
```

> `zbar` installs the required shared library `libzbar.dylib`, which `pyzbar` needs to function.

---

## ❗ Common Error: `Unable to find zbar shared library`

If after installation you see an error like:

```bash
ImportError: Unable to find zbar shared library
```

That means **your Python interpreter (e.g. Python 3.12)** couldn't locate the `libzbar` library installed by Homebrew (typically in `/opt/homebrew/lib` on Apple Silicon).

---

## 🛠️ Solutions

### 1. 🧪 Temporary Fix

Run your script with this command:

```bash
DYLD_LIBRARY_PATH="/opt/homebrew/lib" /usr/local/bin/python3 path/to/code_reader_prototype.py
```

**Why it works:**

* This sets the environment variable `DYLD_LIBRARY_PATH` **just for this one command**.
* macOS's dynamic linker (`dyld`) will look in `/opt/homebrew/lib` first to find `libzbar.dylib`.

---

### 2. 🔁 Persistent Fix

To avoid repeating that every time, you can set it globally in your shell config:

```bash
export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"
```

Add this line to your `~/.zshrc` (or `~/.bash_profile`, depending on your shell), then reload with:

```bash
source ~/.zshrc
```

---

### ✅ Summary

| Command                             | Scope                         | Use Case                                 |
| ----------------------------------- | ----------------------------- | ---------------------------------------- |
| `DYLD_LIBRARY_PATH=... python3 ...` | 🔄 One-time (just this run)   | Good for testing                         |
| `export DYLD_LIBRARY_PATH=...`      | 🔁 Persistent (all terminals) | Good for regular use or development work |

---

## ☁️ Deployment in Linux (e.g., AWS EC2)

If you deploy this to a Linux server (e.g. Ubuntu on EC2), `DYLD_LIBRARY_PATH` becomes irrelevant. Linux uses:

> `LD_LIBRARY_PATH` instead.

### ✅ What to do:

1. **Install `zbar`:**

```bash
sudo apt update
sudo apt install libzbar0
```

2. **Install Python packages:**

```bash
pip install pyzbar Pillow python-telegram-bot
```

3. **(Optional) Set `LD_LIBRARY_PATH`:**

Linux usually finds `libzbar.so` on its own. But if you build your own or install it in a custom path:

```bash
export LD_LIBRARY_PATH="/your/custom/path:$LD_LIBRARY_PATH"
```

Add this to `~/.bashrc` or `~/.profile` if needed.

---

## ✅ Cross-Platform Summary

| Task                  | macOS                | Linux (e.g. EC2)            |
| --------------------- | -------------------- | --------------------------- |
| Install `zbar`        | `brew install zbar`  | `sudo apt install libzbar0` |
| Install `pyzbar`      | `pip install pyzbar` | `pip install pyzbar`        |
| Library path variable | `DYLD_LIBRARY_PATH`  | `LD_LIBRARY_PATH`           |
| Is it usually needed? | ✅ Yes                | ❌ Not usually               |

---

Let me know if you want a `setup.md` separated from your main `README.md` for cleaner structure.

