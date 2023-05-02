import asyncio
from pathlib import Path

import aiohttp
from aiohttp import ClientProxyConnectionError
from fake_useragent import UserAgent
from loguru import logger

from base_exception import ProxyInvalidException
from work_fs import path_near_exefile, auto_create, write_line, get_str_file
from work_fs.PATH import delete_dir

FILE_COUNT = 1

RESP_PATH = path_near_exefile("responses")


def del_all_responses():
    delete_dir(RESP_PATH)


async def fetch(session, proxy_link, auth):
    global FILE_COUNT

    url = 'http://httpbin.org/ip'
    async with session.get(url, proxy=proxy_link, proxy_auth=auth,
                           headers={'User-Agent': UserAgent().random}) as response:
        # _____________________________________________________________________ write to file
        html_to_file = await response.text()
        filepath: Path = auto_create(RESP_PATH, _type="dir") / f"output{FILE_COUNT}.html"
        write_line(filepath, html_to_file)
        # ______________________________________________________________________ get from file
        html = get_str_file(filepath)
        FILE_COUNT += 1
        return html


async def check_proxy(host, port, user, password):
    proxy_link = f"http://{host}:{port}"
    auth = aiohttp.BasicAuth(user, password)

    async with aiohttp.ClientSession() as session:
        try:
            html = await fetch(session, proxy_link, auth)

            print(host + " " + html)
            logger.info(f"Successfully connect to {host}:{port}:{user}:{password}")
            del_all_responses()  # __________________________________________________delete all responses
        except TimeoutError:
            logger.error(f"ReadTimeout connect to {host}:{port}:{user}:{password}")
            return check_proxy(host, port, user, password)
        except ClientProxyConnectionError:
            logger.error(f"Щось з проксі {host}:{port}:{user}:{password}! НЕ  відправляє данні на сайт.")
            raise ProxyInvalidException("ProxyError: Invalid proxy ")


if __name__ == '__main__':
    asyncio.run(check_proxy("185.112.12.107", "2831", "34900", "OhOopsbY"))
