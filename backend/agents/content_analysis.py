from agno.agent import Agent
from agno.models.groq import Groq
from backend.toon_util import structure_template_pydantic
from backend.models.model import ContentAnalysisResponse

_response_template = structure_template_pydantic(ContentAnalysisResponse)

content_analysis_agent=Agent(
    name="content_analysis_agent",
    model=Groq(id="llama-3.1-8b-instant"),
    description="""
        You are a content analysis agent that evaluates transcribed speech for structure, clarity, and filler words.
        You will return grammar corrections, identified filler words, and suggestions for content improvement.
    """,
    instructions=[
        "You will be provided with the transcribed spoken content in TOON format.",
        "Your task is to analyze the transcript and identify:",
        "- Grammar and syntax corrections.",
        "- Filler words and their frequency.",
        "- Suggestions for improving clarity and structure.",
        "Return your response ONLY in TOON format using the following template:",
        _response_template,
         "Rules:",
        "  • Do NOT include any text outside the TOON response.",
        "  • Do NOT wrap the output in JSON, markdown, or code fences.",
        "  • Use TOON tabular format for lists (grammar_corrections, suggestions).",
        "  • Use TOON key-value format for filler_words dict.",
    ],
    markdown=False,
    show_tool_calls=True,
    debug_mode=True
)