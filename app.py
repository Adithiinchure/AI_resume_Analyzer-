import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000/match-zip/"

st.set_page_config(page_title="AI Resume ATS", layout="wide")
st.title("📄 AI Resume Screening (ZIP Upload)")

with st.form("zip_form"):
    zip_file = st.file_uploader("Upload ZIP of Resumes", type=["zip"])
    jd_text = st.text_area("Paste Job Description", height=200)
    submit = st.form_submit_button("🚀 Analyze Resumes")

if submit:
    if not zip_file or not jd_text.strip():
        st.warning("Upload ZIP and paste JD")
    else:
        with st.spinner("Processing resumes..."):
            files = {"file": zip_file}
            data = {"jd": jd_text}

            response = requests.post(API_URL, files=files, data=data)
            data = response.json()["results"]

            df = pd.DataFrame(data)

            st.subheader("📊 Screening Results")
            st.dataframe(df)

            # Download Excel
            excel_file = "ATS_Results.xlsx"
            df.to_excel(excel_file, index=False)

            with open(excel_file, "rb") as f:
                st.download_button(
                    "⬇ Download Excel Report",
                    f,
                    file_name="ATS_Results.xlsx"
                )
