from fastapi import FastAPI, UploadFile, File
import whisper
import tempfile

app = FastAPI()

# Whisperモデルの読み込み（baseを使用）
model = whisper.load_model("tiny")

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    # 一時ファイルとして保存
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    # 音声ファイルから文字起こし
    result = model.transcribe(
        tmp_path,
        language="ja"
    )

    return {"text": result["text"]}
