import asyncio
from pathlib import Path

import aiohttp
from fake_useragent import UserAgent
from loguru import logger

from SETTINGS import db
from database import Cookie
from work_fs.PATH import auto_create
from work_fs.write_to_file import write_line
from work_fs.read_file import get_str_file, get_list_file

FILE_COUNT = 1
COUNT_ACCOUNT = 1


ROOT_DIR = Path(__file__).parent
WORK_LOGIN = [
    'antoncazey', 'kirillorlovmae', 'mukhibzhon7wxrk', 'aslanbegbtxs', 'konstantinqkb', 'ldmilalykhin8h4c',
    'vass-belyakov', 'sergeyfnhburov', 'vakikcn3sayko', 'vadimfszgl', 'antonina-ponomareva', 'zina-semenova',
    'sveta-sveta-orlova', 'vichka_kalinina', 'raisa_davydo', 'sofiyaguseva1979', 'aleksandra-petukhova',
    'dasha_dasha_fedorova', 'katerinkafedotova', 'sofa-semenova-'
]


def get_acc_from_file():
    # file = input('Enter your filename(without extension): ') + ".txt"
    file = '142_mix_EU.txt'
    file_lins = get_list_file(ROOT_DIR / file)
    for line in file_lins:
        login = line.split(":")[0]
        password = line.split(":")[1]

        if login not in WORK_LOGIN:
            yield login, password


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
    global FILE_COUNT

    async with session.get(url, headers={'User-Agent': UserAgent().random}) as response:
        html_to_file = await response.text()
        filepath: Path = auto_create(ROOT_DIR / "responses", _type="dir") / f"output{FILE_COUNT}.html"
        write_line(filepath, html_to_file)
        html = get_str_file(filepath)

        FILE_COUNT += 1

        if not ('page not found' in html and html is None):
            return html

        logger.error(f"page not found: {url}")
        await asyncio.sleep(2)

        return await fetch(session, url)


async def get_ban(login: str, password: str):
    global COUNT_ACCOUNT

    url = f"https://www.reddit.com/user/{login}"

    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        ban = unpack_ban(html)
    #############################################################################
        if ban is None:
            # print(f"{COUNT_ACCOUNT}: {login}")
            print(f"{login}:{password}")
            # COUNT_ACCOUNT += 1
        # else:
        #     logger.critical(f"{COUNT_ACCOUNT}: {login}: {ban}")
        #     COUNT_ACCOUNT += 1
    ##############################################################################


async def create_task():
    tasks = [asyncio.create_task(get_ban(login, password)) for login, password in get_acc_from_file()]
    await asyncio.gather(*tasks)


def check_ban():
    try:
        asyncio.run(create_task())

    finally:
        del_all_responses()


# check if account from file in db
def get_accounts_from_db():
    with db:
        cookies_db_objs = Cookie.select().where((Cookie.is_selected == False) & (Cookie.ban.is_null(True)))
        print(len(cookies_db_objs))
    logins_from_db = [obj.account.login for obj in cookies_db_objs]
    return logins_from_db


def same_account_from_list():
    db_accounts = get_accounts_from_db()
    for login, password in get_acc_from_file():
        if login in db_accounts:
            logger.critical(login)
        else:
            print(f"{login}:{password}")


if __name__ == '__main__':
    check_ban()
    # same_account_from_list()
