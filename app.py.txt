import streamlit as st
import re
import heapq

# ---------- add function here ----------
def summarize_text(text, max_sentences=3):
    if not text or len(text.strip()) == 0:
        return "No text provided to summarize."

    cleaned = re.sub(r'\s+', ' ', text)
    cleaned = re.sub(r'[^a-zA-Z0-9.?! ]', '', cleaned)

    sentences = re.split(r'(?<=[.?!]) +', cleaned)
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
        for w in freq:
            if w in sent_lower:
                sentence_scores[sent] = sentence_scores.get(sent, 0) + freq[w]

    best_sentences = heapq.nlargest(max_sentences, sentence_scores, key=sentence_scores.get)
    ordered_summary = [s for s in sentences if s in best_sentences]
    return " ".join(ordered_summary)
# ---------- function ends here ----------

st.title("ReviseAI Assistant")
st.write("Welcome! You can enter text to summarize or revise it.")

user_input = st.text_area("Enter text here:")

if st.button("Summarize"):
    summary = summarize_text(user_input, max_sentences=3)
    st.subheader("Summary")
    st.write(summary)
