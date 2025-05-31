# Functions for LLM interactions
import os
from openai import OpenAI
import streamlit as st

def get_api_key():
    """
    Get the OpenAI API key from Streamlit secrets (for cloud deployment)
    or fallback to environment variable (for local development).
    """
    try:
        if hasattr(st, 'secrets') and 'OPENAI_API_KEY' in st.secrets:
            return st.secrets["OPENAI_API_KEY"]
    except Exception:
        pass

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("OpenAI API key not found. Please set it in Streamlit secrets or as an environment variable.")
        st.stop()
    return api_key

# Ensure API key is loaded before creating client
os.environ["OPENAI_API_KEY"] = get_api_key()

# Create client without passing api_key explicitly (new SDK style)
client = OpenAI()

def analyze_transcript(transcript, prompt_template="Summarize the following YouTube transcript:"):
    try:
        is_conversational = "\n\n" in prompt_template and ("User:" in prompt_template or "Assistant:" in prompt_template)
        full_prompt = prompt_template if is_conversational else f"{prompt_template}\n\n{transcript}"

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes YouTube video transcripts and answers questions about the content."},
                {"role": "user", "content": full_prompt}
            ],
            max_tokens=800,
            temperature=0.7
        )
        return response.choices[0].message.content

    except Exception as e:
        print(f"Detailed error: {str(e)}")
        return f"Error analyzing transcript: {str(e)}"

def generate_questions(transcript, num_questions=5):
    try:
        prompt = f"Based on the following YouTube transcript, generate {num_questions} thoughtful questions about the content:\n\n{transcript}"

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates insightful questions based on video content."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        return response.choices[0].message.content

    except Exception as e:
        print(f"Detailed error: {str(e)}")
        return f"Error generating questions: {str(e)}"
