# Dependencies

## Python Dependencies
- streamlit as st
- qrcode
- pandas as pd
- Pillow
- reportlab
- io

# The versions

There are two versions of  QR label toy implementations.
1. Reading the book list from a csv file and generate QR based on this book list.
2. Reading the book list from posgres db and generate QR based on qr_code field in the book_copies table

# qr_label_generator.py

Navigate to the directory of qr_label_generator.py and run `streamlit run qr_label_generator.py` in your terminal.

`QR_CSV_TEST.csv` works with `qr_label_generator.py`. The csv file can be uploaded to the streamlit site for testing purpose.

# qr_label_generator_dbversion.py

This file needs to run with the virtual environment where python is modified and installed with sqlalchemy.

- Navigate to the root directory of .venv, 
- Make sure streamlit and necessary dependencies are installed in this virtural environment too.
- In the terminal of this directory: `source venv/bin/activate`
- Ensure posgres is running:
    - `brew services list`         # check status
    - `brew services start postgresql`  # or whatever version you use
- Run streamlit: `./venv/bin/streamlit run qr_label_generator_dbversion.py`


