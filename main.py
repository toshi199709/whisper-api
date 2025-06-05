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

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        audio_path = tmp.name

    subprocess.run(["python3", "scripts/download_audio.py", url, audio_path])

    result = model.transcribe(audio_path, language="ja")
    return JSONResponse(content={"text": result["text"]})
