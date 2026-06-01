
import os
import json
import tempfile

import numpy as np
import librosa
from moviepy import VideoFileClip
from faster_whisper import WhisperModel
from agno.tools import tool

from backend.toon_util import to_toon


# ---------------------------------------------------------------------------
# Internal helpers — not exposed as agno tools
# ---------------------------------------------------------------------------

def _extract_audio_from_video(video_path: str, output_path: str) -> str:
    """Extract audio track from a video file and write it to output_path."""
    video = VideoFileClip(video_path)
    audio_clip = video.audio
    audio_clip.write_audiofile(output_path, logger=None)
    audio_clip.close()
    video.close()
    return output_path


def _load_whisper() -> WhisperModel | None:
    try:
        return WhisperModel("small", device="cpu", compute_type="int8")
    except Exception as e:
        print(f"Error loading Whisper model: {e}")
        return None


def _transcribe(audio_path: str) -> str:
    model = _load_whisper()
    if not model:
        return "Model failed to load."
    try:
        segments, _ = model.transcribe(audio_path)
        text = " ".join(seg.text for seg in segments).strip()
        return text or "Could not understand the audio."
    except Exception as e:
        print(f"Transcription error: {e}")
        return "Transcription failed."


# ---------------------------------------------------------------------------
# Hooks
# ---------------------------------------------------------------------------

def log_before_call(fc):
    print(f"About to call function with arguments: {fc.arguments}")


def log_after_call(fc):
    print(f"Function call completed with result: {fc.result}")


# ---------------------------------------------------------------------------
# Tool
# ---------------------------------------------------------------------------

@tool(
    name="voice_analyzer",
    description="Analyses vocal attributes (clarity, intonation, pace) from a video or audio file.",
    show_result=True,
    stop_after_tool_call=True,
    pre_hook=log_before_call,
    post_hook=log_after_call,
    cache_results=False,
    cache_dir="/tmp/agno_cache",
    cache_ttl=3600,
)
def analyse_voice_attributes(file_path: str) -> str:
    """
    Analyse voice attributes from a video or audio file.
    Returns a TOON-encoded string (not JSON) so the agent receives
    compact, low-token structured data.
    """
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    tmp_audio_path = None

    # ── Extract audio if input is video ─────────────────────────────────────
    if ext in (".mp4", ".mov", ".avi", ".mkv", ".webm"):
        tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        tmp.close()
        tmp_audio_path = tmp.name
        audio_path = _extract_audio_from_video(file_path, tmp_audio_path)
    else:
        audio_path = file_path

    try:
        # ── Transcription ────────────────────────────────────────────────────
        transcription = _transcribe(audio_path)
        words = transcription.split()

        # ── Load audio for signal analysis ───────────────────────────────────
        y, sr = librosa.load(audio_path, sr=16000)
        duration = librosa.get_duration(y=y, sr=sr)

        # ── Speech rate ──────────────────────────────────────────────────────
        speech_rate_wpm = round(len(words) / max(duration / 60.0, 1e-6), 2)

        # ── Pitch variation ──────────────────────────────────────────────────
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch_values = pitches[magnitudes > np.median(magnitudes)]
        pitch_variation = round(float(np.std(pitch_values)) if pitch_values.size > 0 else 0.0, 2)

        # ── Volume consistency ───────────────────────────────────────────────
        rms = librosa.feature.rms(y=y)[0]
        volume_consistency = round(float(np.std(rms)), 4)

    finally:
        # Always clean up the temporary audio file
        if tmp_audio_path and os.path.exists(tmp_audio_path):
            os.remove(tmp_audio_path)

    result = {
        "transcription": transcription,
        "speech_rate_wpm": str(speech_rate_wpm),
        "pitch_variation": str(pitch_variation),
        "volume_consistency": str(volume_consistency),
    }

    # Return TOON instead of JSON — agents get compact structured data
    return to_toon(result)
