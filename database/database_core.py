from peewee import SqliteDatabase, Model, IntegerField, TextField, DateTimeField, AutoField
from loguru import logger


db = SqliteDatabase('search_history.db')


class BaseModel(Model):
    class Meta:
        database = db


class SearchHistory(BaseModel):
    logger.info('Подключение модуля базы данных')
    id = AutoField()
    user_id = IntegerField()
    user_name = TextField()
    datetime_of_search = DateTimeField()
    city_name = TextField()
    region = TextField()
    hotel_name = TextField()
    hotel_id = IntegerField()

