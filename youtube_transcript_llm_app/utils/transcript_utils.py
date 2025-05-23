# Functions for YouTube transcript processing
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
import requests
import json
import re
import time
import urllib.request
import urllib.parse
from typing import List, Dict, Optional
from urllib.parse import urlparse, parse_qs

def extract_video_id(url: str) -> Optional[str]:
    """
    Extracts the video ID from a YouTube URL.

    Args:
        url (str): Full YouTube video URL.

    Returns:
        Optional[str]: Video ID if extractable, else None.
    """
    # Parse URL and query params
    parsed = urlparse(url)
    
    # Handle youtu.be short links
    if parsed.netloc in ("youtu.be", "www.youtu.be"):
        return parsed.path.lstrip('/')

    # Handle regular watch URLs
    if parsed.path == "/watch":
        qs = parse_qs(parsed.query)
        video_ids = qs.get('v')
        if video_ids:
            return video_ids[0]

    # Handle embed URLs
    match = re.search(r"/embed/([\w-]+)", parsed.path)
    if match:
        return match.group(1)

    # Fallback: Check if the URL is already just a video ID
    if re.match(r'^[\w-]{11}$', url):
        return url

    return None

def get_video_id(url: str) -> Optional[str]:
    """
    Extract the video ID from a YouTube URL.
    This is a wrapper around extract_video_id for backward compatibility.
    
    Args:
        url (str): YouTube video URL
        
    Returns:
        str: YouTube video ID or None if not extractable
    """
    return extract_video_id(url)

def get_transcript(video_id_or_url: str, languages: Optional[List[str]] = None) -> str:
    """
    Get the transcript for a YouTube video.
    
    Args:
        video_id_or_url (str): YouTube video ID or URL
        languages (List[str], optional): Preferred language codes (e.g., ['en', 'en-US'])
        
    Returns:
        str: Full transcript text or error message
    """
    # Check if input is a URL and extract video_id if needed
    video_id = video_id_or_url
    if "youtube" in video_id_or_url or "youtu.be" in video_id_or_url:
        video_id = extract_video_id(video_id_or_url)
        if not video_id:
            return "Could not extract video ID from URL."
    
    if not languages:
        languages = ['en']
        
    try:
        # First try to get the transcript in requested languages
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
            transcript = ' '.join([item['text'] for item in transcript_list])
            return transcript
        except NoTranscriptFound:
            # If transcript not found in requested languages, try to get any available transcript
            try:
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                available_transcript = next(iter(transcript_list), None)
                
                if available_transcript:
                    # Try to translate to first requested language if possible
                    try:
                        translated_transcript = available_transcript.translate(languages[0])
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
            except Exception as list_err:
                return f"Error listing transcripts: {str(list_err)}"
                
    except VideoUnavailable:
        return "The video is unavailable. It might be private or removed."
    except TranscriptsDisabled:
        return "Transcripts are disabled for this video."
    except Exception as e:
        error_message = str(e)
        if "no element found" in error_message:
            return "No transcript available for this video. The creator may not have added captions."
        else:
            return f"Error fetching transcript: {error_message}"

def get_youtube_transcript(url: str, languages: Optional[List[str]] = None) -> List[Dict]:
    """
    Fetches the transcript for a given YouTube video URL with detailed segments.

    Args:
        url (str): YouTube video URL.
        languages (List[str], optional): Preferred language codes (e.g., ['en', 'en-US']).

    Returns:
        List[Dict]: A list of transcript segments with 'text', 'start', and 'duration'.

    Raises:
        ValueError: If video ID cannot be extracted.
        VideoUnavailable: If video is private or removed.
        TranscriptsDisabled: If transcripts are disabled for the video.
        NoTranscriptFound: If no transcript is available in requested languages.
    """
    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError(f"Could not extract video ID from URL: {url}")

    try:
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id,
            languages=languages or ['en']
        )
        return transcript

    except VideoUnavailable:
        raise VideoUnavailable(f"Video '{video_id}' is unavailable.")
    except TranscriptsDisabled:
        raise TranscriptsDisabled(f"Transcripts are disabled for video '{video_id}'.")
    except NoTranscriptFound:
        raise NoTranscriptFound(
            f"No transcripts found for video '{video_id}' in languages {languages}."
        )

def get_video_title(url):
    """
    Get the title of a YouTube video using HTML parsing methods.
    
    Args:
        url (str): YouTube video URL
        
    Returns:
        str: Video title
    """
    # Extract video ID first
    video_id = extract_video_id(url)
    if not video_id:
        return "Invalid YouTube URL"
        
    # Method 1: Try using requests to get HTML and extract title
    try:
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
    
    # Method 2: Try using urllib to get the page title
    try:
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
        
    # Method 3: Use video ID as title (ultimate fallback)
    return f"YouTube Video (ID: {video_id})"
