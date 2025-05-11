# Functions for YouTube transcript processing
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
import requests
import json
import re
import time
import urllib.request
import urllib.parse

def get_video_id(url):
    """
    Extract the video ID from a YouTube URL.
    
    Args:
        url (str): YouTube video URL
        
    Returns:
        str: YouTube video ID
    """
    if "youtube.com/watch?v=" in url:
        return url.split("youtube.com/watch?v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    return url

def get_transcript(video_id):
    """
    Get the transcript for a YouTube video.
    
    Args:
        video_id (str): YouTube video ID
        
    Returns:
        str: Full transcript text
    """
    try:
        # First try to get the transcript in English
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
            transcript = ' '.join([item['text'] for item in transcript_list])
            return transcript
        except NoTranscriptFound:
            # If English transcript not found, try to get any available transcript
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            available_transcript = next(iter(transcript_list), None)
            
            if available_transcript:
                # Try to translate to English if possible
                try:
                    translated_transcript = available_transcript.translate('en')
                    transcript_data = translated_transcript.fetch()
                    transcript = ' '.join([item['text'] for item in transcript_data])
                    return transcript
                except Exception:
                    # If translation fails, use the original transcript
                    transcript_data = available_transcript.fetch()
                    transcript = ' '.join([item['text'] for item in transcript_data])
                    return transcript
            else:
                return "No transcript available for this video."
                
    except TranscriptsDisabled:
        return "Transcripts are disabled for this video."
    except Exception as e:
        error_message = str(e)
        if "no element found" in error_message:
            return "No transcript available for this video. The creator may not have added captions."
        else:
            return f"Error fetching transcript: {error_message}"

def get_video_title(url):
    """
    Get the title of a YouTube video using multiple fallback methods.
    
    Args:
        url (str): YouTube video URL
        
    Returns:
        str: Video title
    """
    # Method 1: Try using pytube with retry
    for attempt in range(3):  # Try up to 3 times
        try:
            yt = YouTube(url)
            # Add a small delay to let pytube properly fetch the data
            time.sleep(0.5)
            if yt.title:
                return yt.title
        except Exception as e:
            print(f"Pytube error (attempt {attempt+1}): {str(e)}")
            time.sleep(1)  # Wait before retrying
    
    # Method 2: Try using requests to get HTML and extract title
    try:
        # Make a request to the video page
        video_id = get_video_id(url)
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        }
        
        response = requests.get(video_url, headers=headers)
        
        if response.status_code == 200:
            # Try to extract title from HTML
            title_match = re.search(r'<title>(.*?) - YouTube</title>', response.text)
            if title_match:
                return title_match.group(1)
                
            # Alternative pattern
            title_match = re.search(r'"title":"(.*?)"', response.text)
            if title_match:
                return title_match.group(1)
    except Exception as e:
        print(f"HTML extraction error: {str(e)}")
    
    # Method 3: Try using urllib to get the page title
    try:
        video_id = get_video_id(url)
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        req = urllib.request.Request(
            video_url, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
        )
        
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            title_match = re.search(r'<title>(.*?) - YouTube</title>', html)
            if title_match:
                return title_match.group(1)
    except Exception as e:
        print(f"Urllib error: {str(e)}")
        
    # Method 4: Try using video ID as title (ultimate fallback)
    try:
        video_id = get_video_id(url)
        return f"YouTube Video (ID: {video_id})"
    except Exception as e:
        return "Unknown YouTube Video"
