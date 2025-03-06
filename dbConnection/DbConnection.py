from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine, inspect
from sqlalchemy.pool import StaticPool 
from dotenv import load_dotenv
import os


load_dotenv()

class DbPostgres:
    def __init__(self, connection_string=None):
        self.connection_string = connection_string or os.getenv("DATABASE_URL")
        if not self.connection_string:
            raise ValueError("DATABASE_URL is not set in the .env file")

    def connect_to_db(self):
        return create_engine(self.connection_string, poolclass=StaticPool)
    



