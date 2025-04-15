import argparse
import os
import warnings
import whisper
from typing import NoReturn
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing
from dotenv import load_dotenv

from src.logger import setup_logger
from src.transcriber import transcribe_audio
from src.confidence import estimate_confidence
from src.utils import save_transcription_result, generate_summary_report

load_dotenv()
warnings.filterwarnings("ignore", category=UserWarning)
logger = setup_logger()

CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.7"))


def process_single_file(audio_path: str, output_folder: str) -> dict:
    filename = os.path.basename(audio_path)
    try:
        model = whisper.load_model("base")
        result = transcribe_audio(audio_path, model)
    except Exception as e:
        logger.error(f"❌ Failed to transcribe '{filename}': {e}")
        return None

    try:
        confidence = estimate_confidence(result["transcription"], result["segments"])
    except Exception as e:
        logger.error(f"❌ Confidence estimation failed for '{filename}': {e}")
        confidence = 0.0

    logger.info(f"📄 File: {filename}")
    logger.info(f"📝 Transcription: {result['transcription']}")
    logger.info(f"📊 Confidence: {confidence}")

    result_data = {
        "filename": filename,
        "transcription": result["transcription"],
        "confidence": confidence,
        "needs_review": confidence < CONFIDENCE_THRESHOLD,
        "timestamps": result["timestamps"]
    }

    try:
        save_transcription_result(result_data, output_folder)
    except Exception as e:
        logger.error(f"❌ Failed to save JSON for '{filename}': {e}")

    return result_data


def process_audio_files_parallel(input_folder: str, output_folder: str) -> NoReturn:
    if not os.path.exists(input_folder):
        logger.error(f"❌ Input folder not found: {input_folder}")
        return

    os.makedirs(output_folder, exist_ok=True)

    audio_files = [
        os.path.join(input_folder, f)
        for f in os.listdir(input_folder)
        if f.lower().endswith((".mp3", ".wav"))
    ]

    if not audio_files:
        logger.warning(f"⚠️ No audio files found in: {input_folder}")
        return

    max_workers = min(len(audio_files), multiprocessing.cpu_count())
    logger.info(f"🔧 Starting parallel processing with {max_workers} workers...")

    results = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(process_single_file, path, output_folder)
            for path in audio_files
        ]
        for future in as_completed(futures):
            try:
                result = future.result()
                if result:
                    results.append(result)
            except Exception as e:
                logger.error(f"❌ Error in parallel worker: {e}")

    generate_summary_report(results, output_folder)


def run_cli():
    parser = argparse.ArgumentParser(
        description="🎧 AI Transcription Pipeline using OpenAI Whisper (base model only)"
    )
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Path to the folder containing audio files (.mp3 or .wav)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="results",
        help="Directory where the transcription JSON files will be saved (default: results/)"
    )

    args = parser.parse_args()
    process_audio_files_parallel(args.input, args.output)


if __name__ == "__main__":
    run_cli()
