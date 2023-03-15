import peewee as pw
from database import db


class AllowedUser(pw.Model):
    # user_id = pw.IntegerField()
    username = pw.CharField(max_length=50)

    class Meta:
        database = db


def create_tables():
    with db:
        db.create_tables([AllowedUser])
