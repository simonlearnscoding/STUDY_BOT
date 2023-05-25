/*
  Warnings:

  - You are about to drop the column `bot` on the `User` table. All the data in the column will be lost.
  - You are about to drop the `LevelRole` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `historicLogs` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `logsDate` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `logsNow` table. If the table is not empty, all the data it contains will be lost.

*/
-- DropForeignKey
ALTER TABLE `historicLogs` DROP FOREIGN KEY `historicLogs_userId_fkey`;

-- DropForeignKey
ALTER TABLE `logsDate` DROP FOREIGN KEY `logsDate_userId_fkey`;

-- DropForeignKey
ALTER TABLE `logsNow` DROP FOREIGN KEY `logsNow_userId_fkey`;

-- AlterTable
ALTER TABLE `User` DROP COLUMN `bot`,
    MODIFY `id` BIGINT NOT NULL AUTO_INCREMENT;

-- DropTable
DROP TABLE `LevelRole`;

-- DropTable
DROP TABLE `historicLogs`;

-- DropTable
DROP TABLE `logsDate`;

-- DropTable
DROP TABLE `logsNow`;

-- CreateTable
CREATE TABLE `ActivityType` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(191) NOT NULL,
    `pillar` ENUM('THINKER', 'DISCIPLINE', 'PHYSICAL_WORK') NOT NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `VCType` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(191) NOT NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `Session` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `joinedAt` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    `leftAt` DATETIME(3) NULL,
    `duration` INTEGER NOT NULL DEFAULT 0,
    `userId` BIGINT NOT NULL,
    `status` ENUM('ONGOING', 'COMPLETED') NOT NULL DEFAULT 'ONGOING',

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `ActivityLog` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `joinedAt` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    `leftAt` DATETIME(3) NULL,
    `duration` INTEGER NOT NULL DEFAULT 0,
    `xp` INTEGER NOT NULL,
    `status` ENUM('ONGOING', 'COMPLETED') NOT NULL DEFAULT 'ONGOING',
    `userId` BIGINT NOT NULL,
    `sessionId` BIGINT NOT NULL,
    `activityTypeId` BIGINT NOT NULL,
    `vcTypeId` BIGINT NOT NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `UserLevel` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `pillar` ENUM('THINKER', 'DISCIPLINE', 'PHYSICAL_WORK') NOT NULL,
    `level` INTEGER NOT NULL DEFAULT 1,
    `xp` INTEGER NOT NULL DEFAULT 0,
    `userId` BIGINT NOT NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `Role` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(191) NOT NULL,
    `minLevel` INTEGER NOT NULL,
    `pillar` ENUM('THINKER', 'DISCIPLINE', 'PHYSICAL_WORK') NOT NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- AddForeignKey
ALTER TABLE `Session` ADD CONSTRAINT `Session_userId_fkey` FOREIGN KEY (`userId`) REFERENCES `User`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `ActivityLog` ADD CONSTRAINT `ActivityLog_userId_fkey` FOREIGN KEY (`userId`) REFERENCES `User`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `ActivityLog` ADD CONSTRAINT `ActivityLog_sessionId_fkey` FOREIGN KEY (`sessionId`) REFERENCES `Session`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `ActivityLog` ADD CONSTRAINT `ActivityLog_activityTypeId_fkey` FOREIGN KEY (`activityTypeId`) REFERENCES `ActivityType`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `ActivityLog` ADD CONSTRAINT `ActivityLog_vcTypeId_fkey` FOREIGN KEY (`vcTypeId`) REFERENCES `VCType`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `UserLevel` ADD CONSTRAINT `UserLevel_userId_fkey` FOREIGN KEY (`userId`) REFERENCES `User`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;
