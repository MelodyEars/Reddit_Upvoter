from peewee import *

from SETTINGS import set_database


autoposting_db = PostgresqlDatabase('AutoPosting', **set_database)


class BaseModel(Model):
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = autoposting_db


class Proxy(BaseModel):
    host = CharField()
    port = CharField()
    user = CharField()
    password = CharField()

    class Meta:
        db_table = 'proxies'


class Account(BaseModel):
    login = CharField(unique=True)
    password = CharField()

    class Meta:
        db_table = 'accounts'


class JobModel(BaseModel):
    model_name = CharField()
    account = ForeignKeyField(Account, backref="accounts")
    proxy = ForeignKeyField(Proxy, backref="proxies")
    data_path = CharField()
    cookie_path = CharField()

    class Meta:
        db_table = 'job_model'
