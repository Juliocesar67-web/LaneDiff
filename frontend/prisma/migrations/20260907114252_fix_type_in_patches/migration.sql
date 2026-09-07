/*
  Warnings:

  - You are about to drop the column `isCurrent` on the `patches` table. All the data in the column will be lost.

*/
-- DropIndex
DROP INDEX "patches_isCurrent_idx";

-- AlterTable
ALTER TABLE "patches" DROP COLUMN "isCurrent",
ADD COLUMN     "is_current" BOOLEAN NOT NULL DEFAULT false;

-- CreateIndex
CREATE INDEX "patches_is_current_idx" ON "patches"("is_current");
