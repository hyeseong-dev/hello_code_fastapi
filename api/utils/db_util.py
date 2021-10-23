import databases
import sqlalchemy
from functools import lru_cache

from starlette.config import Config

from api import config
from api.models import metadata

# 1. Using pydantic to load .env configuration file


# @lru_cache()
# def conf():
#     return config.Settings()


# def database_pgsql_url_config():
#     return str(setting().DB_CONNECTION + "://" + setting().DB_USERNAME + ":" + setting().DB_PASSWORD + "@" + setting().DB_HOST + ":" + setting().DB_PORT + "/" + setting().DB_DATABASE)

# 2. Using starlette to load .env configuration file
def database_pgsql_url_config():
    conf = Config('.env')
    return str(conf("DB_CONNECTION") + "://" + conf("DB_USERNAME") + ":" + conf("DB_PASSWORD") + "@" + conf("DB_HOST") + ":" + conf("DB_PORT") + "/" + conf("DB_DATABASE"))


database = databases.Database(database_pgsql_url_config())
engine = sqlalchemy.create_engine(database_pgsql_url_config())
metadata.create_all(engine)
