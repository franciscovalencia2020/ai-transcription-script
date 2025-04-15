import sys
import os
import pytest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.transcriber import transcribe_audio

mock_model = MagicMock()
mock_model.transcribe.return_value = {
    "text": "Hello world",
    "segments": [
        {"start": 0.0, "end": 1.0, "text": "Hello"},
        {"start": 1.0, "end": 2.0, "text": "world"},
    ]
}


@patch("src.transcriber.whisper")
def test_transcribe_audio_success(mock_whisper):
    mock_whisper.load_model.return_value = mock_model

    fake_audio_path = "tests/fake_audio.mp3"
    with open(fake_audio_path, "w") as f:
        f.write("dummy")

    result = transcribe_audio(fake_audio_path, model=mock_model)

    assert result["filename"] == "fake_audio.mp3"
    assert result["transcription"] == "Hello world"
    assert len(result["segments"]) == 2
    assert result["timestamps"][0]["start"] == 0.0

    os.remove(fake_audio_path)


def test_transcribe_audio_file_not_found():
    with pytest.raises(FileNotFoundError):
        transcribe_audio("nonexistent.mp3", model=mock_model)
