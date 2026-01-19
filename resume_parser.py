import re
import spacy
from PyPDF2 import PdfReader

nlp = spacy.load("en_core_web_sm")

# ---------- PDF TEXT EXTRACTION ----------
def extract_text_from_pdf(file):
    file.seek(0)
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"

    return text.strip()


# ---------- NAME EXTRACTION ----------
def extract_name(text):
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    top_lines = lines[:5]

    # spaCy NER
    for line in top_lines:
        doc = nlp(line)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                if 2 <= len(ent.text.split()) <= 3:
                    return ent.text

    # Regex fallback
    for line in top_lines:
        if re.match(r"^[A-Z][a-z]+(?:\s[A-Z][a-z]+){1,2}$", line):
            return line

    return "Not Found"


# ---------- SKILLS EXTRACTION ----------
def extract_skills(text):
    text = text.lower()

    SKILLS_DB = [
        "python", "django", "flask", "sql", "mysql", "postgresql",
        "machine learning", "data science", "numpy", "pandas",
        "tensorflow", "scikit-learn", "java", "aws",
        "docker", "kubernetes", "rest api", "git"
    ]

    skills = []
    for skill in SKILLS_DB:
        if re.search(r"\b" + re.escape(skill) + r"\b", text):
            skills.append(skill.title())

    return skills   # ✅ NEVER return "N/A"


# ---------- MAIN PARSER ----------
def parse_resume(text):
    return {
        "name": extract_name(text),
        "skills": extract_skills(text)
    }
