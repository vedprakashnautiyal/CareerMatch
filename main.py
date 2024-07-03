from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
from utils import input_pdf_setup, get_gemini_response
import prompts
import style

import google.generativeai as genai
genai.configure(api_key=st.secrets["KEY"])

# Streamlit App
st.set_page_config(page_title="Career Match", page_icon=":briefcase:", layout="wide")

# Custom CSS
style.load_custom_css()

st.header("Career Match")
st.subheader('Unlocking Potential with Precision')
st.markdown("---")

input_text = st.text_input("Job Description: ", key="input")

uploaded_file = st.file_uploader("Upload your Resume (PDF)...", type=["pdf"])

pdf_content = ""

if uploaded_file is not None:
    st.success("PDF Uploaded Successfully")

col1, col2, col3, col4 = st.columns(4)

with col1:
    submit1 = st.button("About the Resume")
with col2:
    submit2 = st.button("How Can I Improve")
with col3:
    submit3 = st.button("Missing Keywords")
with col4:
    submit4 = st.button("Percentage Matched")

input_promp = st.text_input("Additional Queries")

submit5 = st.button("Submit")

def handle_submission(prompt):
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(prompt, pdf_content, input_text)
        st.write(response)
    else:
        st.warning("PDF Not Uploaded")

if submit1:
    handle_submission(prompts.input_prompt1)
elif submit2:
    handle_submission(prompts.input_prompt2)
elif submit3:
    handle_submission(prompts.input_prompt3)
elif submit4:
    handle_submission(prompts.input_prompt4)
elif submit5:
    handle_submission(input_promp)
