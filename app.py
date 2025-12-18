import streamlit as st
import re
import heapq
import PyPDF2

# ---------- Summarizer Function ----------
def summarize_text(text, max_sentences=3):
    if not text or len(text.strip()) == 0:
        return "No text provided to summarize."

    cleaned = re.sub(r'\s+', ' ', text).strip()
    sentences = re.split(r'(?<=[.?!।！？]) +', cleaned)
    if len(sentences) <= max_sentences:
        return cleaned

    words = cleaned.lower().split()
    stopwords = set([
        "the","a","an","in","on","and","or","if","is","are","was","were","to",
        "for","of","with","that","this","it","as","at","by","from","be","has",
        "have","had","but","not","can","could","will","would","should"
    ])

    freq = {}
    for w in words:
        if w not in stopwords:
            freq[w] = freq.get(w, 0) + 1
    if not freq:
        return cleaned

    sentence_scores = {}
    for sent in sentences:
        sent_lower = sent.lower()
        score = sum(freq[w] for w in freq if w in sent_lower)
        sentence_scores[sent] = score

    best_sentences = heapq.nlargest(max_sentences, sentence_scores, key=sentence_scores.get)
    ordered_summary = [s for s in sentences if s in best_sentences]

    return " ".join(ordered_summary)

# ---------- Streamlit UI ----------
st.title("ReviseAI PDF Summarizer")
st.write("Upload a PDF (English, Hindi, Telugu, etc.) to get a summary.")

uploaded_file = st.file_uploader("Upload PDF file", type="pdf")
summary_length = st.selectbox("Summary Length", ["Very Short", "Short", "Medium"])

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

if uploaded_file:
    with st.spinner("Extracting text and summarizing..."):
        pdf_text = extract_text_from_pdf(uploaded_file)
        if summary_length == "Very Short":
            max_sents = 2
        elif summary_length == "Short":
            max_sents = 3
        else:
            max_sents = 5
        summary = summarize_text(pdf_text, max_sentences=max_sents)
    st.subheader("📌 Summary")
    for sent in summary.split(". "):
        st.markdown(f"- {sent}")
