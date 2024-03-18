import asyncio
import os
import shutil

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy import insert, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.auth.auth_config import current_verified_user
from src.auth.models import AuthUser
from database.database import get_async_session
from src.docs.models import doc
from src.docs.utils import send_file_to_llm

router = APIRouter()


@router.post(
    '/upload-dock',
    status_code=status.HTTP_202_ACCEPTED,
)
async def upload_form(
        dock_name: str,
        dock_description: str,
        file: UploadFile = File(...),
        user: AuthUser = Depends(current_verified_user),
        session: AsyncSession = Depends(get_async_session)):
    if not user.company_representative:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    try:
        new_name = f"{dock_name}.{file.filename.split('.')[-1]}"
        file_path = f"src/docs/temp/{new_name}"
        with open(file_path, "wb") as file_object:
            shutil.copyfileobj(file.file, file_object)
        print(f'file {new_name} saved at {file_path}')

        await send_file_to_llm(file_path)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await asyncio.to_thread(os.remove, file_path)

    try:
        stmt = insert(doc).values(name=dock_name, description=dock_description, path='/test', user_id=user.id)
        await session.execute(stmt)
        await session.commit()
        return {'status': 'added new doc'}
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Document with this name already exists")


@router.get(
    '/my',
    status_code=status.HTTP_200_OK,
)
async def get_my_docs(user: AuthUser = Depends(current_verified_user), session: AsyncSession = Depends(get_async_session)):
    if not user.company_representative:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    query = select(doc).where(doc.c.user_id == int(user.id))
    result = await session.execute(query)

    return result.mappings().all()


@router.delete(
    '/delete-my/{doc_id}',
    name="docs:delete_doc",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user.",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Not verified or not company representative.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The doc does not exist.",
        },
    },
)
async def del_my_docs(doc_id: int, user: AuthUser = Depends(current_verified_user), session: AsyncSession = Depends(get_async_session)):
    if not user.company_representative:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    query = select(doc).where(doc.c.id == doc_id)
    result = await session.execute(query)

    # Проверка наличия документа
    if not result.mappings().all():
        raise HTTPException(status_code=404, detail="The doc does not exist.")

    # Проверка, что текущий пользователь является владельцем документа
    query = select(doc.c.user_id).where(doc.c.id == int(doc_id))
    result = await (session.execute(query))
    check_owner = result.mappings().one()['user_id']
    if check_owner != user.id:
        raise HTTPException(status_code=403, detail=f"You are not the owner of this document {check_owner, user.id}")

    try:
        stmt = delete(doc).where(doc.c.id == doc_id)
        await session.execute(stmt)
        await session.commit()
        return {'status': 'doc has been deleted'}
    except Exception as e:
        print(e)
