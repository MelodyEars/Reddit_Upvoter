import os
import sys
from ssl import create_default_context
# from pathlib import Path
from tortoise import Tortoise

if getattr(sys, 'frozen', False):
    bundle_dir = sys._MEIPASS
else:
    bundle_dir = os.path.dirname(os.path.abspath(__file__))

path_to_certificate = os.path.join(bundle_dir, 'ca-certificate.crt')
ssl_ctx = create_default_context(cafile=path_to_certificate)

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
                'statement_cache_size': 0,
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
