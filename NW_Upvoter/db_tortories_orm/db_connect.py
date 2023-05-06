
from functools import wraps
from ssl import create_default_context

from tortoise import Tortoise

from work_fs.sertificate_db.path_to_sertificate import path_to_sertificate

path_certificate = path_to_sertificate()
ssl_ctx = create_default_context(cafile=path_certificate)


DATABASE_CONFIG = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "database": "8-core_start_comp",
                "host": "bots-do-user-11731497-0.b.db.ondigitalocean.com",
                "password": "AVNS_XCxtxUH7rZz8txAxKYO",
                "port": 25061,
                "user": "doadmin",
                "statement_cache_size": 0,
                "ssl": ssl_ctx,
            },
        },
    },
    "apps": {
        "models": {
            "models": ["NW_Upvoter.db_tortories_orm.models"],
            "default_connection": "default",
        },
    },
}


async def connect_to_db():
    await Tortoise.init(config=DATABASE_CONFIG)
    await Tortoise.generate_schemas()


async def is_connected():
    try:
        # Виконайте простий запит до бази даних
        await Tortoise.get_connection("default").execute_query("SELECT 1;")
        return True
    except Exception:
        return False


def db_connection_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if not await is_connected():
            await connect_to_db()
        return await func(*args, **kwargs)
    return wrapper
