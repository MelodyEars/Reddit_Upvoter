from peewee import *
from work_fs import path_near_exefile

db = SqliteDatabase(path_near_exefile('db_lib.db'),
                    pragmas={
                        'journal_mode': 'wal',
                        'cache_size': -1024 * 64
                    })


class BaseModel(Model):
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db


class Proxy(BaseModel):
    host = CharField()
    port = CharField()
    user = CharField(unique=True)
    password = CharField()

    class Meta:
        db_table = 'proxies'


class Cookie(BaseModel):
    proxy = ForeignKeyField(Proxy)
    cookie_path = CharField()
    is_work = BooleanField(default=False)  # already work on reddit or no

    class Meta:
        db_table = 'cookies'

