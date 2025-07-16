from agno.agent import Agent
from agno.models.google import Gemini

content_analysis_agent=Agent(
    name="content_analysis_agent",
    model=Gemini(id="gemini-2.5-pro"),
    description="""
        You are a content analysis agent that evaluates transcribed speech for structure, clarity, and filler words.
        You will return grammar corrections, identified filler words, and suggestions for content improvement.
    """,
    instructions=[
        "You will be provided with a transcript of spoken content.",
        "Your task is to analyze the transcript and identify:",
        "- Grammar and syntax corrections.",
        "- Filler words and their frequency.",
        "- Suggestions for improving clarity and structure.",
        "The response MUST be in the following JSON format:",
        "{",
            '"grammar_corrections": [list of corrections],',
            '"filler_words": { "word": count, ... },',
            '"suggestions": [list of suggestions]',
        "}",
        "Ensure the response is in proper JSON format with keys and values in double quotes.",
        "Do not include any additional text outside the JSON response."
    ],
    markdown=True,
    show_tool_calls=True,
    debug_mode=True
)