import asyncio

from Uprove_TG_Bot.db_tortories_orm.db_connect import connect_to_db
from Uprove_TG_Bot.db_tortories_orm.models import RedditLink


# ___________________________________________  create  _________________________________________________________
async def db_get_link_id(link: str):
    """Get or create link id from database"""
    link_id = await RedditLink.get_or_create(link=link)
    return link_id[0].id


async def db_work():
    url = 'https://www.reddit.com/r/OnlyCurvyGW/comments/130cl4s/am_i_wifey_girlfriend_or_one_night_stand_material/'
    await connect_to_db()
    result = await db_get_link_id(url)
    print(result)


# def main():
#     # task = asyncio.create_task(db_work())
#     asyncio.gather(db_work())


if __name__ == '__main__':
    asyncio.run(db_work())

