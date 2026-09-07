/*
  Warnings:

  - You are about to drop the `Patch` table. If the table is not empty, all the data it contains will be lost.

*/
-- DropTable
DROP TABLE "Patch";

-- CreateTable
CREATE TABLE "patches" (
    "id" SERIAL NOT NULL,
    "version" TEXT NOT NULL,
    "start_time" TIMESTAMP(3) NOT NULL,
    "end_time" TIMESTAMP(3),
    "isCurrent" BOOLEAN NOT NULL DEFAULT false,

    CONSTRAINT "patches_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "patches_version_key" ON "patches"("version");

-- CreateIndex
CREATE INDEX "patches_isCurrent_idx" ON "patches"("isCurrent");
