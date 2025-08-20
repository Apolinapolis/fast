import os
import dotenv
import pytest

dotenv.load_dotenv()

@pytest.fixture(scope="session")
def app_url():
    return os.getenv("APP_URL")