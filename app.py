import streamlit as st
import requests
import re
from PyPDF2 import PdfReader

# --- FastAPI endpoint ---
API_URL = "http://127.0.0.1:8000/match/"

st.set_page_config(page_title="AI Resume Screening", layout="wide")
st.title("📄 AI Resume Screening App")
st.write("Upload a candidate resume and a Job Description to get similarity score and parsed details.")

# --- Function to extract candidate name locally (fallback if backend fails) ---
def extract_name_from_pdf(uploaded_file):
    try:
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        # Simple regex to catch first full name (You can make this more advanced)
        match = re.search(r"([A-Z][a-z]+ [A-Z][a-z]+)", text)
        return match.group(1) if match else "Name not found"
    except Exception:
        return "Name not found"

# --- Upload Resume & Job Description ---
with st.form("resume_form"):
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    jd_text = st.text_area("Paste Job Description Here")
    submit_button = st.form_submit_button("Match Resume")

if submit_button:
    if not uploaded_file or not jd_text:
        st.warning("Please upload a resume and provide a job description.")
    else:
        with st.spinner("Analyzing..."):
            files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            data = {"jd": jd_text}

            try:
                response = requests.post(API_URL, files=files, data=data)

                if response.status_code == 200:
                    result = response.json()

                    # --- Parsed Resume Section ---
                    st.subheader("📝 Parsed Resume Details")
                    parsed = result.get("parsed_resume", {})
                    name = parsed.get("name")

                    # If backend didn’t return name correctly, extract locally
                    if not name or name.lower() == "pandas":
                        name = extract_name_from_pdf(uploaded_file)

                    skills = parsed.get("skills", [])
                    st.write(f"**Candidate Name:** {name}")
                    st.write(f"**Skills Extracted:** {', '.join(skills) if skills else 'N/A'}")

                    # --- Similarity Score Section ---
                    st.subheader("📊 Similarity Score")
                    similarity = result.get("similarity_score", 0)
                    st.metric("Similarity with Job Description", f"{similarity*100:.1f}%")
                    st.progress(similarity)

                    # --- Skill Matching Section ---
                    st.subheader("✅ Matched Skills with JD")
                    jd_skills = [word.strip().lower() for word in re.findall(r'\b\w+\b', jd_text.lower())]
                    matched_skills = [s for s in skills if s.lower() in jd_skills]
                    st.write(", ".join(matched_skills) if matched_skills else "No matched skills found.")

                else:
                    st.error(f"API Error: {response.status_code}")

            except Exception as e:
                st.error(f"Request failed: {e}")
