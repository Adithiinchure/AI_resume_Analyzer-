from fastapi import FastAPI, UploadFile, File, Form
from resume_parser import extract_text_from_pdf, parse_resume
from embeddings import get_embedding, cosine_similarity
import zipfile
import io

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI Resume Screening API running"}

@app.post("/match-zip/")
async def match_zip(
    file: UploadFile = File(...),
    jd: str = Form(...)
):
    results = []

    zip_bytes = await file.read()
    zip_file = zipfile.ZipFile(io.BytesIO(zip_bytes))

    for name in zip_file.namelist():
        if name.endswith(".pdf"):
            pdf_bytes = zip_file.read(name)
            pdf_file = io.BytesIO(pdf_bytes)

            text = extract_text_from_pdf(pdf_file)
            parsed = parse_resume(text)

            resume_emb = get_embedding(text)
            jd_emb = get_embedding(jd)

            similarity = cosine_similarity(resume_emb, jd_emb)

            # Decision rule
            if similarity >= 0.75:
                decision = "Selected"
            elif similarity >= 0.55:
                decision = "Hold"
            else:
                decision = "Rejected"

            matched_skills = [
                s for s in parsed["skills"]
                if s.lower() in jd.lower()
            ]

            results.append({
                "Name": parsed["name"],
                "Skills": ", ".join(parsed["skills"]),
                "Similarity": round(similarity * 100, 2),
                "Matched Skills": ", ".join(matched_skills),
                "Decision": decision
            })

    return {"results": results}
