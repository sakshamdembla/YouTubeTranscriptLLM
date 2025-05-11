# YouTube Transcript LLM App

This application allows you to analyze YouTube video transcripts using LLM technology.

## Features

- Extract transcripts from YouTube videos
- Analyze transcripts using LLM technology (OpenAI)
- Generate summaries and insights from video content
- Create questions based on video content

## Installation

1. Clone this repository
2. Install the required dependencies:
```
pip install -r requirements.txt
```
3. Set up your OpenAI API key as an environment variable named `OPENAI_API_KEY`

## Usage

Run the Streamlit app:
```
streamlit run app.py
```

Then open your browser and navigate to the URL shown in the terminal (typically http://localhost:8501).

## Project Structure

- `app.py`: Main Streamlit application
- `utils/transcript_utils.py`: Functions for YouTube transcript processing
- `llm/interactions.py`: Functions for LLM interactions
- `requirements.txt`: Python package dependencies
- `README.md`: Project documentation

## License

MIT
