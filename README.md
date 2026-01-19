


--> AI Resume Screening System (ATS)

This project is an AI-powered Resume Screening System that helps HR teams
automatically evaluate resumes against a Job Description.

-->Features
- Upload ZIP of resumes (PDF)
- Resume parsing (Name, Skills)
- Semantic similarity using Sentence Transformers
- Automatic selection (Selected / Hold / Rejected)
- Excel report download
- FastAPI backend + Streamlit frontend

--> Tech Stack
- Python
- FastAPI
- Streamlit
- spaCy
- Sentence-Transformers
- Pandas

--> How to Run

--> Backend
```bash
cd backend
uvicorn main:app --reload
cd frontend
streamlit run app.py

Output
ATS score
Matched skills

Decision

Excel report for H
