from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import boto3
import os
from typing import Optional, Dict, Any

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

class ChatRequest(BaseModel):
    query: str
    kb_id: Optional[str] = None
    model_arn: Optional[str] = None

# CORS setup to allow frontend to communicate
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev only, restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Check for AWS credentials in env
        access_key = os.getenv("AWS_ACCESS_KEY_ID")
        secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        kb_id = request.kb_id or os.getenv("KNOWLEDGE_BASE_ID")
        model_arn = request.model_arn or os.getenv("BEDROCK_MODEL_ARN")
        
        client = boto3.client(
            "bedrock-agent-runtime",
            region_name="ap-southeast-2",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )

        response = client.retrieve_and_generate(
            input={"text": request.query},
            retrieveAndGenerateConfiguration={
                "type": "KNOWLEDGE_BASE",
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": kb_id,
                    "modelArn": model_arn,
                },
            },
        )

        output_text = response.get("output", {}).get("text", "No response received")
        return {"response": output_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok"}
