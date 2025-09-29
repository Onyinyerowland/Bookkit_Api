import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(".env")
load_dotenv(".env.test")

from pydantic_settings import BaseSettings
from pydantic import ConfigDict


# 🔹 Project root
ROOT_DIR = Path(__file__).resolve().parent.parent

# Decide env file
env_file = ROOT_DIR / (".env.test" if os.getenv("TESTING") == "1" else ".env")

# Load env file if exists
if env_file.exists():
    load_dotenv(env_file, override=True)
    print(f"DEBUG: Loaded env file {env_file}")
else:
    print(f"⚠️ WARNING: {env_file} not found! Using defaults.")

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///:memory:"  # default for tests
    SECRET_KEY: str = "dev-secret"
    ACCESS_TOKEN_EXPIRES_MIN: int = 15
    REFRESH_TOKEN_EXPIRES_DAYS: int = 7
    BCRYPT_ROUNDS: int = 12
    CORS_ORIGINS: list[str] = []
    LOG_LEVEL: str = "info"

    model_config = ConfigDict(
        env_file= env_file, extra="ignore")

# Instantiate settings
settings = Settings()

# Debug prints
print("DEBUG: DATABASE_URL =", settings.DATABASE_URL)
print("DEBUG: SECRET_KEY =", settings.SECRET_KEY)
