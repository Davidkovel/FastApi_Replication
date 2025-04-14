import os

from fastapi import APIRouter, Request, HTTPException
from starlette.responses import JSONResponse

from app.data.queries.functions import get_user_by, add_new_user, authenticate_user
from app.routers.auth.schemas import UserProfileResponseModel, UserModel, UserResponseModel, Token, OAuthForm
from app.utils.security import create_access_token

SECRET_KEY = os.getenv("S")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

auth_router = APIRouter(prefix="/api/auth")


@auth_router.post("/register", response_model=UserProfileResponseModel)
async def register_new_user(request: Request, user_data: UserModel):
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


@auth_router.post("/sign-in", response_model=Token)
async def send_access_token(request: Request, form_data: OAuthForm):
    db_session = request.state.db_session

    user = await authenticate_user(form_data=form_data, db_session=db_session)
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь с указанным логином и паролем не найден")

    access_token_expire = None
    access_token = create_access_token(data={"sub": form_data.login}, expire_delta=access_token_expire)

    response = JSONResponse(status_code=200, content=Token(token=access_token).dict())

    return response



{
  "name": "GreenMonkey2",
  "login": "yellowMonkey2",
  "email": "2@gmail.com",
  "password": "$aba4821FWfew01#.fewA$2",
  "phone": "+36849512399222",
  "image": "https://http.cat/images/1002.jpg"
}