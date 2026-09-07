/*
  Warnings:

  - You are about to drop the column `endTime` on the `Patch` table. All the data in the column will be lost.
  - You are about to drop the column `startTime` on the `Patch` table. All the data in the column will be lost.
  - You are about to drop the column `enemyChampionId` on the `matchups` table. All the data in the column will be lost.
  - You are about to drop the column `mainChampionId` on the `matchups` table. All the data in the column will be lost.
  - You are about to drop the column `championId` on the `stats` table. All the data in the column will be lost.
  - Added the required column `start_time` to the `Patch` table without a default value. This is not possible if the table is not empty.
  - Added the required column `enemy_champion_id` to the `matchups` table without a default value. This is not possible if the table is not empty.
  - Added the required column `main_champion_id` to the `matchups` table without a default value. This is not possible if the table is not empty.
  - Added the required column `champion_id` to the `stats` table without a default value. This is not possible if the table is not empty.

*/
-- DropForeignKey
ALTER TABLE "matchups" DROP CONSTRAINT "matchups_enemyChampionId_fkey";

-- DropForeignKey
ALTER TABLE "matchups" DROP CONSTRAINT "matchups_mainChampionId_fkey";

-- DropForeignKey
ALTER TABLE "stats" DROP CONSTRAINT "stats_championId_fkey";

-- AlterTable
ALTER TABLE "Patch" DROP COLUMN "endTime",
DROP COLUMN "startTime",
ADD COLUMN     "end_time" TIMESTAMP(3),
ADD COLUMN     "start_time" TIMESTAMP(3) NOT NULL;

-- AlterTable
ALTER TABLE "matchups" DROP COLUMN "enemyChampionId",
DROP COLUMN "mainChampionId",
ADD COLUMN     "enemy_champion_id" TEXT NOT NULL,
ADD COLUMN     "main_champion_id" TEXT NOT NULL;

-- AlterTable
ALTER TABLE "stats" DROP COLUMN "championId",
ADD COLUMN     "champion_id" TEXT NOT NULL;

-- AddForeignKey
ALTER TABLE "stats" ADD CONSTRAINT "stats_champion_id_fkey" FOREIGN KEY ("champion_id") REFERENCES "champions"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "matchups" ADD CONSTRAINT "matchups_main_champion_id_fkey" FOREIGN KEY ("main_champion_id") REFERENCES "champions"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "matchups" ADD CONSTRAINT "matchups_enemy_champion_id_fkey" FOREIGN KEY ("enemy_champion_id") REFERENCES "champions"("id") ON DELETE CASCADE ON UPDATE CASCADE;
