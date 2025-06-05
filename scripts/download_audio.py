import sys
import yt_dlp
import os

def download_audio(youtube_url, output_path):
    temp_base = os.path.splitext(output_path)[0]

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': temp_base + '.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    converted_path = temp_base + '.mp3'
    if os.path.exists(converted_path):
        os.rename(converted_path, output_path)
    else:
        raise Exception("MP3変換後のファイルが見つかりませんでした")

if __name__ == "__main__":
    youtube_url = sys.argv[1]
    output_path = sys.argv[2]
    download_audio(youtube_url, output_path)
