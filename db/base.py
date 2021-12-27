from databases import Database
from sqlalchemy import create_engine, MetaData
from core.config import MAIN_DB_URL


database = Database(MAIN_DB_URL)
metadata = MetaData()
engine = create_engine(MAIN_DB_URL)
