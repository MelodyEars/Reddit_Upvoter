import requests

from loguru import logger

from work_fs import write_line, path_near_exefile, get_list_file
from base_exception import ProxyInvalidException


def check_proxy(host, port, user, password):
    # proxies = {"http": "http://username:password@proxy_ip:proxy_port"}
    proxies = {"http": f"http://{user}:{password}@{host}:{port}"}
    try:
        requests.get("https://www.reddit.com/", proxies=proxies)
    except Exception as ex:
        logger.error(ex)
        write_line("proxy_invalid.txt", ":".join((host, port, user, password)))
        raise ProxyInvalidException


def file_get_proxy():
    path_proxies_file = path_near_exefile('proxies.txt')
    list_proxies = get_list_file(path_proxies_file)

    try:
        list_line_content = list_proxies.pop(0).replace(" ", "").split(':')
    except IndexError:
        raise Exception('Не достаточно прокси!')

    logger.info(list_line_content)

    proxy_for_api = {
        'host': list_line_content[0],
        'port': list_line_content[1],
        'user': list_line_content[2],
        'password': list_line_content[3]
    }

    if check_proxy(**proxy_for_api):
        return proxy_for_api, list_proxies, path_proxies_file
    else:
        file_get_proxy()

