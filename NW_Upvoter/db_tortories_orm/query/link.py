from NW_Upvoter.db_tortories_orm.models import RedditLink
from NW_Upvoter.db_tortories_orm.db_connect import db_connection_required


# ___________________________________________  create  _________________________________________________________
@db_connection_required
async def db_get_or_create_link_obj(link: str, who_posted: str, sub: str, count_upvotes: int, reveddit_url: str):
    """Get or create link id from database"""
    link_obj, created = await RedditLink.get_or_create(
        link=link,
        tg_name=who_posted,
        subreddit=sub,
        count_upvotes=count_upvotes,
        reveddit_url=reveddit_url
    )
    return link_obj, created


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
