from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import whisper
import os
import subprocess
import uuid

app = FastAPI()
model = whisper.load_model("base")  # small や medium でもOK

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    # 一時ファイル名をユニークにする
    unique_id = str(uuid.uuid4())
    input_path = f"temp_{unique_id}.webm"
    mp3_path = f"temp_{unique_id}.mp3"

    # アップロードされた音声を保存
    with open(input_path, "wb") as f:
        f.write(await file.read())

    # ffmpeg で webm → mp3 に変換
    try:
        subprocess.run(["ffmpeg", "-y", "-i", input_path, mp3_path], check=True)

        # Whisper で文字起こし
        result = model.transcribe(mp3_path, language="ja")

        # クリーンアップ
        os.remove(input_path)
        os.remove(mp3_path)

        return JSONResponse(content={"text": result["text"]})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
