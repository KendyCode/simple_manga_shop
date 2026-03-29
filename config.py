import os
from dotenv import load_dotenv

# Charge les variables du fichier .env
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cle-secrete-manga'

    user = os.environ.get('DB_USER') or 'root'
    password = os.environ.get('DB_PASSWORD') or ''
    host = os.environ.get('DB_HOST') or 'localhost'
    database = os.environ.get('DB_NAME') or 'manga_bdd'

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{user}:{password}@{host}/{database}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
