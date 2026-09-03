/*
  Warnings:

  - You are about to drop the `MatchQueue` table. If the table is not empty, all the data it contains will be lost.

*/
-- DropTable
DROP TABLE "MatchQueue";

-- CreateTable
CREATE TABLE "champions" (
    "id" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "winrate" DOUBLE PRECISION,
    "main_role" TEXT,

    CONSTRAINT "champions_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "stats" (
    "id" TEXT NOT NULL,
    "championId" TEXT NOT NULL,
    "patch" TEXT NOT NULL,
    "elo" TEXT NOT NULL,
    "role" TEXT NOT NULL,
    "winrate" DOUBLE PRECISION,
    "total_games" INTEGER,

    CONSTRAINT "stats_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "setups" (
    "id" TEXT NOT NULL,
    "matchupId" TEXT NOT NULL,
    "build_path" JSONB NOT NULL,
    "rune_tree" JSONB NOT NULL,
    "summoner_spells" JSONB NOT NULL,
    "skill_order" JSONB NOT NULL,
    "created_at" TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "setups_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "matchups" (
    "id" TEXT NOT NULL,
    "mainChampionId" TEXT NOT NULL,
    "enemyChampionId" TEXT NOT NULL,
    "patch" TEXT NOT NULL,
    "elo" TEXT NOT NULL,
    "winrate" DOUBLE PRECISION,
    "total_games" INTEGER,
    "gold_diff_15" DOUBLE PRECISION,
    "cs_diff_15" DOUBLE PRECISION,
    "xp_diff_15" DOUBLE PRECISION,
    "created_at" TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "matchups_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "match_queue" (
    "id" TEXT NOT NULL,
    "status" "Status" NOT NULL DEFAULT 'PENDING',
    "fetched_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "match_queue_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "champions_name_key" ON "champions"("name");

-- AddForeignKey
ALTER TABLE "stats" ADD CONSTRAINT "stats_championId_fkey" FOREIGN KEY ("championId") REFERENCES "champions"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "setups" ADD CONSTRAINT "setups_matchupId_fkey" FOREIGN KEY ("matchupId") REFERENCES "matchups"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "matchups" ADD CONSTRAINT "matchups_mainChampionId_fkey" FOREIGN KEY ("mainChampionId") REFERENCES "champions"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "matchups" ADD CONSTRAINT "matchups_enemyChampionId_fkey" FOREIGN KEY ("enemyChampionId") REFERENCES "champions"("id") ON DELETE CASCADE ON UPDATE CASCADE;
