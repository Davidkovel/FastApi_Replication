from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from starlette.middleware.base import RequestResponseEndpoint

from app.db.base_class import Base
from app.routers import posts_router
from app.config.config import Config


@asynccontextmanager
async def lifespan(_: FastAPI):
    await create_all_tables()
    yield


app = FastAPI(lifespan=lifespan)

# print(os.environ)

url = f"postgresql+asyncpg://{Config.POSTGRES_USER}:{Config.POSTGRES_PASSWORD}@{Config.POSTGRES_HOST}:{Config.POSTGRES_PORT}/{Config.POSTGRES_DATABASE}"

engine = create_async_engine(url=url, echo=False, future=True)
db_pool = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


async def create_all_tables():
    print("[Info] Creating tables...")
    try:
        async with engine.begin() as conn:
            tables = Base.metadata.tables.keys()
            print(Base.metadata.tables)
            print(f"[Info] Tables to be created: {list(tables)}")

            await conn.run_sync(Base.metadata.create_all)
            print("[Info] Tables created successfully")
    except Exception as e:
        print(f"[Error] Failed to create tables: {e}")


@app.middleware("http")
async def db_session_middleware(request: Request, call_next: RequestResponseEndpoint):
    async with db_pool() as db_session:
        request.state.db_session = db_session
        response = await call_next(request)

    return response


def main():
    app.include_router(router=posts_router)

    import uvicorn
    uvicorn.run(app, port=8001)


if __name__ == '__main__':
    print('[Info] Starting the application...')
    main()
