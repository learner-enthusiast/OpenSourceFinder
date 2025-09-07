/*
  Warnings:

  - A unique constraint covering the columns `[otp_identifier]` on the table `users` will be added. If there are existing duplicate values, this will fail.

*/
-- AlterTable
ALTER TABLE "users" ALTER COLUMN "email" DROP NOT NULL;

-- CreateIndex
CREATE UNIQUE INDEX "users_otp_identifier_key" ON "users"("otp_identifier");
