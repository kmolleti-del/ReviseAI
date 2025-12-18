import streamlit as st
from transformers import pipeline
import PyPDF2

# ---------------- CONFIG ----------------
st.set_page_config(page_title="ReviseAI", layout="centered")
st.title("📘 ReviseAI – AI Study Summarizer")
st.write("Upload a PDF or paste text to get short revision points.")

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    return pipeline("summarization", model="facebook/bart-large-cnn")

summarizer = load_model()

# ---------------- INPUT OPTIONS ----------------
input_type = st.radio("Choose Input Type", ["PDF", "Text"])

uploaded_file = None
text_input = ""

if input_type == "PDF":
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
else:
    text_input = st.text_area("Paste your text here", height=250)

summary_length = st.selectbox(
    "Summary Length",
    ["Very Short", "Short", "Medium"]
)

# ---------------- FUNCTIONS ----------------
def extract_text_from_pdf(pdf):
    reader = PyPDF2.PdfReader(pdf)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

def summarize(text, length):
    if len(text.strip()) == 0:
        return ""

    if length == "Very Short":
        max_len, min_len = 80, 25
    elif length == "Medium":
        max_len, min_len = 200, 80
    else:
        max_len, min_len = 130, 40

    result = summarizer(
        text[:3000],
        max_length=max_len,
        min_length=min_len,
        do_sample=False
    )

    return result[0]["summary_text"]

# ---------------- PROCESS ----------------
if st.button("Generate Summary"):
    with st.spinner("AI is summarizing..."):
        if input_type == "PDF" and uploaded_file:
            content = extract_text_from_pdf(uploaded_file)
        else:
            content = text_input

        summary = summarize(content, summary_length)

    if summary:
        st.subheader("📌 Summary Points")
        for point in summary.split(". "):
            st.markdown(f"- {point.strip()}")
    else:
        st.warning("Please provide valid input text or PDF.")
