/*
  Warnings:

  - You are about to drop the column `vcTypeId` on the `ActivityLog` table. All the data in the column will be lost.
  - You are about to drop the column `duration` on the `Session` table. All the data in the column will be lost.
  - Added the required column `activity` to the `ActivityLog` table without a default value. This is not possible if the table is not empty.
  - Added the required column `activityType` to the `ActivityLog` table without a default value. This is not possible if the table is not empty.
  - Added the required column `activity` to the `Session` table without a default value. This is not possible if the table is not empty.

*/
-- DropForeignKey
ALTER TABLE `ActivityLog` DROP FOREIGN KEY `ActivityLog_activityTypeId_fkey`;

-- DropForeignKey
ALTER TABLE `ActivityLog` DROP FOREIGN KEY `ActivityLog_vcTypeId_fkey`;

-- AlterTable
ALTER TABLE `ActivityLog` DROP COLUMN `vcTypeId`,
    ADD COLUMN `activity` VARCHAR(191) NOT NULL,
    ADD COLUMN `activityType` VARCHAR(191) NOT NULL,
    ADD COLUMN `vCTypeId` BIGINT NULL,
    MODIFY `xp` INTEGER NULL,
    MODIFY `activityTypeId` BIGINT NULL;

-- AlterTable
ALTER TABLE `Session` DROP COLUMN `duration`,
    ADD COLUMN `activity` VARCHAR(191) NOT NULL;

-- AddForeignKey
ALTER TABLE `ActivityLog` ADD CONSTRAINT `ActivityLog_activityTypeId_fkey` FOREIGN KEY (`activityTypeId`) REFERENCES `ActivityType`(`id`) ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `ActivityLog` ADD CONSTRAINT `ActivityLog_vCTypeId_fkey` FOREIGN KEY (`vCTypeId`) REFERENCES `VCType`(`id`) ON DELETE SET NULL ON UPDATE CASCADE;
