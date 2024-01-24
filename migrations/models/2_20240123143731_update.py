from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `session` ADD `duration_in_seconds` INT NOT NULL  DEFAULT 0;
        ALTER TABLE `sessionpartial` ALTER COLUMN `joined_at` SET DEFAULT '2024-01-23 14:37:31.601447';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `session` DROP COLUMN `duration_in_seconds`;
        ALTER TABLE `sessionpartial` ALTER COLUMN `joined_at` DROP DEFAULT;"""
