from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import whisper
import tempfile
import subprocess

app = FastAPI()

model = None  # lazy load

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    global model
    if model is None:
        model = whisper.load_model("tiny")  # 必要なら "base", "small" などに変更

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    result = model.transcribe(
        tmp_path,
        language="ja"
    )

    return {"text": result["text"]}


@app.post("/transcribe_url")
async def transcribe_url(url: str = Form(...)):
    global model
    if model is None:
        model = whisper.load_model("tiny")

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_mp3:
        mp3_path = tmp_mp3.name

    subprocess.run(["python3", "scripts/download_audio.py", url, mp3_path], check=True)

    # MP3 → WAVに変換
    wav_path = mp3_path.replace(".mp3", ".wav")
    subprocess.run([
        "ffmpeg", "-y", "-i", mp3_path,
        "-ar", "16000", "-ac", "1", "-f", "wav", wav_path
    ], check=True)

    # Whisperで文字起こし
    result = model.transcribe(wav_path, language="ja")

    return JSONResponse(content={"text": result["text"]})
