import re
import spacy
from PyPDF2 import PdfReader

nlp = spacy.load("en_core_web_sm")

BAD_NAMES = ["Python", "Django", "SQL", "Machine", "Learning", "AWS", "Excel", "TensorFlow", "Java", "Data", "Science"]

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def parse_resume(text):
    doc = nlp(text)
    
    # --- Try spaCy first ---
    name = None
    for ent in doc.ents:
        if ent.label_ == "PERSON" and ent.text not in BAD_NAMES:
            name = ent.text
            break
    
    # --- Heuristic fallback: first line with 2-4 words, not a skill/library ---
    if not name:
        lines = text.split("\n")
        for line in lines[:5]:  # only top 5 lines
            words = [w for w in line.split() if w.isalpha()]
            if 1 < len(words) <= 4 and all(w[0].isupper() for w in words):
                # ignore skill names
                if not any(w in BAD_NAMES for w in words):
                    name = line.strip()
                    break
    
    # --- Extract skills ---
    skills = re.findall(r'Python|Django|SQL|Machine Learning|AWS|Excel|TensorFlow|Java|Data Science', text, re.I)
    
    return {"name": name or "N/A", "skills": list(set(skills))}
