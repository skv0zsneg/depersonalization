from starlette.config import Config


config = Config('.env')

MAIN_DB_URL = config("MAIN_DB_URL", cast=str, default="")
