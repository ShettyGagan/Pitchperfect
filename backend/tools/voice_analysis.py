# import os
# import json
# import numpy as np
# import librosa
# import tempfile
# from moviepy import VideoFileClip
# from faster_whisper import WhisperModel
# from agno.tools import tool
# from dotenv import load_dotenv

# def extract_audio_from_video(video_path:str,output_path:str)->str:
#     video=VideoFileClip(video_path)
#     audio_clip=video.audio
#     audio_clip.write_audiofile(output_path)
#     audio_clip.close()
#     video.close()
#     return output_path

# def whisper_model():
#     try:
#         model=WhisperModel("small",device="cpu",compute_type="int8")
#         return model
#     except Exception as e:
#         print(f"Error loading Whisper model: {e}")
#         return None
    
# def transcribe_audio(audio_file):
#     model=whisper_model()
#     if not model:
#         return "Model failed to load. Please check system resources or model path."
#     try:
#         segments,_=model.transcribe(audio_file)
#         full_text=" ".join(segment.text for segment in segments)
#         return full_text.strip() if full_text else "I couldn't understand the audio. Please try again."
#     except Exception as e:
#         print(f"Error transcribing audio with faster-whisper: {e}")
#         return "I'm having trouble transcribing your audio. Please try again or speak more clearly."
    
# def log_before_call(fc):
#     """Pre-hook function that runs before the tool execution"""
#     print(f"About to call function with arguments: {fc.arguments}")

# def log_after_call(fc):
#     """Post-hook function that runs after the tool execution"""
#     print(f"Function call completed with result: {fc.result}")

# # @tool(
# #     name="voice_analyzer",
# #     description="Analyzes vocal attributes like clarity, intonation, and pace.",
# #     show_result=True,
# #     stop_after_tool_call=True,
# #     pre_hook=log_before_call,
# #     post_hook=log_after_call,
# #     cache_results=False,
# #     cache_dir="/tmp/agno_cache",
# #     cache_ttl=3600
# # )

# def analyse_voice_attributes(file_path:str)->dict:
#     _, ext = os.path.splitext(file_path)
#     ext = ext.lower()

#     #if file is video extract audio
#     if ext in ['.mp4']:
#         with tempfile.NamedTemporaryFile(suffix='.mp3',delete=False)as temp_audio_file:
#             audio_path=extract_audio_from_video(file_path,temp_audio_file.name)
#     else:
#         audio_path=file_path

#     #transcribe 
#     transcription=transcribe_audio(audio_path)
#     words=transcription.split()

#     #load audio
#     y,sr=librosa.load(audio_path,sr=16000)

#     #calculate speech rate
#     duration=librosa.get_duration(y=y,sr=sr)
#     speech_rate=len(words)/(duration/60.0)

#     #pitch variation
#     pitches,magnitudes=librosa.piptrack(y=y,sr=sr)
#     pitch_values = pitches[magnitudes > np.median(magnitudes)]
#     pitch_variation = np.std(pitch_values) if pitch_values.size > 0 else 0

#     # Volume consistency
#     rms = librosa.feature.rms(y=y)[0]
#     volume_consistency = np.std(rms)

#     # Clean up temporary audio file if created
#     if ext in ['.mp4']:
#         os.remove(audio_path)

#     return json.dumps({
#         "transcription":transcription,
#         "speech_rate_wpm":str(round(speech_rate, 2)),
#         "pitch_variation":str(round(pitch_variation,2)),
#         "volume_consistency": str(round(volume_consistency, 4))
#     })

# # result=analyse_voice_attributes("C:/Users/Gagan Shetty/Documents/Speech_Trainer/backend/harvard.wav")
# # print(result)


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
