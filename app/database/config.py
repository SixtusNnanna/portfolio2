import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.environ.get("DATABASE_URL")

SECRET_KEY = os.environ.get("SECRET_KEY", "unsafe-placeholder-key")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
ALGORITHM = "HS256"
REFRESH_TOKEN_EXPIRE_DAYS = 30