from dotenv import load_dotenv
load_dotenv()

from fastapi import HTTPException
from pydantic import EmailStr
import pathlib
import shutil
import os
import asyncio
import uuid
import tempfile

import boto3
from fastapi import Depends
from typing import Annotated
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from backend.auth import hash_password,verify_password,get_current_user,create_access_token
from backend.db import get_user_by_email,create_user,create_tables

from agno.agent import RunResponse
from backend.agents.teamup_agents import final_agent, parser_agent

app = FastAPI()

@app.on_event("startup")
async def startup():
    await create_tables()

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

class AuthRequest(BaseModel):
    email:EmailStr
    password:str

CurrentUser=Annotated[dict,Depends(get_current_user)]


@app.post("/auth/register")
async def register(body:AuthRequest):
    if await get_user_by_email(body.email):
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed_password=hash_password(body.password)
    user = await create_user(body.email,hashed_password)
    token = create_access_token(user['id'],user['email'])
    return {"access_token":token,"token_type":"bearer"}


@app.post("/auth/login")
async def login(body:AuthRequest):
    user = await get_user_by_email(body.email)
    if not user or not verify_password(body.password,user['password']):
        raise HTTPException(status_code=401,detail="Invalid Credentials")
    
    access_token = create_access_token(user['id'],user['email'])
    return {"access_token":access_token,"token_type":"bearer"}


@app.post("/upload")
async def upload_file(user: CurrentUser, file: UploadFile = File(...)):
    # upload_dir = "video_uploads"
    # os.makedirs(upload_dir, exist_ok=True)

    # file_path = os.path.join(upload_dir, file.filename)
    # with open(file_path, "wb") as f:
    #     shutil.copyfileobj(file.file, f)
    # return {"file_path": str(pathlib.Path(file_path).resolve())}

    key =upload_to_b2(file.file,file.filename)
    return {"key":key}

    


@app.post("/analyze")
async def analyze(request: AnalysisRequest,user:CurrentUser):
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