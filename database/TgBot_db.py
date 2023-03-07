from .models import UserTG, db


def db_add_tg_user(user_id):
	with db:
		UserTG.create(user_id=user_id)


def exists_user(user_id):
	with db:
		result = UserTG.select().where(UserTG.user_id == user_id)
		return bool(len(result))


# def set_nickname(user_id, nickname):
# 	with db:
# 		UserTG.update(nickname=nickname).where(UserTG.user == user_id)

