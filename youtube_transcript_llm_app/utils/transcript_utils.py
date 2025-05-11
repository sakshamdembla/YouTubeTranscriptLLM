# Functions for YouTube transcript processing
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
import requests
import json
import re

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
    # Method 1: Try using pytube
    try:
        yt = YouTube(url)
        if yt.title:
            return yt.title
    except Exception as e:
        print(f"Pytube error: {str(e)}")
    
    # Method 2: Try using video ID as title (fallback)
    try:
        video_id = get_video_id(url)
        return f"YouTube Video (ID: {video_id})"
    except Exception as e:
        return "Unknown YouTube Video"
