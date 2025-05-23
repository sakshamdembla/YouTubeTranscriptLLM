import re
from typing import List, Dict, Optional
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
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

    return None


def get_youtube_transcript(
    url: str,
    languages: Optional[List[str]] = None
) -> List[Dict]:
    """
    Fetches the transcript for a given YouTube video URL.

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


if __name__ == "__main__":
    # Example usage
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    try:
        data = get_youtube_transcript(url, languages=['en'])
        for entry in data:
            print(f"{entry['start']:.2f}s - {entry['text']}")
    except Exception as e:
        print(f"Error: {e}")
