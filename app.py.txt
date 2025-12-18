import streamlit as st
import openai

st.title("ReviseAI Assistant")
st.write("Enter text and get AI-generated summary in points.")

# --- OpenAI API key ---
# Make sure to set environment variable OPENAI_API_KEY on Streamlit Cloud
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else ""

# Text input
user_input = st.text_area("Enter text here:", height=250)

# Button
if st.button("Summarize"):
    if not user_input.strip():
        st.warning("Please enter some text.")
    elif not openai.api_key:
        st.error("OpenAI API key not found! Add it to Streamlit secrets.")
    else:
        with st.spinner("Generating summary..."):
            prompt = f"Summarize the following text into short bullet points:\n\n{user_input}\n\n-"

            response = openai.Completion.create(
                engine="text-davinci-003",  # GPT-3
                prompt=prompt,
                max_tokens=300,
                temperature=0.5,
                top_p=1,
                n=1,
                stop=None
            )

            summary_text = response.choices[0].text.strip()

        st.subheader("📌 Summary Points")
        points = summary_text.split("\n")
        for point in points:
            if point.strip():
                st.markdown(f"- {point.strip().lstrip('-')}")
