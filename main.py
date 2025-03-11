from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.base import engine
from app.db.base_class import Base
from app.routers import posts_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    await create_all_tables()
    yield


app = FastAPI(lifespan=lifespan)


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


def main():
    app.include_router(router=posts_router)

    import uvicorn
    uvicorn.run(app)


if __name__ == '__main__':
    print('[Info] Starting the application...')
    main()
