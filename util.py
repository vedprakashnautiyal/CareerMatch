import fitz
import os
import streamlit as st 
import google.generativeai as genai
from langchain_core.prompts import PromptTemplate
from langchain.docstore.document import Document
from langchain_chroma import Chroma
from langchain.schema import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda


# Configure Gemini model
genai.configure(api_key=os.getenv("KEY"))

# RAG setup
def get_rag_response(template, pdf_content, input_text):
    if input_text.startswith('http://') or input_text.startswith('https://'):
        # It's a URL
        st.info("URL detected. Processing...")
        loader = WebBaseLoader(web_path=input_text)
        docs = loader.load()
        text_content = docs[0].page_content
        docs =  [Document(page_content=text_content)]
    else:
        # It's a string (job description)
        st.info("Job description text detected.")
        docs = [Document(page_content=input_text)]
    # Save to disk
    vectorstore = Chroma.from_documents(
        documents=docs ,                 # Data
        embedding=GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=os.getenv("KEY")),    # Embedding model
        persist_directory="./chroma_db" # Directory to save data
        )
    # Load from disk
    vectorstore_disk = Chroma(
        persist_directory="./chroma_db", # Directory of db
        embedding_function=GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=os.getenv("KEY"))
    )
    retriever = vectorstore_disk.as_retriever(search_kwargs={"k": 1})
    # Define the LLM model
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=os.getenv("KEY"),
        temperature=0.7, top_p=0.85
    )
    # Format the documents in LLM readable format
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    # retrieved_docs = retriever.get_relevant_documents(input_text)
    # Combine retrieved job description with resume content

    # prompt=PromptTemplate(input_variables=["pdf_content","job_description"], template=template)
    prompt = PromptTemplate.from_template(template)
    def prepare_inputs(query):
        return {
            "job_description": retriever.get_relevant_documents(pdf_content),
            "pdf_content": pdf_content
        }

    rag_chain = (
        RunnableLambda(prepare_inputs)
        | {
            "job_description": lambda x: format_docs(x["job_description"]),
            "pdf_content": lambda x: x["pdf_content"]
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    # Combine the retriever and LLM into the RAG chain
    # rag_chain = (
    #     {"context": retriever | format_docs, "question": RunnablePassthrough()}
    #     | prompt  # Apply the prompt template (template4 in this case)
    #     | llm     # Run the LLM (Google Gemini)
    #     | StrOutputParser()  # Parse the output
    # )
    # rag_chain = create_stuff_documents_chain(llm, prompt)

    # Get response
    result = rag_chain.invoke("Don't give any introduction or explanation. Just give the output in the format asked.")
    # result = rag_chain.invoke({"pdf_content": pdf_content, "job_description": retrieved_job_description})

    return result

# Function to extract text from PDF
def input_pdf_setup(resume_file):
    if resume_file is not None:
        # Read the PDF file
        document = fitz.open(stream=resume_file.read(), filetype="pdf")
        text_parts = []

        # Extract text from each page
        for page in document:
            text_parts.append(page.get_text())

        pdf_text_content = " ".join(text_parts)
        text_file = open("Output.txt", "w")
        text_file.write(pdf_text_content)
        text_file.close()
        return pdf_text_content
    else:
        raise FileNotFoundError("No file uploaded")