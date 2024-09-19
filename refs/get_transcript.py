import subprocess
import json
import os
import re
import textwrap
from urllib.parse import urlparse, parse_qs

def slugify(text):
    # Remove non-word characters (everything except numbers and letters)
    text = re.sub(r'[^\w\s-]', '', text.lower())
    # Replace all runs of whitespace with a single dash
    return re.sub(r'[-\s]+', '-', text).strip('-')

def get_video_id(url):
    # Extract video ID from YouTube URL
    parsed_url = urlparse(url)
    if parsed_url.netloc == 'youtu.be':
        return parsed_url.path[1:]
    if parsed_url.netloc in ('www.youtube.com', 'youtube.com'):
        if parsed_url.path == '/watch':
            p = parse_qs(parsed_url.query)
            return p['v'][0]
    return None

def run_yt_command(url):
    # Run the yt command and capture its output
    result = subprocess.run(['yt', url], capture_output=True, text=True)
    return result.stdout

def parse_yt_output(output):
    # Parse the JSON output
    try:
        data = json.loads(output)
        return data
    except json.JSONDecodeError:
        print("Error: Unable to parse JSON output from yt command")
        return None

def save_json_file(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def save_formatted_transcript(transcript, file_path):
    wrapped_transcript = textwrap.fill(transcript, width=80)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(wrapped_transcript)

def main(url):
    # Get video ID
    video_id = get_video_id(url)
    if not video_id:
        print("Invalid YouTube URL")
        return

    # Run yt command
    output = run_yt_command(url)
    
    # Parse the output
    data = parse_yt_output(output)
    if not data:
        return
    
    # Slugify the title
    title = data.get('metadata', {}).get('title', video_id)
    folder_name = slugify(title)
    
    # Create folder if it doesn't exist
    os.makedirs(folder_name, exist_ok=True)
    
    # Save metadata
    metadata_path = os.path.join(folder_name, f"{video_id}_metadata.json")
    save_json_file(data.get('metadata', {}), metadata_path)
    print(f"Metadata written to {metadata_path}")

    # Save transcript as JSON
    transcript_json_path = os.path.join(folder_name, f"{video_id}_transcript.json")
    save_json_file({'transcript': data.get('transcript', '')}, transcript_json_path)
    print(f"Transcript (JSON) written to {transcript_json_path}")

    # Save transcript as formatted TXT
    transcript_txt_path = os.path.join(folder_name, f"{video_id}_transcript.txt")
    save_formatted_transcript(data.get('transcript', ''), transcript_txt_path)
    print(f"Transcript (TXT) written to {transcript_txt_path}")

    # Save comments
    comments_path = os.path.join(folder_name, f"{video_id}_comments.json")
    save_json_file({'comments': data.get('comments', [])}, comments_path)
    print(f"Comments written to {comments_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script.py <YouTube URL>")
    else:
        main(sys.argv[1])
