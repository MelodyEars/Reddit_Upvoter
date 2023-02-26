from work_fs import path_near_exefile, get_list_file, write_list_to_file

from loguru import logger


def get_account_file():
    path_account_file = path_near_exefile('accounts.txt')

    while list_accounts := get_list_file(path_account_file):
        account_line = list_accounts.pop()
        list_line_content = account_line.replace(" ", "").split(':')

        logger.info(list_line_content)
        account = {
            'login': list_line_content[0],
            'password': list_line_content[1]
        }

        try:
            yield account
        finally:
            write_list_to_file(path_account_file, list_accounts)
