from tortoise import Tortoise
from utils.error_handler import error_handler


@error_handler
async def init_db_connection():

    await Tortoise.init(
        db_url='mysql://simon:3112@localhost:3306/discordjs',
        modules={'models': ['tortoise_models', 'aerich.models']}
    )
    await Tortoise.generate_schemas()


@error_handler
async def close():
    await Tortoise.close_connections()
