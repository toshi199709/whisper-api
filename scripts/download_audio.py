import sys
import yt_dlp
import os

def download_audio(youtube_url, output_path):
    temp_base = os.path.splitext(output_path)[0]

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': temp_base + '.%(ext)s',
        'cookiefile': '/app/scripts/youtube_cookies.txt',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'prefer_ffmpeg': True,
        'quiet': True,
        'noplaylist': True
    }

    # ✅ クッキーファイルの存在確認
    if not os.path.exists(ydl_opts["cookiefile"]):
        raise FileNotFoundError("指定されたクッキーファイルが存在しません: " + ydl_opts["cookiefile"])
    else:
        print("✅ クッキーファイルを検出:", ydl_opts["cookiefile"])

    # 🍪 クッキーの先頭5行を表示（安全な範囲）
    with open(ydl_opts["cookiefile"], "r") as f:
        lines = f.readlines()
        print("🍪 クッキーの先頭5行:")
        for line in lines[:5]:
            print(line.strip())

    # 🎬 対象URLを表示
    print("🎬 ダウンロード対象のURL:", youtube_url)

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
