from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import whisper
import os
import subprocess
import uuid

app = FastAPI()

# ✅ CORS設定：ローカル開発や本番からのアクセスを許可
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ← 本番でのCORSを許すために "*"（必要ならドメインを限定）
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Renderヘルスチェック対応
@app.get("/")
async def root():
    return {"message": "Whisper API is running"}

# ✅ Whisperモデルをグローバルに1度だけロード
model = whisper.load_model("tiny")

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    # 一時ファイル名生成
    uid = str(uuid.uuid4())
    input_path = f"temp_{uid}.webm"
    mp3_path = f"temp_{uid}.mp3"

    try:
        # アップロードされたファイル保存
        with open(input_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # webm → mp3 変換（Render上のffmpegは基本OK）
        subprocess.run([
            "ffmpeg", "-i", input_path, "-ar", "16000", "-ac", "1", "-acodec", "libmp3lame", mp3_path, "-y"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        # whisperで文字起こし
        result = model.transcribe(mp3_path, language="ja")

        return JSONResponse(content={"text": result["text"]})

    except subprocess.CalledProcessError as e:
        return JSONResponse(content={"error": f"ffmpeg変換エラー: {str(e)}"}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"error": f"内部エラー: {str(e)}"}, status_code=500)

    finally:
        # ファイルクリーンアップ
        for path in [input_path, mp3_path]:
            if os.path.exists(path):
                os.remove(path)
