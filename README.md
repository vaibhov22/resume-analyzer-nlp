# NLP Resume Analyzer (ATS)

An NLP-based web application that analyzes resumes against job descriptions
and provides ATS score, skill match, missing skills, and a downloadable PDF report.

## Features
- Resume PDF parsing
- Skill extraction
- Resume–JD matching using TF-IDF & cosine similarity
- ATS score calculation
- PDF report generation
- Dockerized deployment

## Tech Stack
- Python
- Flask
- NLTK
- scikit-learn
- Docker

## Run with Docker
```bash
docker build -t resume-analyzer .
docker run -p 5000:5000 resume-analyzer
