from typing import List, Dict, Any


def estimate_confidence(text: str, segments: List[Dict[str, Any]]) -> float:
    """
    Estimates transcription confidence using 3 heuristics:
    1. Word density (words per second)
    2. Penalty for short or empty segments
    3. Penalty for repeated words

    Returns a float between 0.0 and 1.0
    """

    if not segments or not text.strip():
        return 0.0

    words = text.strip().split()
    total_words = len(words)

    try:
        total_duration = sum(
            float(seg.get("end", 0)) - float(seg.get("start", 0))
            for seg in segments
            if isinstance(seg.get("start"), (int, float)) and isinstance(seg.get("end"), (int, float))
        )
    except Exception:
        return 0.0

    if total_duration <= 0 or total_words == 0:
        return 0.0

    # 1. Word density (higher = better)
    words_per_second = total_words / total_duration

    # 2. Penalty for short segments
    short_segments = [s for s in segments if len(s.get("text", "").strip()) < 5]
    short_penalty = len(short_segments) / len(segments)

    # 3. Penalty for word repetition
    unique_words = set(words)
    repetition_penalty = 1 - (len(unique_words) / total_words)

    # Final score: apply penalties
    confidence = words_per_second * (1 - short_penalty) * (1 - repetition_penalty)

    return round(max(0.0, min(confidence, 1.0)), 2)
