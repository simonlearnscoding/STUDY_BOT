/*
  Warnings:

  - You are about to drop the column `nick` on the `User` table. All the data in the column will be lost.

*/
-- DropIndex
DROP INDEX `historicLogs_activityId_fkey` ON `historicLogs`;

-- DropIndex
DROP INDEX `logsDate_activityId_fkey` ON `logsDate`;

-- AlterTable
ALTER TABLE `User` DROP COLUMN `nick`;
