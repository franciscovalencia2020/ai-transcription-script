import os
from typing import List, Dict, Any
import whisper


def transcribe_audio(file_path: str, model: whisper.Whisper) -> Dict[str, Any]:
    """
    Transcribes an audio file using a preloaded Whisper model.

    Args:
        file_path: Path to the audio file (.mp3 or .wav)
        model: A loaded Whisper model instance

    Returns:
        Dictionary with:
        - filename
        - transcription
        - segments
        - timestamps
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"❌ File not found: {file_path}")

    if not file_path.lower().endswith((".mp3", ".wav")):
        raise ValueError(f"❌ Unsupported audio format: {file_path}")

    print(f"🔊 Transcribing file: {file_path}")

    try:
        result = model.transcribe(file_path, verbose=False)
    except Exception as e:
        raise ValueError(f"❌ Transcription failed for '{file_path}': {e}")

    segments = result.get("segments", [])
    transcription = result.get("text", "").strip()

    timestamps: List[Dict[str, Any]] = [
        {
            "start": round(seg["start"], 2),
            "end": round(seg["end"], 2),
            "text": seg.get("text", "").strip()
        }
        for seg in segments
        if seg.get("text", "").strip()
    ]

    return {
        "filename": os.path.basename(file_path),
        "transcription": transcription,
        "segments": segments,
        "timestamps": timestamps
    }
