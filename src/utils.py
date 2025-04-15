import os
import json
from typing import Dict, Any, List
from datetime import datetime


def save_transcription_result(data: Dict[str, Any], output_dir: str = "results") -> str:
    """
    Saves the transcription result as a JSON file in the specified output folder.

    Args:
        data: Dictionary containing the transcription result.
        output_dir: Folder where the JSON file will be saved.

    Returns:
        The full path to the saved JSON file.
    """
    try:
        os.makedirs(output_dir, exist_ok=True)

        filename = data.get("filename", "output").split('.')[0] + ".json"
        output_path = os.path.join(output_dir, filename)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"✅ Transcription result saved at: {output_path}")
        return output_path

    except Exception as e:
        print(f"❌ Failed to save transcription result: {e}")
        raise


def generate_summary_report(results: List[Dict[str, Any]], output_dir: str = "results") -> None:
    """
    Generates a summary JSON file with insights like average confidence and files needing review.
    """
    try:
        total = len(results)
        if total == 0:
            return

        avg_conf = round(sum(r["confidence"] for r in results) / total, 2)
        flagged = [r["filename"] for r in results if r["needs_review"]]

        summary = {
            "total_files": total,
            "average_confidence": avg_conf,
            "low_confidence_files": flagged,
            "generated_at": datetime.now().isoformat()
        }

        summary_path = os.path.join(output_dir, "summary.json")
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=4)

        print(f"📊 Summary report saved at: {summary_path}")

    except Exception as e:
        print(f"❌ Failed to generate summary report: {e}")