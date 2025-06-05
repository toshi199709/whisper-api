# 軽量なベースイメージ
FROM python:3.10-slim

# ffmpeg（Whisper用）と依存ライブラリのインストール
RUN apt-get update && apt-get install -y ffmpeg libsndfile1 && \
  apt-get clean && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリを設定
WORKDIR /app

# 先に依存ファイルをコピーしてキャッシュ効かせる
COPY requirements.txt .

# ライブラリをインストール
RUN pip install --no-cache-dir --upgrade pip && \
  pip install --no-cache-dir -r requirements.txt

# アプリ本体をコピー
COPY . .

# FastAPIアプリを起動
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
