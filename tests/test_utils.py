import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
import tempfile
from src.utils import save_transcription_result, generate_summary_report


def test_save_transcription_result_creates_file():
    sample_data = {
        "filename": "example.mp3",
        "transcription": "Hello world",
        "confidence": 0.9,
        "needs_review": False,
        "timestamps": []
    }

    with tempfile.TemporaryDirectory() as temp_dir:
        save_transcription_result(sample_data, temp_dir)

        output_path = os.path.join(temp_dir, "example.json")
        assert os.path.exists(output_path)

        with open(output_path, "r", encoding="utf-8") as f:
            content = json.load(f)

        assert content["filename"] == "example.mp3"
        assert content["transcription"] == "Hello world"
        assert content["confidence"] == 0.9
        assert content["needs_review"] is False


def test_generate_summary_report_creates_summary_json():
    sample_results = [
        {"filename": "file1.mp3", "confidence": 0.85, "needs_review": False},
        {"filename": "file2.mp3", "confidence": 0.65, "needs_review": True},
    ]

    with tempfile.TemporaryDirectory() as temp_dir:
        generate_summary_report(sample_results, temp_dir)

        summary_path = os.path.join(temp_dir, "summary.json")
        assert os.path.exists(summary_path)

        with open(summary_path, "r", encoding="utf-8") as f:
            summary = json.load(f)

        assert summary["total_files"] == 2
        assert summary["average_confidence"] == 0.75
        assert "file2.mp3" in summary["low_confidence_files"]
        assert "generated_at" in summary