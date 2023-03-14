import peewee as pw
from SETTINGS import set_database

db = pw.PostgresqlDatabase('database', **set_database)


class AllowedUser(pw.Model):
    # user_id = pw.IntegerField()
    username = pw.CharField(max_length=50)

    class Meta:
        database = db


def create_tables():
    db.create_tables([AllowedUser])
