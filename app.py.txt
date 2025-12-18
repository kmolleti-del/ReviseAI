import streamlit as st
import re
import heapq

# ---------- PDF reader import ----------
# Try modern 'pypdf', fallback to 'PyPDF2'
try:
    from pypdf import PdfReader
except ImportError:
    from PyPDF2 import PdfReader
# ---------- PDF reader import ends ----------

# -------- Summarizer Function --------
def summarize_text(text, max_points=3):
    if not text or len(text.strip()) == 0:
        return ["No text provided to summarize."]

    # Clean text
    cleaned = re.sub(r'\s+', ' ', text)
    cleaned = re.sub(r'[^a-zA-Z0-9.?! ]', '', cleaned)

    # Split into sentences
    sentences = re.split(r'(?<=[.?!]) +', cleaned)
    if len(sentences) <= max_points:
        return sentences

    # Word frequencies (ignoring stopwords)
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
        return sentences

    # Score sentences by word frequency, normalized by sentence length
    sentence_scores = {}
    for sent in sentences:
        sent_lower = sent.lower()
        score = 0
        for w in freq:
            if w in sent_lower:
                score += freq[w]
        sentence_scores[sent] = score / max(len(sent.split()), 1)

    # Pick top N sentences as summary points
    best_sentences = heapq.nlargest(max_points, sentence_scores, key=sentence_scores.get)

    # Keep original order
    ordered_summary = [s for s in sentences if s in best_sentences]

    return ordered_summary

# -------- PDF Text Extraction --------
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + " "
    return text

# -------- Streamlit UI --------
st.title("ReviseAI Assistant")
st.write("Enter text or upload a PDF to get important summary points.")

# Text input
user_input = st.text_area("Enter text here (optional):")

# PDF upload
uploaded_pdf = st.file_uploader("Or upload a PDF", type=["pdf"])

# Number of points
max_points = st.slider("Number of summary points:", 1, 10, 3)

# Summarize button
if st.button("Summarize"):
    source_text = ""

    # Priority: PDF > text input
    if uploaded_pdf is not None:
        source_text = extract_text_from_pdf(uploaded_pdf)
    elif user_input.strip():
        source_text = user_input
    else:
        st.warning("Please enter text or upload a PDF.")
    
    if source_text:
        summary_points = summarize_text(source_text, max_points)
        st.subheader("Summary Points")
        for i, point in enumerate(summary_points, 1):
            st.write(f"{i}. {point}")
