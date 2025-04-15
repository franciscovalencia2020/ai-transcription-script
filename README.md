# 🧠 AI Transcription Script

This project is a Python-based transcription pipeline using OpenAI Whisper.  
It transcribes audio files, estimates transcription confidence, and flags files that may require manual review.

## ⚙️ Features

- 🔊 Transcribes `.mp3` and `.wav` files using OpenAI Whisper.
- 📊 Calculates transcription confidence using smart heuristics.
- 🚩 Flags low-confidence results for manual review.
- 🧾 Saves output as structured JSON.
- ⏱️ Includes timestamped transcription segments.
- 🖥️ Command-line interface (CLI) for batch processing.
- 🪵 Logs progress and errors to a log file.
- ⚙️ Confidence threshold is configurable via `.env` file.
- 🧪 Automated unit tests with `pytest`.
- 🧵 Parallel processing for multiple audio files.
- 🐳 Dockerfile + Docker Compose ready.
- 📈 Generates summary report after transcription.
- 📦 Modular `/src` package structure for scalability.

## 📁 Project Structure

```text
ai-transcription-script/
├── audio_files/           # Input files (.mp3/.wav)
├── results/               # JSON output files
├── logs/                  # Transcription log file
├── src/                   # Project source code
│   ├── __main__.py        # Entry point for CLI (python -m src)
│   ├── main.py            # CLI logic
│   ├── transcriber.py     # Whisper integration
│   ├── confidence.py      # Confidence logic
│   ├── utils.py           # File I/O and summary report
│   └── logger.py          # Logging setup
├── tests/                 # Unit tests
├── .env                   # Confidence threshold config
├── requirements.txt       # Project dependencies
├── Dockerfile             # Docker image config
├── docker-compose.yml     # Run app easily with Docker
└── README.md              # This file
```

## 🚀 Setup Instructions

### 1. Clone the repo (or unzip)
```bash
git clone https://github.com/franciscovalencia2020/ai-transcription-script.git
cd ai-transcription-script
```

### 2. Create a virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Install ffmpeg (required by Whisper)
```bash
Download FFmpeg from https://ffmpeg.org
Add the bin folder to your system PATH.
```

### 5. Create a `.env` file (optional)
```env
CONFIDENCE_THRESHOLD=0.7
```

## 🖥️ CLI Usage

- ### Basic usage (uses `base` model by default — no need to specify model):
```bash
python -m src --input audio_files
```

- ### Custom output folder:
```bash
python -m src --input audio_files --output my_output_folder
```

- ### View help and all available options:
```bash
python -m src --help
```

> 🔒 Note: This script uses only the `base` Whisper model by default for maximum compatibility and reliability.

## 🧪 Running Tests

### 🔹 Run all tests
```bash
pytest tests/ -v
```

## 🧠 Confidence Estimation Heuristics

The following strategies are used to estimate confidence:

 - 1. **Word density**: Words per second of audio.
 - 2. **Segment quality**: Penalty for short or empty segments.
 - 3. **Repetition penalty**: Penalizes repeated words.

Final confidence is a score between `0.0` and `1.0`.  
Files below the threshold defined in `.env` (e.g., `0.7`) are flagged for review.

## 📎 Sample Output (.json)

```json
{
  "filename": "test.wav",
  "transcription": "Hello, this is a test audio.",
  "confidence": 0.92,
  "needs_review": false,
  "timestamps": [
    { "start": 0.0, "end": 2.3, "text": "Hello," },
    { "start": 2.4, "end": 4.7, "text": "this is a test audio." }
  ]
}
```

## 📈 Summary Report Example (summary.json)

```json
{
  "total_files": 5,
  "average_confidence": 0.81,
  "low_confidence_files": ["file2.mp3", "file5.mp3"],
  "generated_at": "2025-04-14T18:37:00"
}
```

## 📚 Dependencies

- `openai-whisper`
- `python-dotenv`
- `pytest`
- `ffmpeg (external)`

See `requirements.txt` for full list.

## 🐳 Docker Usage

- ### Build and run
```bash
docker-compose up --build
```

- ### Run tests inside Docker
```bash
docker-compose run whisper pytest tests/
```

## ✅ Final Notes

- Designed for CPU use; GPU-compatible with `torch` if available.
- Fully CLI-driven and scalable.
- Clean modular code structure with test coverage and logging.
- Easy to configure and run locally or in Docker.
