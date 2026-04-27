import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='config.env')

DATABASE_URL = os.getenv('DATABASE_URL')
JWT_KEY = os.getenv('JWT_KEY')