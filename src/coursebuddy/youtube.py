import re
import subprocess
import json


def parse_youtube_url(url: str) -> dict:
    """Parse a YouTube URL and determine if it's a playlist or single video."""
    playlist_match = re.search(r'[?&]list=([^&]+)', url)
    video_match = re.search(r'(?:v=|youtu\.be/)([^&?]+)', url)

    if playlist_match:
        return {
            'type': 'playlist',
            'playlist_id': playlist_match.group(1),
            'video_id': video_match.group(1) if video_match else None
        }
    elif video_match:
        return {
            'type': 'video',
            'video_id': video_match.group(1)
        }
    else:
        raise ValueError(f"Could not parse YouTube URL: {url}")


def get_playlist_info(playlist_id: str) -> dict:
    """Get playlist title and list of video IDs using yt-dlp."""
    url = f"https://www.youtube.com/playlist?list={playlist_id}"

    result = subprocess.run(
        ['yt-dlp', '--flat-playlist', '-J', url],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(f"Failed to fetch playlist: {result.stderr}")

    data = json.loads(result.stdout)

    return {
        'title': data.get('title', 'Unknown Playlist'),
        'videos': [
            {'id': entry['id'], 'title': entry.get('title', 'Unknown')}
            for entry in data.get('entries', [])
        ]
    }


def get_video_info(video_id: str) -> dict:
    """Get video title using yt-dlp."""
    url = f"https://www.youtube.com/watch?v={video_id}"

    result = subprocess.run(
        ['yt-dlp', '--skip-download', '-J', url],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(f"Failed to fetch video info: {result.stderr}")

    data = json.loads(result.stdout)

    return {
        'id': video_id,
        'title': data.get('title', 'Unknown Video')
    }


def sanitize_filename(name: str) -> str:
    """Sanitize a string to be used as a filename."""
    # Remove or replace invalid characters
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    # Replace multiple spaces with single space
    name = re.sub(r'\s+', ' ', name)
    # Trim and limit length
    return name.strip()[:200]
