from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os
import streamlit as st
from langchain_core.documents import Document

load_dotenv()

def get_chunks(raw_text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", " ", ""]
    )
    # Convert text chunks to Document objects
    chunks = text_splitter.create_documents([raw_text])
    return chunks

def get_vectorstore(chunks):
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        st.error("OPENAI_API_KEY not found in environment variables.")
        return None

    try:
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            base_url="https://api.avalai.ir/v1",
            api_key=openai_api_key,
            dimensions=1024
        )
        # Create vectorstore from Document objects
        vectorstore = FAISS.from_documents(chunks, embeddings)
        return vectorstore
    except Exception as e:
        st.error(f"Error creating vector store: {str(e)}")
        return None