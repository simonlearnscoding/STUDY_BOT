from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `session` ALTER COLUMN `joined_at` SET DEFAULT '2024-01-23 17:43:48.739172';
        ALTER TABLE `session` MODIFY COLUMN `left_at` DATETIME(6);
        ALTER TABLE `session` ALTER COLUMN `left_at` DROP DEFAULT;
        ALTER TABLE `sessionpartial` ALTER COLUMN `joined_at` SET DEFAULT '2024-01-23 17:43:48.744824';
        ALTER TABLE `task` ALTER COLUMN `add_date` SET DEFAULT '2024-01-23 17:43:48.749875';
        ALTER TABLE `userserver` ALTER COLUMN `joined_at` SET DEFAULT '2024-01-23 17:43:48.763622';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `session` ALTER COLUMN `joined_at` SET DEFAULT '2024-01-23 15:29:07.877767';
        ALTER TABLE `session` MODIFY COLUMN `left_at` DATETIME(6) NOT NULL  DEFAULT '2024-01-23 15:29:07.877785';
        ALTER TABLE `session` ALTER COLUMN `left_at` SET DEFAULT '2024-01-23 15:29:07.877785';
        ALTER TABLE `sessionpartial` ALTER COLUMN `joined_at` SET DEFAULT '2024-01-23 15:29:07.884792';
        ALTER TABLE `task` ALTER COLUMN `add_date` SET DEFAULT '2024-01-23 15:29:07.890820';
        ALTER TABLE `userserver` ALTER COLUMN `joined_at` SET DEFAULT '2024-01-23 15:29:07.905126';"""
