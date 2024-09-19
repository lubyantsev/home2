from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import User
from app.schemas import CreateUser, UpdateUser
from sqlalchemy import select, insert, update, delete
# from slugify import slugify

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/")
async def all_users(db: Annotated[Session, Depends(get_db)]):
    # Получаем всех пользователей из БД
    users = db.execute(select(User)).scalars().all()
    return users


@router.get("/{user_id}")
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    # Извлекаем пользователя по user_id
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    return user


@router.post("/create", response_model=dict)
async def create_user(user: CreateUser, db: Annotated[Session, Depends(get_db)]):
    # Создаем нового пользователя
    new_user = User(**user.model_dump())
    db.execute(insert(User).values(new_user.__dict__))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.put("/update/{user_id}", response_model=dict)
async def update_user(user_id: int, user: UpdateUser, db: Annotated[Session, Depends(get_db)]):
    # Обновляем пользователя
    existing_user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User was not found")

    db.execute(update(User).where(User.id == user_id).values(user.model_dump()))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}


@router.delete("/delete/{user_id}", response_model=dict)
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    # Удаляем пользователя
    existing_user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User was not found")

    db.execute(delete(User).where(User.id == user_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User deleted successfully!'}





# from fastapi import APIRouter, HTTPException
# from app.schemas import CreateUser, UpdateUser
#
# router = APIRouter(prefix="/user", tags=["user"])
#
# users = []
#
# @router.get("/")
# async def all_users():
#     return users
#
# @router.get("/{user_id}")
# async def user_by_id(user_id: int):
#     user = next((user for user in users if user.id == user_id), None)
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user
#
# @router.post("/create", response_model=dict)
# async def create_user(user: CreateUser):
#     user_id = len(users) + 1
#     new_user = user.dict()
#     new_user["id"] = user_id
#     users.append(new_user)
#     return new_user
#
# @router.put("/update/{user_id}", response_model=dict)
# async def update_user(user_id: int, user: UpdateUser):
#     for u in users:
#         if u["id"] == user_id:
#             u.update(user.dict())
#             return u
#     raise HTTPException(status_code=404, detail="User not found")
#
# @router.delete("/delete/{user_id}", response_model=dict)
# async def delete_user(user_id: int):
#     for u in users:
#         if u["id"] == user_id:
#             users.remove(u)
#             return u
#     raise HTTPException(status_code=404, detail="User not found")