from peewee import PostgresqlDatabase, Model, PrimaryKeyField, CharField, ForeignKeyField, BooleanField, IntegerField
from SETTINGS import set_database, mine_project

db = PostgresqlDatabase('database', **set_database)


class BaseModel(Model):
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db


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


class Cookie(BaseModel):
    account = ForeignKeyField(Account, backref="accounts", on_delete='CASCADE')
    proxy = ForeignKeyField(Proxy, backref="proxies", on_delete='CASCADE')
    cookie_path = CharField()
    is_selected = BooleanField(default=False)
    ban = CharField(null=True, default=None)

    class Meta:
        db_table = 'cookies'


class RedditLink(BaseModel):
    link = CharField()

    class Meta:
        db_table = "reddit links"


class WorkAccountWithLink(BaseModel):
    cookie = ForeignKeyField(Cookie, backref='cookies')
    link = ForeignKeyField(RedditLink, backref='reddit links')

    class Meta:
        db_table = "work account with link"


class UserTG(BaseModel):
    user_id = IntegerField()

    class Meta:
        db_table = "telegram users"
