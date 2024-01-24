from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `session` ALTER COLUMN `joined_at` SET DEFAULT '2024-01-23 15:29:04.407172';
        ALTER TABLE `session` ALTER COLUMN `left_at` SET DEFAULT '2024-01-23 15:29:04.407194';
        ALTER TABLE `sessiondata` MODIFY COLUMN `activity_record_type` VARCHAR(50) NOT NULL  COMMENT 'VC: VC\nSS: SS\nBOTH: BOTH\nCAM: CAM\nNONE: NONE\nLOG: LOG';
        ALTER TABLE `sessionpartial` MODIFY COLUMN `activity_record_type` VARCHAR(50) NOT NULL  COMMENT 'VC: VC\nSS: SS\nBOTH: BOTH\nCAM: CAM\nNONE: NONE\nLOG: LOG';
        ALTER TABLE `sessionpartial` ALTER COLUMN `joined_at` SET DEFAULT '2024-01-23 15:29:04.413545';
        ALTER TABLE `task` ALTER COLUMN `add_date` SET DEFAULT '2024-01-23 15:29:04.418495';
        ALTER TABLE `userserver` ALTER COLUMN `joined_at` SET DEFAULT '2024-01-23 15:29:04.430568';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `session` ALTER COLUMN `joined_at` SET DEFAULT '2024-01-23 14:39:05.853002';
        ALTER TABLE `session` ALTER COLUMN `left_at` SET DEFAULT '2024-01-23 14:39:05.853021';
        ALTER TABLE `sessiondata` MODIFY COLUMN `activity_record_type` VARCHAR(50) NOT NULL  COMMENT 'VC: VC\nSS: SS\nBOTH: BOTH\nVOICE: VOICE\nNONE: NONE\nLOG: LOG';
        ALTER TABLE `sessionpartial` MODIFY COLUMN `activity_record_type` VARCHAR(50) NOT NULL  COMMENT 'VC: VC\nSS: SS\nBOTH: BOTH\nVOICE: VOICE\nNONE: NONE\nLOG: LOG';
        ALTER TABLE `sessionpartial` ALTER COLUMN `joined_at` SET DEFAULT '2024-01-23 14:39:05.859130';
        ALTER TABLE `task` ALTER COLUMN `add_date` SET DEFAULT '2024-01-23 14:39:05.865917';
        ALTER TABLE `userserver` ALTER COLUMN `joined_at` SET DEFAULT '2024-01-23 14:39:05.883329';"""
