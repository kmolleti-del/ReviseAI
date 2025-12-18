import streamlit as st
import re
import heapq
from graphviz import Digraph

# ---------- Summarizer Function ----------
def summarize_text(text, max_points=3):
    if not text or len(text.strip()) == 0:
        return ["No text provided to summarize."]
    
    cleaned = re.sub(r'\s+', ' ', text)
    cleaned = re.sub(r'[^a-zA-Z0-9.?! ]', '', cleaned)
    
    sentences = re.split(r'(?<=[.?!]) +', cleaned)
    if len(sentences) <= max_points:
        return sentences
    
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
    
    sentence_scores = {}
    for sent in sentences:
        sent_lower = sent.lower()
        score = 0
        for w in freq:
            if w in sent_lower:
                score += freq[w]
        sentence_scores[sent] = score / max(len(sent.split()), 1)
    
    best_sentences = heapq.nlargest(max_points, sentence_scores, key=sentence_scores.get)
    ordered_summary = [s for s in sentences if s in best_sentences]
    
    return ordered_summary

# -------- Streamlit UI ----------
st.title("ReviseAI Assistant with Mind Map")
st.write("Enter text to summarize into important points and see a mind map.")

# Text input
user_input = st.text_area("Enter text here:")

# Number of points
max_points = st.slider("Number of summary points:", 1, 10, 3)

# Summarize button
if st.button("Summarize"):
    if not user_input.strip():
        st.warning("Please enter some text.")
    else:
        summary_points = summarize_text(user_input, max_points)
        
        # Display summary
        st.subheader("Summary Points")
        for i, point in enumerate(summary_points, 1):
            st.write(f"{i}. {point}")
        
        # Create a mind map using Graphviz
        dot = Digraph(comment='Mind Map', format='png')
        dot.node('A', 'Main Topic')
        
        for idx, point in enumerate(summary_points):
            dot.node(f'B{idx}', point)
            dot.edge('A', f'B{idx}')
        
        st.subheader("Mind Map")
        st.graphviz_chart(dot)
