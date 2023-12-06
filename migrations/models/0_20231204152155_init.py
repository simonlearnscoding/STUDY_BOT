from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `activityhabit` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL,
    `min_time` INT NOT NULL,
    `suggested_weekly_times` INT NOT NULL,
    `suggested_level` INT NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `activityrewards` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL,
    `done_reward` INT NOT NULL,
    `habit_win_reward` INT NOT NULL,
    `streak_reward` INT NOT NULL,
    `reward_treshold` INT NOT NULL,
    `reward_per_minute` INT NOT NULL,
    `reward_after_treshold` INT NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `pillar` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(10) NOT NULL,
    `description` LONGTEXT,
    `color` VARCHAR(10) NOT NULL  DEFAULT '#000000'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `activity` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL,
    `description` LONGTEXT,
    `creation_date` DATETIME(6) NOT NULL,
    `pillar_id` INT,
    `activity_rewards_id` INT NOT NULL UNIQUE,
    `activity_habit_id` INT NOT NULL UNIQUE,
    CONSTRAINT `fk_activity_pillar_d292e0c6` FOREIGN KEY (`pillar_id`) REFERENCES `pillar` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_activity_activity_cf6a11be` FOREIGN KEY (`activity_rewards_id`) REFERENCES `activityrewards` (`id`) ON DELETE RESTRICT,
    CONSTRAINT `fk_activity_activity_a1b01f7b` FOREIGN KEY (`activity_habit_id`) REFERENCES `activityhabit` (`id`) ON DELETE RESTRICT
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `role` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(30) NOT NULL,
    `level_to_reach_it` INT NOT NULL  DEFAULT 999,
    `description` LONGTEXT,
    `color` VARCHAR(10) NOT NULL  DEFAULT '#000000'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `server` (
    `id` VARCHAR(100) NOT NULL  PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `channel` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL,
    `discord_id` VARCHAR(100) NOT NULL,
    `activity_id` INT,
    `server_id` VARCHAR(100) NOT NULL,
    CONSTRAINT `fk_channel_activity_bced7dbc` FOREIGN KEY (`activity_id`) REFERENCES `activity` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_channel_server_3f305061` FOREIGN KEY (`server_id`) REFERENCES `server` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `tag` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `user` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `discord_id` VARCHAR(100),
    `display_name` VARCHAR(30),
    `timezone` INT   DEFAULT 2,
    `role_id` INT NOT NULL  DEFAULT 1,
    CONSTRAINT `fk_user_role_68c1d370` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `project` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `description` LONGTEXT,
    `start_date` DATETIME(6),
    `end_date` DATETIME(6),
    `priority` VARCHAR(9)   COMMENT 'LOW: LOW\nMEDIUM: MEDIUM\nHIGH: HIGH\nVERY_HIGH: VERY HIGH',
    `user_id` INT NOT NULL,
    CONSTRAINT `fk_project_user_7cc4fc0f` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `session` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `joined_at` DATETIME(6) NOT NULL,
    `server_id` VARCHAR(100),
    `user_id` INT NOT NULL,
    CONSTRAINT `fk_session_server_a36c29b5` FOREIGN KEY (`server_id`) REFERENCES `server` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_session_user_4e399dc8` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `sessiondata` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `activity_record_type` VARCHAR(50) NOT NULL  COMMENT 'CAM: CAM\nSS: SS\nBOTH: BOTH\nVOICE: VOICE\nNONE: NONE\nLOG: LOG',
    `total_record_seconds` INT NOT NULL,
    `percentage_of_total` INT NOT NULL,
    `session_id` INT NOT NULL,
    CONSTRAINT `fk_sessiond_session_a23b48b6` FOREIGN KEY (`session_id`) REFERENCES `session` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `sessionpartial` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `start_time` DATETIME(6) NOT NULL,
    `end_time` DATETIME(6) NOT NULL,
    `is_active` BOOL NOT NULL,
    `total_record_seconds` INT NOT NULL,
    `activity_record_type` VARCHAR(50) NOT NULL  COMMENT 'CAM: CAM\nSS: SS\nBOTH: BOTH\nVOICE: VOICE\nNONE: NONE\nLOG: LOG',
    `session_id` INT NOT NULL,
    CONSTRAINT `fk_sessionp_session_9989a94a` FOREIGN KEY (`session_id`) REFERENCES `session` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `task` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `completed` BOOL NOT NULL  DEFAULT 0,
    `add_date` DATETIME(6) NOT NULL,
    `due_date` DATETIME(6),
    `planned` VARCHAR(10) NOT NULL  COMMENT 'TODAY: TODAY\nTHIS_WEEK: THIS_WEEK\nTHIS_MONTH: THIS_MONTH\nNEXT_MONTH: NEXT_MONTH',
    `priority` VARCHAR(50)   COMMENT 'LOW: LOW\nMEDIUM: MEDIUM\nHIGH: HIGH\nVERY_HIGH: VERY HIGH',
    `project_id` INT,
    `session_id` INT,
    CONSTRAINT `fk_task_project_9f778443` FOREIGN KEY (`project_id`) REFERENCES `project` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_task_session_d92981ac` FOREIGN KEY (`session_id`) REFERENCES `session` (`id`) ON DELETE SET NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `tasktag` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `tag_id` INT NOT NULL,
    `task_id` INT NOT NULL,
    CONSTRAINT `fk_tasktag_tag_a05104bc` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_tasktag_task_55d804a9` FOREIGN KEY (`task_id`) REFERENCES `task` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `userhabits` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `start_date` DATETIME(6) NOT NULL,
    `stopped_date` DATETIME(6) NOT NULL,
    `frequency` INT NOT NULL,
    `completed` BOOL NOT NULL,
    `activity_habit_id` INT NOT NULL,
    `user_id` INT NOT NULL,
    CONSTRAINT `fk_userhabi_activity_9e69acb5` FOREIGN KEY (`activity_habit_id`) REFERENCES `activityhabit` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_userhabi_user_078d1b38` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `userlevel` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `level` INT NOT NULL  DEFAULT 1,
    `xp` INT NOT NULL  DEFAULT 0,
    `pillar_id` INT NOT NULL,
    `user_id` INT NOT NULL,
    CONSTRAINT `fk_userleve_pillar_c3641d66` FOREIGN KEY (`pillar_id`) REFERENCES `pillar` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_userleve_user_4a6589ad` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `userpillar` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `xp` INT NOT NULL  DEFAULT 0,
    `level` INT NOT NULL  DEFAULT 0,
    `pillar_id` INT NOT NULL,
    `user_id` INT NOT NULL,
    CONSTRAINT `fk_userpill_pillar_313721b1` FOREIGN KEY (`pillar_id`) REFERENCES `pillar` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_userpill_user_9bc8b28f` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `userserver` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `joined_at` DATETIME(6) NOT NULL,
    `user_id` INT NOT NULL UNIQUE,
    `server_id` VARCHAR(100) NOT NULL UNIQUE,
    CONSTRAINT `fk_userserv_user_d09f7fdd` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_userserv_server_45cf603b` FOREIGN KEY (`server_id`) REFERENCES `server` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
