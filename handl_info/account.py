from work_fs import path_near_exefile, get_list_file, write_list_to_file

from loguru import logger


def get_account_file():
    path_account_file = path_near_exefile('accounts.txt')
    list_accounts = get_list_file(path_account_file)
    for account in list_accounts:
        list_line_content = account.replace(" ", "").split(':')

        logger.info(list_line_content)
        account = {
            'login': list_line_content[0],
            'password': list_line_content[1]
        }

        yield account

        list_accounts.remove(account)
        write_list_to_file(path_account_file, list_accounts)