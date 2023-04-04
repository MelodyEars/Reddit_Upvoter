import peewee as pw
from database import db
from database.vote_tg_bot.models import BaseModel


class AllowedUser(BaseModel):
    # user_id = pw.IntegerField()
    username = pw.CharField(max_length=50)

    class Meta:
        database = db


def create_tables():
    with db:
        db.create_tables([AllowedUser])
