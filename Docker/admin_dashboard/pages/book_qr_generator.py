import streamlit as st
import pandas as pd
import qrcode
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from utils.api_client import APIClient
import os


st.set_page_config(page_title="QR Label Generator", layout="wide")
st.title("🏷️ QR Code Label Generator")

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


from reportlab.lib.units import mm

def create_pdf(rows):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    page_width, page_height = A4

    # Define label dimensions (in mm)
    label_width = 70 * mm      # 7 cm wide
    label_height = 37 * mm     # 3.7 cm high
    num_cols = 3
    num_rows = 8

    # Optional fine-tuning margins (some printers can’t print to the edge)
    left_margin = 0 * mm
    top_margin = 0 * mm

    count = 0
    for _, row in rows.iterrows():
        uid = row["qr_code"]
        title = row["title"]
        call_number = row["call_number"]
        isbn = row["isbn"] if pd.notna(row["isbn"]) else ""

        # Generate QR code
        qr = qrcode.make(uid)
        qr_buf = BytesIO()
        qr.save(qr_buf, format="PNG")
        qr_buf.seek(0)

        # Compute grid position
        col = count % num_cols
        row_num = (count // num_cols) % num_rows

        # Top-left coordinate for this label
        x = left_margin + col * label_width
        y = page_height - top_margin - (row_num + 1) * label_height

        # --- Draw content inside the label box ---
        qr_size = 25 * mm
        qr_x = x + 3 * mm
        qr_y = y + (label_height - qr_size) / 2  # vertically centered
        c.drawImage(ImageReader(qr_buf), qr_x, qr_y, width=qr_size, height=qr_size)

        text_x = qr_x + qr_size + 3 * mm
        text_y = y + label_height - 10 * mm
        c.setFont("Helvetica", 8)
        c.drawString(text_x, text_y, f"Title: {title[:30]}")
        c.drawString(text_x, text_y - 8, f"Call No: {call_number}")
        if isbn:
            c.drawString(text_x, text_y - 16, f"ISBN: {isbn}")

        count += 1

        # New page after filling 24 labels
        if count % (num_cols * num_rows) == 0:
            c.showPage()

    c.save()
    buffer.seek(0)
    return buffer


def show_qr_label_tab():

    @st.cache_data(ttl=600)
    def load_books_from_api():
        try:
            data = APIClient.get_book_copy_labels()
            return pd.DataFrame(data)
        except Exception as e:
            st.error(f"Error loading book data: {e}")
            return pd.DataFrame()

    df = load_books_from_api()

    if df.empty:
        st.warning("No book data available.")
        return

    st.markdown("### Step 1: Select books to generate labels")
    select_all = st.checkbox("✅ Select All")
    df["select"] = select_all
    cols = df.columns.tolist()
    cols.insert(0, cols.pop(cols.index("select")))
    df = df[cols]

    edited_df = st.data_editor(
        df, 
        num_rows="dynamic", 
        use_container_width=True,
        column_config={"select": st.column_config.CheckboxColumn("Print", default=False)},
        disabled=["qr_code", "title", "call_number", "isbn"]
    )

    selected_books = edited_df[edited_df["select"]]

    if not selected_books.empty:
        st.markdown("### Step 2: Download the PDF")
        pdf_buffer = create_pdf(selected_books)
        st.download_button("📥 Download PDF Labels", pdf_buffer, file_name="qr_labels.pdf", mime="application/pdf")
        st.info(
            '''
            🖨️ **Printing Reminder:**\n
            When printing the PDF, choose **“Actual Size”** (not “Fit to Page”).
            This ensures perfect alignment with the *Unistat A4 24-label sticker paper (3×8 layout, 70 mm × 37 mm)*.
            '''
        )
        image_path = os.path.join(os.path.dirname(__file__), "..", "assets", "QR_Printer_Config.png")
        st.image(image_path, caption="Printer Configuration" )

show_qr_label_tab()