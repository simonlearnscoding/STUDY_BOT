/*
  Warnings:

  - The primary key for the `LevelRole` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - The values [FREEDMAN] on the enum `LevelRole_name` will be removed. If these variants are still used in the database, this will fail.
  - You are about to drop the column `activityId` on the `logsNow` table. All the data in the column will be lost.
  - You are about to drop the `Activity` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `ActivityRewards` table. If the table is not empty, all the data it contains will be lost.
  - Added the required column `activity` to the `historicLogs` table without a default value. This is not possible if the table is not empty.
  - Added the required column `activity` to the `logsDate` table without a default value. This is not possible if the table is not empty.
  - Added the required column `activity` to the `logsNow` table without a default value. This is not possible if the table is not empty.

*/
-- DropForeignKey
ALTER TABLE `ActivityRewards` DROP FOREIGN KEY `ActivityRewards_activityID_fkey`;

-- DropForeignKey
ALTER TABLE `historicLogs` DROP FOREIGN KEY `historicLogs_activityId_fkey`;

-- DropForeignKey
ALTER TABLE `logsDate` DROP FOREIGN KEY `logsDate_activityId_fkey`;

-- DropForeignKey
ALTER TABLE `logsNow` DROP FOREIGN KEY `logsNow_activityId_fkey`;

-- AlterTable
ALTER TABLE `LevelRole` DROP PRIMARY KEY,
    MODIFY `name` ENUM('GLADIATOR', 'FREEDMANEEDMAN', 'PLEBEIAN', 'PATRICIAN', 'SENATOR', 'CONSUL', 'EMPEROR') NOT NULL,
    ADD PRIMARY KEY (`name`);

-- AlterTable
ALTER TABLE `historicLogs` ADD COLUMN `activity` VARCHAR(191) NOT NULL;

-- AlterTable
ALTER TABLE `logsDate` ADD COLUMN `activity` VARCHAR(191) NOT NULL;

-- AlterTable
ALTER TABLE `logsNow` DROP COLUMN `activityId`,
    ADD COLUMN `activity` VARCHAR(191) NOT NULL;

-- DropTable
DROP TABLE `Activity`;

-- DropTable
DROP TABLE `ActivityRewards`;
