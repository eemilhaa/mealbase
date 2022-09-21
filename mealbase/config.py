from os import getenv
from dotenv import load_dotenv


DATABASE_URL = getenv("DATABASE_URL")
SECRET_KEY = getenv("SECRET_KEY")
