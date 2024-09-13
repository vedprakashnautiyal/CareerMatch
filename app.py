__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import chromadb
import chromadb.config
from dotenv import load_dotenv
import streamlit as st 
from util import input_pdf_setup, get_rag_response
import prompt
import style
# Load environment variables
load_dotenv()

# Streamlit App
st.set_page_config(page_title="Career Match", page_icon=":briefcase:", layout="centered")

# Custom CSS
style.load_custom_css()

st.header("Career Match")
st.subheader('Unlocking Potential with Precision')
st.markdown("---")

# Input job description
input_text = st.text_input("Job Description or Job URL: ", key="input")

# Upload Resume (PDF)
resume_file = st.file_uploader("Upload your Resume (PDF)...", type=["pdf"])
resume_content = None

# Extract content from uploaded PDF
if resume_file is not None:
    with st.spinner("Processing PDF..."):
        resume_content = input_pdf_setup(resume_file)
    st.success("PDF Uploaded and Processed Successfully")

# Layout for buttons
buttons = {
    "About the Resume": prompt.template1,
    "How Can I Improve": prompt.template2,
    "Missing Keywords": prompt.template3,
    "Percentage Matched": prompt.template4
}

cols = st.columns(len(buttons))

# Handle the submission for generating responses
def handle_submission(prompt):
    if not input_text:
        st.warning("Please enter a job description or URL.")
        return
    if not resume_content:
        st.warning("Please upload a PDF resume.")
        return
    
    with st.spinner("Generating response..."):
        response = get_rag_response(prompt, resume_content, input_text)
    st.write(response)

# Create buttons and handle clicks
for col, (button_text, prompt) in zip(cols, buttons.items()):
    if col.button(button_text):
        handle_submission(prompt)
