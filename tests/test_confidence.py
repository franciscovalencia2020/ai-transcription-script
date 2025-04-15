import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.confidence import estimate_confidence


def test_confidence_high_score():
    text = "Hello world this is a test of the transcription script"
    segments = [{"start": 0.0, "end": 4.0, "text": text}]
    assert estimate_confidence(text, segments) > 0.8


def test_confidence_low_score_empty_segments():
    text = ""
    segments = []
    assert estimate_confidence(text, segments) == 0.0


def test_confidence_zero_duration():
    text = "Some words"
    segments = [{"start": 0.0, "end": 0.0, "text": text}]
    assert estimate_confidence(text, segments) == 0.0


def test_confidence_with_repetition_penalty():
    text = "hello hello hello hello"
    segments = [{"start": 0.0, "end": 4.0, "text": text}]
    score = estimate_confidence(text, segments)
    assert 0.0 < score < 0.5