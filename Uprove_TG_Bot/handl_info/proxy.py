import requests

from loguru import logger
from requests.exceptions import ProxyError, ReadTimeout

from base_exception import ProxyInvalidException
from work_fs import path_near_exefile, get_list_file, write_list_to_file


def check_proxy(host, port, user, password):
    proxies = {"http": f"http://{user}:{password}@{host}:{port}"}
    # url = "http://ipinfo.io/json"
    url = 'http://httpbin.org/ip'

    try:
        response = requests.get(url, proxies=proxies, timeout=10)
        print(host + response.text)
        logger.info(f"Successfully connect to {host}:{port}:{user}:{password}")
    except ReadTimeout:
        logger.error(f"ReadTimeout connect to {host}:{port}:{user}:{password}")
        return check_proxy(host, port, user, password)
    except ProxyError:
        logger.error(f"Щось з проксі {host}:{port}:{user}:{password}! НЕ  відправляє данні на сайт.")
        raise ProxyInvalidException("ProxyError: Invalid proxy ")


def file_get_proxy():
    path_proxies_file = path_near_exefile('proxies.txt')
    list_proxies = get_list_file(path_proxies_file)
    print(list_proxies)

    try:
        line_content = list_proxies.pop(-1)
        list_line_content = line_content.replace(" ", "").split(':')
        logger.info(f"Get proxy {list_line_content}")
    except IndexError:
        raise ProxyInvalidException('Недостатньо проксі!')

    proxy_for_api = {
        'host': list_line_content[0],
        'port': list_line_content[1],
        'user': list_line_content[2],
        'password': list_line_content[3]
    }

    try:
        check_proxy(**proxy_for_api)
        return proxy_for_api, list_proxies, path_proxies_file
    except ProxyInvalidException:
        list_line_content.insert(0, line_content)
        write_list_to_file(path_proxies_file, list_proxies)
        return file_get_proxy()


if __name__ == '__main__':
    check_proxy("62.109.29.75", "12296", "modeler_ZBzURk", "RqF3o1B9EDKr")
