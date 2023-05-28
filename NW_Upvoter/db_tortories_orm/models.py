from tortoise import fields
from tortoise.models import Model


class BaseModel(Model):
    id = fields.IntField(pk=True)


class Proxy(BaseModel):
    host = fields.CharField(max_length=255)
    port = fields.CharField(max_length=255)
    user = fields.CharField(max_length=255)
    password = fields.CharField(max_length=255)

    class Meta:
        table = 'proxies'


class Account(BaseModel):
    login = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)

    class Meta:
        table = 'accounts'


class Cookie(BaseModel):
    account = fields.ForeignKeyField('models.Account', related_name='cookies')
    proxy = fields.ForeignKeyField('models.Proxy', related_name='cookies')
    cookie_path = fields.CharField(max_length=255)
    is_selected = fields.BooleanField(default=False)
    ban = fields.CharField(max_length=255, null=True)

    def __str__(self):
        return self.cookie_path

    class Meta:
        table = 'cookies'


class RedditLink(BaseModel):
    link = fields.CharField(max_length=255)
    date = fields.DatetimeField(auto_now_add=True, timezone=True)
    reveddit_url = fields.CharField(max_length=255, null=True)
    tg_name = fields.CharField(max_length=255, null=True)
    subreddit = fields.CharField(max_length=255, null=True)
    count_upvotes = fields.IntField(default=0)

    def __str__(self):
        return self.link

    class Meta:
        table = 'reddit links'


class WorkAccountWithLink(BaseModel):
    cookie = fields.ForeignKeyField('models.Cookie', related_name='work_accounts', null=True)
    link = fields.ForeignKeyField('models.RedditLink', related_name='work_accounts', null=True)

    class Meta:
        table = 'work account with link'

    # cookie = fields.ManyToManyField('models.Cookie', related_name='work_account_links', null=True)
    # link = fields.ManyToManyField('models.RedditLink', related_name='work_account_links', null=True)
