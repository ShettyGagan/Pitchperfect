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

    prompt = f"Analyze the following video: {video_path.as_posix()}"

    response:RunResponse=final_agent.run(prompt)
    json_compatible_response = jsonable_encoder(response.content)
    return JSONResponse(content=json_compatible_response)




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=1010,
        reload=True
    )