import requests

from loguru import logger

import work_fs as wf


def check_proxy(host, port, user, password):
    # proxies = {"http": "http://username:password@proxy_ip:proxy_port"}
    proxies = {"http": f"http://{user}:{password}@{host}:{port}"}
    print(proxies)
    try:
        requests.get("https://www.reddit.com/", proxies=proxies)
    except Exception as ex:
        logger.error(ex)
        wf.write_line("proxy_invalid.txt", ":".join((host, port, user, password)))
        raise ProxyInvalid
