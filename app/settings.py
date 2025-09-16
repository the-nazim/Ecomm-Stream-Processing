import os
from dotenv import load_dotenv

BASEDIR = os.path.dirname(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(BASEDIR, ".env"))

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    APP_NAME: str = "E-Commerce Store"

settings = Settings()