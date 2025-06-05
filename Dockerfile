# ベースイメージ（Python 3.10）
FROM python:3.10

# ffmpeg をインストール（Whisper用）
RUN apt-get update && apt-get install -y ffmpeg

# 作業ディレクトリを設定
WORKDIR /app

# アプリの全ファイルをコピー
COPY . /app

# ライブラリをインストール
RUN pip install --upgrade pip && \
  pip install -r requirements.txt

# FastAPIアプリを起動
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
