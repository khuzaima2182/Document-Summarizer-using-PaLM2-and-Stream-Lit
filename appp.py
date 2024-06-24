import streamlit as st
import PyPDF2
import requests
import google.generativeai as palm

# Function to interact with the PaLM 2 API
def palm2_summarize(text):
    API_KEY = #Input you Api Key Here
    palm.configure(api_key=API_KEY)
    examples = [('Hello', 'Hi there Sir. How can I be your assistant')]
    response = palm.chat(messages=text, temperature=0.2, context='Speak like Document Summarizer', examples=examples)
    
    summary = ""
    for message in response.messages:
        summary += message['content'] + "\n"
    return summary.strip()

# Function to read text from a text file
def read_text(file):
    return file.read().decode("utf-8")

# Function to read text from a PDF file
def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Streamlit app title
st.title("Document Summarizer")

# File uploader
uploaded_file = st.file_uploader("Upload a text or PDF file", type=["txt", "pdf"])

# Display file name
if uploaded_file is not None:
    file_details = {
        "filename": uploaded_file.name,
        "filetype": uploaded_file.type,
        "filesize": uploaded_file.size,
    }
    st.write(file_details)

    # Read the uploaded file
    if uploaded_file.type == "text/plain":
        document = read_text(uploaded_file)
    elif uploaded_file.type == "application/pdf":
        document = read_pdf(uploaded_file)

    # Display the document
    st.subheader("Document Content")
    st.write(document)

    # Button to generate summary
    if st.button("Summarize"):
        if document:
            try:
                # Perform summarization using PaLM 2
                summary = palm2_summarize(document)
                st.subheader("Summary")
                st.write(summary)
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please upload a document to summarize.")
