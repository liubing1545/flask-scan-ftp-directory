/*
Navicat PGSQL Data Transfer

Source Server         : 192.168.33.10
Source Server Version : 90305
Source Host           : 192.168.33.10:5432
Source Database       : ftp_files
Source Schema         : public

Target Server Type    : PGSQL
Target Server Version : 90305
File Encoding         : 65001

Date: 2018-04-03 09:38:40
*/


-- ----------------------------
-- Sequence structure for files_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "files_id_seq";
CREATE SEQUENCE "files_id_seq"
 INCREMENT 1
 MINVALUE 1
 MAXVALUE 9223372036854775807
 START 48
 CACHE 1;
SELECT setval('"public"."files_id_seq"', 48, true);

-- ----------------------------
-- Table structure for files
-- ----------------------------
DROP TABLE IF EXISTS "files";
CREATE TABLE "files" (
"id" int4 DEFAULT nextval('files_id_seq'::regclass) NOT NULL,
"language" varchar(10) COLLATE "default",
"phone_num" varchar(20) COLLATE "default",
"word_type" varchar(10) COLLATE "default",
"word_num" varchar(10) COLLATE "default",
"file_name" text COLLATE "default"
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of files
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Alter Sequences Owned By 
-- ----------------------------
ALTER SEQUENCE "files_id_seq" OWNED BY "files"."id";

-- ----------------------------
-- Indexes structure for table files
-- ----------------------------
CREATE INDEX "ix_files_language" ON "files" USING btree (language);
CREATE INDEX "ix_files_phone_num" ON "files" USING btree (phone_num);

-- ----------------------------
-- Primary Key structure for table files
-- ----------------------------
ALTER TABLE "files" ADD PRIMARY KEY ("id");

