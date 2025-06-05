from fastapi import FastAPI, UploadFile, File
import whisper
import tempfile

app = FastAPI()

model = None  # lazy load 用に初期化だけしておく

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    global model
    if model is None:
        model = whisper.load_model("tiny")  # 最初のリクエスト時に読み込む

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    result = model.transcribe(
        tmp_path,
        language="ja"
    )

    return {"text": result["text"]}
