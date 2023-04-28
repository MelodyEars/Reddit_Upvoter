from tortoise import Tortoise
from tortoise.fields import *
from tortoise.models import Model

# Налаштування підключення до бази даних
DATABASE = {
    "provider": "asyncpg",
    "user": "doadmin",
    "password": "AVNS_XCxtxUH7rZz8txAxKYO",
    "host": "bots-do-user-11731497-0.b.db.ondigitalocean.com",
    "port": "25061",
    "database": "8-core_start_comp",
}

# Ініціалізація підключення до бази даних
Tortoise.init(DATABASE)

class BaseModel(Model):
    id = IntField(pk=True)

    class Meta:
        abstract = True

class Proxy(BaseModel):
    host = CharField(max_length=255)
    port = CharField(max_length=255)
    user = CharField(max_length=255)
    password = CharField(max_length=255)

    class Meta:
        table = 'proxies'


class Account(BaseModel):
    login = CharField(max_length=255, unique=True)
    password = CharField(max_length=255)

    class Meta:
        table = 'accounts'


class Cookie(BaseModel):
    account = ForeignKeyField("models.Account", related_name="cookies", on_delete='CASCADE')
    proxy = ForeignKeyField("models.Proxy", related_name="cookies", on_delete='CASCADE')
    cookie_path = CharField(max_length=255)
    is_selected = BooleanField(default=False)
    ban = CharField(max_length=255, null=True, default=None)

    class Meta:
        table = 'cookies'


class RedditLink(BaseModel):
    link = CharField(max_length=255)

    class Meta:
        table = "reddit_links"


class WorkAccountWithLink(BaseModel):
    cookie = ForeignKeyField("models.Cookie", related_name="work_accounts", null=True, on_delete='SET NULL')
    link = ForeignKeyField("models.RedditLink", related_name="work_accounts", null=True, on_delete='SET NULL')

    class Meta:
        table = "work_account_with_links"
