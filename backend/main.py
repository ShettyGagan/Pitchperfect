# import json
# import pathlib
# from fastapi import FastAPI, UploadFile,File
# import os
# import shutil
# from dotenv import load_dotenv
# load_dotenv()  # Load .env file at startup — must be before any agent imports
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.encoders import jsonable_encoder
# from fastapi.responses import JSONResponse
# from pydantic import BaseModel
# from agno.agent import RunResponse
# from backend.agents.teamup_agents import final_agent
# import re

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class AnalysisRequest(BaseModel):
#     video_url: str


# @app.post("/upload")
# async def upload_file(file:UploadFile=File(...)):
#     upload_dir="video_uploads"
#     os.makedirs(upload_dir,exist_ok=True)

#     file_path=os.path.join(upload_dir,file.filename)
#     with open(file_path,"wb") as f:
#         shutil.copyfileobj(file.file,f)

#     return {"file_path":str(pathlib.Path(file_path).resolve())}

# @app.post("/analyze")
# async def analyze(request: AnalysisRequest):
#     video_path = pathlib.Path(request.video_url)

#     if not video_path.exists():
#         return JSONResponse(
#             status_code=404,
#             content={"error": f"File not found at the specified path: {video_path}"}
#         )

#     prompt = f"Analyze the following video: {video_path.as_posix()}"

#     response:RunResponse=final_agent.run(prompt)
#     json_compatible_response = jsonable_encoder(response.content)
#     return JSONResponse(content=json_compatible_response)





import pathlib
import shutil
import os
import asyncio
import uuid
import tempfile

import boto3
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from agno.agent import RunResponse
from backend.agents.teamup_agents import final_agent, parser_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("B2_KEY_ID"),
    aws_secret_access_key=os.getenv("B2_APP_KEY"),
    endpoint_url=f"https://s3.{os.getenv('B2_REGION')}.backblazeb2.com",
    region_name=os.getenv("B2_REGION")
)

BUCKET = os.getenv("B2_BUCKET_NAME")

def upload_to_b2(file_obj,file_name:str)->str:
    key = f"{uuid.uuid4()}_{file_name}"
    _s3.upload_fileobj(file_obj,BUCKET,key)
    return key

def download_from_b2(key:str)->pathlib.Path:
    with tempfile.NamedTemporaryFile(delete=False, suffix=pathlib.Path(key).suffix) as tmp:
        _s3.download_fileobj(BUCKET,key,tmp)
        return pathlib.Path(tmp.name)


def delete_from_b2(key:str):
    _s3.delete_object(Bucket=BUCKET,Key=key)

class AnalysisRequest(BaseModel):
    tmp_video_key: str


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # upload_dir = "video_uploads"
    # os.makedirs(upload_dir, exist_ok=True)

    # file_path = os.path.join(upload_dir, file.filename)
    # with open(file_path, "wb") as f:
    #     shutil.copyfileobj(file.file, f)
    # return {"file_path": str(pathlib.Path(file_path).resolve())}

    key =upload_to_b2(file.file,file.filename)
    return {"key":key}

    


@app.post("/analyze")
async def analyze(request: AnalysisRequest):
    # video_path = pathlib.Path(request.video_url)

    # if not video_path.exists():
    #     return JSONResponse(
    #         status_code=404,
    #         content={"error": f"File not found at the specified path: {video_path}"}
    #     )

    tmp_video_path = download_from_b2(request.tmp_video_key)

    try:
        prompt = f"Analyze the following video: {tmp_video_path.as_posix()}"

        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Step 1 — coordinator orchestrates sub-agents, returns TOON summary
                coord_response: RunResponse = final_agent.run(prompt)
                toon_summary = coord_response.content

                # Step 2 — parser converts TOON summary to structured JSON
                parse_prompt = f"Parse this analysis into JSON:\n{toon_summary}"
                final_response: RunResponse = parser_agent.run(parse_prompt)

                return JSONResponse(content=jsonable_encoder(final_response.content))

            except Exception as e:
                error_str = str(e)
                if "429" in error_str and attempt < max_retries - 1:
                    wait = 30 * (attempt + 1) 
                    print(f"Rate limit hit (attempt {attempt + 1}), retrying in {wait}s...")
                    await asyncio.sleep(wait)
                else:
                    return JSONResponse(
                        status_code=500,
                        content={"error": f"Analysis failed: {error_str}"}
                    )
    finally:
        tmp_video_path.unlink(missing_ok=True)
        delete_from_b2(request.tmp_video_key)