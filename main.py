from fastapi import FastAPI, UploadFile, Form
from resume_parser import extract_text_from_pdf, parse_resume
from embeddings import get_embedding, cosine_similarity

import os

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI Resume Screening API is running ✅"}

@app.post("/match/")
async def match_resume(file: UploadFile, jd: str = Form(...)):
    # Extract text directly from uploaded PDF
    text = extract_text_from_pdf(file.file)
    parsed = parse_resume(text)

    # Get embeddings
    resume_emb = get_embedding(text)
    jd_emb = get_embedding(jd)

    # Compute similarity
    similarity_score = cosine_similarity(resume_emb, jd_emb)

    return {
        "parsed_resume": parsed,
        "similarity_score": round(similarity_score, 3)
    }
