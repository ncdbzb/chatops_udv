from fastapi import APIRouter, Depends

from src.auth.models import AuthUser
from src.llm_service.utils import send_data_to_llm
from src.auth.auth_config import current_verified_user

router = APIRouter()


@router.post("/get_answer")
async def send_data(
        filename: str,
        question: str,
):
    data = {'filename': filename,
            'question': question}
    result = await send_data_to_llm('process_questions', data)
    return {"result_from_gigachatAPI": result}


@router.post("/get_test")
async def send_data(
        filename: str,
        que_num: int,
        #user: AuthUser = Depends(current_verified_user),
):
    data = {'filename': filename,
            'que_num': que_num}
    result = await send_data_to_llm('process_data', data)
    return {"result_from_gigachatAPI": result}
