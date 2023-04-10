import asyncio
from pathlib import Path

import aiohttp
from fake_useragent import UserAgent
from loguru import logger

from work_fs.PATH import auto_create
from work_fs.write_to_file import write_line
from work_fs.read_file import get_str_file, get_list_file

COUNT = 1
COUNT_ACCOUNT = 1
DICT_ACC_BAN = {}

ROOT_DIR = Path(__file__).parent


def get_acc_from_file():
    # file = input('Enter your filename(without extension): ') + ".txt"
    file = '142_mix_EU.txt'
    file_lins = get_list_file(ROOT_DIR / file)
    for line in file_lins:
        yield line


def unpack_ban(html):
    permanent = 'suspended' in html
    shadow = 'Sorry, nobody on Reddit goes by that name.' in html

    if permanent:
        ban = "permanent"

    elif shadow:
        ban = "shadow"

    else:
        ban = None

    return ban


def del_all_responses():
    folder_with_resps = ROOT_DIR / "responses"
    folder_with_resps.unlink()


async def fetch(session, url):
    global COUNT

    async with session.get(url, headers={'User-Agent': UserAgent().random}) as response:
        html_to_file = await response.text()
        filepath: Path = auto_create(ROOT_DIR / "responses", _type="dir") / f"output{COUNT}.html"
        write_line(filepath, html_to_file)
        html = get_str_file(filepath)

        COUNT += 1

        if not ('page not found' in html and html is None):
            return html

        logger.error(f"page not found: {url}")
        await asyncio.sleep(2)

        return await fetch(session, url)


async def get_ban(line: str):
    global COUNT_ACCOUNT
    login = line.split(":")[0]

    url = f"https://www.reddit.com/user/{login}"

    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        ban = unpack_ban(html)

        if ban is None:
            # print(f"{COUNT_ACCOUNT}: {line}")
            print(line)
        #     COUNT_ACCOUNT += 1
        # else:
        #     logger.critical(f"{COUNT_ACCOUNT}: {line}: {ban}")
        #     COUNT_ACCOUNT += 1


async def create_task():
    tasks = [asyncio.create_task(get_ban(line)) for line in get_acc_from_file()]
    await asyncio.gather(*tasks)


def check_ban():
    try:
        asyncio.run(create_task())

    finally:
        del_all_responses()

    return DICT_ACC_BAN


if __name__ == '__main__':
    check_ban()

