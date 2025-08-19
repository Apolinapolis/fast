from fastapi import APIRouter
from http import HTTPStatus
from app.database.engine import check_db_available
from app.models.AppStatus import AppStatus


router = APIRouter()

@router.get("/status", status_code=HTTPStatus.OK)
def status() -> AppStatus:
    return AppStatus(database=check_db_available())