from .models_posting import autoposting_db, Proxy, JobModel, Account

from database.vote_tg_bot.models import Cookie as Cookie_base_db


def dp_ap_create_table():
    with autoposting_db:
        autoposting_db.create_tables([Proxy, JobModel, Account])


def db_ap_create_account_for_posting(model_name: str, data_path: str, cookie_path: str, cookie_obj: Cookie_base_db):
    with autoposting_db:
        old_proxy = cookie_obj.proxy
        proxy = Proxy.create(host=old_proxy.host, port=old_proxy.port, user=old_proxy.user, password=old_proxy.password)

        old_account = cookie_obj.account
        account = Account.create(login=old_account.login, password=old_account.password)

        JobModel.create(model_name=model_name, account=account, proxy=proxy, data_path=data_path,
                        cookie_path=cookie_path)

