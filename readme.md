# CourseBuddy

Convert YouTube videos and playlists to markdown transcripts.

## Installation

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/CourseBuddy.git
cd CourseBuddy

# Install with uv
uv sync
```

## Usage

```bash
# Single video
uv run coursebuddy https://www.youtube.com/watch?v=VIDEO_ID

# Playlist
uv run coursebuddy https://www.youtube.com/playlist?list=PLAYLIST_ID

# Custom output directory
uv run coursebuddy URL --output ./my_transcripts
```

## Examples

```bash
# Stanford CS229 Machine Learning playlist
uv run coursebuddy "https://www.youtube.com/playlist?list=PLoROMvodv4rOY23Y0BoGoBGgQ1zmU_MT_"
```

## Output

- Single videos: `output/single_videos/{video_title}.md`
- Playlists: `output/{playlist_name}/{video_title}.md`

Each markdown file contains the video title as a heading followed by the plain transcript text.
