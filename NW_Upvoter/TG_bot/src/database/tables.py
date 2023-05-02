import peewee as pw

db = pw.SqliteDatabase('app.db')


class AllowedUser(pw.Model):
    # user_id = pw.IntegerField()
    username = pw.CharField(max_length=50)

    class Meta:
        database = db


def create_tables_user_tg():
    db.create_tables([AllowedUser])
