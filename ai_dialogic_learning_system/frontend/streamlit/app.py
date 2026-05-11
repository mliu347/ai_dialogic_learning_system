import streamlit as st

st.title("AI-Mediated Dialogic Learning System")

student_input = st.text_area("Student Input")

if st.button("Submit"):
    st.write("AI Response Placeholder")
