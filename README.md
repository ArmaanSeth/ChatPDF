# ChatPDF

A **Streamlit** web application that allows users to upload a PDF file, extract the content, and interact with **Google Gemini AI** to ask questions based on the extracted PDF content and receive AI-generated responses.

## Features

- **PDF File Upload**: Upload a PDF file, and the app extracts its content.
- **PDF Content Preview**: Preview the extracted text from the uploaded PDF.
- **Interactive AI Chatbot**: Ask questions based on the PDF content, and Google Gemini AI provides answers.
- **Response Generation**: The app uses the Google Gemini AI API to generate answers from the PDF.

## How to Use

### 1. Navigate to the project directory:


### 2. Install required dependencies:


### 3. Set up Google Gemini API:

- Sign up for the **Google Gemini API** and obtain your API key.
- Open the `app.py` file and configure the API key:



Replace `"YourAPIKEY"` with your actual API key.

### 4. Run the app:


### 5. Open a browser and visit:


## How It Works

- **Upload PDF**: The user uploads a PDF file, and the app extracts the text content.
- **PDF Content Preview**: The first 1500 characters of the extracted text are displayed.
- **User Question**: The user asks a question related to the PDF content.
- **AI Response**: The app uses the Google Gemini AI API to generate a response, which is then displayed.

## Dependencies

- **Streamlit**: For building the web app interface.
- **PyMuPDF (fitz)**: For extracting text from the uploaded PDF.
- **Google Gemini AI**: For generating responses to user queries.


