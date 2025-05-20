import streamlit as st
import qrcode
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

from io import BytesIO


# ----------------------
# 0. Connect to DB
# ----------------------
from sqlalchemy import create_engine

DB_USER = "testuser"
DB_PASSWORD = "000000"
DB_HOST = "db" #"localhost"
DB_PORT = "5432"
DB_NAME = "MyLibrary2"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

# ----------------------
# 1. Generate QR + Label Image
# ----------------------
def generate_label_image(uid, title, call_number, isbn):
    qr = qrcode.make(uid)
    qr = qr.resize((150, 150))

    img = Image.new("RGB", (300, 220), color="white")
    img.paste(qr, (10, 10))

    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    draw.text((170, 10), f"Title: {title}", font=font, fill="black")
    draw.text((170, 50), f"Call No: {call_number}", font=font, fill="black")
    if isbn:
        draw.text((170, 90), f"ISBN: {isbn}", font=font, fill="black")

    return img

# ----------------------
# 2. Generate PDF of Labels
# ----------------------

def create_pdf(rows):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    label_width = 180
    label_height = 140
    x_start = 40
    y_start = 700  # slightly lowered start to avoid top cutoff
    x, y = x_start, y_start
    count = 0

    for _, row in rows.iterrows():
        uid = row["qr_code"]
        title = row["title"]
        call_number = row["call_number"]
        isbn = row["isbn"] if pd.notna(row["isbn"]) else ""

        # Generate QR code image
        qr = qrcode.make(uid)
        qr_buf = BytesIO()
        qr.save(qr_buf, format="PNG")
        qr_buf.seek(0)

        # Draw QR on the left (smaller size)
        c.drawImage(ImageReader(qr_buf), x, y, width=60, height=60)

        # Draw text on the right
        text_x = x + 65
        text_y = y + 40
        c.setFont("Helvetica", 8)
        c.drawString(text_x, text_y, f"Title: {title[:40]}")
        c.drawString(text_x, text_y - 12, f"Call No: {call_number}")
        if isbn:
            c.drawString(text_x, text_y - 24, f"ISBN: {isbn}")

        # Move to next column
        x += label_width
        count += 1

        if count % 3 == 0:
            x = x_start
            y -= label_height

        if count % 15 == 0:  # 3 cols x 5 rows
            c.showPage()
            x, y = x_start, y_start

    c.save()
    buffer.seek(0)
    return buffer


# ----------------------
# 3. Streamlit App UI,  CSV based
# ----------------------
st.title("📚 QR Code Label Generator")

st.markdown("""
### 📋 How to Use

0. It may take a while to load the data. Please be patient
1. After the data is loaded from the backend, **select** the rows you want to print using the checkboxes  
2. **Download** the PDF and print the labels  
3. Stick the QR labels on the corresponding books
""")


st.markdown("## Wait for book data to be fetched from PostgreSQL...")

@st.cache_data
def load_books_from_db():
    query = """
        SELECT 
            bc.qr_code,
            b.title,
            bc.call_number,
            b.isbn
        FROM book_copies bc
        JOIN books b ON bc.book_id = b.book_id
        ORDER BY bc.qr_code
    """
    df = pd.read_sql_query(query, engine)
    return df

df = load_books_from_db()




st.markdown("""
## 1. Select the rows you want to print using the checkboxes  
""")
# Show select-all checkbox
select_all = st.checkbox("✅ Select all rows for printing")

# Create or reset selection column
df['select'] = select_all  # sets all rows to True or False

# Move 'select' to first column
cols = df.columns.tolist()
cols.insert(0, cols.pop(cols.index("select")))
df = df[cols]

edited_df = st.data_editor(
    df, 
    num_rows="dynamic", 
    use_container_width=True,
    column_config={
        "select": st.column_config.CheckboxColumn("Print", default=False)
    },
    disabled=["qr_code", "title", "call_number", "isbn"]  # make other columns read-only
    )

# Filter selected rows
selected_books = edited_df[edited_df['select']]

if not selected_books.empty:
    labels = [
        generate_label_image(
            row.qr_code,
            row.title,
            row.call_number,
            row.isbn if pd.notna(row.isbn) else ""
        )
        for _, row in selected_books.iterrows()
    ]
    
    pdf_buffer = create_pdf(selected_books)

    st.markdown("""
    ## 2. Download the PDF and print the labels  
    After downloading, you can stick the QR labels on the corresponding books
    """)
    
    st.download_button("Download PDF of Labels", pdf_buffer, file_name="qr_labels.pdf", mime="application/pdf")
