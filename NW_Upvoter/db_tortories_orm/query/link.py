import asyncio

from NW_Upvoter.db_tortories_orm.models import RedditLink
from NW_Upvoter.db_tortories_orm.db_connect import connect_to_db, db_connection_required


# ___________________________________________  create  _________________________________________________________
@db_connection_required
async def db_get_or_create_link_obj(link: str):
    """Get or create link id from database"""
    link_obj, _ = await RedditLink.get_or_create(link=link)
    return link_obj


# @db_connection_required
# async def db_work():
#     url = 'https://www.reddit.com/r/OnlyCurvyGW/comments/130cl4s/am_i_wifey_girlfriend_or_one_night_stand_material/'
#     await connect_to_db()
#     result = await db_get_or_create_link_obj(url)
#     print(result.link)
#
#
# if __name__ == '__main__':
#     asyncio.run(db_work())
