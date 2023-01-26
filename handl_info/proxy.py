import requests

from loguru import logger
from work_fs import write_line


def check_proxy(host, port, user, password):
    # proxies = {"http": "http://username:password@proxy_ip:proxy_port"}
    proxies = {"http": f"http://{user}:{password}@{host}:{port}"}
    print(proxies)
    try:
        requests.get("http://www.example.com/", proxies=proxies)
        working_proxy = True
    except Exception as ex:
        logger.error(ex)
        write_line("proxy_invalid.txt", ":".join((host, port, user, password)))
        working_proxy = False

    return working_proxy
