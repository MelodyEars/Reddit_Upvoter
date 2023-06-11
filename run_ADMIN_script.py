import asyncio

from loguru import logger

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
             username reddit: {link_obj.reveddit_url} 
              link: {link_obj.link} """
              )


@db_connection_required
async def db_selected_cookies():
    print(f"All cookies: {len(await Cookie.all())}")
    print(f"cookies is selected: {len(await Cookie.filter(is_selected=True))}")
    print(f"cookies is NOT selected: {len(await Cookie.filter(is_selected=False))}")


@db_connection_required
async def db_delete_link():
    link_obj = await RedditLink.get(link='https://www.reddit.com/r/fuckdoll/comments/1453umr/i_dream_to_be_your_fuckdoll_247/')
    # link_objs = await RedditLink.all()
    # for link_obj in link_objs:
    #     print(f"id {link_obj.id} link {link_obj.link}")
    await link_obj.delete()


@db_connection_required
async def db_print_selected_accounts():
    selected_objs = await Cookie.filter(is_selected=True).prefetch_related("proxy",  "work_accounts", "account")
    for obj in selected_objs:
        print(f"""
        id: {obj.id}
         is_selected: {obj.is_selected}
          proxy: {obj.proxy.host}:{obj.proxy.port}:{obj.proxy.user}:{obj.proxy.password}
            host {obj.proxy.host}
            port {obj.proxy.port}
            
           account: {obj.account.login}:{obj.account.password}
             ban: {obj.ban} 
              """)


@logger.catch
async def main():
    # await db_print_selected_accounts()
    await db_selected_cookies()
    await db_update_0_all()
    # await db_about_🪖🇺🇦link()
    # await db_delete_link()


if __name__ == '__main__':
    asyncio.run(main())



