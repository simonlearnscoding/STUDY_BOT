from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `session` ALTER COLUMN `joined_at` SET DEFAULT '2024-01-23 14:39:00.287842';
        ALTER TABLE `session` ALTER COLUMN `left_at` SET DEFAULT '2024-01-23 14:39:00.287855';
        ALTER TABLE `sessiondata` RENAME COLUMN `total_record_seconds` TO `duration_in_seconds`;
        ALTER TABLE `sessionpartial` ALTER COLUMN `joined_at` SET DEFAULT '2024-01-23 14:39:00.293527';
        ALTER TABLE `task` ALTER COLUMN `add_date` SET DEFAULT '2024-01-23 14:39:00.299687';
        ALTER TABLE `userserver` ALTER COLUMN `joined_at` SET DEFAULT '2024-01-23 14:39:00.316437';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `session` ALTER COLUMN `joined_at` SET DEFAULT '2024-01-23 14:37:33.680129';
        ALTER TABLE `session` ALTER COLUMN `left_at` SET DEFAULT '2024-01-23 14:37:33.680151';
        ALTER TABLE `sessiondata` RENAME COLUMN `duration_in_seconds` TO `total_record_seconds`;
        ALTER TABLE `sessionpartial` ALTER COLUMN `joined_at` SET DEFAULT '2024-01-23 14:37:33.686228';
        ALTER TABLE `task` ALTER COLUMN `add_date` SET DEFAULT '2024-01-23 14:37:33.692389';
        ALTER TABLE `userserver` ALTER COLUMN `joined_at` SET DEFAULT '2024-01-23 14:37:33.709312';"""
