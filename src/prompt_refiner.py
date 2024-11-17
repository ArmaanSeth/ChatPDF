import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def refine_prompt_with_llm(prompt):
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if not openai_api_key:
        st.error("OPENAI_API_KEY not found in environment variables")
        return prompt

    try:
        # Initialize the LLM client with additional parameters for refinement
        llm = ChatOpenAI(
            temperature=0.1,  # Low temperature for more deterministic outputs
            top_p=0.9,        # Controls diversity of output; set to 0.9 for focused results
            frequency_penalty=0.5,  # Penalizes repetition; helps avoid redundant phrasing
            presence_penalty=0.0,   # No penalty for introducing new topics
            base_url="https://api.avalai.ir/v1",
            api_key=openai_api_key,
            model="gpt-4o-mini-2024-07-18"
        )

        # Define the prompt template
        template = ChatPromptTemplate.from_messages([
            ("system", 
            "PROMPT REFINEMENT INSTRUCTIONS:\n\n"
            "You are an AI tool exclusively for refining text prompts. Your task is to make prompts **clearer, concise, and precise** while preserving their **original meaning**. Follow these rules strictly:\n\n"
            "1. Refine prompts without interpreting or answering them.\n"
            "2. Preserve the exact meaning; do not add, remove, or alter intent.\n"
            "3. Focus on fixing ambiguities, redundancies, or dictation errors.\n"
            "4. Maintain the original tone, style, and technical terminology.\n"
            "5. Provide the input unchanged if it is already clear and concise.\n"
            "6. Avoid conversational phrasing, commentary, or explanations.\n\n"
            "Output only the refined prompt text, strictly adhering to these rules."),
            ("human", "{original_prompt}")
        ])

        # Use the LLM to refine the prompt
        refined_prompt = llm.invoke(template.format_messages(original_prompt=prompt)).content.strip()

        # Return the refined prompt
        return refined_prompt

    except Exception as e:
        st.error(f"Error refining prompt: {str(e)}")
        return prompt
