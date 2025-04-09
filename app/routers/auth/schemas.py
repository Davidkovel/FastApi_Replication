import re
from typing import Annotated, Optional

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, Field, constr, field_validator

userName = Annotated[constr(max_length=50), Field(
    title="User Name",
    description="Имя пользователя",
    max_length=50,
    examples=['Green Monkey']
)]

userLogin = Annotated[constr(max_length=30, pattern=r'^[a-zA-Z0-9-]+$'), Field(
    title="User Login",
    description="Логин пользователя",
    max_length=30,
    pattern=r'^[a-zA-Z0-9-]+$',
    examples=['yellowMonkey']
)]

userEmail = Annotated[constr(min_length=1, max_length=50), Field(
    title="User Email",
    description="E-mail пользователя",
    min_length=1,
    max_length=50,
    examples=['yellowstone1980@gmail.com']
)]

userPassword = Annotated[constr(min_length=6, max_length=100), Field(
    title="User Password",
    description="""
    Пароль пользователя, к которому предъявляются следующие требования:

    Длина пароля не менее 6 символов.
    Присутствуют латинские символы в нижнем и верхнем регистре.
    Присутствует минимум одна цифра.
    """,
    min_length=6,
    max_length=100,
    examples=['$aba4821FWfew01#.fewA$']
)]

userPhone = Annotated[Optional[constr(max_length=200)], Field(
    title="User Phone",
    description="Номер телефона пользователя в формате +123456789",
    pattern=r'^\+[\d]+$',
    max_length=20,
    default=None,
    examples=['+3684951239922']
)]

userImage = Annotated[Optional[constr(min_length=1, max_length=200)], Field(
    title="User Image Url",
    description="Ссылка на фото для аватара пользователя",
    min_length=1,
    max_length=200,
    default=None,
    examples=['https://http.cat/images/100.jpg']
)]


class UserModel(BaseModel):
    """
    Информация о профиле пользователя
    """

    name: userName
    login: userLogin
    email: userEmail
    password: userPassword
    phone: userPhone
    image: userImage

    @field_validator('name', mode='before')
    def validate_name(cls, name):
        if not name:
            raise HTTPException(status_code=400, detail="Имя не указано.")
        elif len(name) < 3:
            raise HTTPException(status_code=400, detail="Имя слишком короткое.")
        elif len(name) > 50:
            raise HTTPException(status_code=400, detail="Имя слишком длинное.")
        elif not re.search(pattern=r'[a-zA-Z0-9_.±]+', string=name):
            raise HTTPException(status_code=400, detail="Имя не соответствует шаблону.")

        return name

    @field_validator('login', mode='before')
    def validate_login(cls, login):
        if not login:
            raise HTTPException(status_code=400, detail="Логин не указан.")
        elif len(login) < 3:
            raise HTTPException(status_code=400, detail="Длина логина слишком маленькая.")
        elif len(login) > 30:
            raise HTTPException(status_code=400, detail="Длина логина превышает допустимый лимит.")

        return login

    @field_validator('password', mode='before')
    def validate_password(cls, password):
        if not password:
            raise HTTPException(status_code=400, detail="Пароль не указан.")
        elif len(password) < 6:
            raise HTTPException(status_code=400, detail="Недостаточно надежный пароль.")
        elif len(password) > 100:
            raise HTTPException(status_code=400, detail="Длина пароля превышает допустимый лимит.")

        return password

    @field_validator('email', mode='before')
    def validate_email(cls, email):
        if not email:
            raise HTTPException(status_code=400, detail="E-mail не указан.")
        elif not re.search(pattern=r'^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$', string=email):
            raise HTTPException(status_code=400, detail="E-mail не валидный.")
        elif len(email) > 50:
            raise HTTPException(status_code=400, detail="Длина e-mail превышает допустимый лимит.")

        return email

    @field_validator('phone', mode='before')
    def validate_phone(cls, phone):
        if not phone:
            return phone

        if not re.search(pattern=r'^\+[\d]+$', string=phone):
            raise HTTPException(status_code=400, detail="Номер телефона не соответствует шаблону.")
        elif len(phone) > 20:
            raise HTTPException(status_code=400, detail="Длина номера телефона превышает допустимый лимит.")
        elif len(phone) < 5:
            raise HTTPException(status_code=400, detail="Длина номера телефона слишком маленькая")

        return phone

    @field_validator('image', mode='before')
    def validate_image(cls, image):
        if not image:
            return image

        if len(image) > 200:
            raise HTTPException(status_code=400,
                                detail="Длина ссылки на аватар пользователя превышает допустимый лимит.")
        elif len(image) < 5:
            raise HTTPException(status_code=400, detail="Длина ссылки на аватар пользователя слишком маленькая.")

        return image


class UserResponseModel(BaseModel):
    """
    Информация о профиле пользователя без пароля
    """

    name: userName
    login: userLogin
    email: userEmail
    phone: userPhone
    image: userImage


class UserProfileResponseModel(BaseModel):
    """
    Информация о профиле пользователя
    """

    profile: UserResponseModel


class OAuthForm(BaseModel):
    login: userLogin
    password: userPassword


class Token(BaseModel):
    token: str = Field(
        title="Access Token",
        default="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    )
