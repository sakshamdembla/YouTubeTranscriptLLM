# YouTube Transcript LLM App

A powerful application that leverages AI to analyze, summarize, and interact with YouTube video transcripts. This tool allows you to extract valuable insights from video content using OpenAI's language models.

![YouTube Transcript LLM App](https://img.shields.io/badge/App-YouTube%20Transcript%20LLM-red)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0%2B-orange)
![License](https://img.shields.io/badge/License-MIT-green)

## Features

- **Transcript Extraction**: Automatically fetch transcripts from any YouTube video that has captions available
- **Multi-Language Support**: Translate non-English transcripts to English when available
- **Interactive Chat Interface**: Have conversations with the AI about the video content
- **Real-time Analysis**: Get instant insights and answers about the video content
- **Memory Management**: Chat history is cleared when loading a new transcript, allowing fresh analysis
- **Manual Chat Clearing**: Clear the chat history at any time with a dedicated button

## Demo

Enter a YouTube URL, and the app will:
1. Extract the video title and transcript
2. Display the transcript in a collapsible section
3. Provide a chat interface where you can ask questions about the content

Example questions you can ask:
- "What is the main topic of this video?"
- "Can you summarize the key points in bullet points?"
- "What was discussed at the 5-minute mark?"
- "What evidence was provided for the main argument?"

## Installation

### Prerequisites
- Python 3.9 or higher
- pip (Python package installer)
- An OpenAI API key

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sakshamdembla/YouTubeTranscriptLLM.git
   cd YouTubeTranscriptLLM/youtube_transcript_llm_app
   ```

2. **Create and activate a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install the required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your OpenAI API key**
   
   Create a `.env` file in the project root:
   ```bash
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   ```
   
   Replace `your_api_key_here` with your actual OpenAI API key.

## Usage

### Running the Application

1. **Start the Streamlit app**
   ```bash
   python -m streamlit run app.py
   ```

2. **Access the web interface**
   Open your browser and navigate to the URL shown in the terminal (typically http://localhost:8501).

3. **Enter a YouTube URL**
   Paste the URL of any YouTube video that has captions available.

4. **Interact with the transcript**
   Once the transcript is loaded, use the chat interface to ask questions and analyze the content.

### Example Commands

```bash
# Start the app with a specific port
python -m streamlit run app.py --server.port 8888

# Run in headless mode (for servers)
python -m streamlit run app.py --server.headless true
```

## Troubleshooting

### Common Issues

- **"No transcript available for this video"**: The video either doesn't have captions or they're disabled. Try another video.
- **"HTTP Error 400: Bad Request"**: This is often a temporary issue with YouTube's API. Try again later.
- **OpenAI API errors**: Make sure your API key is correctly set in the `.env` file and that you have sufficient credits.

### Fixing Pytube Errors

If you're consistently seeing Pytube errors, check that you have the latest version:
```bash
pip install --upgrade pytube
```

## Project Structure

```
youtube_transcript_llm_app/
├── app.py                     # Main Streamlit application
├── requirements.txt           # Python package dependencies
├── .env                       # Environment variables (create this yourself)
├── README.md                  # Project documentation
├── utils/
│   ├── __init__.py            # Package initializer
│   └── transcript_utils.py    # Functions for YouTube transcript processing
└── llm/
    ├── __init__.py            # Package initializer
    └── interactions.py        # Functions for LLM interactions
```

## How It Works

1. **Transcript Retrieval**: Uses the `youtube_transcript_api` to fetch the closed captions.
2. **Language Handling**: Attempts to find English transcripts first, then falls back to translating other languages if needed.
3. **Title Extraction**: Uses web requests to extract the video title from the YouTube page.
4. **LLM Integration**: Sends the transcript and user questions to OpenAI's GPT model for analysis.
5. **Session Management**: Maintains chat history within the session until a new video is loaded or the history is manually cleared.

## Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add some amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

Please make sure to update tests as appropriate and follow the existing code style.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Streamlit](https://streamlit.io/) for the web application framework
- [YouTube Transcript API](https://github.com/jdepoix/youtube-transcript-api) for transcript extraction
- [OpenAI](https://openai.com/) for providing the AI models
- All contributors who have helped to improve this project
