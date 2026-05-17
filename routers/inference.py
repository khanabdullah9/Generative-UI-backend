from fastapi import APIRouter, status, HTTPException

import utils
from models.models import Prompt, UsageModel
from LLM.infer_ollama import is_ollama_running, execute_chain
from database.relational.crud import UsageCrud

router = APIRouter(prefix = "/api/infer")

@router.get("/is_ollama_responsive/", status_code= status.HTTP_200_OK)
def is_ollama_responsive():
    return {"message":"Responsive"} if is_ollama_running() else {"message":"NOT Responsive"}

@router.post("/infer_ollama/", status_code=status.HTTP_200_OK)
def infer_ollama(prompt: Prompt):
    # if not is_ollama_running(): # temp.. using groq's llama api
    #     return {}

    obj = UsageCrud()
    success = obj.update(user_id=prompt.user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usage incrementation failed")

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