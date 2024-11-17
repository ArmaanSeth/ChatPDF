from PyPDF2 import PdfReader
import csv
from unstructured.partition.auto import partition
import streamlit as st
from text_processing import get_chunks, get_vectorstore
from conversation import get_conversationchain
from transformers import pipeline
import requests
from nltk.translate.bleu_score import sentence_bleu
import nltk
import os
from dotenv import load_dotenv
import warnings
from langchain_core.documents import Document
import warnings

warnings.filterwarnings(
    "ignore",
    category=FutureWarning,
    message=r".*clean_up_tokenization_spaces.*"
)

# Set environment variables for OpenMP and NLTK data path
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

load_dotenv()

# Hugging Face API setup
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"}

def query(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error in API request: {e}")
        return {"error": str(e)}

def summarize_text(text, min_length, max_length):
    payload = {
        "inputs": text,
        "parameters": {"min_length": min_length, "max_length": max_length}
    }
    output = query(payload)

    if isinstance(output, list) and output:
        return output[0].get('summary_text', "Error: Summary text not found.")
    else:
        return "Error: Unable to get a summary."

# Summarizer model initialization
model_name = "sshleifer/distilbart-cnn-12-6"
summarizer = None
try:
    summarizer = pipeline("summarization", model=model_name)
except Exception as e:
    st.warning(f"Failed to load summarizer model locally: {e}")

def summarize(text, min_length=10, max_length=564):
    max_input_length = 1024  # Maximum input length for BART model

    # Truncate input text if necessary
    if len(text.split()) > max_input_length:
        text = ' '.join(text.split()[:max_input_length])
        st.warning("Input text was too long and has been truncated.")

    # Calculate appropriate max_length based on input length, but don't exceed 70% of input length
    input_length = len(text.split())
    max_length = min(int(input_length * 0.7), max_length, max_input_length)

    if summarizer:
        try:
            summary = summarizer(
                text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False,
                clean_up_tokenization_spaces=True
            )
            return summary[0].get('summary_text', "Error: Summary text not found.")
        except Exception as e:
            st.error(f"An error occurred during summarization: {e}")
            return None
    else:
        return summarize_text(text, min_length, max_length)

def get_text_from_file(uploaded_file):
    try:
        if uploaded_file.type == "application/pdf":
            pdf_reader = PdfReader(uploaded_file)
            text = "".join(page.extract_text() for page in pdf_reader.pages)
            if not text.strip():
                raise ValueError("The PDF file is empty or couldn't be read properly.")
            return text

        elif uploaded_file.type == "text/plain":
            text = uploaded_file.read().decode('utf-8')
            if not text.strip():
                raise ValueError("The text file is empty.")
            return text

        elif uploaded_file.type == "text/csv":
            text = "".join(", ".join(row) + "\n" for row in csv.reader(uploaded_file.read().decode('utf-8').splitlines()))
            if not text.strip():
                raise ValueError("The CSV file is empty or couldn't be read properly.")
            return text

        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            elements = partition(file=uploaded_file)
            text = "\n".join(map(str, elements))
            if not text.strip():
                raise ValueError("The DOCX file is empty or couldn't be read properly.")
            return text

        else:
            st.error(f"Unsupported file type: {uploaded_file.type}")
            return None

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
        return None

def get_text_from_docs(docs):
    separator = "\n\nnext docs: (previous information before this are from previous docs, ignore them)\n\n"
    text = ""
    for i, doc in enumerate(docs):
        file_text = get_text_from_file(doc)
        if file_text:
            if i > 0:
                text += separator
            text += file_text
    return text

def process_documents(docs):
    try:
        raw_text = get_text_from_docs(docs)
        text_chunks = get_chunks(raw_text)
        
        # Process Documents and create summarized Documents
        summarized_chunks = []
        for chunk in text_chunks:
            if chunk.page_content.strip():  # Check the page_content instead of the Document object
                summary = summarize(chunk.page_content)
                if summary:
                    summarized_chunks.append(Document(
                        page_content=summary,
                        metadata=chunk.metadata
                    ))

        vectorstore = get_vectorstore(summarized_chunks)

        if vectorstore:
            st.session_state.conversation = get_conversationchain(vectorstore)
            st.success("Documents have been processed successfully! You can now ask questions.")
        else:
            st.error("Failed to create vector store. Please check your API key and try again.")

    except Exception as e:
        st.error(f"An error occurred during document processing: {e}")