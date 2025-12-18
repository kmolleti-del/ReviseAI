import streamlit as st
import re
import heapq
from pypdf import PdfReader  # uses the modern 'pypdf' package

# -------- summarizer (short summary) --------
def summarize_text(text, max_sentences=3):
    if not text or len(text.strip()) == 0:
        return "No text provided to summarize."

    # Clean text
    cleaned = re.sub(r'\s+', ' ', text)  # collapse spaces/newlines
    cleaned = re.sub(r'[^a-zA-Z0-9.?! ]', '', cleaned)  # remove special chars

    # Split into sentences
    sentences = re.split(r'(?<=[.?!]) +', cleaned)
    if len(sentences) <= max_sentences:
        return cleaned

    # Word frequencies
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

    # Score sentences
    sentence_scores = {}
    for sent in sentences:
        sent_lower = sent.lower()
        for w in freq:
            if w in sent_lower:
                sentence_scores[sent] = sentence_scores.get(sent, 0) + freq[w]

    # Top N sentences
    best_sentences = heapq.nlargest(max_sentences, sentence_scores, key=sentence_scores.get)

    # Keep original order
    ordered_summary = [s for s in sentences if s in best_sentences]

    return " ".join(ordered_summary)

# -------- PDF text extractor --------
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

# -------- Streamlit UI --------
st.title("ReviseAI Assistant")
st.write("Upload a PDF or paste text, then click Summarize to get short revision notes.")

# Text input
user_input = st.text_area("Enter text here (optional):")

# PDF upload
uploaded_pdf = st.file_uploader("Or upload a PDF", type=["pdf"])

if st.button("Summarize"):
    source_text = ""

    # Priority: PDF if provided, else text box
    if uploaded_pdf is not None:
        source_text = extract_text_from_pdf(uploaded_pdf)
    elif user_input.strip():
        source_text = user_input
    else:
        st.warning("Please enter some text or upload a PDF.")

    if source_text:
        summary = summarize_text(source_text, max_sentences=3)
        st.subheader("Summary")
        st.write(summary)
