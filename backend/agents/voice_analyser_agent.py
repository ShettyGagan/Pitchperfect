from agno.agent import Agent,RunResponse
from agno.models.google import Gemini
from backend.tools.voice_analysis import analyse_voice_attributes as voice_analyser_tool
from agno.utils.pprint import pprint_run_response

voice_analyser_agent= Agent(
    name="voice_analysis_agent",
    model=Gemini(id="gemini-2.5-pro"),
    tools=[voice_analyser_tool],
    description="""
        You are a voice analysis agent that evaluates vocal attributes like clarity, intonation, and pace.
        You will return the transcribed text, speech rate, pitch variation, and volume consistency.
    """,
    instructions=[
        "You will be provided with an audio file of a person speaking.",
        "Your task is to analyze the vocal attributes in the audio to detect speech rate, pitch variation, and volume consistency.",
        "The response MUST be in the following JSON format:",
        "{",
            '"transcription": [transcription]',
            '"speech_rate_wpm": [speech_rate_wpm],',
            '"pitch_variation": [pitch_variation],',
            '"volume_consistency": [volume_consistency]',
        "}",
        "The response MUST be in proper JSON format with keys and values in double quotes.",
        "The final response MUST not include any other text or anything else other than the JSON response."
    ],
    markdown=True,
    show_tool_calls=True,
    debug_mode=True
)