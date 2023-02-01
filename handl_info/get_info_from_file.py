import requests

import work_fs as wf

from loguru import logger


def check_proxy(host, port, user, password):
    # proxies = {"http": "http://username:password@proxy_ip:proxy_port"}
    proxies = {"http": f"http://{user}:{password}@{host}:{port}"}
    print(proxies)
    try:
        requests.get("https://www.reddit.com/", proxies=proxies)
        working_proxy = True
    except Exception as ex:
        logger.error(ex)
        wf.write_line("proxy_invalid.txt", ":".join((host, port, user, password)))
        working_proxy = False

    return working_proxy


def get_proxy():
    path_proxy_file = wf.path_near_exefile('proxies.txt')
    list_proxies = wf.getter_file_list(path_proxy_file)

    try:
        list_line_content = list_proxies.pop(0).replace(" ", "").split(':')
    except IndexError:
        raise Exception('Не достаточно прокси!')

    logger.info(list_line_content)

    proxy = {
        'host': list_line_content[0],
        'port': list_line_content[1],
        'user': list_line_content[2],
        'password': list_line_content[3]
    }

    if check_proxy(**proxy):
        return proxy, list_proxies, path_proxy_file
    else:
        get_proxy()


def get_account():
    path_account_file = wf.path_near_exefile('accounts.txt')
    list_accounts = wf.getter_file_list(path_account_file)
    for account in list_accounts:
        list_line_content = account.replace(" ", "").split(':')

        logger.info(list_line_content)
        account = {
            'login': list_line_content[0],
            'password': list_line_content[1]
        }

        yield account


if __name__ == '__main__':
    print(get_proxy())
