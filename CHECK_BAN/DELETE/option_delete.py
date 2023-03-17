from loguru import logger

from work_fs.PATH import file_exists, path_near_exefile

from database import Cookie
from database.vote_tg_bot.delete import db_delete_cookie_by_id


def delete_account(cookie_obj: Cookie):
    path_cookie = path_near_exefile(cookie_obj.cookie_path)

    logger.info(f"Delete account: {cookie_obj.account.login}:{cookie_obj.account.password}")
    logger.info(f'''Delete proxy: 
            {cookie_obj.proxy.host}:{cookie_obj.proxy.port}:{cookie_obj.proxy.user}:{cookie_obj.proxy.password}''')

    db_delete_cookie_by_id(cookie_obj)

    if file_exists(path_cookie):
        logger.info("Видалений з папки з куками.")
        path_cookie.unlink()  # delete in folder

    logger.info(f'{path_cookie.stem} був видалений з бд.')
