import asyncio

from NW_Upvoter.db_tortories_orm.db_connect import db_connection_required
from NW_Upvoter.db_tortories_orm.models import Cookie, RedditLink
from NW_Upvoter.db_tortories_orm.query.bot_accounts import db_update_0_all


@db_connection_required
async def db_about_link():
    link_objs: list[RedditLink] = await RedditLink.all()
    for link_obj in link_objs:
        print(f"""
        id: {link_obj.id}
         date: {link_obj.date}
          tg_name: @{link_obj.tg_name}
           subreddit: {link_obj.subreddit}
            count: {link_obj.count_upvotes}
             link: {link_obj.link} """)


@db_connection_required
async def db_selected_cookies():
    print(f"All cookies: {len(await Cookie.all())}")
    print(f"cookies is selected: {len(await Cookie.filter(is_selected=True))}")
    print(f"cookies is NOT selected: {len(await Cookie.filter(is_selected=False))}")


async def main():
    await db_selected_cookies()
    # await db_update_0_all()
    # await db_about_link()

if __name__ == '__main__':
    asyncio.run(main())
