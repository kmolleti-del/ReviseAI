import streamlit as st
from transformers import pipeline

st.title("ReviseAI Assistant")
st.write("Welcome! Enter text to summarize it using AI.")

# Load AI model (cached)
@st.cache_resource
def load_model():
    return pipeline("summarization", model="facebook/bart-large-cnn")

summarizer = load_model()

# Text input
user_input = st.text_area("Enter text here:", height=250)

# Button
if st.button("Summarize"):
    if user_input.strip() == "":
        st.warning("Please enter some text.")
    else:
        with st.spinner("AI is summarizing..."):
            result = summarizer(
                user_input[:3000],  # model limit
                max_length=130,
                min_length=40,
                do_sample=False
            )

            summary = result[0]["summary_text"]

        st.subheader("📌 Summary Points")
        for point in summary.split(". "):
            st.markdown(f"- {point.strip()}")
