import streamlit as st
import re
import heapq

# ---------- Summarizer Function ----------
def summarize_text(text, max_sentences=3):
    if not text or len(text.strip()) == 0:
        return "No text provided to summarize."

    # Keep Unicode characters (Telugu, Hindi, etc.)
    cleaned = re.sub(r'\s+', ' ', text)  # collapse whitespace
    # Don't remove non-English letters, just normalize spaces
    cleaned = cleaned.strip()

    # Split sentences using punctuation
    sentences = re.split(r'(?<=[.?!।！？]) +', cleaned)
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
        score = 0
        for w in freq:
            if w in sent_lower:
                score += freq[w]
        sentence_scores[sent] = score

    # Top N sentences
    best_sentences = heapq.nlargest(max_sentences, sentence_scores, key=sentence_scores.get)
    ordered_summary = [s for s in sentences if s in best_sentences]

    return " ".join(ordered_summary)

# ---------- Streamlit UI ----------
st.title("ReviseAI Assistant (Supports Hindi & Telugu)")
st.write("Enter text in any language (English, Hindi, Telugu, etc.) to summarize.")

user_input = st.text_area("Enter text here:")

if st.button("Summarize"):
    summary = summarize_text(user_input, max_sentences=3)
    st.subheader("Summary")
    st.write(summary)
