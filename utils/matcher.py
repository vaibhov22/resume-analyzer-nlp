from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def normalize(text):
    return text.lower().replace("-", " ")

def extract_skills(text, skills_list):
    text = normalize(text)
    found = []
    for skill in skills_list:
        if normalize(skill) in text:
            found.append(skill)
    return list(set(found))

def match_resume_job(resume_text, job_text):
    vectorizer = TfidfVectorizer(
        ngram_range=(1,2),
        stop_words="english"
    )
    vectors = vectorizer.fit_transform([resume_text, job_text])
    score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    return round(score * 100, 2)
def section_score(found, required):
    if not required:
        return 0
    return round((len(found) / len(required)) * 100, 2)
