import streamlit as st
import pandas as pd
import io
from utils.api_client import APIClient

st.set_page_config(page_title="Student Management", layout="wide")
st.title("🧑‍🎓 Student Management")
st.markdown("""
You can **view** all students information, **create** new student information or **update** existing student information on this page.
            """)

# ---- Load all students ----
@st.cache_data(ttl=10)
def load_students():
    try:
        data = APIClient.get_api_data("students")
        df = pd.DataFrame(data)
        if "updated_at" in df.columns:
            df["updated_at"] = pd.to_datetime(df["updated_at"], errors="coerce")
            df = df.sort_values("updated_at", ascending=False)
        return df
    except Exception as e:
        st.error(f"Error loading students: {e}")
        return pd.DataFrame()


def process_file(file, mode="create"):
    """Process uploaded CSV/Excel for create/update"""
    # Parse CSV or Excel
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    results = []
    for _, row in df.iterrows():
        student = {
            "matric_number": str(row["matric_number"]).strip().upper(),
            "full_name": str(row["full_name"]).strip().upper(),
            "email": str(row["email"]).strip().lower(),
            "telegram_id": str(row.get("telegram_id", "")).strip(),
            "status": str(row.get("status", "active")).strip().lower()
        }
        print("student: ", student)
        existing = APIClient.search_student(student["matric_number"])

        if mode == "create":
            if existing:
                results.append({
                    "matric_number": student["matric_number"],
                    "full_name": student["full_name"],
                    "result": "❌ Student with the same matric number already exists thus not created as a new student (skipped)"
                })
            else:
                code, resp = APIClient.create_student(student)
                if code in (200, 201):
                    results.append({
                        "matric_number": student["matric_number"],
                        "full_name": student["full_name"],
                        "result": "✅ Created"
                    })
                else:
                    results.append({
                        "matric_number": student["matric_number"],
                        "full_name": student["full_name"],
                        "result": f"❌ Failed to create student: {resp}"
                    })

        elif mode == "update":
            if not existing:
                results.append({
                    "matric_number": student["matric_number"],
                    "full_name": student["full_name"],
                    "result": "❌ Student matric number not found and cannot update as existing student (skipped)"
                })
            else:
                code, resp = APIClient.update_student(student["matric_number"], student)
                if code == 200:
                    results.append({
                        "matric_number": student["matric_number"],
                        "full_name": student["full_name"],
                        "result": "🔄 Student info updated"
                    })
                else:
                    results.append({
                        "matric_number": student["matric_number"],
                        "full_name": student["full_name"],
                        "result": f"❌ Failed to update student info: {resp}"
                    })
    return pd.DataFrame(results)

def refresh_students():
    st.cache_data.clear()
    st.rerun()

def get_sample_csv():
    sample = pd.DataFrame([{
        "matric_number": "A1234567X",
        "full_name": "JOHN DOE",
        "email": "john.doe@u.nus.edu",
        "telegram_id": "123456789",
        "status": "active"
    }])
    buffer = io.StringIO()
    sample.to_csv(buffer, index=False)
    return buffer.getvalue()


# ---- UI ----
df = load_students()
if df.empty:
    st.warning("No student data available.")
else:
    st.markdown("### 📋 Students Information")
    st.dataframe(df, use_container_width=True)

st.markdown("---")
st.markdown("### 📂 Create or Upload Student Information")
st.markdown("""
Upload a CSV or Excel file with the following columns:

- **matric_number** (Required, e.g. A0012345X)
- **full_name** (Required)
- **email** (Required)
- **telegram_id** (Required)
- **status** (optional, defaults to active. Valid status values include "active", "inactive", "suspended")

⚠️ Then choose **one action** only:
- **➕ Create Students** → Adds new students. Existing ones will be skipped with an error.
- **✏️ Update Students** → Updates existing students. New ones will be skipped with an error.
""")

st.download_button(
    label="📥 Download Sample CSV",
    data=get_sample_csv(),
    file_name="sample_students.csv",
    mime="text/csv"
)

file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])

col1, col2 = st.columns(2)

if file and col1.button("➕ Create Students"):
    st.info("Processing in **Create mode**...")
    results_df = process_file(file, mode="create")
    st.markdown("### Results")
    st.dataframe(results_df, use_container_width=True)
    st.info("✅ Operation finished. Please refresh the page in your browser (⌘R / Ctrl+R) to see updated student table.")

if file and col2.button("✏️ Update Students"):
    st.info("Processing in **Update mode**...")
    results_df = process_file(file, mode="update")
    st.markdown("### Results")
    st.dataframe(results_df, use_container_width=True)
    st.info("✅ Operation finished. Please refresh the page in your browser (⌘R / Ctrl+R) to see updated student table.")