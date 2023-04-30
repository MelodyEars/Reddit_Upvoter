import ssl
from pathlib import Path

from tortoise import Tortoise


path_to_certificate = str(Path(__file__).parent / 'ca-certificate.crt')
ssl_ctx = ssl.create_default_context(cafile=path_to_certificate)

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
                "ssl": ssl_ctx,
            },
        },
    },
    "apps": {
        "models": {
            "models": ["Uprove_TG_Bot.db_tortories_orm.models"],
            "default_connection": "default",
        },
    },
}


async def connect_to_db():
    await Tortoise.init(config=DATABASE_CONFIG)
    await Tortoise.generate_schemas()
