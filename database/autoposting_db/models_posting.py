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
    root_folder = CharField()
    account = ForeignKeyField(Account, backref="accounts", on_delete='CASCADE')
    proxy = ForeignKeyField(Proxy, backref="proxies", on_delete='CASCADE')
    cookie_path = CharField()

    class Meta:
        db_table = 'job_models'


class Photo(BaseModel):
    path_photo = CharField()
    is_submitted = BooleanField(default=False)

    class Meta:
        db_table = 'photos'


class LinkSubReddit(BaseModel):
    link_SubReddit = CharField()
    is_submitted = BooleanField(default=False)

    class Meta:
        db_table = 'links_sub_reddit'


class Category(BaseModel):
    name_category = CharField()

    class Meta:
        db_table = 'categories'


class Posting(BaseModel):
    id_jobmodel = ForeignKeyField(JobModel, backref='job_models', null=True, on_delete='SET NULL')
    id_link_sub_reddit = ForeignKeyField(LinkSubReddit, backref='links_sub_reddit', null=True, on_delete='SET NULL')
    id_photo = ForeignKeyField(Photo, backref='photos', null=True, on_delete='SET NULL')
    id_category = ForeignKeyField(Category, backref='categories', null=True, on_delete='SET NULL')

    class Meta:
        db_table = 'posting'


class UrlPost(BaseModel):
    url = CharField()

    class Meta:
        db_table = 'urls post'
