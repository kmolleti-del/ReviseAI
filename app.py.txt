import streamlit as st

st.set_page_config(page_title="ReviseAI Assistant", page_icon="📝", layout="wide")
st.title("📝 ReviseAI Assistant")
st.write("Paste your notes or text below and get a concise revision summary!")

user_text = st.text_area("Enter your text here:", height=200)

if st.button("Generate Summary"):
    if user_text.strip() == "":
        st.warning("Please enter some text to summarize.")
    else:
        sentences = user_text.split(". ")
        summary = ". ".join(sentences[:3]) + ("..." if len(sentences) > 3 else "")
        
        st.subheader("Summary:")
        st.write(summary)
        st.info(f"Word count: {len(user_text.split())}")
