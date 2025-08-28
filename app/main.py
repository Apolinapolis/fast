from contextlib import asynccontextmanager

import uvicorn
import dotenv
dotenv.load_dotenv()
from fastapi import FastAPI
from app.routers import status, users
from app.database.engine import create_db_tables


@asynccontextmanager
async def lifespan(_: FastAPI):
    print('on startup')
    create_db_tables()
    yield
    print('on shutdown')


app = FastAPI(lifespan=lifespan)
app.include_router(status.router)
app.include_router(users.router)


if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8002)