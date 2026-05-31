from agno.agent import Agent,RunResponse
from agno.models.groq import Groq
from backend.tools.facial_expression import analyze_facial_expression as facial_expression_tool
from agno.utils.pprint import pprint_run_response
from backend.toon_util import structure_template_pydantic
from backend.models.model import FacialExpressionResponse
from dotenv import load_dotenv
import os

load_dotenv()

_response_template = structure_template_pydantic(FacialExpressionResponse)
#facial expression agent

facial_expression_agent = Agent(
    name="facial_expression_agent",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[facial_expression_tool],
    description=
    '''
        You are a facial expression agent that will analyze facial expressions in videos to detect emotions and engagement.
        You will return the emotion timeline and engagement metrics.
    ''',
    instructions=[
        "You will be provided with a video file of a person speaking in a public setting.",
        "Your task is to analyze the facial expressions in the video to detect emotions and engagement.",
        "You will analyze the video frame by frame to detect and classify facial expressions such as happiness, sadness, anger, surprise, and neutrality.",
        "You will also analyze the engagement metrics such as eye contact count and smile count",
        "Return your response ONLY in TOON format using the following template:",
        _response_template,
        "",
        "Rules:",
        "  • Do NOT include any text outside the TOON response.",
        "  • Do NOT wrap the output in JSON, markdown, or code fences.",
        "  • Do NOT include backslashes in the response.",
        "  • emotion_timeline must be a TOON tabular array with columns: timestamp, emotion.",
        "  • engagement_metrics must be TOON key-value pairs.",
    ],
    markdown=False,
    show_tool_calls=True,
    debug_mode=True
)

# video="C:/Users/Gagan Shetty\Documents/Speech_Trainer/backend/3249935-uhd_3840_2160_25fps.mp4"
# prompt = f"Analyze facial expressions in the video file to detect emotions and engagement in the following video: {video}"
# facial_expression_agent.print_response(prompt, stream=True)

# # Run agent and return the response as a variable
# response: RunResponse = facial_expression_agent.run(prompt)
# # Print the response in markdown format
# pprint_run_response(response, markdown=True)