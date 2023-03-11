from pathlib import Path

from .models_posting import autoposting_db, Proxy, JobModel, Account

from .models import Cookie as Cookie_base_db


def dp_ap_create_table():
    with autoposting_db:
        autoposting_db.create_tables([Proxy, JobModel, Account])


def db_ap_create_account_for_posting(model_name: str, data_path: str, cookie_path: str, cookie_obj: Cookie_base_db):
    with autoposting_db:
        JobModel.create(model_name=model_name, account=cookie_obj.account, proxy=cookie_obj.proxy, data_path=data_path,
                        cookie_path=cookie_path)

        proxy = cookie_obj.proxy
        Proxy.create(host=proxy.host, port=proxy.port, user=proxy.user, password=proxy.password)

        account = cookie_obj.account
        Account.create(login=account.login, password=account.password)
