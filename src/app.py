import streamlit as st
from document_utils import process_documents
from conversation import handle_question, user_template, bot_template
from htmlTemplates import css
from prompt_refiner import refine_prompt_with_llm

def main():
    st.set_page_config(page_title="Chat with Multiple Documents", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    # Initialize session state variables
    if "docs" not in st.session_state:
        st.session_state.docs = []
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "processed" not in st.session_state:
        st.session_state.processed = False
    if "enable_refinement" not in st.session_state:
        st.session_state.enable_refinement = False

    st.header("Chat with Your Documents :books:")

    # Sidebar
    with st.sidebar:
        
        # Add toggle for prompt refinement
        st.markdown("## :gear: Settings")
        st.session_state.enable_refinement = st.toggle("Enable Prompt Refinement", value=st.session_state.enable_refinement)

        st.markdown("## :information_source: About")
        st.info("**Upload your files and press 'Process'** to prepare the documents for questioning.")

        with st.expander("Need Help?"):
            st.write(""" 
            - **Upload files**: Use the file uploader to upload your documents.
            - **Supported formats**: PDF, TXT, CSV, DOCX.
            - **Process files**: Click 'Process' to analyze the uploaded documents.
            - **Prompt Refinement**: Enable this feature in Settings to improve question accuracy:
                - When enabled: Your questions will be automatically refined for better context and clarity
                - When disabled: Your questions will be processed exactly as written
                - Recommended: Enable for complex questions or when you need more accurate answers
            """)
        
        # Document uploader
        docs = st.file_uploader("Upload your files here", accept_multiple_files=True, type=["pdf", "txt", "csv", "docx"])
        if docs:
            st.session_state.docs = docs
            st.subheader("Uploaded Files")
            for i, doc in enumerate(docs):
                st.write(f"{i+1}. {doc.name}")

        # Processing logic
        if st.button("Process"):
            if docs:
                with st.spinner("Processing documents, please wait..."):
                    st.session_state.chat_history = []
                    st.session_state.conversation = None
                    process_documents(docs)
                    st.session_state.processed = True
            else:
                st.error("Please upload at least one document before processing.")

    # Main chat area
    if st.session_state.processed:
        st.success("Documents have been processed successfully! You can now ask questions.")

    # Use st.chat_input instead of st.text_input
    question = st.chat_input("Ask a question from your document:")
    
    if question:
        # Only refine the question if the toggle is enabled
        if st.session_state.enable_refinement:
            refined_question = refine_prompt_with_llm(question)
            handle_question(refined_question)
        else:
            handle_question(question)

    # Clear chat history button
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

if __name__ == '__main__':
    main()
