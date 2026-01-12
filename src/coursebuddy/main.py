import argparse
from pathlib import Path

from .youtube import parse_youtube_url, get_playlist_info, get_video_info, sanitize_filename
from .transcript import fetch_transcript, format_as_markdown, save_markdown


def process_video(video_id: str, video_title: str, output_dir: Path) -> bool:
    """Process a single video and save its transcript."""
    try:
        print(f"  Fetching transcript for: {video_title}")
        transcript = fetch_transcript(video_id)
        markdown = format_as_markdown(transcript, video_title)

        filename = f"{sanitize_filename(video_title)}.md"
        filepath = output_dir / filename
        save_markdown(markdown, filepath)

        print(f"  Saved: {filepath}")
        return True
    except Exception as e:
        print(f"  Error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Convert YouTube videos/playlists to markdown transcripts'
    )
    parser.add_argument('url', help='YouTube video or playlist URL')
    parser.add_argument(
        '-o', '--output',
        default='./output',
        help='Output directory (default: ./output)'
    )

    args = parser.parse_args()

    output_base = Path(args.output)

    try:
        parsed = parse_youtube_url(args.url)
    except ValueError as e:
        print(f"Error: {e}")
        return 1

    if parsed['type'] == 'playlist':
        print(f"Fetching playlist info...")
        playlist_info = get_playlist_info(parsed['playlist_id'])
        print(f"Playlist: {playlist_info['title']}")
        print(f"Videos: {len(playlist_info['videos'])}")

        output_dir = output_base / sanitize_filename(playlist_info['title'])

        success = 0
        failed = 0

        for i, video in enumerate(playlist_info['videos'], 1):
            print(f"\n[{i}/{len(playlist_info['videos'])}] {video['title']}")
            if process_video(video['id'], video['title'], output_dir):
                success += 1
            else:
                failed += 1

        print(f"\nComplete! Success: {success}, Failed: {failed}")

    else:
        print(f"Fetching video info...")
        video_info = get_video_info(parsed['video_id'])
        print(f"Video: {video_info['title']}")

        output_dir = output_base / "single_videos"

        if process_video(video_info['id'], video_info['title'], output_dir):
            print("\nComplete!")
        else:
            print("\nFailed to process video.")
            return 1

    return 0


if __name__ == '__main__':
    exit(main())
