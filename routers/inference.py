from fastapi import APIRouter, status, HTTPException

from backend.models.models import Prompt
from backend.LLM.infer_ollama import is_ollama_running, execute_chain

router = APIRouter(prefix = "/api/infer/")

@router.get("/is_ollama_responsive/", status_code= status.HTTP_200_OK)
def is_ollama_responsive():
    return {"message":"Responsive"} if is_ollama_running() else {"message":"NOT Responsive"}

@router.post("/infer_ollama/", status_code=status.HTTP_200_OK)
def infer_ollama(prompt: Prompt):
    if not is_ollama_running():
        return {}

    return execute_chain(prompt.text)