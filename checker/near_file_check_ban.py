import asyncio
from pathlib import Path

import aiohttp
from fake_useragent import UserAgent
from loguru import logger

from NW_Upvoter.db_tortories_orm.db_connect import db_connection_required
from NW_Upvoter.db_tortories_orm.models import Account, Proxy
from work_fs.PATH import auto_create, path_near_exefile
from work_fs.write_to_file import write_line
from work_fs.read_file import get_str_file, get_list_file

FILE_COUNT = 1
COUNT_ACCOUNT = 0
COUNT_ACCOUNT_BAN = 0
ROOT_DIR = Path(__file__).parent

NOT_UPVOTED = [
    'Charming-Resource202',
    'Far-Chef9170',
    'Kindly_Tackle_6367',

]

@db_connection_required
async def get_accounts_from_db() -> list:
    accounts = await Account.all()

    logins_from_db = [obj.login for obj in accounts]
    return logins_from_db


def get_acc_from_file(WORK_LOGIN):
    # file = input('Enter your filename(without extension): ') + ".txt"
    # filepath = path_near_exefile('accounts.txt')
    filepath = ROOT_DIR / 'accounts.txt'
    print(filepath)
    file_lins = get_list_file(filepath)
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
    # folder_with_resps = path_near_exefile("responses")
    folder_with_resps = ROOT_DIR / "responses"
    folder_with_resps.unlink()


async def fetch(session, url):
    global FILE_COUNT

    async with session.get(url, headers={'User-Agent': UserAgent().random}) as response:
        # await asyncio.sleep(0.3)
        filepath: Path = auto_create(ROOT_DIR / "responses", _type="dir") / f"output{FILE_COUNT}.html"
        html_to_file = await response.text()

        write_line(filepath, html_to_file)
        html = get_str_file(filepath)

        FILE_COUNT += 1

        if not ('page not found' in html and html is None):
            return html

        logger.error(f"page not found: {url}")
        await asyncio.sleep(2)

        return await fetch(session, url)


async def get_ban(login: str, password: str):
    global COUNT_ACCOUNT, COUNT_ACCOUNT_BAN

    url = f"https://www.reddit.com/user/{login}"

    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        ban = unpack_ban(html)
    #############################################################################
        if ban is None:
            # print(f"{COUNT_ACCOUNT}: {login}")
            print(f"{login}:{password}")
            COUNT_ACCOUNT += 1
        else:
            COUNT_ACCOUNT_BAN += 1
        #     logger.critical(f"{COUNT_ACCOUNT}: {login}: {ban}")
        #     COUNT_ACCOUNT += 1
    ##############################################################################


async def create_task():
    WORK_LOGIN = await get_accounts_from_db() + NOT_UPVOTED
    # WORK_LOGIN = []
    tasks = [asyncio.create_task(get_ban(login, password)) for login, password in get_acc_from_file(WORK_LOGIN)]

    for task in tasks:
        await task
    # await asyncio.gather(*tasks)

@logger.catch
def check_ban():
    try:
        asyncio.run(create_task())
        print(f"norm: {COUNT_ACCOUNT}")
        print(f"in ban {COUNT_ACCOUNT_BAN}")

    finally:
        del_all_responses()
        input("Press Enter to close.")

# check if account from file in db


# def same_account_from_list():
#     db_accounts = get_accounts_from_db()
#     for login, password in get_acc_from_file():
#         if login in db_accounts:
#             logger.critical(login)
#         else:
#             print(f"{login}:{password}")

# @db_connection_required
# async def get_account_pwd():
#     # accounts = await Account.all()
#     # for obj in accounts:
#     #     print(f"{obj.id}:{obj.login}:{obj.password}")
#
#     proxy = await Proxy.get(id=60)
#     print(f"{proxy.host}:{proxy.port}:{proxy.user}:{proxy.password}")

def sort_same_account():
    filepath = ROOT_DIR / 'accounts.txt'
    file_lins = get_list_file(filepath)

    print(f'before: {len(file_lins)}')
    file_lins = list(set(file_lins))
    print(f'after: {len(file_lins)}')

    write_line(filepath, file_lins)


if __name__ == '__main__':
    check_ban()
    # sort_same_account()
    # same_account_from_list()
    # asyncio.run(get_account_pwd())
