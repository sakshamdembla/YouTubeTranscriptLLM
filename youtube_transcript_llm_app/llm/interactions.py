# Functions for LLM interactions
import os
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st

# Load environment variables from .env file (for local development)
load_dotenv()

def get_api_key():
    """
    Get the OpenAI API key from either Streamlit secrets (for cloud deployment)
    or environment variables (for local development).
    """
    try:
        # Try to get from Streamlit secrets first (for cloud deployment)
        if hasattr(st, 'secrets') and 'OPENAI_API_KEY' in st.secrets:
            return st.secrets["OPENAI_API_KEY"]
    except Exception:
        pass
    
    # Fallback to environment variable (for local development)
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        st.error("OpenAI API key not found. Please set it in Streamlit secrets or as an environment variable.")
        st.stop()
    
    return api_key

# Get API key using the appropriate method
api_key = get_api_key()

# Initialize OpenAI client with the API key (new API format)
openai.api_key = api_key

def analyze_transcript(transcript, prompt_template="Summarize the following YouTube transcript:"):
    """
    Analyze a YouTube transcript using an LLM.
    
    Args:
        transcript (str): The transcript text to analyze
        prompt_template (str): The template for the prompt to send to the LLM
        
    Returns:
        str: The LLM response
    """
    try:
        # Check if this is a conversational prompt (contains newlines and specific markers)
        is_conversational = "\n\n" in prompt_template and ("User:" in prompt_template or "Assistant:" in prompt_template)
        
        if is_conversational:
            full_prompt = prompt_template
        else:
            full_prompt = f"{prompt_template}\n\n{transcript}"
        
        # Using the new OpenAI client API format (1.0.0+)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes YouTube video transcripts and answers questions about the content."},
                {"role": "user", "content": full_prompt}
            ],
            max_tokens=800,  # Increased token limit for more detailed responses
            temperature=0.7  # Slightly increased creativity
        )
        
        return response.choices[0].message.content
    except Exception as e:
        # Print the detailed error for debugging
        print(f"Detailed error: {str(e)}")
        return f"Error analyzing transcript: {str(e)}"

def generate_questions(transcript, num_questions=5):
    """
    Generate questions about the content in the transcript.
    
    Args:
        transcript (str): The transcript text
        num_questions (int): Number of questions to generate
        
    Returns:
        str: Generated questions
    """
    try:
        prompt = f"Based on the following YouTube transcript, generate {num_questions} thoughtful questions about the content:\n\n{transcript}"
        
        # Using the new OpenAI client API format (1.0.0+)
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
        # Print the detailed error for debugging
        print(f"Detailed error: {str(e)}")
        return f"Error generating questions: {str(e)}" 
