-- CreateTable
CREATE TABLE `User` (
    `id` INTEGER NOT NULL,
    `name` VARCHAR(191) NOT NULL,
    `bot` BOOLEAN NOT NULL,
    `nick` VARCHAR(191) NOT NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `Activity` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(191) NOT NULL,

    UNIQUE INDEX `Activity_id_key`(`id`),
    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `ActivityRewards` (
    `activityID` INTEGER NOT NULL,
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `rewardMinute` INTEGER NOT NULL,
    `rewardMinuteCam` INTEGER NOT NULL,
    `rewardMinuteLog` INTEGER NOT NULL,
    `RewardStreak` INTEGER NOT NULL,
    `RewardRestart` INTEGER NOT NULL,
    `rewardMin` INTEGER NOT NULL,
    `rewardMax` INTEGER NOT NULL,
    `reward` INTEGER NOT NULL,

    UNIQUE INDEX `ActivityRewards_activityID_key`(`activityID`),
    UNIQUE INDEX `ActivityRewards_id_key`(`id`),
    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `logsNow` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `timestamp` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    `type` ENUM('CAM', 'LOG', 'SS', 'BOTH', 'VC') NOT NULL,
    `userId` INTEGER NOT NULL,
    `activityId` INTEGER NOT NULL,
    `guildId` VARCHAR(191) NOT NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `LevelRole` (
    `name` ENUM('GLADIATOR', 'FREEDMAN', 'PLEBEIAN', 'PATRICIAN', 'SENATOR', 'CONSUL', 'EMPEROR') NOT NULL,
    `minlevel` INTEGER NOT NULL,

    PRIMARY KEY (`name`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- AddForeignKey
ALTER TABLE `ActivityRewards` ADD CONSTRAINT `ActivityRewards_activityID_fkey` FOREIGN KEY (`activityID`) REFERENCES `Activity`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;
