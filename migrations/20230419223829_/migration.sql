-- AlterTable
ALTER TABLE `ActivityLog` MODIFY `duration` INTEGER NULL DEFAULT 0;

-- AlterTable
ALTER TABLE `Session` ADD COLUMN `duration` INTEGER NOT NULL DEFAULT 0;
