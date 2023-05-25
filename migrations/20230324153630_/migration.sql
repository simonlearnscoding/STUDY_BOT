/*
  Warnings:

  - The primary key for the `logsNow` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `guildId` on the `logsNow` table. All the data in the column will be lost.
  - You are about to alter the column `id` on the `logsNow` table. The data in that column could be lost. The data in that column will be cast from `BigInt` to `Int`.

*/
-- AlterTable
ALTER TABLE `logsNow` DROP PRIMARY KEY,
    DROP COLUMN `guildId`,
    MODIFY `id` INTEGER NOT NULL AUTO_INCREMENT,
    MODIFY `type` ENUM('CAM', 'TOTAL', 'LOG', 'SS', 'BOTH', 'VC') NOT NULL,
    MODIFY `userId` BIGINT NOT NULL,
    ADD PRIMARY KEY (`id`);

-- CreateTable
CREATE TABLE `logsDate` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `date` DATETIME(3) NOT NULL,
    `Type` VARCHAR(191) NOT NULL,
    `minutes` INTEGER NOT NULL DEFAULT 0,
    `userId` BIGINT NOT NULL,
    `activityId` INTEGER NOT NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `historicLogs` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `type` ENUM('CAM', 'TOTAL', 'LOG', 'SS', 'BOTH', 'VC') NOT NULL,
    `startedAt` DATETIME(3) NOT NULL,
    `endedAt` DATETIME(3) NOT NULL,
    `userId` BIGINT NOT NULL,
    `activityId` INTEGER NOT NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- AddForeignKey
ALTER TABLE `logsNow` ADD CONSTRAINT `logsNow_userId_fkey` FOREIGN KEY (`userId`) REFERENCES `User`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `logsNow` ADD CONSTRAINT `logsNow_activityId_fkey` FOREIGN KEY (`activityId`) REFERENCES `Activity`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `logsDate` ADD CONSTRAINT `logsDate_userId_fkey` FOREIGN KEY (`userId`) REFERENCES `User`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `logsDate` ADD CONSTRAINT `logsDate_activityId_fkey` FOREIGN KEY (`activityId`) REFERENCES `Activity`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `historicLogs` ADD CONSTRAINT `historicLogs_userId_fkey` FOREIGN KEY (`userId`) REFERENCES `User`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `historicLogs` ADD CONSTRAINT `historicLogs_activityId_fkey` FOREIGN KEY (`activityId`) REFERENCES `Activity`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;
