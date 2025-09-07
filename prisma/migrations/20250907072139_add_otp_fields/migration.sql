/*
  Warnings:

  - A unique constraint covering the columns `[phone]` on the table `users` will be added. If there are existing duplicate values, this will fail.

*/
-- AlterTable
ALTER TABLE "users" ADD COLUMN     "is_otp_used" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "otp_attempts" INTEGER NOT NULL DEFAULT 0,
ADD COLUMN     "otp_created_at" TIMESTAMP(3),
ADD COLUMN     "otp_expires_at" TIMESTAMP(3),
ADD COLUMN     "otp_hash" TEXT,
ADD COLUMN     "otp_identifier" TEXT,
ADD COLUMN     "otp_max_retries" INTEGER NOT NULL DEFAULT 3,
ADD COLUMN     "otp_type" TEXT,
ADD COLUMN     "phone" TEXT;

-- CreateIndex
CREATE UNIQUE INDEX "users_phone_key" ON "users"("phone");
