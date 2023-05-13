from datetime import datetime

from peewee import Model, PrimaryKeyField, CharField, ForeignKeyField, BooleanField, DateTimeField, IntegerField
from SETTINGS import db


class BaseModel(Model):
    id = PrimaryKeyField(unique=True)

    # @classmethod
    # def get_or_create_crdb(cls, **kwargs):
    #     with cls._meta.database.transaction():
    #         try:
    #             record = cls.select().for_update().get(**kwargs)
    #             created = False
    #         except cls.DoesNotExist:
    #             record = cls.create(**kwargs)
    #             created = True
    #     return record, created

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
    date = DateTimeField(default=datetime.now)
    tg_name = CharField(max_length=255, null=True)
    subreddit = CharField(max_length=255, null=True)
    count_upvotes = IntegerField(default=0)

    class Meta:
        db_table = "reddit links"


class WorkAccountWithLink(BaseModel):
    cookie = ForeignKeyField(Cookie, backref='cookies', null=True, on_delete='SET NULL')
    link = ForeignKeyField(RedditLink, backref='reddit links', null=True, on_delete='SET NULL')

    class Meta:
        db_table = "work account with link"
