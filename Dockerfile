FROM python:3.12-slim

RUN apt-get update && apt-get install -y ffmpeg git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt

RUN mkdir -p results logs

CMD ["python", "-m", "src", "--input", "audio_files", "--output", "results"]
