import uvicorn
import dotenv
dotenv.load_dotenv()
from fastapi import FastAPI
from routers import status, users
from app.database.engine import create_db_tables



app = FastAPI()
app.include_router(status.router)
app.include_router(users.router)


if __name__ == "__main__":
    create_db_tables()
    uvicorn.run(app, host='localhost', port=8002)