from agno.agent import Agent,RunResponse
from agno.models.groq import Groq
from backend.tools.voice_analysis import analyse_voice_attributes as voice_analyser_tool
from agno.utils.pprint import pprint_run_response
from backend.models.model import VoiceAnalysisResponse
from backend.toon_util import structure_template_pydantic

_response_template = structure_template_pydantic(VoiceAnalysisResponse)




voice_analyser_agent= Agent(
    name="voice_analysis_agent",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[voice_analyser_tool],
    description="""
        You are a voice analysis agent that evaluates vocal attributes like clarity, intonation, and pace.
        You will return the transcribed text, speech rate, pitch variation, and volume consistency.
    """,
    instructions=[
         # ── Input 
        "You will be provided with an audio or video file path.",
        "Use the voice analyser tool to extract audio attributes from the file.",
 
        # ── Task 
        "Transcribe the spoken content fully.",
        "Measure speech rate in words per minute (wpm).",
        "Assess pitch variation: low | medium | high.",
        "Assess volume consistency: consistent | moderate | inconsistent.",
        "Return your response ONLY in TOON format using the following template:",
        _response_template,
        "",
        "Rules:",
        "  • Do NOT include any text outside the TOON response.",
        "  • Do NOT wrap the output in JSON, markdown, or code fences.",
        "  • transcription value must be the complete verbatim text.",
    ],
    markdown=False,
    show_tool_calls=True,
    debug_mode=True
)