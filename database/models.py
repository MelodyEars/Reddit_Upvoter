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
    account = ForeignKeyField(Account, backref="accounts")
    proxy = ForeignKeyField(Proxy, backref="proxies")
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
    user = IntegerField()
    # nickname = CharField(null=True)
    # timesub = DateField() # time when user was bought tair
    # signup = CharField()# єтапьі регистрации пользователя
