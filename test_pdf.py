from utils.resume_parser import extract_text_from_pdf

resume_text = extract_text_from_pdf("sample_resume.pdf")
print(resume_text)
