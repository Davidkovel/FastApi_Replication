from passlib.context import CryptContext

from app.routers.auth.schemas import userPassword

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    @staticmethod
    def hash_password(password: userPassword) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: userPassword, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

