from pathlib import Path
from youtube_transcript_api import YouTubeTranscriptApi


def fetch_transcript(video_id: str) -> list:
    """Fetch transcript for a YouTube video."""
    api = YouTubeTranscriptApi()
    transcript = api.fetch(video_id)
    return list(transcript)


def format_as_markdown(transcript: list, video_title: str) -> str:
    """Format transcript as plain markdown text."""
    # Join all transcript segments into plain text
    text_parts = [segment.text for segment in transcript]
    full_text = ' '.join(text_parts)

    # Create markdown with title as header
    markdown = f"# {video_title}\n\n{full_text}\n"

    return markdown


def save_markdown(content: str, filepath: Path) -> None:
    """Save markdown content to a file."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(content, encoding='utf-8')
