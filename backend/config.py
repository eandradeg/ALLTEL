import os
from dotenv import load_dotenv

load_dotenv()  # Cargar variables de entorno desde un archivo .env

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")

settings = Settings()
