from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import whisper
import os
import subprocess
import uuid

app = FastAPI()

# ✅ CORS設定：Railsローカルからのアクセス許可
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ ルートエンドポイント（Renderのヘルスチェック用）
@app.get("/")
async def root():
    return {"message": "Whisper API is running"}

# ✅ Whisperモデルの読み込み（tiny使用）
model = whisper.load_model("tiny")

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    unique_id = str(uuid.uuid4())
    input_path = f"temp_{unique_id}.webm"
    mp3_path = f"temp_{unique_id}.mp3"

    try:
        # アップロードされた音声ファイルを保存
        with open(input_path, "wb") as f:
            f.write(await file.read())

        # webm → mp3 へ変換
        subprocess.run(["ffmpeg", "-y", "-i", input_path, mp3_path], check=True)

        # Whisperで文字起こし
        result = model.transcribe(mp3_path, language="ja")

        return JSONResponse(content={"text": result["text"]})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

    finally:
        # 一時ファイルを削除
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(mp3_path):
            os.remove(mp3_path)
