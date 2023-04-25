from peewee import Model, PrimaryKeyField, CharField, ForeignKeyField, BooleanField
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

    class Meta:
        db_table = "reddit links"


class WorkAccountWithLink(BaseModel):
    cookie = ForeignKeyField(Cookie, backref='cookies', null=True, on_delete='SET NULL')
    link = ForeignKeyField(RedditLink, backref='reddit links', null=True, on_delete='SET NULL')

    class Meta:
        db_table = "work account with link"
