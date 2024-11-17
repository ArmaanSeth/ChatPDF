from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_openai import ChatOpenAI
import streamlit as st
from htmlTemplates import user_template, bot_template
from dotenv import load_dotenv
import os
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()

# Updated Prompts
prompt_search_query = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    ("user", "Given the above conversation, generate a search query to look up information relevant to the conversation.")
])

prompt_get_answer = ChatPromptTemplate.from_messages([
    ("system", "You are an AI assistant that answers questions based on the provided context. When asked, use your general knowledge to respond if the context does not have the necessary information. For greetings or unrelated queries, respond appropriately without relying solely on the context."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    ("system", "Here is the context from the documents (if available):"),
    ("user", "{context}"),
    ("system", "Based on the context and your general knowledge, provide the most relevant and complete answer to the user's query.")
])

def get_conversationchain(vectorstore):
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        st.error("OPENAI_API_KEY not found in environment variables")
        return None

    try:
        llm = ChatOpenAI(model="gpt-4o-mini-2024-07-18", temperature=0.2, base_url="https://api.avalai.ir/v1", api_key=openai_api_key)
        
        retriever = vectorstore.as_retriever()

        # Create history-aware retriever
        retriever_chain = create_history_aware_retriever(llm, retriever, prompt_search_query)

        # Create document chain
        document_chain = create_stuff_documents_chain(llm, prompt_get_answer)

        # Create retrieval chain
        retrieval_chain = create_retrieval_chain(retriever_chain, document_chain)

        return retrieval_chain
    except Exception as e:
        st.error(f"Error creating conversation chain: {str(e)}")
        return None

def format_chat_history(chat_history):
    formatted_messages = []
    for message in chat_history:
        if message["role"] == "user":
            formatted_messages.append(HumanMessage(content=message["content"]))
        elif message["role"] == "assistant":
            formatted_messages.append(AIMessage(content=message["content"]))
    return formatted_messages

def handle_question(question):
    if st.session_state.conversation:
        try:
            # Format the chat history properly
            formatted_history = format_chat_history(st.session_state.chat_history)
            
            # Prepare the input for the chain
            chain_input = {
                "chat_history": formatted_history,
                "input": question
            }

            # Invoke the chain
            response = st.session_state.conversation.invoke(chain_input)
            
            # Extract the answer from the response
            answer = response.get('answer', None)
            
            # If no answer, fall back to general response
            if not answer or answer.strip() == "":
                llm = ChatOpenAI(
                    temperature=0.7,
                    base_url="https://api.avalai.ir/v1",
                    api_key=os.getenv("OPENAI_API_KEY"),
                    model="gpt-4o-mini-2024-07-18"
                )
                answer = llm.invoke([HumanMessage(content=question)]).content.strip()

            # Update chat history
            st.session_state.chat_history.append({"role": "user", "content": question})
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            
            # Display chat history
            for message in st.session_state.chat_history:
                if message["role"] == "user":
                    st.write(user_template.replace("{{MSG}}", message["content"]), unsafe_allow_html=True)
                else:
                    st.write(bot_template.replace("{{MSG}}", message["content"]), unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error processing question: {str(e)}")
    else:
        st.error("Please process documents first before asking questions.")
