-- CreateTable
CREATE TABLE "Patch" (
    "id" SERIAL NOT NULL,
    "version" TEXT NOT NULL,
    "startTime" TIMESTAMP(3) NOT NULL,
    "endTime" TIMESTAMP(3),
    "isCurrent" BOOLEAN NOT NULL DEFAULT false,

    CONSTRAINT "Patch_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "Patch_version_key" ON "Patch"("version");

-- CreateIndex
CREATE INDEX "Patch_isCurrent_idx" ON "Patch"("isCurrent");
