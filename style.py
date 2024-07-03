import streamlit as st

def load_custom_css():
    st.markdown(
        """
        <style>
        .main {
            background-color: #f5f5f5;
            padding: 20px;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 24px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .stTextInput>div>div>input {
            border: 2px solid #ddd;
            border-radius: 4px;
            padding: 8px;
        }
        .stFileUploader>label {
            border: 2px dashed #ddd;
            border-radius: 4px;
            padding: 16px;
            text-align: center;
        }
        .stFileUploader>label:hover {
            background-color: #f1f1f1;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
