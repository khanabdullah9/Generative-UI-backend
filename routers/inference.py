from fastapi import APIRouter, status, HTTPException

import utils
from models.models import Prompt
from LLM.infer_ollama import is_ollama_running, execute_chain

router = APIRouter(prefix = "/api/infer")

@router.get("/is_ollama_responsive/", status_code= status.HTTP_200_OK)
def is_ollama_responsive():
    return {"message":"Responsive"} if is_ollama_running() else {"message":"NOT Responsive"}

@router.post("/infer_ollama/", status_code=status.HTTP_200_OK)
def infer_ollama(prompt: Prompt):
    if not is_ollama_running():
        return {}

    return execute_chain(prompt.text)

@router.post("/mock_infer/", status_code=status.HTTP_200_OK)
def mock_infer(prompt: Prompt):
    """
    For testing the UI
    Args:
        prompt: user prompt pydantic model

    Returns: JSON: pre generated layout

    """
    return utils.get_form_layout()