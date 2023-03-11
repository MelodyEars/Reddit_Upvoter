
from database import Cookie
from database.posting_Actions import dp_ap_create_table, db_ap_create_account_for_posting

from .create_folder import move_cookie, prepare_folder


def create_model(cookie_obj: Cookie):
	model_name = input("Зарееєструй ім'я моделі (щоб тобі було зрозуміло хто це): ")
	old_path_cookie = cookie_obj.cookie_path

	data_path = prepare_folder(model_name)
	new_cookie_path_to_db = move_cookie(data_path, old_path_cookie)

	dp_ap_create_table()
	db_ap_create_account_for_posting(
		model_name=model_name,
		data_path=data_path,
		cookie_path=new_cookie_path_to_db,
		cookie_obj=cookie_obj
	)
