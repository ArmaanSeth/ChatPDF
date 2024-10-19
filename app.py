import streamlit as st
import fitz  # PyMuPDF for PDF extraction
import google.generativeai as genai

# Manually pass the API key for Google Gemini API
genai.configure(api_key="YourAPIKEY")

# Streamlit interface
def main():
    st.set_page_config(page_title="Gemini AI Chatbot with PDF Support", page_icon=":robot_face:", layout="wide")

    st.title("Gemini AI Chatbot with PDF Support")
    st.markdown("""
    This app allows you to upload a PDF file, ask questions based on the PDF content, and get answers using the **Google Gemini AI API**.
    """)
    
    # File upload section
    st.subheader("Step 1: Upload Your PDF File")
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf", label_visibility="collapsed")
    
    # If PDF is uploaded
    if uploaded_file:
        # PDF Extraction
        with st.spinner("Extracting text from PDF..."):
            pdf_text = extract_pdf_text(uploaded_file)
        
        # PDF Preview
        st.subheader("PDF Content Preview")
        st.text_area("Preview of PDF Content", pdf_text[:1500], height=300)

        # User question input
        st.subheader("Step 2: Enter Your Question")
        user_input = st.text_input("Ask a question based on the PDF content:")

        if st.button("Generate Response"):
            if user_input:
                with st.spinner("Generating response..."):
                    response = generate_response(user_input, pdf_text)
                    st.subheader("AI Response:")
                    st.write(response)
            else:
                st.warning("Please enter a question to get a response!")

# Extract PDF text function
def extract_pdf_text(uploaded_file):
    """Extract text from PDF using PyMuPDF (fitz)."""
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    pdf_text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pdf_text += page.get_text("text")
    return pdf_text

# Generate response function using Google Gemini API
def generate_response(prompt, pdf_text):
    """Generate response based on PDF content using Google Gemini API."""
    try:
        # Generate a response by combining the PDF content with the user prompt
        context = f"Here is the content extracted from the PDF:\n\n{pdf_text}\n\nUser's Question: {prompt}\nAnswer:"

        # Use the correct generate_content method for text-only input
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(context)

        # Return the response's text
        return response.text
    except Exception as e:
        return f"Error occurred: {str(e)}"

# Run the app
if __name__ == "__main__":
    main()
