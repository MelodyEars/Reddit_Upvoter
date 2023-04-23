import asyncio
import json
from pathlib import Path

import aiohttp
from fake_useragent import UserAgent
from pydantic import BaseModel
from loguru import logger

from work_fs.PATH import auto_create
from work_fs.write_to_file import write_line
from work_fs.read_file import get_str_file, get_list_file

FILE_COUNT = 1

ROOT_DIR = Path(__file__).parent
DICT_ID_INFO = {}


# _______________________________________________________________________ pydantic
# class IpInfo(BaseModel):
#     ip: str
#     hostname: str | None
#     city: str
#     region: str
#     country: str
#     loc: str
#     org: str
#     postal: str
#     timezone: str
#     readme: str

# _______________________________________________________________________ from file
def get_proxy_from_file():
    # 165	"216.73.159.44"	"10047"	"modeler_kDmcKT"	"GFks5gG4KoLV"
    # ['165\t', '216.73.159.44', '\t', '10047', '\t', 'modeler_kDmcKT', '\t', 'GFks5gG4KoLV', '']
    file = "proxy_list.txt"
    file_lins = get_list_file(ROOT_DIR / file)
    for line in file_lins:
        # line_in_list = line.split('"')
        # db_id = line_in_list[0].strip()
        # host: str = line_in_list[1]
        # port = line_in_list[3]
        # user = line_in_list[5]
        # password = line_in_list[7]

        # list ":"
        line_in_list = line.split(':')
        host = line_in_list[0]
        port = line_in_list[1]
        user = line_in_list[2]
        password = line_in_list[3]
        proxy_link = f"http://{host}:{port}"
        auth = aiohttp.BasicAuth(user, password)
        proxy_view = f"{host}:{port}:{user}:{password}"
        yield proxy_view, proxy_link, auth


# ____________________________________________________________________________________ Connect to ipinfo
# def proxy_data(proxy_link: str):
#     url = "http://ipinfo.io/json"
#
#     try:
#         resp = requests.get(url, proxies=proxy_link, timeout=10)
#
#     except ProxyError:
#         logger.error(f"Щось з проксі {proxy['user']}:{proxy['password']}:{proxy['host']}:{proxy['port']}!")
#         raise ProxyInvalidException("ProxyError: Invalid proxy ")
#     logger.info(resp)
#     return resp


async def ipinfo(session: aiohttp.ClientSession, proxy_link: str, auth: aiohttp.BasicAuth):
    global FILE_COUNT
    url = "http://ipinfo.io/json"

    async with session.get(url, proxy=proxy_link, proxy_auth=auth, headers={'User-Agent': UserAgent().random}) as response:
        # write to file
        html_to_file = await response.text()
        filepath: Path = auto_create(ROOT_DIR / "responses", _type="dir") / f"output{FILE_COUNT}.html"
        write_line(filepath, html_to_file)
        # get from file
        html = get_str_file(filepath)
        FILE_COUNT += 1
        return html
        # if not ('page not found' in html and html is None):
        #     return html
        #
        # logger.error(f"page not found: {url}")
        # await asyncio.sleep(2)
        #
        # return await ipinfo(session, proxy_link, auth)


async def about_proxy(db_id, proxy_link, auth):
    async with aiohttp.ClientSession() as session:
        html = await ipinfo(session, proxy_link, auth)
        # ip_info = IpInfo.parse_raw(html)
        json_obj = json.loads(html)
        # print(f"{db_id}: {json_obj['loc']}")
        print(html)
        try:
            DICT_ID_INFO[db_id] = json_obj['hostname']
            # print(f"{db_id}: {json_obj['hostname']}")
        except KeyError:
            DICT_ID_INFO[db_id] = ""
            # logger.critical(db_id)

# {
#   "ip": "216.73.159.44",
#   "city": "Valdivia",
#   "region": "Los Ríos Region",
#   "country": "CL",
#   "loc": "-39.8142,-73.2459", ---- uf1
#   "org": "AS61138 Zappie Host LLC",
#   "postal": "5090000",
#   "timezone": "America/Santiago",
#   "readme": "https://ipinfo.io/missingauth"
# }

# {
#   "ip": "167.179.91.8",
#   "hostname": "167.179.91.8.vultrusercontent.com",   ---- uf2
#   "city": "Ōi",
#   "region": "Saitama",
#   "country": "JP",
#   "loc": "35.6090,139.7302",
#   "org": "AS20473 The Constant Company, LLC",
#   "postal": "140-8508",
#   "timezone": "Asia/Tokyo",
#   "readme": "https://ipinfo.io/missingauth"
# }


async def create_task():
    tasks = [asyncio.create_task(about_proxy(db_id, proxy_link, auth)) for db_id, proxy_link, auth in get_proxy_from_file()]
    await asyncio.gather(*tasks)


def run():
    asyncio.run(create_task())
    same_count = 0
    different_count = 0
    for id_db, location in DICT_ID_INFO.items():
        if location:
        # if list(DICT_ID_INFO.values()).count(location) > 1 or location is not None:
            logger.critical(f"{id_db}: {location}")
            same_count += 1
        else:
            print(f"{id_db}: {location}")
            different_count += 1

    print(f"different count: {different_count}")
    print(f"same count: {same_count}")
    print(len(DICT_ID_INFO))


if __name__ == '__main__':
    run()

