import os

from fastapi import APIRouter, Request, HTTPException
from starlette.responses import JSONResponse

from app.data.queries.functions import get_user_by, add_new_user
from app.routers.auth.schemas import UserProfileResponseModel, UserModel, UserResponseModel

SECRET_KEY = os.getenv("S")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

auth_router = APIRouter(prefix="/api/auth")


@auth_router.post("/register", response_model=UserProfileResponseModel)
async def register(request: Request, user_data: UserModel):
    db_session = request.state.db_session

    check_user = await get_user_by(db_session, user_data)
    if check_user:
        raise HTTPException(status_code=409,
                            detail="Пользователь с таким e-mail, номером телефона или логином уже зарегистрирован.")

    new_user = await add_new_user(user_data=user_data, db_session=db_session)

    return JSONResponse(status_code=201, content=UserProfileResponseModel(profile=UserResponseModel(
        name=new_user.name,
        login=new_user.login,
        email=new_user.email,
        phone=new_user.phone,
        image=new_user.image
    )).dict())


@auth_router.get("/login")
async def login():
    return {"message": "Login endpoint"}


@auth_router.get("/logout")
async def logout():
    return {"message": "Logout endpoint"}
