from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware

from src.auth.auth_config import auth_backend, fastapi_users, current_user
from src.auth.models import AuthUser
from src.auth.schemas import UserRead, UserCreate, UserUpdate
from src.auth.routers.verify_router import router as verify_router
from src.auth.routers.forgot_pass_router import router as forgot_pass_router
from src.docs.router import router as upload_docs_router
from src.llm_service.utils import send_data_to_llm

app = FastAPI(
    title="UDV LLM",
)

origins = [
    "http://localhost:3000",
    "http://localhost:3000/signUp",
    "http://localhost:8001",
    "http://localhost:3000/logIn",
    "http://localhost:3000/request",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend, requires_verification=True),
    prefix="/auth",
    tags=["Auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
app.include_router(
    verify_router,
    prefix="/auth",
    tags=["Auth"],
)
app.include_router(
    forgot_pass_router,
    prefix="/auth",
    tags=["Auth"],
)
app.include_router(
    upload_docs_router,
    prefix="/docks",
    tags=["Docs"],
)


@app.get('/')
async def hello():
    return {'result': 'start_page'}


@app.post("/get_answer")
async def send_data(data: dict):
    result = await send_data_to_llm('process_questions', data)
    return {"result_from_gigachatAPI": result}


@app.post("/get_test")
async def send_data(data: dict):
    result = await send_data_to_llm('process_data', data)
    return {"result_from_gigachatAPI": result}


@app.get("/protected-route")
async def protected_route(user: AuthUser = Depends(current_user)):
    return f"Hello, {user.name}"
