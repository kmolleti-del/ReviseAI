import streamlit as st

st.title("ReviseAI Assistant")
st.write("Welcome! You can enter text to summarize or revise it.")

# Add a text input box
user_input = st.text_area("Enter text here:")

# Add a button
if st.button("Summarize"):
    st.write("You entered:", user_input)
    st.write("This is where AI summary would appear.")
