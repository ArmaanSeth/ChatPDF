# 📄 Document Chatbot with Retrieval Augmented Generation (RAG)

Welcome to the **Document Chatbot with Retrieval Augmented Generation (RAG)** repository! This project enables interactive document retrieval using cutting-edge AI techniques. By integrating the RAG methodology with a Streamlit-powered interface, it allows seamless querying across multiple document formats.

---
## 📚 Table of Contents

- [✨ Overview](#-overview)
- [🗂️ File Structure](#️-file-structure)
- [🚀 Features](#-features)
- [📋 Requirements](#-requirements)
- [💻 Installation](#-installation)

---

## ✨ Overview

This chatbot leverages the RAG framework to enhance information retrieval from documents using natural language queries. It combines retrieval-based and generative AI capabilities for a smooth querying experience, making it ideal for dynamic, knowledge-intensive tasks.

The user-friendly Streamlit interface simplifies interaction, ensuring accessibility for users across various domains.

---

## 🗂️ File Structure

```
.
├── icons/                    # Icons for UI (bot, user)
│   ├── bot-icon.png
│   └── user-icon.png
├── src/                      # Source code for the app
│   ├── app.py                # Main application logic
│   ├── conversation.py       # Chat handling and AI chain integration
│   ├── document_utils.py     # Document processing and summarization logic
│   ├── htmlTemplates.py      # HTML and CSS templates for UI
│   ├── prompt_refiner.py     # Logic for refining prompts with LLM
│   └── text_processing.py    # Text splitting and vector store generation
├── test/                     # Test files for the app (PDF, TXT)
│   ├── test.pdf
│   └── test.txt
├── .env                      # Store your API keys and sensitive data
├── .gitignore                # Git ignore rules
├── LICENSE                   # Project License
├── README.md                 # Project documentation and setup guide
├── directory_tree.py         # Script for visualizing the directory tree (optional)
├── pyproject.toml            # Project dependencies and configuration
├── setup.sh                  # Setup script for environment and dependencies
└── uv.lock                   # UV lock file for environment management

```

---

## 🚀 Features

- **Multi-File Upload**: Process and query multiple documents in formats like PDF, TXT, CSV, and DOCX.
- **AI-Powered Chat**: Ask natural language questions, and the bot retrieves accurate answers from document content.
- **Document Summarization**: Summarizes content for better context understanding.
- **Prompt Refinement**: Refines user questions for more precise responses. You can **enable or disable** this feature via the toggle, allowing you to improve prompt clarity and conciseness when enabled.
- **Memory Retention**: Tracks conversation history for maintaining context.
- **Interactive UI**: A Streamlit-powered interface for intuitive interactions.
- **Extensibility**: Easily customizable for additional document types and use cases.

---

## 📋 Requirements

Ensure the following tools are installed:

- **Python 3.8+**: The version is automatically managed in the `setup.sh` script.
- **Dependencies**: Listed in `pyproject.toml` and installed automatically using the `setup.sh` script with the `uv sync` command.
- **UV**: Install via pip:

   ```bash
   pip install uv
   ```

   For more details, visit the [UV documentation page](https://pypi.org/project/uv/).

- **Python-dotenv**: For managing environment variables. Install via pip:

   ```bash
   pip install python-dotenv
   ```

   Add your API keys to a `.env` file in this format:

   ```plaintext
   OPENAI_API_KEY=your_openai_api_key_here
   HUGGINGFACE_API_KEY=your_huggingface_api_key_here
   ```

- **OpenAI API Key**: Required for GPT-4o mini and embedding models.
- **Hugging Face API Key**: Used to interact with Hugging Face's `facebook/bart-large-cnn` model for text summarization when the local summarizer model fails to load.
- **Bash**: Available on Unix-based systems (Linux/macOS). Windows users can use Git Bash or WSL.

---

## 💻 Installation

Follow these steps to set up your environment and install the necessary packages:

1. **Clone the Repository**  

   Clone the repository to your local machine:

   ```bash
   git clone https://github.com/ErfanShm/ChatDoc.git
   cd ChatDoc
   ```

2. **Run the Setup Script**  

   The `setup.sh` script automates the environment setup, including virtual environment creation, dependency synchronization, and application launch options:

   ```bash
   bash setup.sh
   ```

   Choose from the following options:
   - Sync dependencies
   - Run with Streamlit interface
   - Exit

3. **Access the User Interface**  

   Once running, access the user interface by navigating to [http://localhost:8000](http://localhost:8000) in your browser (usually done automatically).

---

## 📝 Usage

- **Input**: Upload multiple documents for analysis.
- **VectorStore Creation**: Converts documents into vector stores using FAISS and OpenAI embeddings.
- **Memory Integration**: Maintains context with a conversational memory buffer.
- **Text Generation**: Leverages GPT-4o mini Turbo for generating accurate responses.
- **Prompt Refinement**: Toggle this feature to refine and clarify your prompts for more concise, understandable outputs.
- **User Interface**: Streamlit provides an intuitive querying experience.

---

## 🙌 Acknowledgments

We extend our gratitude to the following tools and libraries that make this project possible:

- [Streamlit](https://streamlit.io/): For powering the intuitive user interface.
- [OpenAI](https://openai.com/): For GPT models and embeddings.
- [Hugging Face](https://huggingface.co/): For the `facebook/bart-large-cnn` summarization model.
- [UV](https://pypi.org/project/uv/): For streamlined environment and dependency management.
- [FAISS](https://github.com/facebookresearch/faiss): For efficient similarity search and clustering.
- [LangChain](https://langchain.com/): For chaining multiple AI models into a cohesive workflow.

---

## 📜 License

This repository is licensed under the [MIT License](https://opensource.org/licenses/MIT). You are free to use, modify, and distribute the code, provided you include the original copyright notice and license.
