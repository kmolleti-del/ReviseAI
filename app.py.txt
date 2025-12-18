import streamlit as st
import re
import heapq

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

    # Score sentences by word frequency
    sentence_scores = {}
    for sent in sentences:
        sent_lower = sent.lower()
        score = 0
        for w in freq:
            if w in sent_lower:
                score += freq[w]
        sentence_scores[sent] = score / max(len(sent.split()), 1)  # normalize by length

    # Pick top N sentences as summary points
    best_sentences = heapq.nlargest(max_points, sentence_scores, key=sentence_scores.get)

    # Keep original order
    ordered_summary = [s for s in sentences if s in best_sentences]

    return ordered_summary

# -------- Streamlit UI --------
st.title("ReviseAI Assistant")
st.write("Enter text to summarize into important points.")

# Input box
user_input = st.text_area("Enter text here:")

# Number of points
max_points = st.slider("Number of summary points:", 1, 10, 3)

# Summarize button
if st.button("Summarize"):
    points = summarize_text(user_input, max_points)
    st.subheader("Summary Points")
    for i, p in enumerate(points, 1):
        st.write(f"{i}. {p}")
