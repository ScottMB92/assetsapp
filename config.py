import os
from dotenv import load_dotenv

# The following code is used to retrieve the environment variables from the .dotenv file (the secret key and Uniform Resource Identifier) for the SQLite database. These are then passed into a Config class which is called in __init__.py for connecting to the database


load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
