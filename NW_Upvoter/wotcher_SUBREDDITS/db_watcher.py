import asyncio

from colorama import init, deinit

from NW_Upvoter.db_tortories_orm.db_connect import db_connection_required
from NW_Upvoter.db_tortories_orm.models import RedditLink
from work_fs.color import green_color, magenta_color
from work_fs.PATH import path_near_exefile
from work_fs.read_file import get_list_file


# ___________________________________________  file  _______________________________________________________
def name_subreddit_from_file():
    """Get all links from file."""
    path_to_file = path_near_exefile('list_reddit.txt')
    subs_from_file = get_list_file(path_to_file)
    return subs_from_file


# ___________________________________________  db  _________________________________________________________
@db_connection_required
async def get_all_data_from_db() -> set[str]:
    all_link_objs = await RedditLink.all()
    unique_list_link = set([link_obj.link for link_obj in all_link_objs])

    return unique_list_link


# ___________________________________________  print  _________________________________________________________
async def pars_name_reddit():
    """Get all links from database and print them."""
    unique_list_link: set[str] = await get_all_data_from_db()
    subs_from_file = name_subreddit_from_file()
    print(magenta_color('Point on the subreddit names are not in the file:'))
    for link in unique_list_link:
        name_subreddit = link.split('/')[4]
        if name_subreddit not in subs_from_file:

            print(f"{green_color(name_subreddit)}")


if __name__ == '__main__':
    try:
        init()
        asyncio.run(pars_name_reddit())
        deinit()
    finally:
        input('Done!')
