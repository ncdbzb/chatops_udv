from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.auth.auth_config import current_verified_user
from src.auth.models import AuthUser
from database.database import get_async_session
from src.docs.schemas import DocCreate
from src.docs.models import doc

router = APIRouter()


@router.post(
    '/upload-dock',
    status_code=status.HTTP_201_CREATED,
)
async def upload_form(dock_name: str, dock_description: str, file: UploadFile = File(...),
                      user: AuthUser = Depends(current_verified_user), session: AsyncSession = Depends(get_async_session)):
    if not user.company_representative:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    try:
        stmt = insert(doc).values(name=dock_name, description=dock_description, path='/test', user_id=user.id)
        await session.execute(stmt)
        await session.commit()
        return {'status': 'added new doc'}
    except IntegrityError as e:
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
        raise HTTPException(status_code=404, detail="Document not found")

    # Проверка, что текущий пользователь является владельцем документа
    if doc.c.user_id != user.id:
        raise HTTPException(status_code=403, detail="You are not the owner of this document")

    return {'status': '200 OK'}
