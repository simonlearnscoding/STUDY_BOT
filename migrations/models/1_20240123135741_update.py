from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `sessionpartial` MODIFY COLUMN `left_at` DATETIME(6);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `sessionpartial` MODIFY COLUMN `left_at` DATETIME(6) NOT NULL;"""
