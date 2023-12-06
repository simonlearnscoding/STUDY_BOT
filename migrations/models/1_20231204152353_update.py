from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `channel` ADD `channel_type` VARCHAR(50) NOT NULL  COMMENT 'LEADERBOARD: LEADERBOARD\nTASKS: TASKS\nVOICE: VOICE\nTEXT: TEXT';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `channel` DROP COLUMN `channel_type`;"""
