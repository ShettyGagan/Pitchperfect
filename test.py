from agno.team import Team
from agno.models.google import Gemini
from backend.agents.content_analysis import content_analysis_agent
from backend.agents.feedback_agent import feedback_agent

from backend.models.model import CoordinatorResponse


#team of agents
final_agent=Team(
    name="coordinator_agent",
    model=Gemini(id="gemini-2.5-flash"),
    mode="coordinate",
    members=[content_analysis_agent,feedback_agent],
    description="You are a public speaking coach who helps individuals improve their presentation skills through feedback and analysis.",
    instructions=[
        "You will be provided with pre-computed facial expression analysis results and voice analysis results, along with the video context.",
        "The facial expression results and voice analysis results are already computed and provided to you directly in the prompt. Do NOT try to re-analyze them.",
        "Ask the content analysis agent to analyze the transcript (from the voice analysis results) for structure, clarity, and filler words.",
        "Ask the feedback agent to evaluate the analysis results from the facial expression data, voice analysis data, and content analysis agent to provide feedback on the overall effectiveness of the presentation, highlighting strengths and areas for improvement.",
        "Your response MUST include the exact pre-computed facial expression and voice analysis results, along with responses from the content analysis agent and feedback agent.",
        "Additionally, your response MUST provide lists of the speaker's strengths, weaknesses, and suggestions for improvement based on all the responses and feedback provided by the feedback agent.",
        "Important: You MUST directly address the speaker while providing strengths, weaknesses, and suggestions for improvement in a clear and constructive manner.",
        "The response MUST be in the following strict JSON format:",
        "{",
            '"facial_expression_response": [facial_expression_data],',
            '"voice_analysis_response": [voice_analysis_data],',
            '"content_analysis_response": [content_analysis_agent_response],',
            '"feedback_response": [feedback_agent_response]',
            '"strengths": [speaker_strengths_list],',
            '"weaknesses": [speaker_weaknesses_list],',
            '"suggestions": [suggestions_for_improvement_list]',
        "}",
        "The response MUST be in strict JSON format with keys and values in double quotes.",
        "The values in the JSON response MUST NOT be null or empty.",
        "The final response MUST not include any other text or anything else other than the JSON response.",
        "The final response MUST not include any backslashes in the JSON response.",
        "The final response MUST be a valid JSON object and MUST not have any unterminated strings in the JSON response."
    ],
    add_datetime_to_instructions=True,
    add_member_tools_to_system_message=False,
    enable_agentic_context=True,
    share_member_interactions=True,
    show_members_responses=True,
    response_model=CoordinatorResponse,
    use_json_mode=True,
    markdown=True,
    show_tool_calls=True,
    debug_mode=True

)




import json
import pathlib
from fastapi import FastAPI, UploadFile,File
import os
import shutil
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from agno.agent import RunResponse
from backend.agents.teamup_agents import final_agent
from backend.tools.facial_expression import analyze_facial_expression
from backend.tools.voice_analysis import analyse_voice_attributes
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalysisRequest(BaseModel):
    video_url: str


@app.post("/upload")
async def upload_file(file:UploadFile=File(...)):
    upload_dir="video_uploads"
    os.makedirs(upload_dir,exist_ok=True)

    file_path=os.path.join(upload_dir,file.filename)
    with open(file_path,"wb") as f:
        shutil.copyfileobj(file.file,f)

    return {"file_path":str(pathlib.Path(file_path).resolve())}

@app.post("/analyze")
async def analyze(request: AnalysisRequest):
    video_path = pathlib.Path(request.video_url)

    if not video_path.exists():
        return JSONResponse(
            status_code=404,
            content={"error": f"File not found at the specified path: {video_path}"}
        )

    video_posix = video_path.as_posix()

    # Call tools directly instead of going through agents (faster, no LLM overhead)
    facial_expression_result = analyze_facial_expression(video_posix)
    voice_analysis_result = analyse_voice_attributes(video_posix)

    prompt = (
        f"Here are the pre-computed analysis results for the video: {video_posix}\n\n"
        f"Facial Expression Analysis Results:\n{facial_expression_result}\n\n"
        f"Voice Analysis Results:\n{voice_analysis_result}\n\n"
        "Use these results directly. Ask the content analysis agent to analyze the transcript from the voice analysis results. "
        "Then ask the feedback agent to evaluate all the data and provide scoring and feedback."
    )

    response:RunResponse=final_agent.run(prompt)
    json_compatible_response = jsonable_encoder(response.content)
    return JSONResponse(content=json_compatible_response)




