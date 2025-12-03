import streamlit as st
import requests

# ---------- Page config ----------
st.set_page_config(
    page_title="Automated Insight Engine",
    page_icon="📊",
    layout="centered",
)

# ---------- Title & description ----------
st.title("Automated Insight Engine")
st.write(
    "Upload a CSV dataset and automatically generate an executive-ready PowerPoint and PDF report with AI-driven insights."
)

# ---------- File uploader ----------
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    st.success(f"File uploaded: {uploaded_file.name}")

# ---------- Generate button ----------
if st.button("Generate Report"):
    if uploaded_file is None:
        st.error("Please upload a CSV file first.")
    else:
        with st.spinner("Analyzing data and generating report... ⏳"):
            try:
                # Send file to FastAPI backend
                files = {
                    "data_csv": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")
                }

                response = requests.post(
                    "http://127.0.0.1:8000/generate-report",
                    files=files,
                    timeout=300,
                )

                if response.status_code == 200:
                    res_json = response.json()
                    st.success(res_json.get("message", "Report completed! 🎉"))

                    ppt_link = f"http://127.0.0.1:8000{res_json['ppt_path']}"
                    pdf_link = f"http://127.0.0.1:8000{res_json['pdf_path']}"

                    # Download buttons
                    st.markdown(f"[📥 Download PPT Report]({ppt_link})", unsafe_allow_html=True)
                    st.markdown(f"[📄 Download PDF Report]({pdf_link})", unsafe_allow_html=True)

                else:
                    st.error(f"Backend error {response.status_code}: {response.text}")

            except Exception as e:
                st.error(f"Failed to connect to backend: {e}")
