-- MySQL dump 10.13  Distrib 8.0.45, for Linux (x86_64)
--
-- Host: localhost    Database: ECHS
-- ------------------------------------------------------
-- Server version	8.0.45-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `account_type_master`
--

DROP TABLE IF EXISTS `account_type_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_type_master` (
  `ATM_ID` int NOT NULL,
  `ATM_NAME` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ATM_ECS_CODE` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ATM_ACTIVE` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`ATM_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ack_claim_list`
--

DROP TABLE IF EXISTS `ack_claim_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ack_claim_list` (
  `ACL_CLAIM_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `ACL_STAGE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ACL_STATUS` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ACL_INT_DATE` datetime NOT NULL,
  `ACL_ACK_USER` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ACL_ACK_DATE` datetime DEFAULT NULL,
  `ACL_PRIORITY` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`ACL_CLAIM_ID`),
  KEY `Idx_Ack_User` (`ACL_ACK_USER`),
  KEY `IDX_stage` (`ACL_STAGE`),
  KEY `idx_status` (`ACL_STATUS`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `adv_paym_cheque`
--

DROP TABLE IF EXISTS `adv_paym_cheque`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `adv_paym_cheque` (
  `APC_APPLY_ID` int NOT NULL,
  `APC_BANK_NAME` varchar(50) NOT NULL,
  `APC_BANK_BRANCH` varchar(50) NOT NULL,
  `APC_ACC_NO` varchar(20) NOT NULL,
  `APC_CHQ_NO` varchar(6) NOT NULL,
  `APC_CHQ_DT` date NOT NULL,
  `APC_CHQ_AMT` int NOT NULL,
  `APC_CLAIM_ID` varchar(15) NOT NULL,
  `APC_USER_ID` varchar(10) DEFAULT NULL,
  `APC_DATE` datetime DEFAULT NULL,
  PRIMARY KEY (`APC_APPLY_ID`),
  UNIQUE KEY `APC_CLAIM_ID_UNIQUE` (`APC_CLAIM_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `adv_paym_event`
--

DROP TABLE IF EXISTS `adv_paym_event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `adv_paym_event` (
  `APE_EVENT_ID` int NOT NULL AUTO_INCREMENT,
  `APE_APPLY_ID` int NOT NULL,
  `APE_GROUP_ID` varchar(3) NOT NULL,
  `APE_NMI_COUNT` int NOT NULL DEFAULT '0',
  `APE_PROC_ID` int NOT NULL,
  `APE_DATE` datetime NOT NULL,
  `APE_AMT_EST` int DEFAULT '0',
  `APE_BENF_REMARK` text,
  `APE_AMT_SANC` int DEFAULT '0',
  `APE_PROC_REMARK` text,
  `APE_USER_ID` varchar(10) NOT NULL,
  `APE_IP_ADDR` varchar(30) DEFAULT NULL,
  `APE_IS_REVERTED` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`APE_EVENT_ID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=94 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `adv_paym_process`
--

DROP TABLE IF EXISTS `adv_paym_process`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `adv_paym_process` (
  `APP_PROC_ID` int NOT NULL AUTO_INCREMENT,
  `APP_GROUP_ID` varchar(3) NOT NULL,
  `APP_STATUS_ID` int DEFAULT '0',
  `APP_NEXT_GROUP_ID` varchar(3) DEFAULT NULL,
  `APP_IS_APPLY` int DEFAULT '0',
  `APP_IS_NMI` int DEFAULT '0',
  `APP_IS_REPLY` int DEFAULT '0',
  `APP_IS_ACCEPT` int DEFAULT '0',
  `APP_IS_FINAL` int DEFAULT '0',
  `APP_APPR_LIMIT` int DEFAULT '0',
  `APP_ORDER` int DEFAULT '0',
  PRIMARY KEY (`APP_PROC_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `adv_paym_status`
--

DROP TABLE IF EXISTS `adv_paym_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `adv_paym_status` (
  `APS_ID` int NOT NULL,
  `APS_STATUS` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`APS_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `adv_payment_setting`
--

DROP TABLE IF EXISTS `adv_payment_setting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `adv_payment_setting` (
  `APS_ID` int NOT NULL AUTO_INCREMENT,
  `APS_FROM_DATE` date DEFAULT NULL,
  `APS_TO_DATE` date DEFAULT NULL,
  `APS_LUMPSUM` int DEFAULT NULL,
  `APS_PERCENT` decimal(6,2) DEFAULT '0.00',
  PRIMARY KEY (`APS_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `advance_payment`
--

DROP TABLE IF EXISTS `advance_payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `advance_payment` (
  `AP_APPLY_ID` int NOT NULL,
  `AP_PAT_TYPE` varchar(1) DEFAULT NULL,
  `AP_INIT_BY` varchar(5) DEFAULT NULL,
  `AP_APPLY_DATE` datetime NOT NULL,
  `AP_ADV_REQ_ID` int DEFAULT NULL,
  `AP_CLAIM_ID` varchar(15) DEFAULT NULL,
  `AP_BENF_ID` int NOT NULL DEFAULT '0',
  `AP_PARENT_OIC` varchar(5) DEFAULT NULL,
  `AP_LIST_HOSP_ID` int DEFAULT '0',
  `AP_HOSP_NAME` varchar(50) DEFAULT NULL,
  `AP_ADMIT_DATE` date NOT NULL,
  `AP_AILMENT` text NOT NULL,
  `AP_TREATMENT` text NOT NULL,
  `AP_AMT_EST` int DEFAULT '0',
  `AP_COMMENTS` text,
  `AP_PROC_ID` int DEFAULT '0',
  `AP_GROUP_ID` varchar(5) DEFAULT NULL,
  `AP_PROC_USER` varchar(10) DEFAULT NULL,
  `AP_PROC_DATE` datetime DEFAULT NULL,
  `AP_PROC_REMARK` text,
  `AP_REQUERY_BY` varchar(5) DEFAULT NULL,
  `AP_AMT_SANC` int DEFAULT '0',
  `AP_ACTIVE` int DEFAULT '1',
  PRIMARY KEY (`AP_APPLY_ID`),
  UNIQUE KEY `AP_ADV_REQ_ID_UNIQUE` (`AP_ADV_REQ_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ailment_code`
--

DROP TABLE IF EXISTS `ailment_code`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ailment_code` (
  `AC_AILMENT_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `AC_AILMENT_DESC` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `AC_AILMENT_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`AC_AILMENT_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `amt_ded_reason`
--

DROP TABLE IF EXISTS `amt_ded_reason`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `amt_ded_reason` (
  `ADR_ID` int NOT NULL AUTO_INCREMENT,
  `ADR_PAT_TYPE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'O',
  `ADR_EXP_ID` int DEFAULT '0',
  `ADR_DESC` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ADR_ACTIVE` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`ADR_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_property`
--

DROP TABLE IF EXISTS `app_property`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_property` (
  `AP_KEY` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `AP_VALUE` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `AP_FROM_DATE` datetime NOT NULL,
  `AP_TO_DATE` datetime DEFAULT NULL,
  `AP_ACTIVE` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`AP_KEY`,`AP_FROM_DATE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `applicant_master`
--

DROP TABLE IF EXISTS `applicant_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `applicant_master` (
  `AM_ID` int NOT NULL,
  `AM_DESC` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`AM_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `application_settings`
--

DROP TABLE IF EXISTS `application_settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `application_settings` (
  `AS_ID` int NOT NULL AUTO_INCREMENT,
  `AS_CODE` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `AS_VALUE` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `AS_IP` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `AS_ACTIVE` int DEFAULT '1',
  PRIMARY KEY (`AS_ID`),
  UNIQUE KEY `AS_CODE_UNIQUE` (`AS_CODE`)
) ENGINE=InnoDB AUTO_INCREMENT=107 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `appr_allot`
--

DROP TABLE IF EXISTS `appr_allot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appr_allot` (
  `AA_CLAIM_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `AA_ALLOT_DATE` datetime NOT NULL,
  `AA_ACCEPT_DATE` datetime NOT NULL,
  `AA_CLAIM_AMT` double(10,2) NOT NULL,
  `AA_SANCTION_AMT` double(10,2) NOT NULL,
  `AA_AMOUNT` double(10,2) NOT NULL,
  `AA_STAGE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `AA_STATUS` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `AA_REVIEW_CASE` int NOT NULL DEFAULT '0',
  `AA_BPA_REVIEW_CASE` int NOT NULL DEFAULT '0',
  `AA_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `AA_MANDATORY` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`AA_CLAIM_ID`),
  KEY `Idx_User_Id` (`AA_USER_ID`),
  KEY `Idx_Amount` (`AA_AMOUNT`),
  KEY `Idx_Review_Case` (`AA_REVIEW_CASE`),
  KEY `Idx_BPA_Review_Case` (`AA_BPA_REVIEW_CASE`),
  KEY `Idx_Mandatory` (`AA_MANDATORY`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `appr_allot_setting`
--

DROP TABLE IF EXISTS `appr_allot_setting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appr_allot_setting` (
  `AAS_FROM_DATE` date NOT NULL,
  `AAS_TO_DATE` date DEFAULT NULL,
  `AAS_FROM_AMT` double(10,2) NOT NULL,
  `AAS_TO_AMT` double(10,2) NOT NULL,
  `AAS_MAND_PERC` double(6,2) NOT NULL,
  PRIMARY KEY (`AAS_FROM_DATE`,`AAS_FROM_AMT`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `appr_dealloc`
--

DROP TABLE IF EXISTS `appr_dealloc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appr_dealloc` (
  `AD_ID` int NOT NULL,
  `AD_DATE` datetime DEFAULT NULL,
  `AD_COUNTS` int DEFAULT '0',
  `AD_APP_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `AD_REMARKS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `AD_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `AD_IP_ADDRESS` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`AD_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `approval_documents`
--

DROP TABLE IF EXISTS `approval_documents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `approval_documents` (
  `AD_ID` int NOT NULL,
  `AD_APP_ID` int NOT NULL,
  `AD_DOC_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `AD_REMARK` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `AD_FILENAME` varchar(75) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `AD_RECEIVED` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `AD_REC_REMARK` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `AD_REC_REMARK_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `AD_SUBMIT_TIME` datetime DEFAULT NULL,
  `AD_FILE_SRNO` int DEFAULT '0',
  `AD_FILE_SIZE` decimal(10,2) DEFAULT NULL,
  `AD_SIGNED` int unsigned DEFAULT '0',
  PRIMARY KEY (`AD_ID`),
  KEY `Index_1` (`AD_APP_ID`),
  KEY `Idx_Signed` (`AD_SIGNED`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `audit_query`
--

DROP TABLE IF EXISTS `audit_query`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `audit_query` (
  `AQ_CLAIM_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `AQ_QUERY_ID` int unsigned NOT NULL DEFAULT '0',
  `AQ_REQUERY_ID` int unsigned NOT NULL DEFAULT '0',
  `AQ_LEVEL` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `AQ_RECOVERY_TYPE` int unsigned NOT NULL,
  `AQ_QUERY_NO` int unsigned DEFAULT NULL,
  `AQ_QUERY` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `AQ_CDA_AMT` decimal(15,2) NOT NULL DEFAULT '0.00',
  `AQ_RECOVER_AMT` decimal(15,2) NOT NULL DEFAULT '0.00',
  `AQ_CLOSE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'N',
  `AQ_QUERY_USER` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `AQ_QUERY_DATE` datetime DEFAULT NULL,
  `AQ_FORWARD_TO` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'R',
  `AQ_FORWARD_DATE` datetime DEFAULT NULL,
  `AQ_REPLY_ID` int unsigned DEFAULT NULL,
  PRIMARY KEY (`AQ_QUERY_ID`,`AQ_CLAIM_ID`,`AQ_REQUERY_ID`),
  KEY `Idx_Claim_Id` (`AQ_CLAIM_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `audit_questionare`
--

DROP TABLE IF EXISTS `audit_questionare`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `audit_questionare` (
  `AQ_QUE_ID` int unsigned NOT NULL DEFAULT '0',
  `AQ_INTIMATION_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `AQ_QUESTION_1` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `AQ_AUDITOR_STATUS` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'Y',
  `AQ_QUESTION_2` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `AQ_AAO_STATUS` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'Y',
  `AQ_QUESTION_3` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `AQ_SAO_STATUS` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'Y',
  `AQ_REPLY` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `AQ_STATUS` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'N',
  `AQ_DATE_1` datetime DEFAULT NULL,
  `AQ_DATE_2` datetime DEFAULT NULL,
  `AQ_DATE_3` datetime DEFAULT NULL,
  `AQ_REPLY_DATE` datetime DEFAULT NULL,
  PRIMARY KEY (`AQ_QUE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `audit_recovery`
--

DROP TABLE IF EXISTS `audit_recovery`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `audit_recovery` (
  `ARV_CLAIM_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `ARV_RECOV_FROM` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `ARV_SETTLEMENT_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ARV_RECOVER_AMT` decimal(14,2) DEFAULT '0.00',
  PRIMARY KEY (`ARV_CLAIM_ID`,`ARV_RECOV_FROM`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `audit_remarks`
--

DROP TABLE IF EXISTS `audit_remarks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `audit_remarks` (
  `AR_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `AR_REM_TYPE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `AR_HOS_REMARK` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `AR_PAR_REMARK` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `AR_SUP_REMARK` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `AR_APP_REMARK` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  PRIMARY KEY (`AR_INTIMATION_ID`,`AR_REM_TYPE_ID`),
  KEY `FK_audit_remarks_2` (`AR_REM_TYPE_ID`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `audit_reply`
--

DROP TABLE IF EXISTS `audit_reply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `audit_reply` (
  `AR_REPLY_ID` int NOT NULL DEFAULT '0',
  `AR_QUERY_ID` int unsigned NOT NULL,
  `AR_REQUERY_ID` int unsigned NOT NULL,
  `AR_REPLY` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `AR_RECOVER_AMT` decimal(15,2) DEFAULT '0.00',
  `AR_FORWARD_TO` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `AR_USER_ID` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `AR_REPLY_DATE` datetime DEFAULT NULL,
  `AR_REPLY_BY` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`AR_REPLY_ID`),
  KEY `Idx_Query_ID` (`AR_QUERY_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `audit_reply_back`
--

DROP TABLE IF EXISTS `audit_reply_back`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `audit_reply_back` (
  `AR_REPLY_ID` int NOT NULL DEFAULT '0',
  `AR_QUERY_ID` int unsigned NOT NULL,
  `AR_REQUERY_ID` int unsigned NOT NULL,
  `AR_REPLY` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `AR_RECOVER_AMT` decimal(15,2) DEFAULT '0.00',
  `AR_FORWARD_TO` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `AR_USER_ID` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `AR_REPLY_DATE` datetime DEFAULT NULL,
  `AR_REPLY_BY` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`AR_REPLY_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `audit_status`
--

DROP TABLE IF EXISTS `audit_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `audit_status` (
  `AS_CLAIM_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `AS_AUD_STAGE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `AS_AUD_STATUS` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `AS_QUERIES_NOS` int unsigned DEFAULT '0',
  `AS_AUD_NOS` int unsigned DEFAULT '0',
  `AS_AAO_NOS` int unsigned DEFAULT '0',
  `AS_SAO_IN_DATE` datetime DEFAULT NULL,
  `AS_SAO_NOS` int unsigned DEFAULT '0',
  `AS_RC_IN_DATE` datetime DEFAULT NULL,
  `AS_RC_NOS` int unsigned DEFAULT '0',
  `AS_BPA_IN_DATE` datetime DEFAULT NULL,
  `AS_BPA_NOS` int unsigned DEFAULT '0',
  `AS_HOS_IN_DATE` datetime DEFAULT NULL,
  `AS_HOS_NOS` int DEFAULT '0',
  `AS_CORG_IN_DATE` datetime DEFAULT NULL,
  `AS_CORG_NOS` int unsigned DEFAULT '0',
  `AS_CFA_IN_DATE` datetime DEFAULT NULL,
  `AS_CFA_NOS` int unsigned NOT NULL DEFAULT '0',
  `AS_CDA_AMT` decimal(14,2) NOT NULL DEFAULT '0.00',
  `AS_RECOVER_AMT` decimal(14,2) NOT NULL DEFAULT '0.00',
  `AS_RECOVERED_AMT` decimal(14,2) NOT NULL DEFAULT '0.00',
  `AS_CLOSED` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'N',
  `AS_ACCEPT_NOS` int unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`AS_CLAIM_ID`),
  KEY `Idx_Aud_Status` (`AS_AUD_STATUS`),
  KEY `Idx_Aud_Stage` (`AS_AUD_STAGE`),
  KEY `Idx_Closed` (`AS_CLOSED`),
  KEY `Idx_AUD_NOS` (`AS_AUD_NOS`),
  KEY `Idx_SAO_NOS` (`AS_SAO_NOS`),
  KEY `Idx_RC_NOS` (`AS_RC_NOS`),
  KEY `Idx_BPA_NOS` (`AS_BPA_NOS`),
  KEY `Idx_HOS_NOS` (`AS_HOS_NOS`),
  KEY `Idx_CFA_NOS` (`AS_CFA_NOS`),
  KEY `Idx_ACCEPT_NOS` (`AS_ACCEPT_NOS`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `audit_trail`
--

DROP TABLE IF EXISTS `audit_trail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `audit_trail` (
  `AT_ENTITY_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `AT_OFFICE_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `AT_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `AT_TRAN_NO` int NOT NULL AUTO_INCREMENT,
  `AT_IP_ADDRESS` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `AT_MAC_ADDRESS` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `AT_SESSION_ID` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `AT_LOGIN_TIME` datetime NOT NULL,
  `AT_LOGOUT_TIME` datetime DEFAULT NULL,
  `AT_SESSION_EXPIRED` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'N',
  `AT_LOGIN_TYPE` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`AT_TRAN_NO`)
) ENGINE=InnoDB AUTO_INCREMENT=14313481 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auto_allot_users`
--

DROP TABLE IF EXISTS `auto_allot_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auto_allot_users` (
  `AAU_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `AAU_LAST_DATE` datetime DEFAULT NULL,
  `AAU_LAST_CLAIM` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `AAU_ACTIVE` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`AAU_USER_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bank_actype`
--

DROP TABLE IF EXISTS `bank_actype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bank_actype` (
  `BA_ACTYPE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `BA_ACTYPE_DESC` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BA_ACTYPE_CODE` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BA_ACTYPE_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`BA_ACTYPE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bank_master`
--

DROP TABLE IF EXISTS `bank_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bank_master` (
  `BM_BANK_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `BM_BANK_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_BANK_BRANCH` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_BANK_ADD1` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_BANK_ADD2` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_BANK_ADD3` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_BANK_CITY` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_BANK_STATE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_BANK_PIN` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_BANK_ACTYPE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_BANK_ACNO` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_BANK_MICR` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_BANK_IFSC` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_OFFICE_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_ENTITY_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_BANK_STATUS` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_PAY_MODE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_PAYEE_NAME` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`BM_BANK_ID`),
  KEY `FK_bank_master_1` (`BM_BANK_ACTYPE`),
  KEY `FK_bank_master_2` (`BM_OFFICE_ID`) USING BTREE,
  CONSTRAINT `FK_BM_ACTYPE` FOREIGN KEY (`BM_BANK_ACTYPE`) REFERENCES `bank_actype` (`BA_ACTYPE_ID`),
  CONSTRAINT `FK_BM_OFFICE_ID` FOREIGN KEY (`BM_OFFICE_ID`) REFERENCES `office_master` (`OM_OFFICE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `benf_mast_32kb`
--

DROP TABLE IF EXISTS `benf_mast_32kb`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `benf_mast_32kb` (
  `PensionerName` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PenServiceNumber` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PenForceType` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BPA_SERVICE_CODE` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PenRankName` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BPA_RANK_ID` int DEFAULT '0',
  `PenDOB` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PenDOR` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PenCityName` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `FamilyPensionerRelation` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `FPenGender` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PenPolyclinic` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PenGender` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PenDOC` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DepName` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DepRelation` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BPA_RELATION_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DepDOB` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CardNo` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `Whether32KB` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PenDORAF` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  KEY `Idx_Ser_No` (`PenServiceNumber`),
  KEY `Idx_Card_No` (`CardNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `benf_master_live`
--

DROP TABLE IF EXISTS `benf_master_live`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `benf_master_live` (
  `BM_BEN_ID` decimal(10,0) NOT NULL DEFAULT '0',
  `BM_PENSION_TYPE` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'N',
  `BM_PENSIONER_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_GENDER` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'M',
  `BM_FORCE_TYPE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_SERVICE_NO` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_CARD_NO` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_RANK_CODE` int DEFAULT '0',
  `BM_ROOM_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_FAMILY_RELATION_ID` int DEFAULT '0',
  `BM_DOB` date DEFAULT NULL,
  `BM_DOR` date DEFAULT NULL,
  `BM_DOE` date DEFAULT NULL,
  `BM_CITY` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_STATE_ID` int DEFAULT '0',
  `BM_PIN` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_REGION_ID` int DEFAULT '0',
  `BM_POLYCLINIC` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_POLYCLINIC_ID` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_DISTRICT` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_DOM` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_DISABILITY` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_WAR_WIDOW` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_DRUG_ALLERGY` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_EMPLOYED` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_MARITAL_STATUS` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_POLYCLINIC_CODE` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_CARD_UPGRADE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_NEW_CARD_NO` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`BM_BEN_ID`),
  KEY `Index_2` (`BM_CARD_NO`),
  KEY `Index_3` (`BM_FORCE_TYPE`,`BM_SERVICE_NO`),
  KEY `Index_4` (`BM_SERVICE_NO`),
  KEY `Index_5` (`BM_FORCE_TYPE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bpa_allot_config`
--

DROP TABLE IF EXISTS `bpa_allot_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bpa_allot_config` (
  `BAC_SETUP_ID` int NOT NULL AUTO_INCREMENT,
  `BAC_ALLOT_ID` int DEFAULT NULL,
  `BAC_MODE` int DEFAULT '1',
  `BAC_RANGE_ID` int NOT NULL,
  `BAC_HCF_ID` int DEFAULT NULL,
  `BAC_ENTITY_ID` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BAC_CLAIM_TYPE` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BAC_REGION_ID` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BAC_TARGET` int DEFAULT NULL,
  `BAC_PREV_ID` int DEFAULT '0',
  `BAC_MAX_AMT` int NOT NULL DEFAULT '0',
  `BAC_NMI_ENTITY` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BAC_ACTIVE` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`BAC_SETUP_ID`),
  KEY `IDX_ALLOT` (`BAC_ALLOT_ID`) /*!80000 INVISIBLE */,
  KEY `idx_mode` (`BAC_MODE`)
) ENGINE=InnoDB AUTO_INCREMENT=152415 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bpa_allot_master`
--

DROP TABLE IF EXISTS `bpa_allot_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bpa_allot_master` (
  `BAM_ALLOT_ID` int NOT NULL AUTO_INCREMENT,
  `BAM_LEADER_ID` int NOT NULL,
  `BAM_MEMBER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BAM_ALLOT_DATE` date NOT NULL,
  `BAM_WEEK_DAY` int NOT NULL DEFAULT '0',
  `BAM_CR_DATE` date NOT NULL,
  `BAM_CR_BY` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BAM_MOD_DATE` date DEFAULT NULL,
  `BAM_MOD_BY` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BAM_SPEC_DAY` int NOT NULL DEFAULT '0',
  `BAM_SPEC_REASON` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `BAM_CLOSED` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`BAM_ALLOT_ID`),
  UNIQUE KEY `IDX_UNIQ` (`BAM_LEADER_ID`,`BAM_MEMBER_ID`,`BAM_ALLOT_DATE`,`BAM_WEEK_DAY`),
  KEY `IDX_LEADER` (`BAM_LEADER_ID`),
  KEY `IDX_MEMBER` (`BAM_MEMBER_ID`),
  KEY `IDX_DATE` (`BAM_ALLOT_DATE`)
) ENGINE=InnoDB AUTO_INCREMENT=23838 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bpa_allot_stage`
--

DROP TABLE IF EXISTS `bpa_allot_stage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bpa_allot_stage` (
  `BAS_GROUP_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `BAS_ID` int NOT NULL,
  `BAS_STAGE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `BAS_STATUS` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `BAS_TYPE` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`BAS_ID`,`BAS_STAGE`,`BAS_STATUS`,`BAS_GROUP_ID`,`BAS_TYPE`),
  KEY `idx_id` (`BAS_ID`),
  KEY `IDX_STAGE` (`BAS_STAGE`),
  KEY `IDX_status` (`BAS_STATUS`),
  KEY `IDX_TYPES` (`BAS_TYPE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bpa_allot_status`
--

DROP TABLE IF EXISTS `bpa_allot_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bpa_allot_status` (
  `BAS_GROUP_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `BAS_ID` int NOT NULL,
  `BAS_STAGE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `BAS_STATUS` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `BAS_TYPE` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`BAS_ID`,`BAS_STAGE`,`BAS_STATUS`,`BAS_GROUP_ID`,`BAS_TYPE`),
  KEY `idx_id` (`BAS_ID`),
  KEY `IDX_STAGE` (`BAS_STAGE`),
  KEY `IDX_status` (`BAS_STATUS`),
  KEY `IDX_TYPES` (`BAS_TYPE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bpa_allot_type`
--

DROP TABLE IF EXISTS `bpa_allot_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bpa_allot_type` (
  `BAT_ID` int NOT NULL,
  `BAT_DESC` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BAT_ALLOW_SKIP` int NOT NULL DEFAULT '1',
  `BAT_PRIORITY` int NOT NULL DEFAULT '1',
  `BAT_TAR_PRIORITY` int NOT NULL DEFAULT '0',
  `BAT_STATUS` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'S',
  `BAT_SAME_USER` int DEFAULT '0',
  `BAT_PROC_MODE` int DEFAULT '0',
  `BAT_ADD_TARGET` int DEFAULT '0',
  `BAT_CNT_TARGET` int DEFAULT '0',
  `BAT_ACTIVE` int NOT NULL DEFAULT '1',
  `BAT_FRESH` int NOT NULL DEFAULT '0',
  `BAT_OWN` int NOT NULL DEFAULT '0',
  `BAT_RESIGNED` int NOT NULL DEFAULT '0',
  `BAT_OTHERS` int NOT NULL DEFAULT '0',
  `BAT_ABSENT` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`BAT_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bpa_carry_fwd`
--

DROP TABLE IF EXISTS `bpa_carry_fwd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bpa_carry_fwd` (
  `BCF_ID` int NOT NULL AUTO_INCREMENT,
  `BCF_DATE` date NOT NULL,
  `BCF_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BCF_CF_DATE` date NOT NULL,
  `BCF_ACTIVE` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`BCF_ID`),
  UNIQUE KEY `IDX_UN_USER_DATE` (`BCF_USER_ID`,`BCF_DATE`),
  UNIQUE KEY `IDX_UN_USER_CF` (`BCF_USER_ID`,`BCF_CF_DATE`,`BCF_DATE`),
  KEY `IDX_USER` (`BCF_USER_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=22558 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bpa_cf_setup`
--

DROP TABLE IF EXISTS `bpa_cf_setup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bpa_cf_setup` (
  `BCS_ID` int NOT NULL,
  `BCS_ALLOT_ID` int NOT NULL,
  `BCS_SETUP_ID` int NOT NULL,
  `BCS_CF_QTY` int NOT NULL DEFAULT '0',
  `BCS_CF_TARGET` int NOT NULL DEFAULT '0',
  `BCS_CF_PROCESS` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`BCS_ID`,`BCS_SETUP_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bpa_claim_list`
--

DROP TABLE IF EXISTS `bpa_claim_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bpa_claim_list` (
  `BCL_BPA_ID` int NOT NULL AUTO_INCREMENT,
  `BCL_CLAIM_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BCL_DATE` datetime NOT NULL,
  `BCL_RANGE_ID` int DEFAULT NULL,
  `BCL_PAT_TYPE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BCL_ENTITY_ID` int DEFAULT NULL,
  `BCL_REGION_ID` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BCL_REIMB_TYPE` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BCL_HOSP_ID` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BCL_CATG_ID` int DEFAULT NULL,
  `BCL_HOS_PRTY` int DEFAULT NULL,
  `BCL_ACCEPT_DATE` datetime NOT NULL,
  `BCL_TAT` int NOT NULL DEFAULT '0',
  `BCL_PRIORITY` int NOT NULL DEFAULT '0',
  `BCL_LAST_BPA` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BCL_CLAIM_AMT` decimal(10,2) NOT NULL,
  `BCL_SETUP_ID` int DEFAULT NULL,
  `BCL_STAGE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BCL_STATUS` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BCL_PROC_ID` int DEFAULT '0',
  `BCL_BPA_USER` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BCL_PROC_DATE` datetime DEFAULT NULL,
  `BCL_BPA_PRTY` int DEFAULT '0',
  `BCL_FORCE_USER` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BCL_CLAIM_TYPE` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BCL_NO_DOCS` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`BCL_BPA_ID`),
  UNIQUE KEY `IDX_CLAIM` (`BCL_CLAIM_ID`),
  KEY `IDX_LAST_BPA` (`BCL_LAST_BPA`),
  KEY `IDX_STAGE` (`BCL_STAGE`),
  KEY `IDX_STATUS` (`BCL_STATUS`),
  KEY `IDX_BPA_USER` (`BCL_BPA_USER`),
  KEY `IDX_CLAIM_TYPE` (`BCL_CLAIM_TYPE`),
  KEY `IDX_RANGE` (`BCL_RANGE_ID`),
  KEY `IDX_TAT` (`BCL_TAT`) /*!80000 INVISIBLE */,
  KEY `IDX_AMT` (`BCL_CLAIM_AMT`)
) ENGINE=InnoDB AUTO_INCREMENT=22284569 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bpa_claim_process`
--

DROP TABLE IF EXISTS `bpa_claim_process`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bpa_claim_process` (
  `BCP_ID` int NOT NULL AUTO_INCREMENT,
  `BCP_ALLOT_ID` int NOT NULL,
  `BCP_SETUP_ID` int DEFAULT NULL,
  `BCP_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BCP_CLAIM_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BCP_ALLOT_TYPE` int NOT NULL DEFAULT '0',
  `BCP_STAGE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BCP_STATUS` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BCP_FWD` int DEFAULT '0',
  `BCP_DATE` date NOT NULL,
  `BCP_TIME` time DEFAULT NULL,
  `BCP_FIN_DATE` date DEFAULT NULL,
  `BCP_FIN_TIME` time DEFAULT NULL,
  `BCP_IP_ADDR` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`BCP_ID`),
  KEY `IDX_USER_date` (`BCP_DATE`),
  KEY `IDX_CLAIM` (`BCP_CLAIM_ID`),
  KEY `IDX_USER_ID` (`BCP_USER_ID`) /*!80000 INVISIBLE */,
  KEY `IDX_STAGE` (`BCP_STAGE`) /*!80000 INVISIBLE */,
  KEY `IDX_STATUS` (`BCP_STATUS`) /*!80000 INVISIBLE */,
  KEY `IDX_ALLOT_TYPE` (`BCP_ALLOT_TYPE`)
) ENGINE=InnoDB AUTO_INCREMENT=7971913 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bpa_daily_allot`
--

DROP TABLE IF EXISTS `bpa_daily_allot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bpa_daily_allot` (
  `BDA_ALLOT_ID` int NOT NULL DEFAULT '0',
  `BDA_SETUP_ID` int NOT NULL,
  `BDA_DATE` date NOT NULL,
  `BDA_FWD` int NOT NULL DEFAULT '0',
  `BDA_CF_DATE` date DEFAULT NULL,
  `BDA_TARGET` int DEFAULT '0',
  `BDA_PROCESS` int DEFAULT '0',
  PRIMARY KEY (`BDA_ALLOT_ID`,`BDA_SETUP_ID`,`BDA_DATE`,`BDA_FWD`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bpa_leave_master`
--

DROP TABLE IF EXISTS `bpa_leave_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bpa_leave_master` (
  `BLM_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `BLM_FROM_DATE` date NOT NULL,
  `BLM_TO_DATE` date DEFAULT NULL,
  `BLM_LEAVE_ID` int NOT NULL,
  `BLM_ACTIVE` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`BLM_USER_ID`,`BLM_FROM_DATE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bpa_serfee_reco`
--

DROP TABLE IF EXISTS `bpa_serfee_reco`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bpa_serfee_reco` (
  `bsr_settlement_id` decimal(10,0) NOT NULL,
  `bsr_region_id` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `bsr_ser_fee` decimal(15,2) NOT NULL DEFAULT '0.00',
  `bsr_ser_fee_recvd` decimal(15,2) NOT NULL DEFAULT '0.00',
  `bsr_credit_date` datetime NOT NULL,
  `bsr_neft_ref_no` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `bsr_neft_amount` decimal(15,2) DEFAULT '0.00',
  `bsr_voucher_no` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `bsr_gst_tds` decimal(15,2) NOT NULL DEFAULT '0.00',
  `bsr_diff_fee` decimal(15,2) DEFAULT '0.00',
  `bsr_user_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `bsr_update_date` datetime NOT NULL,
  `bsr_ip_address` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`bsr_settlement_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bpa_sites`
--

DROP TABLE IF EXISTS `bpa_sites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bpa_sites` (
  `BS_ID` int NOT NULL,
  `BS_NAME` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BS_HOSTS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `BS_ACTIVE` int DEFAULT '1',
  PRIMARY KEY (`BS_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bpa_skiped_claim`
--

DROP TABLE IF EXISTS `bpa_skiped_claim`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bpa_skiped_claim` (
  `BSC_CLAIM_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `BSC_ALLOT_ID` int NOT NULL DEFAULT '0',
  `BSC_SETUP_ID` int NOT NULL DEFAULT '0',
  `BSC_SKIP_MODE` int DEFAULT '0',
  `BSC_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BSC_SKIP_DATE` date NOT NULL,
  `BSC_SKIP_TIME` time DEFAULT NULL,
  `BSC_SKIP_TYPE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BSC_REPLY` int NOT NULL DEFAULT '0',
  `BSC_SKIP_REASON` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `BSC_PROC_TIME` datetime DEFAULT NULL,
  `BSC_DRAFT_SAVE` int NOT NULL DEFAULT '0',
  `BSC_FWD` int DEFAULT '0',
  PRIMARY KEY (`BSC_CLAIM_ID`),
  KEY `IDX_USER` (`BSC_USER_ID`),
  KEY `IDX_ALLOT` (`BSC_ALLOT_ID`),
  KEY `IDX_SETUP` (`BSC_SETUP_ID`),
  KEY `IDX_SKIP_TYPE` (`BSC_SKIP_TYPE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `budget_forecaster`
--

DROP TABLE IF EXISTS `budget_forecaster`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `budget_forecaster` (
  `bf_crtn_dt` date NOT NULL,
  `bf_office_cghs_city_id` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `bf_crm_city_name` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `bf_crdramt` decimal(16,2) DEFAULT NULL,
  `bf_aprpay` decimal(16,2) DEFAULT NULL,
  `bf_maypay` decimal(16,2) DEFAULT NULL,
  `bf_junpay` decimal(16,2) DEFAULT NULL,
  `bf_julpay` decimal(16,2) DEFAULT NULL,
  `bf_augpay` decimal(16,2) DEFAULT NULL,
  `bf_seppay` decimal(16,2) DEFAULT NULL,
  `bf_octpay` decimal(16,2) DEFAULT NULL,
  `bf_novpay` decimal(16,2) DEFAULT NULL,
  `bf_decpay` decimal(16,2) DEFAULT NULL,
  `bf_janpay` decimal(16,2) DEFAULT NULL,
  `bf_febpay` decimal(16,2) DEFAULT NULL,
  `bf_marpay` decimal(16,2) DEFAULT NULL,
  `bf_totpay` decimal(16,2) DEFAULT NULL,
  KEY `inx_bf001` (`bf_crtn_dt`),
  KEY `inx_bf002` (`bf_crtn_dt`,`bf_office_cghs_city_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `calendar_year`
--

DROP TABLE IF EXISTS `calendar_year`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `calendar_year` (
  `CY_YEAR` int unsigned NOT NULL AUTO_INCREMENT,
  `CY_START_DATE` date NOT NULL,
  `CY_END_DATE` date NOT NULL,
  `CY_DESC` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`CY_YEAR`),
  KEY `Index_2` (`CY_START_DATE`),
  KEY `Index_3` (`CY_END_DATE`)
) ENGINE=InnoDB AUTO_INCREMENT=2027 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `category_master`
--

DROP TABLE IF EXISTS `category_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category_master` (
  `CM_CAT_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `CM_CAT_DESC` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CM_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`CM_CAT_ID`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cda_payment_file`
--

DROP TABLE IF EXISTS `cda_payment_file`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cda_payment_file` (
  `CPF_UPLOAD_ID` int NOT NULL,
  `CPF_REGION_ID` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CPF_SETTLE_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CPF_SETTLE_DATE` date DEFAULT NULL,
  `CPF_FILE_SIZE` int NOT NULL,
  `CPF_FILE_DATE` datetime NOT NULL,
  `CPF_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CPF_IPADDRESS` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CPF_SETTLED` int NOT NULL DEFAULT '0',
  `CPF_CLAIM_CNT` int NOT NULL DEFAULT '0',
  `CPF_PAY_CNT` int NOT NULL DEFAULT '0',
  `CPF_REJ_CNT` int NOT NULL DEFAULT '0',
  `CPF_REJ_UPLOAD` int DEFAULT '0',
  `CPF_ACTIVE` int DEFAULT '1',
  `CPF_REMARK` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  PRIMARY KEY (`CPF_UPLOAD_ID`),
  KEY `Idx_Settle_Id` (`CPF_SETTLE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cda_payment_reject`
--

DROP TABLE IF EXISTS `cda_payment_reject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cda_payment_reject` (
  `CPR_SETTLEMENT_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `CPR_CLAIM_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `CPR_OFFICE_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CPR_ENTITY_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CPR_REASON` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `CPR_REMARKS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `CPR_ACCEPT_DATE` date DEFAULT NULL,
  `CPR_CARD_ID` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CPR_SERVICE_NO` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CPR_BENF_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CPR_RANK` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CPR_PATIENT_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CPR_RELATION` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CPR_ADMIT_DATE` date DEFAULT NULL,
  `CPR_DOD` date DEFAULT NULL,
  `CPR_CLAIM_AMT` decimal(15,2) DEFAULT NULL,
  `CPR_APP_AMT` decimal(15,2) DEFAULT NULL,
  `CPR_DISALLOW_AMT` decimal(16,2) DEFAULT NULL,
  `CPR_BPA_FEES` decimal(16,2) DEFAULT NULL,
  `CPR_PENALITY` decimal(15,2) DEFAULT NULL,
  `CPR_HOS_UTI_SER` decimal(15,2) DEFAULT NULL,
  `CPR_DISC_AMT` decimal(15,2) DEFAULT NULL,
  `CPR_RECOV_AMT` decimal(15,2) DEFAULT NULL,
  `CPR_PAYEE_NAME` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CPR_IFSC` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CPR_ACC_NO` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CPR_ACTYPE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CPR_PAN_NO` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CPR_NEW_SETTLE_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CPR_NEW_SETTLE_DT` date DEFAULT NULL,
  `CPR_REJECT_COUNT` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`CPR_SETTLEMENT_ID`,`CPR_CLAIM_ID`),
  KEY `Idx_New_Settle_Id` (`CPR_NEW_SETTLE_ID`),
  KEY `Idx_New_Settle_Dt` (`CPR_NEW_SETTLE_DT`),
  KEY `Idx_Office_Id` (`CPR_OFFICE_ID`),
  KEY `Idx_Claim_Id` (`CPR_CLAIM_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cda_payment_response`
--

DROP TABLE IF EXISTS `cda_payment_response`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cda_payment_response` (
  `CPR_CLAIM_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `CPR_SETTLEMENT_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CPR_PAYEE_NAME` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CPR_PAY_REFERENCE` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CPR_AMT_PAID` decimal(10,2) NOT NULL DEFAULT '0.00',
  `CPR_SERVICE_FEES` decimal(10,2) NOT NULL DEFAULT '0.00',
  `CPR_TDS_GST_BPA` decimal(10,2) NOT NULL DEFAULT '0.00',
  `CPR_TDS_HOSP_FEES` decimal(10,2) NOT NULL DEFAULT '0.00',
  `CPR_TDS_BPA_FEES` decimal(10,2) NOT NULL DEFAULT '0.00',
  `CPR_IFSC_CODE` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CPR_ACC_NUM` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CPR_UTR_NO` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CPR_UTR_DATE` datetime DEFAULT NULL,
  `CPR_13_NUM` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CPR_CDA_13_DATE` datetime DEFAULT NULL,
  `CPR_SCROLL_NUM` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CPR_SCROLL_DATE` datetime DEFAULT NULL,
  `CPR_REJ_SCROLL_NUM` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CPR_REJ_SCROLL_DATE` datetime DEFAULT NULL,
  `CPR_CMP_FILE_DATE` date DEFAULT NULL,
  `CPR_CMP_REJ_REASON` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CPR_BPA_FILE_DATE` date DEFAULT NULL,
  `CPR_BPA_PAY_REFNO` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CPR_BPA_UTR_NO` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CPR_BPA_UTR_DATE` date DEFAULT NULL,
  `CPR_BPA_SCROLL_NO` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CPR_BPA_SCROLL_DATE` date DEFAULT NULL,
  `CPR_BPA_CDA13_NO` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CPR_BPA_CDA13_DATE` date DEFAULT NULL,
  `CPR_BPA_REJ_SCROLL_NO` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CPR_BPA_REJ_SCROLL_DATE` date DEFAULT NULL,
  `CPR_BPA_REJ_REASON` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  PRIMARY KEY (`CPR_CLAIM_ID`),
  KEY `Idx_Settlement_Id` (`CPR_SETTLEMENT_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cda_reject_history`
--

DROP TABLE IF EXISTS `cda_reject_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cda_reject_history` (
  `CRH_SETTLEMENT_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `CRH_NEW_SETTLE_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `CRH_CLAIM_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `CRH_REJECT_SRNO` int DEFAULT '0',
  `CRH_REASON` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `CRH_DATE` datetime DEFAULT NULL,
  PRIMARY KEY (`CRH_SETTLEMENT_ID`,`CRH_NEW_SETTLE_ID`,`CRH_CLAIM_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cda_rejection_response`
--

DROP TABLE IF EXISTS `cda_rejection_response`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cda_rejection_response` (
  `CRR_CLAIM_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `CRR_SETTLEMENT_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `CRR_PAYEE_NAME` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CRR_IFSC_CODE` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CRR_ACC_NO` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CRR_PAN` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CRR_ACC_TYPE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CRR_REASON` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `CRR_REMARK` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`CRR_SETTLEMENT_ID`,`CRR_CLAIM_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cda_remarks`
--

DROP TABLE IF EXISTS `cda_remarks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cda_remarks` (
  `CDR_INTIMATION_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CDA_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CDA_DATE` datetime NOT NULL,
  `CDA_REMARKS` mediumtext NOT NULL,
  `CDA_STAGE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '1',
  `CDA_STATUS` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CDA_MODE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  KEY `Index_1` (`CDR_INTIMATION_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cghs_card_type`
--

DROP TABLE IF EXISTS `cghs_card_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cghs_card_type` (
  `CT_TYPE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `CT_TYPE_DESC` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CT_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`CT_TYPE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cghs_holiday`
--

DROP TABLE IF EXISTS `cghs_holiday`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cghs_holiday` (
  `CH_HOL_ID` decimal(10,0) NOT NULL,
  `CH_HOL_DATE` date NOT NULL,
  `CH_HOL_REASON` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CH_NOT_TAT` int NOT NULL DEFAULT '1',
  `CH_HOL_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CH_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CH_IP_ADDRESS` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CH_UPDATE_DATE` datetime DEFAULT NULL,
  PRIMARY KEY (`CH_HOL_ID`),
  UNIQUE KEY `Index_2` (`CH_HOL_DATE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cghs_region_master`
--

DROP TABLE IF EXISTS `cghs_region_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cghs_region_master` (
  `CRM_CITY_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `CRM_CITY_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CRM_CITY_CODE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CRM_RC_CODE` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CRM_CDA_CODE` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CRM_STATE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CRM_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CRM_PROC_RATE` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CRM_LAB_RATE` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CRM_CDA_REGION_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CRM_RATE_REMARK` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `CRM_EXP_BREAK` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'N',
  `CRM_UID_CHECK` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CRM_GSTTDS` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'N',
  `CRM_CURR_RATIO` decimal(8,2) NOT NULL DEFAULT '1.00',
  `CRM_SAME_REGION` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`CRM_CITY_ID`),
  KEY `FK_cghs_region_master_1` (`CRM_STATE_ID`),
  KEY `Idx_CDA_Region` (`CRM_CDA_REGION_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `check_list`
--

DROP TABLE IF EXISTS `check_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `check_list` (
  `CL_TYPE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `CL_TYPE_DESC` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CL_TYPE_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`CL_TYPE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `check_list_details`
--

DROP TABLE IF EXISTS `check_list_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `check_list_details` (
  `CLD_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `CLD_LIST_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `CLD_IS_PRESENT` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'N',
  PRIMARY KEY (`CLD_INTIMATION_ID`,`CLD_LIST_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `city_master`
--

DROP TABLE IF EXISTS `city_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `city_master` (
  `CM_CITY_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `CM_CITY_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CM_STATE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CM_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`CM_CITY_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `city_tier_master`
--

DROP TABLE IF EXISTS `city_tier_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `city_tier_master` (
  `CTM_ID` int NOT NULL,
  `CTM_NAME` varchar(45) DEFAULT NULL,
  `CTM_ACTIVE` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`CTM_ID`),
  UNIQUE KEY `CTM_NAME_UNIQUE` (`CTM_NAME`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `claim_alert_message`
--

DROP TABLE IF EXISTS `claim_alert_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `claim_alert_message` (
  `CAM_ID` int NOT NULL AUTO_INCREMENT,
  `CAM_CLAIM_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CAM_TOP_PRIOR` int NOT NULL DEFAULT '0',
  `CAM_MESSAGE` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `CAM_GROUP_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CAM_MESG_DATE` datetime NOT NULL,
  `CAM_MESG_BY` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CAM_POPUP_DATE` datetime DEFAULT NULL,
  `CAM_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CAM_ACTIVE` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`CAM_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=24786 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `claim_category`
--

DROP TABLE IF EXISTS `claim_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `claim_category` (
  `CC_CAT_ID` int unsigned NOT NULL,
  `CC_HEAD_ID` int unsigned NOT NULL DEFAULT '0',
  `CC_CAT_DESC` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CC_ACTIVE` int unsigned NOT NULL DEFAULT '1',
  PRIMARY KEY (`CC_CAT_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `claim_catg_header`
--

DROP TABLE IF EXISTS `claim_catg_header`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `claim_catg_header` (
  `CCH_ID` int unsigned NOT NULL,
  `CCH_DESC` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`CCH_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `claim_changes`
--

DROP TABLE IF EXISTS `claim_changes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `claim_changes` (
  `cc_intimation_id` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `cc_change_id` int unsigned DEFAULT '0',
  `cc_change_type` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `cc_change_desc` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `cc_prev_value` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `cc_curr_value` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `cc_user_id` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `cc_field_map` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CC_REQUEST_ID` int unsigned DEFAULT '0',
  KEY `Index_1` (`cc_intimation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `claim_enhancement`
--

DROP TABLE IF EXISTS `claim_enhancement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `claim_enhancement` (
  `CE_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `CE_ENHANCE_ID` int unsigned NOT NULL DEFAULT '0',
  `CE_ENHANCE_DATE` datetime NOT NULL,
  `CE_AILMENT` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CE_STAGE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CE_STATUS` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CE_USERID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`CE_INTIMATION_ID`,`CE_ENHANCE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `claim_folder`
--

DROP TABLE IF EXISTS `claim_folder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `claim_folder` (
  `CF_CLAIM_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `CF_DATE` datetime NOT NULL,
  `CF_OFFICE_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CF_FOLDER` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CF_FLDR_CRTN_DT` date DEFAULT NULL,
  `CF_FLDR_LCTN` int DEFAULT '0',
  PRIMARY KEY (`CF_CLAIM_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `claim_in_progress`
--

DROP TABLE IF EXISTS `claim_in_progress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `claim_in_progress` (
  `CIP_CLAIM_ID` int NOT NULL,
  `CIP_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CIP_ALLOT_ID` int DEFAULT NULL,
  `CIP_SETUP_ID` int DEFAULT NULL,
  `CIP_DATE` datetime NOT NULL,
  `CIP_SKIP_LIST` int DEFAULT '0',
  `CIP_NMI_LIST` int DEFAULT '0',
  PRIMARY KEY (`CIP_CLAIM_ID`),
  KEY `IDX_USER` (`CIP_USER_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `claim_intimation`
--

DROP TABLE IF EXISTS `claim_intimation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `claim_intimation` (
  `CI_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `CI_BENF_ID` decimal(10,0) DEFAULT '0',
  `CI_DEP_ID` decimal(10,0) DEFAULT '0',
  `CI_PATIENT_TYPE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_ADMISSION_NO` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_ADMISSION_DATE` datetime DEFAULT NULL,
  `CI_CARD_ID` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_CARD_MAKE` int DEFAULT '0',
  `CI_WHITE_CARD` int DEFAULT '0',
  `CI_APP_TYPE_ID` int DEFAULT '0',
  `CI_DIS_TYPE_ID` int DEFAULT '0',
  `CI_SERV_PERIOD` int DEFAULT '0',
  `CI_BENEFICIARY_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_CARD_TYPE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_CARD_VALID_DT` date DEFAULT NULL,
  `CI_OFFICE_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_OFFICE_DEPARTMENT` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_PATIENT_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_AGE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_SEX` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_RELATION_ID` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_PHONE_NO` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_MOBILE` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_EMAIL` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_ADDRESS1` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_ADDRESS2` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_ADDRESS3` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_CITY` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_STATE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_PIN` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_CGHS_REGION_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_HOSPITAL_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_ROOM_TYPE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_REF_TYPE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_ADM_AILMENT` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `CI_PRE_AILMENT_DUR` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_IS_RTA` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_RTA_REASON` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_RTA_DATE` date DEFAULT NULL,
  `CI_RTA_DOC_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_INT_STATUS` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_INT_STAGE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_CR_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_CR_DATE` datetime DEFAULT NULL,
  `CI_CR_OFFICE_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_CR_ENTITY_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_ROOM_NO` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_HOSPITAL_REMARK` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `CI_CARD_ROOM_TYPE` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_EXP_DOD` datetime DEFAULT NULL,
  `CI_UP_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_UP_DATE` datetime DEFAULT NULL,
  `CI_UP_OFFICE_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_UP_ENTITY_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_ENTITLEMENT_REMARK` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `CI_ENTITLEDIFF_REASON` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_SETTLEMENT_ID` decimal(10,0) DEFAULT NULL,
  `CI_INT_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_INT_DATE` datetime DEFAULT NULL,
  `CI_INT_OFFICE_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_INT_ENTITY_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_DEDUCT_ID` int DEFAULT '0',
  `CI_SERVICE_TYPE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_SERVICE_RANK` int DEFAULT '0',
  `CI_EXTENDED_STAY` int DEFAULT NULL,
  `CI_SERVICE_NO` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_CFA_REVIEW` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'N',
  `CI_NONEMPANELLED_HOSPITAL` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_REQUEST_ID` int unsigned DEFAULT '0',
  `CI_NONEMP_FLG` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_AUDIT_STAGE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_AUDIT_STATUS` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_AUDIT_SEND` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_AUDIT_DATE_1` datetime DEFAULT NULL,
  `CI_AUDIT_DATE_2` datetime DEFAULT NULL,
  `CI_AUDIT_DATE_3` datetime DEFAULT NULL,
  `CI_REPLY_DATE` datetime DEFAULT NULL,
  `CI_LAST_AUDIT_BY_1` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_LAST_AUDIT_BY_2` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_LAST_AUDIT_BY_3` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_LAST_REPLY_BY` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_EXP_BREAK` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_APPROX_COST` decimal(14,2) DEFAULT '0.00',
  `CI_REF_CLAIM_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_UID_NUMBER` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_UID_STATUS` int DEFAULT '0',
  `CI_REIMB_TYPE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_DRAFT_SAVE` int DEFAULT '0',
  PRIMARY KEY (`CI_INTIMATION_ID`),
  KEY `FK_claim_intimation_1` (`CI_PATIENT_TYPE`),
  KEY `FK_claim_intimation_2` (`CI_RELATION_ID`),
  KEY `Index_4` (`CI_SERVICE_NO`),
  KEY `Index_5` (`CI_CR_OFFICE_ID`),
  KEY `Index_6` (`CI_INT_OFFICE_ID`),
  KEY `Index_7` (`CI_INT_STAGE`),
  KEY `Index_8` (`CI_INT_STATUS`),
  KEY `Idx_Audit_Status` (`CI_AUDIT_STATUS`),
  KEY `Idx_Card_Id` (`CI_CARD_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `claim_lock`
--

DROP TABLE IF EXISTS `claim_lock`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `claim_lock` (
  `cl_claim_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `cl_session_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `cl_user_id` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `cl_ip_address` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `cl_lock_date` datetime DEFAULT NULL,
  PRIMARY KEY (`cl_claim_id`),
  KEY `Index_1` (`cl_claim_id`),
  KEY `Index_2` (`cl_lock_date`),
  KEY `Index_3` (`cl_user_id`),
  KEY `Index_4` (`cl_session_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `claim_remarks`
--

DROP TABLE IF EXISTS `claim_remarks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `claim_remarks` (
  `CR_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CR_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CR_USER_REMARKS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `CR_UPDATE_DATE` datetime NOT NULL,
  `CR_INT_STAGE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CR_REMARK_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CR_INT_STATUS` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CR_HISTORY_ID` int unsigned DEFAULT '0',
  `CR_ENHANCE_ID` int DEFAULT '0',
  `CR_IP_ADDRESS` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CR_AUTO_UPDATE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'N',
  `CR_CHANGE_ID` int unsigned DEFAULT NULL,
  `CR_REQUEST_ID` int unsigned NOT NULL DEFAULT '0',
  KEY `FK_claim_remarks_1` (`CR_INTIMATION_ID`) USING BTREE,
  KEY `Index_2` (`CR_UPDATE_DATE`),
  KEY `Index_3` (`CR_USER_ID`),
  KEY `idx_cr_int_stage` (`CR_INT_STAGE`),
  KEY `idx_cr_int_status` (`CR_INT_STATUS`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `claim_request`
--

DROP TABLE IF EXISTS `claim_request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `claim_request` (
  `CQ_REQUEST_ID` int unsigned NOT NULL AUTO_INCREMENT,
  `CQ_CLAIM_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CQ_REQ_PROC` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CQ_REQ_DATE` datetime NOT NULL,
  `CQ_REQ_USER_ID` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CQ_REQ_REMARK` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `CQ_REQ_IPADDRESS` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CQ_PROC_STATUS` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'P',
  `CQ_PROC_DATE` datetime DEFAULT NULL,
  `CQ_PROC_USER_ID` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CQ_PROC_REMARK` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `CQ_PROC_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'Y',
  PRIMARY KEY (`CQ_REQUEST_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=450142 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `claim_sequence`
--

DROP TABLE IF EXISTS `claim_sequence`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `claim_sequence` (
  `ID` bigint NOT NULL DEFAULT '0',
  `MIN_VALUE` int NOT NULL DEFAULT '0',
  `MAX_VALUE` bigint NOT NULL DEFAULT '0',
  `RESET_ON_MAX` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'N',
  `RESET_FREQUENCY` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '0',
  `LAST_ACCESS_ON` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `claim_submission`
--

DROP TABLE IF EXISTS `claim_submission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `claim_submission` (
  `CS_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `CS_ADMISSION_DATE` datetime DEFAULT NULL,
  `CS_ADM_AILMENT` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `CS_PRE_AILMENT_DUR` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_AILMENT_HIST` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_FIRST_OCC_DATE` date DEFAULT NULL,
  `CS_DOD` datetime DEFAULT NULL,
  `CS_DISCHARGE_TYPE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_TREAT_DOCT` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_SUB_DATE` datetime DEFAULT NULL,
  `CS_SUB_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_SUB_OFFICE_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_SUB_ENTITY_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_ACCEPT_DATE` datetime DEFAULT NULL,
  `CS_GR_CLAIM_AMT` decimal(15,2) unsigned DEFAULT '0.00',
  `CS_PAT_AMT` decimal(15,2) unsigned DEFAULT '0.00',
  `CS_PAT_DISC_AMT` decimal(15,2) unsigned DEFAULT '0.00',
  `CS_NET_CLAIM_AMT` decimal(15,2) unsigned DEFAULT '0.00',
  `CS_UTI_PAR_AMT` decimal(15,2) unsigned DEFAULT '0.00',
  `CS_UTI_SUP_AMT` decimal(15,2) unsigned DEFAULT '0.00',
  `CS_UTI_APP_AMT` decimal(15,2) DEFAULT '0.00',
  `CS_ROOM_TYPE` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_ROOM_NO` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_PAR_IRREV_CHARGES` decimal(15,2) DEFAULT '0.00',
  `CS_PAR_EXCESS_AMT` decimal(15,2) DEFAULT '0.00',
  `CS_SUP_IRREV_CHARGES` decimal(15,2) DEFAULT '0.00',
  `CS_SUP_EXCESS_AMT` decimal(15,2) DEFAULT '0.00',
  `CS_APP_IRREV_CHARGES` decimal(15,2) DEFAULT '0.00',
  `CS_APP_EXCESS_AMT` decimal(15,2) DEFAULT '0.00',
  `CS_PAT_DIS_STATUS` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_REC_DATE` datetime DEFAULT NULL,
  `CS_REC_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_REC_OFFICE_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_REC_ENTITY_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_PAR_DATE` datetime DEFAULT NULL,
  `CS_PAR_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_PAR_OFFICE_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_PAR_ENTITY_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_SUP_DATE` datetime DEFAULT NULL,
  `CS_SUP_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_SUP_OFFICE_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_SUP_ENTITY_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_APP_DATE` datetime DEFAULT NULL,
  `CS_APP_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_APP_OFFICE_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_APP_ENTITY_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_BILL_NO` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_BILL_DATE` date DEFAULT NULL,
  `CS_PHY_REC_DATE` date DEFAULT NULL,
  `CS_PHY_REC_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_PHY_OFFICE_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_PHY_REC_ENTITY_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_LAST_HISTORY_ID` int unsigned NOT NULL,
  `CS_IFA_CFA_FWD` int DEFAULT '0',
  `CS_IFA_ALLOT_ID` int DEFAULT '0',
  `CS_IFA_STAGE` int DEFAULT '0',
  `CS_IFA_DATE` datetime DEFAULT NULL,
  `CS_CFA_DATE` datetime DEFAULT NULL,
  `CS_SETTLE_DATE` datetime DEFAULT NULL,
  `CS_ARBITAGE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'N',
  `CS_ALLOTED_TO` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_ALLOTED_DATE` datetime DEFAULT NULL,
  `CS_CON_NET_AMT` int DEFAULT '0',
  `CS_CLAIM_CATEGORY` int unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`CS_INTIMATION_ID`),
  KEY `Index_2` (`CS_SUB_OFFICE_ID`),
  KEY `Index_3` (`CS_BILL_NO`),
  KEY `idx_cs_alloted_to` (`CS_ALLOTED_TO`),
  KEY `idx_CS_SUB_ENTITY_ID` (`CS_SUB_ENTITY_ID`),
  KEY `idx_CS_UTI_SUP_AMT` (`CS_UTI_SUP_AMT`),
  KEY `idx_CS_UTI_APP_AMT` (`CS_UTI_APP_AMT`),
  KEY `idx_CS_NET_CLAIM_AMT` (`CS_NET_CLAIM_AMT`),
  KEY `Idx_CFA_DATE` (`CS_CFA_DATE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `claim_work_sheet`
--

DROP TABLE IF EXISTS `claim_work_sheet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `claim_work_sheet` (
  `cws_intimation_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `cws_work_sheet` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`cws_intimation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `claimstage_description`
--

DROP TABLE IF EXISTS `claimstage_description`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `claimstage_description` (
  `CSD_STAGE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `CSD_STATUS` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `CSD_DESCP` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CSD_DESCP_DASHBOARD` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CSD_LIST_TITLE` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CSD_LIST_TITLE_DB` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CSD_PAGE_TITLE` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CSD_PAGE_TITLE_DB` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`CSD_STAGE`,`CSD_STATUS`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `clinical_findings_int`
--

DROP TABLE IF EXISTS `clinical_findings_int`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clinical_findings_int` (
  `CF_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `CF_CLTEST_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `CT_IS_CLTEST` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CF_CLTEST_DETAILS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `CF_ENHANCE_ID` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`CF_INTIMATION_ID`,`CF_CLTEST_ID`,`CF_ENHANCE_ID`) USING BTREE,
  KEY `FK_clinical_findings_int_1` (`CF_CLTEST_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `clinical_findings_sub`
--

DROP TABLE IF EXISTS `clinical_findings_sub`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clinical_findings_sub` (
  `CF_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `CF_CLTEST_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `CT_IS_CLTEST` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CF_CLTEST_DETAILS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  PRIMARY KEY (`CF_INTIMATION_ID`,`CF_CLTEST_ID`),
  KEY `FK_clinical_findings_sub_1` (`CF_CLTEST_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `clinical_test_type`
--

DROP TABLE IF EXISTS `clinical_test_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clinical_test_type` (
  `CFT_CLTEST_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `CFT_CLTEST_DESC` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CFT_CLTEST_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`CFT_CLTEST_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `consult_map`
--

DROP TABLE IF EXISTS `consult_map`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `consult_map` (
  `CM_ID` int NOT NULL,
  `CM_FROM_DATE` date NOT NULL,
  `CM_TO_DATE` date DEFAULT NULL,
  `CM_PROC_ID` int NOT NULL,
  PRIMARY KEY (`CM_ID`,`CM_FROM_DATE`,`CM_PROC_ID`),
  UNIQUE KEY `idx_unique` (`CM_ID`,`CM_FROM_DATE`,`CM_TO_DATE`,`CM_PROC_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `consult_types`
--

DROP TABLE IF EXISTS `consult_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `consult_types` (
  `CT_ID` int NOT NULL AUTO_INCREMENT,
  `CT_NAME` varchar(100) NOT NULL,
  `CT_ACTIVE` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`CT_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `country_master`
--

DROP TABLE IF EXISTS `country_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `country_master` (
  `CM_ID` int NOT NULL,
  `CM_NAME` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CM_CNTRY_CODE` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CM_NORTH_LAT` decimal(12,8) DEFAULT NULL,
  `CM_SOUTH_LAT` decimal(12,8) DEFAULT NULL,
  `CM_EAST_LON` decimal(12,8) DEFAULT NULL,
  `CM_WEST_LON` decimal(12,8) DEFAULT NULL,
  PRIMARY KEY (`CM_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `daily_allot_changes`
--

DROP TABLE IF EXISTS `daily_allot_changes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `daily_allot_changes` (
  `DAC_ID` int NOT NULL,
  `DAC_SETUP_ID` int DEFAULT NULL,
  `DAC_DATE` date DEFAULT NULL,
  `DAC_CHANGES` int DEFAULT '0',
  PRIMARY KEY (`DAC_ID`),
  UNIQUE KEY `IDX_UNQ` (`DAC_SETUP_ID`,`DAC_DATE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `daily_allot_summary`
--

DROP TABLE IF EXISTS `daily_allot_summary`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `daily_allot_summary` (
  `DAS_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `DAS_DATE` date NOT NULL,
  `DAS_ALLOT_TYPE` int NOT NULL DEFAULT '1',
  `DAS_SETUP_ID` int NOT NULL,
  `DAS_TARGET` int NOT NULL DEFAULT '0',
  `DAS_DONE` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`DAS_USER_ID`,`DAS_DATE`,`DAS_ALLOT_TYPE`,`DAS_SETUP_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `daily_office_pendency`
--

DROP TABLE IF EXISTS `daily_office_pendency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `daily_office_pendency` (
  `DOP_DATE_ID` int NOT NULL DEFAULT '0',
  `DOP_REGION_ID` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `DOP_OFFICE_ID` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `DOP_PATIENT_TYPE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `DOP_ADM_TYPE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `DOP_STAGE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `DOP_STATUS` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `DOP_GROUP_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `DOP_CLAIM_COUNT` int DEFAULT '0',
  `DOP_TOTAL_NET` bigint DEFAULT '0',
  `DOP_TOTAL_SUP` bigint DEFAULT '0',
  `DOP_TOTAL_APP` bigint DEFAULT '0',
  PRIMARY KEY (`DOP_REGION_ID`,`DOP_OFFICE_ID`,`DOP_PATIENT_TYPE`,`DOP_ADM_TYPE`,`DOP_STAGE`,`DOP_STATUS`,`DOP_GROUP_ID`,`DOP_DATE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `daily_pendency`
--

DROP TABLE IF EXISTS `daily_pendency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `daily_pendency` (
  `DP_DATE` date NOT NULL,
  `DP_REGION_ID` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `DP_ENTITY_ID` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `DP_PATIENT_TYPE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `DP_ADM_TYPE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `DP_STAGE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `DP_STATUS` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `DP_GROUP_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `DP_CLAIM_COUNT` int DEFAULT '0',
  `DP_TOTAL_NET` bigint DEFAULT '0',
  `DP_TOTAL_SUP` bigint DEFAULT '0',
  `DP_TOTAL_APP` bigint DEFAULT '0',
  PRIMARY KEY (`DP_DATE`,`DP_REGION_ID`,`DP_PATIENT_TYPE`,`DP_ENTITY_ID`,`DP_ADM_TYPE`,`DP_STAGE`,`DP_STATUS`,`DP_GROUP_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `daily_region_pendency`
--

DROP TABLE IF EXISTS `daily_region_pendency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `daily_region_pendency` (
  `DP_DATE_ID` int NOT NULL DEFAULT '0',
  `DP_REGION_ID` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `DP_ENTITY_ID` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `DP_PATIENT_TYPE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `DP_ADM_TYPE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `DP_STAGE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `DP_STATUS` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `DP_GROUP_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `DP_CLAIM_COUNT` int DEFAULT '0',
  `DP_TOTAL_NET` bigint DEFAULT '0',
  `DP_TOTAL_SUP` bigint DEFAULT '0',
  `DP_TOTAL_APP` bigint DEFAULT '0',
  PRIMARY KEY (`DP_REGION_ID`,`DP_ENTITY_ID`,`DP_PATIENT_TYPE`,`DP_ADM_TYPE`,`DP_STAGE`,`DP_STATUS`,`DP_GROUP_ID`,`DP_DATE_ID`),
  KEY `idx_id` (`DP_DATE_ID`),
  KEY `idx_region_id` (`DP_REGION_ID`),
  KEY `id_group_id` (`DP_GROUP_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dash_group_master`
--

DROP TABLE IF EXISTS `dash_group_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dash_group_master` (
  `dash_grp_id` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `dash_grp_desc` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `dash_grp_srno` decimal(10,0) NOT NULL DEFAULT '0',
  PRIMARY KEY (`dash_grp_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dashboard_det`
--

DROP TABLE IF EXISTS `dashboard_det`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dashboard_det` (
  `dash_group` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '0',
  `dash_stage` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `dash_status` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `dash_desp` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `dash_history` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `dash_enhance` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `dash_short_desc` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `dash_srno` int unsigned NOT NULL DEFAULT '0',
  `dash_group_id` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `dash_entity_id` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `dash_que` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`dash_group`,`dash_stage`,`dash_status`,`dash_history`,`dash_enhance`),
  KEY `Idx_Stage_Status` (`dash_stage`,`dash_status`),
  KEY `Idx_Group` (`dash_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dbt_xml_detail`
--

DROP TABLE IF EXISTS `dbt_xml_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dbt_xml_detail` (
  `DXD_HEADER_ID` int NOT NULL,
  `DXD_ID` int NOT NULL,
  `DXD_ORDER_NUM` int NOT NULL,
  `DXD_XML_TAG` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `DXD_XML_DESP` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `DXD_BPA_SOURCE` int NOT NULL DEFAULT '0',
  `DXD_BPA_FIELD` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DXD_DEF_VALUE` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DXD_ACTIVE` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`DXD_ID`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dbt_xml_header`
--

DROP TABLE IF EXISTS `dbt_xml_header`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dbt_xml_header` (
  `DXH_ID` int NOT NULL,
  `DXH_XML_TAG` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DXH_XML_TEXT` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  PRIMARY KEY (`DXH_ID`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dbt_xml_transaction`
--

DROP TABLE IF EXISTS `dbt_xml_transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dbt_xml_transaction` (
  `DXT_YEAR` int NOT NULL,
  `DXT_MONTH` int NOT NULL,
  `DXT_ID` int NOT NULL,
  `DXT_DATE` date NOT NULL,
  `DXT_VALUE` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`DXT_YEAR`,`DXT_MONTH`,`DXT_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `deduction_reasons`
--

DROP TABLE IF EXISTS `deduction_reasons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `deduction_reasons` (
  `DR_ID` int NOT NULL AUTO_INCREMENT,
  `DR_NAME` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DR_ACTIVE` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`DR_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `del_prop_treatment`
--

DROP TABLE IF EXISTS `del_prop_treatment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `del_prop_treatment` (
  `PT_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PT_TRTYPE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PR_IS_TREATMENT` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PR_TR_DETAILS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `PR_ENHANCE_ID` int NOT NULL DEFAULT '0',
  `PR_PRE_AUTH_ID` int NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dep_master_live`
--

DROP TABLE IF EXISTS `dep_master_live`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dep_master_live` (
  `DEP_BEN_ID` decimal(10,0) NOT NULL DEFAULT '0',
  `DEP_ID` decimal(10,0) NOT NULL DEFAULT '0',
  `DEP_NAME` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DEP_GENDER` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DEP_RELN` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DEP_RELATION_ID` int NOT NULL DEFAULT '0',
  `DEP_DOB` date DEFAULT NULL,
  `DEP_DOE` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DEP_BLOOD_GRP` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DEP_CARD_NO` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DEP_NEW_CARD_NO` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`DEP_ID`),
  KEY `Index_1` (`DEP_BEN_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dependant_master`
--

DROP TABLE IF EXISTS `dependant_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dependant_master` (
  `DEP_BENF_ID` decimal(10,0) DEFAULT NULL,
  `DEP_ID` decimal(10,0) DEFAULT NULL,
  `DEP_CARD_NO` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DEP_NAME` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DEP_BLOOD_GRP` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DEP_STATUS` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DEP_RELN` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DEP_EMP` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DEP_DOB` date DEFAULT NULL,
  `DEP_HANDICAP` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DEP_POLY` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DEP_CITY` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DEP_STATE` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DEP_PIN` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DEP_WAR_WIDOW` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DEP_GENDER` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'M',
  `DEP_RELATION_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '0',
  KEY `Index_1` (`DEP_CARD_NO`),
  KEY `Index_2` (`DEP_BENF_ID`),
  KEY `Index_3` (`DEP_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `diag_details`
--

DROP TABLE IF EXISTS `diag_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `diag_details` (
  `DD_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `DD_DIAG_SEQ_NO` int unsigned NOT NULL,
  `DD_DIAG_TYPE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DD_DIAG_DETAILS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `DD_DIAG_ICD_CODE` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DD_DIAG_PAR_DETAILS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `DD_DIAG_PAR_ICD_CODE` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DD_DIAG_PAR_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'Y',
  `DD_DIAG_SUP_DETAILS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `DD_DIAG_SUP_ICD_CODE` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DD_DIAG_SUP_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'Y',
  `DD_DIAG_APP_DETAILS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `DD_DIAG_APP_ICD_CODE` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DD_DIAG_APP_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'Y',
  `DD_ALREADY_SUBMITTED` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'N',
  `DD_ENHANCE_ID` int unsigned DEFAULT '0',
  PRIMARY KEY (`DD_INTIMATION_ID`,`DD_DIAG_SEQ_NO`),
  KEY `FK_diag_details_1` (`DD_DIAG_TYPE_ID`),
  KEY `Idx_Diag_ICD_Code` (`DD_DIAG_ICD_CODE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Diagonisis Details; InnoDB free: 13312 kB; (`DD_DIAG_TYPE_ID';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `diag_type`
--

DROP TABLE IF EXISTS `diag_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `diag_type` (
  `DT_DIAG_TYPE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `DT_DIAG_TYPE_CODE` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DT_DIAG_TYPE_DESC` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DT_DIAG_TYPE_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DT_DIAG_STAGE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'I',
  PRIMARY KEY (`DT_DIAG_TYPE_ID`),
  KEY `Idx_Diag_Stage` (`DT_DIAG_STAGE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `disability_master`
--

DROP TABLE IF EXISTS `disability_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `disability_master` (
  `DM_ID` int NOT NULL DEFAULT '0',
  `DM_DESC` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DM_WHITE_CARD` int unsigned NOT NULL DEFAULT '1',
  PRIMARY KEY (`DM_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `discharge_type`
--

DROP TABLE IF EXISTS `discharge_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `discharge_type` (
  `DT_TYPE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `DT_TYPE_DESC` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DT_TYPE_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DT_TYPE_CODE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`DT_TYPE_ID`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `district_master`
--

DROP TABLE IF EXISTS `district_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `district_master` (
  `DM_CODE` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `DM_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DM_STATE_CODE` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`DM_CODE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `district_state`
--

DROP TABLE IF EXISTS `district_state`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `district_state` (
  `DM_DISTRICT_CODE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DM_DISTRICT_NAME` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DM_STATE_CODE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DM_STATE_NAME` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `doc_check_list`
--

DROP TABLE IF EXISTS `doc_check_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doc_check_list` (
  `DCL_DOC_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `DCL_DOC_DESC` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DCL_DOC_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DCL_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'Y',
  PRIMARY KEY (`DCL_DOC_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `doc_mgrt_ngc_list2`
--

DROP TABLE IF EXISTS `doc_mgrt_ngc_list2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doc_mgrt_ngc_list2` (
  `dmnl_id` int NOT NULL AUTO_INCREMENT,
  `dmnl_fld1` varchar(45) DEFAULT NULL,
  `dmnl_fld2` varchar(45) DEFAULT NULL,
  `dmnl_fld3` varchar(45) DEFAULT NULL,
  `dmnl_fld4` varchar(45) DEFAULT NULL,
  `dmnl_doc_sz` varchar(6) DEFAULT NULL,
  `dmnl_doc_mnth` varchar(5) DEFAULT NULL,
  `dmnl_doc_dt` varchar(5) DEFAULT NULL,
  `dmnl_doc_yr` varchar(5) DEFAULT NULL,
  `dmnl_doc_clmid` varchar(10) DEFAULT NULL,
  `dmnl_doc_upld_tm` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`dmnl_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `document_list`
--

DROP TABLE IF EXISTS `document_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `document_list` (
  `DL_DOC_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `DL_DOC_DESC` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DL_DOC_TYPE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `DL_DOC_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DL_DOC_NAME_CONV` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DL_IS_MULT_DOC` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DL_MUL_DOC_NAME_CONV` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DL_SRNO` int unsigned NOT NULL DEFAULT '0',
  `DL_DISPLAY_ORDER` int NOT NULL,
  `DL_FOR_IP` int NOT NULL DEFAULT '1',
  `DL_FOR_OPD` int NOT NULL DEFAULT '1',
  `DL_IP_STAGE` int NOT NULL DEFAULT '0',
  `DL_OPD_STAGE` int NOT NULL DEFAULT '0',
  `DL_FOR_MEMBILL` int NOT NULL DEFAULT '1',
  `DL_IP_MANDATORY` int NOT NULL DEFAULT '0',
  `DL_OP_MANDATORY` int NOT NULL DEFAULT '0',
  `DL_REF` int NOT NULL DEFAULT '0',
  `DL_EMER` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`DL_DOC_ID`,`DL_DOC_TYPE_ID`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `document_require`
--

DROP TABLE IF EXISTS `document_require`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `document_require` (
  `DR_DOC_ID` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `DR_CLAIM_TYPE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `DR_PT_TYPE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `DR_IS_REQ` int DEFAULT '1',
  `DR_IS_MAND` int DEFAULT '0',
  `DR_IS_REF` int DEFAULT '0',
  `DR_IS_EMER` int DEFAULT '0',
  `DR_INT_STAGE` int DEFAULT '0',
  `DR_SUB_STAGE` int DEFAULT '0',
  `DR_ORDER` int DEFAULT NULL,
  `DR_CONDITION` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  PRIMARY KEY (`DR_DOC_ID`,`DR_CLAIM_TYPE`,`DR_PT_TYPE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `document_submitted`
--

DROP TABLE IF EXISTS `document_submitted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `document_submitted` (
  `DS_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `DS_DOCTYPE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DS_DOC_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DS_REMARK` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `DS_FILENAME` varchar(75) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DS_FILE_SR_NO` int NOT NULL,
  `DS_IS_RECEIVED` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DS_REC_REMARK` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `DS_REC_REMARK_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DS_MUL_DOC` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DS_DOC_SUBMITTED` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DS_DOC_COUNT` int unsigned DEFAULT '1',
  `DS_DOC_SUBMIT_BY` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DS_ENHANCE_ID` int(10) unsigned zerofill DEFAULT '0000000000',
  `DS_SUBMIT_TIME` datetime DEFAULT NULL,
  `DS_FILE_SIZE` decimal(10,2) DEFAULT NULL,
  `DS_SIGNED` int unsigned DEFAULT '0',
  PRIMARY KEY (`DS_INTIMATION_ID`,`DS_FILE_SR_NO`),
  KEY `Index_1` (`DS_INTIMATION_ID`),
  KEY `FK_document_submitted_2` (`DS_DOCTYPE_ID`),
  KEY `Idx_Signed` (`DS_SIGNED`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `document_type`
--

DROP TABLE IF EXISTS `document_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `document_type` (
  `DT_DOCTYPE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `DT_DOCTYPE_DESC` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DT_DOCTYPE_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DT_SUBMIT_BY` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'I',
  `DT_SRNO` int unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`DT_DOCTYPE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dsc_upload`
--

DROP TABLE IF EXISTS `dsc_upload`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dsc_upload` (
  `DU_OFFICE_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `DU_FILE_NAME` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DU_FROM_DATE` date NOT NULL,
  `DU_TO_DATE` date NOT NULL,
  `DU_THUMB_PRINT` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DU_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DU_IP_ADDRESS` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DU_UPLOAD_DATE` datetime NOT NULL,
  PRIMARY KEY (`DU_OFFICE_ID`,`DU_FROM_DATE`,`DU_TO_DATE`),
  CONSTRAINT `FK_DSC_OFFICE_ID` FOREIGN KEY (`DU_OFFICE_ID`) REFERENCES `office_master` (`OM_OFFICE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `echs_64bit_card`
--

DROP TABLE IF EXISTS `echs_64bit_card`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `echs_64bit_card` (
  `EBC_CARD_NUMBER` int NOT NULL DEFAULT '0',
  `EBC_TEMP_SLIP_NO` int DEFAULT '0',
  `EBC_RC_CARD_ID` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBC_BEN_ID` int NOT NULL DEFAULT '0',
  `EBC_BENEFICIARY_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBC_PATIENT_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBC_SERVICE_TYPE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBC_SERVICE_RANK` int DEFAULT '0',
  `EBC_SERVICE_NO` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBC_COMM_DATE` date DEFAULT NULL,
  `EBC_RETIRE_DATE` date DEFAULT NULL,
  `EBC_APP_TYPE_ID` int DEFAULT '0',
  `EBC_DIS_TYPE_ID` int DEFAULT '0',
  `EBC_BLOOD_GROUP` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBC_UID_NUMBER` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBC_UID_STATUS` int DEFAULT '4',
  `EBC_DOB` date DEFAULT NULL,
  `EBC_DOE` date DEFAULT NULL,
  `EBC_GENDER` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBC_RELATION_ID` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBC_PHONE_NO` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBC_MOBILE` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBC_EMAIL` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBC_ADDRESS1` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBC_ADDRESS2` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBC_ADDRESS3` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBC_CITY` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBC_STATE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBC_PIN` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBC_CARD_ROOM_TYPE` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBC_CR_USER` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBC_CR_DATE` datetime NOT NULL,
  `EBC_IP_ADDRESS` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBC_MAIN_CLINIC_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBC_FROM_API` int DEFAULT '1',
  PRIMARY KEY (`EBC_CARD_NUMBER`),
  UNIQUE KEY `uq_benf_id` (`EBC_BEN_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ecs_contra`
--

DROP TABLE IF EXISTS `ecs_contra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecs_contra` (
  `EC_TRAN_CODE` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EC_USER_NO` varchar(7) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EC_USER_NAME` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EC_CR_REF` varchar(14) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `EC_TAPE_NO` varchar(9) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EC_SP_BNK_BRN_SORT_CD` varchar(9) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EC_USER_BNK_ACNO` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EC_FOLIO_NO` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EC_CR_LIMIT` varchar(13) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EC_TOT_AMT` varchar(13) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EC_SETTLE_DT` datetime NOT NULL,
  `EC_RESV_1` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EC_RESV_2` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EC_FILLER` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`EC_CR_REF`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ecs_control`
--

DROP TABLE IF EXISTS `ecs_control`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecs_control` (
  `EC_USER_NO` varchar(7) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EC_USER_NAME` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EC_SP_BNK_BRN_SORT_CD` varchar(9) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EC_USER_BNK_ACNO` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EC_CR_LIMIT` varchar(13) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EC_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EC_CGHS_CITY_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `EC_PAY_MODE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`EC_CGHS_CITY_ID`,`EC_PAY_MODE`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ecs_cr_recs`
--

DROP TABLE IF EXISTS `ecs_cr_recs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecs_cr_recs` (
  `ECR_TRAN_CODE` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ECR_DES_BNK_BRN_SORT_CD` varchar(9) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ECR_DES_BNK_ACTYPE` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ECR_FOLIO_NO` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ECR_DES_BNK_ACNO` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ECR_DES_BENE_NAME` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ECR_SP_BNK_BRN_SORT_CD` varchar(9) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ECR_USER_NO` varchar(7) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ECR_USER_NAME` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ECR_CR_REF` varchar(13) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `ECR_CR_AMOUNT` varchar(13) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ECR_RESV_1` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ECR_RESV_2` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ECR_RESV_3` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ECR_FILLER` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ECR_SETTLEMENT_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ECR_TRAN_NO` int unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`ECR_CR_REF`,`ECR_TRAN_NO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ecs_region`
--

DROP TABLE IF EXISTS `ecs_region`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecs_region` (
  `ER_REGION_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `ER_REGION_CODE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ER_REGION_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ER_REGION_ACIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`ER_REGION_ID`),
  KEY `Idx_Region_Active` (`ER_REGION_ACIVE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `emergency_data_daily`
--

DROP TABLE IF EXISTS `emergency_data_daily`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `emergency_data_daily` (
  `edd_intimation_id` int unsigned NOT NULL AUTO_INCREMENT,
  `edd_region_id` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `edd_cghs_disp_id` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `edd_hosp_id` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `edd_update_date` datetime NOT NULL,
  PRIMARY KEY (`edd_intimation_id`),
  KEY `Idx_Region_Id` (`edd_region_id`),
  KEY `Idx_Disp_Id` (`edd_cghs_disp_id`),
  KEY `Idx_Hosp_Id` (`edd_hosp_id`),
  KEY `Idx_Cr_Date` (`edd_update_date`)
) ENGINE=InnoDB AUTO_INCREMENT=43827164 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `empanel_facility`
--

DROP TABLE IF EXISTS `empanel_facility`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `empanel_facility` (
  `EF_HEADER_ID` int NOT NULL,
  `EF_FACILITY_ID` int NOT NULL,
  `EF_FACILITY` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`EF_FACILITY_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `empanel_header`
--

DROP TABLE IF EXISTS `empanel_header`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `empanel_header` (
  `EH_ID` int NOT NULL,
  `EH_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`EH_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `empanel_hospital_service`
--

DROP TABLE IF EXISTS `empanel_hospital_service`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `empanel_hospital_service` (
  `EHS_OFFICE_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `EHS_ID` int DEFAULT '0',
  `EHS_FACILITY_ID` int NOT NULL,
  `EHS_FROM_DATE` date NOT NULL,
  `EHS_TO_DATE` date NOT NULL,
  PRIMARY KEY (`EHS_OFFICE_ID`,`EHS_FACILITY_ID`,`EHS_FROM_DATE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `error_class`
--

DROP TABLE IF EXISTS `error_class`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `error_class` (
  `EC_ERROR_ID` decimal(10,0) DEFAULT NULL,
  `EC_FILENAME` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EC_METHODNAME` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EC_LINENUMBER` int unsigned DEFAULT NULL,
  KEY `Idx_id` (`EC_ERROR_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `error_log`
--

DROP TABLE IF EXISTS `error_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `error_log` (
  `EL_ERROR_ID` decimal(10,0) NOT NULL DEFAULT '0',
  `EL_DATE` datetime DEFAULT NULL,
  `EL_USER_ID` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EL_GROUP_NAME` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EL_STATUS` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EL_CLAIM_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EL_ERROR_TYPE` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EL_ERROR_MESSAGE` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `EL_IP_ADDRESS` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`EL_ERROR_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `esm_bank_details`
--

DROP TABLE IF EXISTS `esm_bank_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `esm_bank_details` (
  `EBD_CLAIM_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `EBD_BANK_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBD_BRANCH_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBD_IFSC_CODE` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBD_MICR_CODE` varchar(9) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBD_ACC_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBD_ACC_TYPE` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBD_ACC_NUMBER` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBD_UPDATE_DATE` datetime DEFAULT NULL,
  `EBD_IP_ADDRESS` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBD_USER_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`EBD_CLAIM_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `event_messages`
--

DROP TABLE IF EXISTS `event_messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event_messages` (
  `EM_EVENT_ID` int unsigned NOT NULL DEFAULT '0',
  `EM_FROM_DATE` datetime DEFAULT NULL,
  `EM_TO_DATE` datetime DEFAULT NULL,
  `EM_MESSAGE_TEXT` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `EM_USER_ID` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EM_IP_ADDRESS` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EM_STATUS` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`EM_EVENT_ID`),
  KEY `Index_2` (`EM_FROM_DATE`),
  KEY `Index_3` (`EM_TO_DATE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `exp_category`
--

DROP TABLE IF EXISTS `exp_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exp_category` (
  `EC_ID` int NOT NULL,
  `EC_DESC` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EC_ACTIVE` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`EC_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `expense_group`
--

DROP TABLE IF EXISTS `expense_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `expense_group` (
  `EG_GROUP_ID` int unsigned NOT NULL DEFAULT '0',
  `EG_GROUP_NAME` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EG_ADD_COL` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'N',
  PRIMARY KEY (`EG_GROUP_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `expense_header`
--

DROP TABLE IF EXISTS `expense_header`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `expense_header` (
  `EH_EXP_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `EH_EXP_SUBID` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'N',
  `EH_EXP_DESC` varchar(75) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EH_EXP_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'Y',
  `EH_DISP_ORDER` int unsigned NOT NULL,
  PRIMARY KEY (`EH_EXP_SUBID`,`EH_EXP_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `expense_type`
--

DROP TABLE IF EXISTS `expense_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `expense_type` (
  `ET_EXPTYPE_ID` int unsigned NOT NULL AUTO_INCREMENT,
  `ET_EXPTYPE_DESC` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ET_RATE_TYPE` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ET_RATE_CATG` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ET_ORDER` int unsigned NOT NULL DEFAULT '1',
  `ET_CATEGORY` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ET_NEW_ORDER` int NOT NULL,
  PRIMARY KEY (`ET_EXPTYPE_ID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ext_stay_process`
--

DROP TABLE IF EXISTS `ext_stay_process`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ext_stay_process` (
  `ESP_ID` int NOT NULL,
  `ESP_SET_ID` int NOT NULL,
  `ESP_GROUP_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ESP_ACTION` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ESP_STATUS_ID` int DEFAULT '0',
  `ESP_NEXT_GROUP_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ESP_IS_FINAL` int DEFAULT '0',
  `ESP_IS_ACCEPT` int DEFAULT '0',
  `ESP_ORDER_ID` int DEFAULT '0',
  `ESP_NMI` int DEFAULT '0',
  `ESP_REPLY_NMI` int DEFAULT '0',
  `ESP_DOC_REQ` int DEFAULT '0',
  `ESP_DOC_ID` int DEFAULT '0',
  PRIMARY KEY (`ESP_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ext_stay_summary`
--

DROP TABLE IF EXISTS `ext_stay_summary`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ext_stay_summary` (
  `ESU_ID` int NOT NULL,
  `ESU_APPX_HOSP` int DEFAULT '0',
  `ESU_APPX_OIC` int DEFAULT '0',
  `ESU_APPX_JDHS` int DEFAULT '0',
  `ESU_APPX_RCDIR` int DEFAULT '0',
  `ESU_APPX_MEDDIR` int DEFAULT '0',
  `ESU_APPX_DYMD` int DEFAULT '0',
  `ESU_APPX_MD` int DEFAULT '0',
  `ESU_ACTIVE` int DEFAULT '1',
  PRIMARY KEY (`ESU_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `extended_stay_setting`
--

DROP TABLE IF EXISTS `extended_stay_setting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `extended_stay_setting` (
  `ESS_ID` int NOT NULL DEFAULT '0',
  `ESS_FROM_DATE` date NOT NULL,
  `ESS_TO_DATE` date DEFAULT NULL,
  `ESS_FROM_DAYS` int NOT NULL,
  `ESS_TO_DAYS` int NOT NULL,
  `ESS_GROUP_LEVEL_1` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ESS_GROUP_LEVEL_2` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ESS_GROUP_LEVEL_3` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ESS_PERM_REQ` int DEFAULT '0',
  `ESS_APPX_CODE` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`ESS_FROM_DATE`,`ESS_FROM_DAYS`,`ESS_TO_DAYS`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `feedback_query`
--

DROP TABLE IF EXISTS `feedback_query`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedback_query` (
  `FQ_ID` int NOT NULL,
  `FQ_QUERY` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `FQ_ACTIVE` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`FQ_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `feedback_rating`
--

DROP TABLE IF EXISTS `feedback_rating`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedback_rating` (
  `FR_CLAIM_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `FR_QUERY_ID` int NOT NULL,
  `FR_RATING` int NOT NULL,
  PRIMARY KEY (`FR_CLAIM_ID`,`FR_QUERY_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `financial_year`
--

DROP TABLE IF EXISTS `financial_year`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `financial_year` (
  `FY_YEAR` int unsigned NOT NULL AUTO_INCREMENT,
  `FY_START_DATE` date NOT NULL,
  `FY_END_DATE` date NOT NULL,
  `FY_DESC` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`FY_YEAR`),
  KEY `Index_2` (`FY_START_DATE`),
  KEY `Index_3` (`FY_END_DATE`)
) ENGINE=InnoDB AUTO_INCREMENT=2026 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fund_details`
--

DROP TABLE IF EXISTS `fund_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fund_details` (
  `FD_TRAN_ID` int unsigned NOT NULL,
  `FD_TRAN_DATE` datetime DEFAULT NULL,
  `FD_TRAN_AMOUNT` decimal(15,2) DEFAULT NULL,
  `FD_TRAN_COUNT` int unsigned DEFAULT NULL,
  `FD_TRAN_TYPE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `FD_SETTLEMENT_ID` int unsigned DEFAULT NULL,
  `FD_REMARK` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `FD_LAST_UPDATED` datetime DEFAULT NULL,
  `FD_REJECTION_MARK` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'N',
  PRIMARY KEY (`FD_TRAN_ID`),
  KEY `Index_2` (`FD_TRAN_DATE`),
  KEY `Index_3` (`FD_TRAN_TYPE`),
  KEY `Index_4` (`FD_SETTLEMENT_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `gender_type`
--

DROP TABLE IF EXISTS `gender_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gender_type` (
  `gender_ID` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `gender_desc` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`gender_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `group_sanction_limit`
--

DROP TABLE IF EXISTS `group_sanction_limit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `group_sanction_limit` (
  `GSL_GROUP_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `GSL_LOWER_LIMIT` decimal(15,2) NOT NULL DEFAULT '0.00',
  `GSL_UPPER_LIMIT` decimal(15,2) NOT NULL DEFAULT '0.00'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `groupwise_status`
--

DROP TABLE IF EXISTS `groupwise_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `groupwise_status` (
  `GS_GROUP_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `GS_INT_STAGE` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `GS_INT_STATUS` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `GS_REMARK_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '0',
  `GS_REMARK_DESC` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `GS_REMARK_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `GS_INOUT_TYPE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'A',
  `GS_DE_LIST_TITLE` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `GS_DB_LIST_TITLE` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `GS_DB_PAGE_TITLE` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `GS_DE_PAGE_TITLE` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`GS_GROUP_ID`,`GS_INT_STAGE`,`GS_INT_STATUS`,`GS_REMARK_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `health_care_facility`
--

DROP TABLE IF EXISTS `health_care_facility`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `health_care_facility` (
  `HCF_ID` int unsigned NOT NULL AUTO_INCREMENT,
  `HCF_CATEGORY` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `HCF_DISP_ORDER` int NOT NULL DEFAULT '10',
  `HCF_PRIORITY` int unsigned NOT NULL DEFAULT '99',
  PRIMARY KEY (`HCF_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `his_audit_remarks`
--

DROP TABLE IF EXISTS `his_audit_remarks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `his_audit_remarks` (
  `AR_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `AR_REM_TYPE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `AR_HOS_REMARK` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `AR_PAR_REMARK` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `AR_SUP_REMARK` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `AR_APP_REMARK` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `AR_HISTORY_ID` int unsigned NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `his_bank_master`
--

DROP TABLE IF EXISTS `his_bank_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `his_bank_master` (
  `BM_BANK_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_BANK_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_BANK_BRANCH` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_BANK_ADD1` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_BANK_ADD2` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_BANK_ADD3` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_BANK_CITY` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_BANK_STATE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_BANK_PIN` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_BANK_ACTYPE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_BANK_ACNO` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_BANK_MICR` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_BANK_IFSC` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_OFFICE_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_ENTITY_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_BANK_STATUS` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_PAY_MODE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_PAYEE_NAME` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_HISTORY_ID` int unsigned NOT NULL,
  `BM_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `BM_UPDATE_DATE` datetime NOT NULL,
  `BM_IP_ADDRESS` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`BM_HISTORY_ID`),
  KEY `Index_2` (`BM_OFFICE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `his_claim_intimation`
--

DROP TABLE IF EXISTS `his_claim_intimation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `his_claim_intimation` (
  `CI_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `CI_PATIENT_TYPE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_ADMISSION_NO` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_ADMISSION_DATE` datetime DEFAULT NULL,
  `CI_CARD_ID` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_BENEFICIARY_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_CARD_TYPE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_CARD_VALID_DT` date DEFAULT NULL,
  `CI_OFFICE_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_OFFICE_DEPARTMENT` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_PATIENT_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_AGE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_SEX` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_RELATION_ID` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_PHONE_NO` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_MOBILE` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_EMAIL` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_ADDRESS1` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_ADDRESS2` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_ADDRESS3` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_CITY` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_STATE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_PIN` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_CGHS_REGION_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_HOSPITAL_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_ROOM_TYPE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_REF_TYPE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_ADM_AILMENT` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `CI_PRE_AILMENT_DUR` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_IS_RTA` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_RTA_REASON` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_RTA_DATE` date DEFAULT NULL,
  `CI_RTA_DOC_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_INT_STATUS` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_INT_STAGE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_CR_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_CR_DATE` datetime DEFAULT NULL,
  `CI_CR_OFFICE_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_CR_ENTITY_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_ROOM_NO` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_HOSPITAL_REMARK` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `CI_CARD_ROOM_TYPE` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_EXP_DOD` datetime DEFAULT NULL,
  `CI_UP_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_UP_DATE` datetime DEFAULT NULL,
  `CI_UP_OFFICE_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_UP_ENTITY_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_ENTITLEMENT_REMARK` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `CI_ENTITLEDIFF_REASON` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_SETTLEMENT_ID` decimal(10,0) DEFAULT NULL,
  `CI_INT_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_INT_DATE` datetime DEFAULT NULL,
  `CI_INT_OFFICE_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_INT_ENTITY_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_DEDUCT_ID` int DEFAULT '0',
  `CI_SERVICE_TYPE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_SERVICE_RANK` int unsigned DEFAULT NULL,
  `CI_EXTENDED_STAY` int unsigned DEFAULT NULL,
  `CI_SERVICE_NO` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_CFA_REVIEW` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CI_HISTORY_ID` int unsigned NOT NULL,
  PRIMARY KEY (`CI_INTIMATION_ID`,`CI_HISTORY_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `his_claim_remarks`
--

DROP TABLE IF EXISTS `his_claim_remarks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `his_claim_remarks` (
  `CR_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CR_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CR_USER_REMARKS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `CR_UPDATE_DATE` datetime NOT NULL,
  `CR_INT_STAGE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CR_REMARK_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CR_INT_STATUS` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CR_HISTORY_ID` int unsigned DEFAULT '0',
  `CR_ENHANCE_ID` int DEFAULT '0',
  `CR_IP_ADDRESS` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CR_AUTO_UPDATE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CR_CHANGE_ID` int unsigned DEFAULT NULL,
  `CR_REQUEST_ID` int unsigned NOT NULL DEFAULT '0',
  KEY `FK_claim_remarks_1` (`CR_INTIMATION_ID`) USING BTREE,
  KEY `Index_2` (`CR_UPDATE_DATE`),
  KEY `Index_3` (`CR_USER_ID`),
  KEY `idx_cr_int_stage` (`CR_INT_STAGE`),
  KEY `idx_cr_int_status` (`CR_INT_STATUS`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `his_claim_submission`
--

DROP TABLE IF EXISTS `his_claim_submission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `his_claim_submission` (
  `CS_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `CS_ADMISSION_DATE` datetime DEFAULT NULL,
  `CS_ADM_AILMENT` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `CS_PRE_AILMENT_DUR` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_AILMENT_HIST` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_FIRST_OCC_DATE` date DEFAULT NULL,
  `CS_DOD` datetime DEFAULT NULL,
  `CS_TREAT_DOCT` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_SUB_DATE` datetime DEFAULT NULL,
  `CS_SUB_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_SUB_OFFICE_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_SUB_ENTITY_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_ACCEPT_DATE` datetime DEFAULT NULL,
  `CS_GR_CLAIM_AMT` decimal(15,2) unsigned DEFAULT '0.00',
  `CS_PAT_AMT` decimal(15,2) unsigned DEFAULT '0.00',
  `CS_PAT_DISC_AMT` decimal(15,2) unsigned DEFAULT '0.00',
  `CS_NET_CLAIM_AMT` decimal(15,2) unsigned DEFAULT '0.00',
  `CS_UTI_PAR_AMT` decimal(15,2) unsigned DEFAULT '0.00',
  `CS_UTI_SUP_AMT` decimal(15,2) unsigned DEFAULT '0.00',
  `CS_UTI_APP_AMT` decimal(15,2) DEFAULT '0.00',
  `CS_ROOM_TYPE` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_ROOM_NO` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_PAR_IRREV_CHARGES` decimal(15,2) DEFAULT '0.00',
  `CS_PAR_EXCESS_AMT` decimal(15,2) DEFAULT '0.00',
  `CS_SUP_IRREV_CHARGES` decimal(15,2) DEFAULT '0.00',
  `CS_SUP_EXCESS_AMT` decimal(15,2) DEFAULT '0.00',
  `CS_APP_IRREV_CHARGES` decimal(15,2) DEFAULT '0.00',
  `CS_APP_EXCESS_AMT` decimal(15,2) DEFAULT '0.00',
  `CS_PAT_DIS_STATUS` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_REC_DATE` datetime DEFAULT NULL,
  `CS_REC_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_REC_OFFICE_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_REC_ENTITY_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_PAR_DATE` datetime DEFAULT NULL,
  `CS_PAR_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_PAR_OFFICE_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_PAR_ENTITY_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_SUP_DATE` datetime DEFAULT NULL,
  `CS_SUP_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_SUP_OFFICE_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_SUP_ENTITY_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_APP_DATE` datetime DEFAULT NULL,
  `CS_APP_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_APP_OFFICE_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_APP_ENTITY_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_BILL_NO` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_BILL_DATE` date DEFAULT NULL,
  `CS_PHY_REC_DATE` date DEFAULT NULL,
  `CS_PHY_REC_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_PHY_OFFICE_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_PHY_REC_ENTITY_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CS_HISTORY_ID` int unsigned NOT NULL,
  PRIMARY KEY (`CS_INTIMATION_ID`,`CS_HISTORY_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `his_clinical_findings_int`
--

DROP TABLE IF EXISTS `his_clinical_findings_int`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `his_clinical_findings_int` (
  `CF_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CF_CLTEST_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CT_IS_CLTEST` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CF_CLTEST_DETAILS` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CF_ENHANCE_ID` int unsigned DEFAULT '0',
  `CF_HISTORY_ID` int unsigned NOT NULL,
  KEY `Index_1` (`CF_INTIMATION_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `his_clinical_findings_sub`
--

DROP TABLE IF EXISTS `his_clinical_findings_sub`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `his_clinical_findings_sub` (
  `CF_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CF_CLTEST_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CT_IS_CLTEST` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CF_CLTEST_DETAILS` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CF_HISTORY_ID` int unsigned NOT NULL,
  KEY `Index_1` (`CF_INTIMATION_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `his_diag_details`
--

DROP TABLE IF EXISTS `his_diag_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `his_diag_details` (
  `DD_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DD_DIAG_SEQ_NO` int unsigned NOT NULL,
  `DD_DIAG_TYPE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DD_DIAG_DETAILS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `DD_DIAG_ICD_CODE` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DD_DIAG_PAR_DETAILS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `DD_DIAG_PAR_ICD_CODE` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DD_DIAG_PAR_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'Y',
  `DD_DIAG_SUP_DETAILS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `DD_DIAG_SUP_ICD_CODE` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DD_DIAG_SUP_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'Y',
  `DD_DIAG_APP_DETAILS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `DD_DIAG_APP_ICD_CODE` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DD_DIAG_APP_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'Y',
  `DD_ALREADY_SUBMITTED` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DD_ENHANCE_ID` int DEFAULT '0',
  `DD_HISTORY_ID` int unsigned NOT NULL,
  KEY `Index_1` (`DD_INTIMATION_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `his_document_submitted`
--

DROP TABLE IF EXISTS `his_document_submitted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `his_document_submitted` (
  `DS_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DS_DOCTYPE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DS_DOC_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DS_REMARK` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `DS_FILENAME` varchar(75) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DS_FILE_SR_NO` int DEFAULT NULL,
  `DS_IS_RECEIVED` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DS_REC_REMARK` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `DS_REC_REMARK_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DS_MUL_DOC` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DS_DOC_SUBMITTED` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DS_DOC_COUNT` int DEFAULT '1',
  `DS_DOC_SUBMIT_BY` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DS_ENHANCE_ID` int DEFAULT '0',
  `DS_SUBMIT_TIME` datetime DEFAULT NULL,
  `DS_FILE_SIZE` decimal(10,0) DEFAULT NULL,
  `DS_SIGNED` int unsigned DEFAULT '0',
  `DS_HISTORY_ID` int unsigned NOT NULL,
  KEY `Index_1` (`DS_INTIMATION_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `his_esm_bank_details`
--

DROP TABLE IF EXISTS `his_esm_bank_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `his_esm_bank_details` (
  `EBD_HISTORY_ID` int NOT NULL AUTO_INCREMENT,
  `EBD_CLAIM_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBD_BANK_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBD_BRANCH_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBD_IFSC_CODE` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBD_MICR_CODE` varchar(9) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBD_ACC_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBD_ACC_TYPE` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBD_ACC_NUMBER` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBD_UPDATE_DATE` datetime DEFAULT NULL,
  `EBD_IP_ADDRESS` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBD_USER_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBD_CHANGE_BY` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `EBD_CHANGE_DATE` datetime DEFAULT NULL,
  PRIMARY KEY (`EBD_HISTORY_ID`),
  KEY `Index_1` (`EBD_CLAIM_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=102627 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `his_hosp_exp`
--

DROP TABLE IF EXISTS `his_hosp_exp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `his_hosp_exp` (
  `HE_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `HE_EXP_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `HE_CLAIM_AMOUNT` decimal(15,2) unsigned DEFAULT '0.00',
  `HE_PAR_AMOUNT` decimal(15,2) unsigned DEFAULT '0.00',
  `HE_SUP_AMOUNT` decimal(15,2) unsigned DEFAULT '0.00',
  `HE_APP_AMOUNT` decimal(15,2) unsigned DEFAULT '0.00',
  `HE_HOS_REMARK` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `HE_PAR_REMARK` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `HE_SUP_REMARK` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `HE_APP_REMARK` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `HE_PAR_EXCESS_AMT` decimal(15,2) DEFAULT '0.00',
  `HE_PAR_IRREV_AMT` decimal(15,2) DEFAULT '0.00',
  `HE_SUP_EXCESS_AMT` decimal(15,2) DEFAULT '0.00',
  `HE_SUP_IRREV_AMT` decimal(15,2) DEFAULT '0.00',
  `HE_APP_EXCESS_AMT` decimal(15,2) DEFAULT '0.00',
  `HE_APP_IRREV_AMT` decimal(15,2) DEFAULT '0.00',
  `HE_HISTORY_ID` int unsigned NOT NULL,
  KEY `Index_1` (`HE_INTIMATION_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `his_hosp_exp_det`
--

DROP TABLE IF EXISTS `his_hosp_exp_det`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `his_hosp_exp_det` (
  `HED_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `HED_EXP_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `HED_CAT_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `HED_CAT_SUB_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `HED_REGION_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `HED_ACT_RATE` decimal(15,2) DEFAULT NULL,
  `HED_HOS_RATE` decimal(15,2) DEFAULT NULL,
  `HED_CLAIM_UNITS` decimal(15,2) DEFAULT NULL,
  `HED_CLAIM_AMOUNT` decimal(15,2) DEFAULT NULL,
  `HED_PAR_AMOUNT` decimal(15,2) DEFAULT NULL,
  `HED_SUP_AMOUNT` decimal(15,2) DEFAULT NULL,
  `HED_APP_AMOUNT` decimal(15,2) DEFAULT NULL,
  `HED_HISTORY_ID` int unsigned NOT NULL,
  KEY `Index_1` (`HED_INTIMATION_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `his_office_master`
--

DROP TABLE IF EXISTS `his_office_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `his_office_master` (
  `OM_OFFICE_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_OFFICE_NAME` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_OFFICE_ADD1` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_OFFICE_ADD2` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_OFFICE_ADD3` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_OFFICE_CITY` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_OFFICE_STATE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_OFFICE_PIN` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_OFFICE_PHONE` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_OFFICE_FAX` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_OFFICE_EMAIL` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_OFFICE_ALTER_EMAIL` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_OFFICE_CONTACT` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_OFFICE_CGHS_CITY_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_OFFICE_CON_DESG` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_OFFICE_PAN` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_OFFICE_STAX_NO` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_OFFICE_ENTITY_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_OFFICE_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_REG_DT` datetime NOT NULL,
  `OM_TAX_EXEMPT` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_CGHS_DIS_PERC` decimal(5,2) NOT NULL,
  `OM_NABH` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_HISTORY_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `OM_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_UPDATE_DATE` datetime NOT NULL,
  `OM_IP_ADDRESS` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`OM_HISTORY_ID`),
  KEY `FK_office_entity_Id` (`OM_OFFICE_ENTITY_ID`),
  KEY `FK_office_master_2` (`OM_OFFICE_STATE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `his_office_reg_valdate`
--

DROP TABLE IF EXISTS `his_office_reg_valdate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `his_office_reg_valdate` (
  `ORV_OFFICE_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ORV_VAL_FROM` date NOT NULL,
  `ORV_VAL_TO` date NOT NULL,
  `ORV_TRAN_NO` int NOT NULL,
  `ORV_CREATE_BY` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ORV_CREATE_DATE` datetime NOT NULL,
  `ORV_CREATE_IP` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ORV_UPDATED_BY` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ORV_UPDATE_DATE` datetime NOT NULL,
  `ORV_UPDATE_IP` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ORV_MOU_FILENAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ORV_VAL_TYPE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'M',
  `ORV_REMARK` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `his_opd_ph_answers`
--

DROP TABLE IF EXISTS `his_opd_ph_answers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `his_opd_ph_answers` (
  `opd_ans_id` int unsigned NOT NULL DEFAULT '0',
  `opd_ans_anyhistory` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'M',
  `opd_ans_details` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `opd_claim_id` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `opd_history_ID` int DEFAULT '0',
  KEY `Index_1` (`opd_claim_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `his_patient_register`
--

DROP TABLE IF EXISTS `his_patient_register`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `his_patient_register` (
  `PTR_HISTORY_ID` int NOT NULL AUTO_INCREMENT,
  `PTR_CARD_ID` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_TEMP_SLIP_NO` int DEFAULT '0',
  `PTR_BEN_ID` bigint NOT NULL DEFAULT '0',
  `PTR_BENEFICIARY_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_PATIENT_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_SERVICE_TYPE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_SERVICE_RANK` int DEFAULT '0',
  `PTR_SERVICE_NO` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_UID_NUMBER` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_UID_STATUS` int DEFAULT '0',
  `PTR_DOB` date DEFAULT NULL,
  `PTR_COMM_DATE` date DEFAULT NULL,
  `PTR_RETIRE_DATE` date DEFAULT NULL,
  `PTR_APP_TYPE_ID` int DEFAULT '0',
  `PTR_DIS_TYPE_ID` int DEFAULT '0',
  `PTR_SEX` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_RELATION_ID` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_PHONE_NO` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_MOBILE` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_EMAIL` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_ADDRESS1` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_ADDRESS2` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_ADDRESS3` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_CITY` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_STATE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_PIN` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_CARD_ROOM_TYPE` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_CR_USER` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_CR_DATE` datetime DEFAULT NULL,
  `PTR_IP_ADDRESS` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_UPDATE_BY` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_UPDATE_ON` datetime NOT NULL,
  `PTR_DOE` date DEFAULT NULL,
  PRIMARY KEY (`PTR_HISTORY_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=14939087 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `his_pre_exist_ailment`
--

DROP TABLE IF EXISTS `his_pre_exist_ailment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `his_pre_exist_ailment` (
  `PEA_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PEA_AILMENT_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PEA_IS_AILMENT` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PEA_AILMENT_DETAILS` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PEA_ENHANCE_ID` int unsigned DEFAULT '0',
  `PEA_HISTORY_ID` int unsigned NOT NULL,
  KEY `Index_1` (`PEA_INTIMATION_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `his_prop_treatment`
--

DROP TABLE IF EXISTS `his_prop_treatment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `his_prop_treatment` (
  `PT_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PT_TRTYPE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PR_IS_TREATMENT` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PR_TR_DETAILS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `PR_ENHANCE_ID` int unsigned DEFAULT '0',
  `PR_PRE_AUTH_ID` int unsigned NOT NULL,
  `PT_HISTORY_ID` int unsigned NOT NULL,
  KEY `Index_1` (`PT_INTIMATION_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `his_referal_details`
--

DROP TABLE IF EXISTS `his_referal_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `his_referal_details` (
  `REF_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `REF_NUMBER` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `REF_CGHS_REGION_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `REF_CGHS_DISP_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `REF_ISS_DATE` date DEFAULT NULL,
  `REF_ADV_BY` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `REF_APP_BY` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `REF_HOSPITAL_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `REF_ROOM_TYPE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `REF_VAL_DATE` date DEFAULT NULL,
  `REF_SESSIONS` int DEFAULT NULL,
  `REF_PROCEDURES` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `REF_ENTRY_BY` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `REF_BAL_SESSION` int unsigned DEFAULT NULL,
  `REF_ADM_PROCEDURES` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `REF_INV_PROCEDURES` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `REF_CON_PROCEDURES` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `REF_TRAVEL_REIMBURSE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `REF_ATTENDANT_REIMBURSE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `REF_PATIENT_TYPE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `REF_HISTORY_ID` int unsigned NOT NULL,
  KEY `Index_1` (`REF_INTIMATION_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `his_treatment_details`
--

DROP TABLE IF EXISTS `his_treatment_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `his_treatment_details` (
  `TD_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `TD_TRTYPE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `TD_IS_TREATMENT` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `TD_TR_DETAILS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `TD_HISTORY_ID` int unsigned NOT NULL,
  KEY `Index_1` (`TD_INTIMATION_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `his_web_referral`
--

DROP TABLE IF EXISTS `his_web_referral`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `his_web_referral` (
  `WR_TRAN_NO` int NOT NULL,
  `WR_REL_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `WR_REL_DATE` datetime NOT NULL,
  `WR_REFERENCE_NO` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `WR_CLAIM_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `WR_HOSPITAL_ID` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `WR_POLYCLINIC_ID` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `WR_DATE` datetime NOT NULL,
  `WR_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `WR_IP_ADDRESS` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`WR_TRAN_NO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `hos_types`
--

DROP TABLE IF EXISTS `hos_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hos_types` (
  `hos_type_id` int unsigned NOT NULL AUTO_INCREMENT,
  `hos_type_description` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `hos_type_code` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`hos_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `hosp_audit`
--

DROP TABLE IF EXISTS `hosp_audit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hosp_audit` (
  `HA_CLAIM_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `HA_STAGE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `HA_STATUS` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `HA_DATE` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `hosp_exp`
--

DROP TABLE IF EXISTS `hosp_exp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hosp_exp` (
  `HE_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `HE_EXP_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `HE_CLAIM_AMOUNT` decimal(15,2) unsigned DEFAULT '0.00',
  `HE_PAR_AMOUNT` decimal(15,2) unsigned DEFAULT '0.00',
  `HE_SUP_AMOUNT` decimal(15,2) unsigned DEFAULT '0.00',
  `HE_APP_AMOUNT` decimal(15,2) unsigned DEFAULT '0.00',
  `HE_HOS_REMARK` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `HE_PAR_REMARK` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `HE_SUP_REMARK` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `HE_APP_REMARK` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `HE_PAR_EXCESS_AMT` decimal(15,2) DEFAULT '0.00',
  `HE_PAR_IRREV_AMT` decimal(15,2) DEFAULT '0.00',
  `HE_SUP_EXCESS_AMT` decimal(15,2) DEFAULT '0.00',
  `HE_SUP_IRREV_AMT` decimal(15,2) DEFAULT '0.00',
  `HE_APP_EXCESS_AMT` decimal(15,2) DEFAULT '0.00',
  `HE_APP_IRREV_AMT` decimal(15,2) DEFAULT '0.00',
  PRIMARY KEY (`HE_INTIMATION_ID`,`HE_EXP_ID`),
  KEY `FK_hosp_exp_1` (`HE_EXP_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `hosp_exp_det`
--

DROP TABLE IF EXISTS `hosp_exp_det`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hosp_exp_det` (
  `HED_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `HED_EXP_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `HED_CAT_ID` varchar(10) DEFAULT NULL,
  `HED_CAT_SUB_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `HED_REGION_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `HED_ACT_RATE` decimal(15,2) DEFAULT '0.00',
  `HED_HOS_RATE` decimal(15,2) DEFAULT '0.00',
  `HED_CLAIM_UNITS` decimal(15,2) DEFAULT '0.00',
  `HED_CLAIM_AMOUNT` decimal(15,2) DEFAULT '0.00',
  `HED_PAR_AMOUNT` decimal(15,2) DEFAULT '0.00',
  `HED_SUP_AMOUNT` decimal(15,2) DEFAULT '0.00',
  `HED_APP_AMOUNT` decimal(15,2) DEFAULT '0.00',
  `HED_PAR_DEDUCT` decimal(15,2) DEFAULT '0.00',
  `HED_SUPER_RATE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `HED_RATE_TYPE` varchar(1) NOT NULL DEFAULT 'L',
  `HED_PROC_DESC` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `HED_PROC_TYPE` varchar(1) NOT NULL DEFAULT 'N',
  `HED_CAT_DESC` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `HED_PAR_REMARKS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `HED_SUPER_REMARKS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `HED_HOS_REMARKS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `HED_ID` decimal(10,0) NOT NULL DEFAULT '0',
  `HED_ID_SRNO` int NOT NULL DEFAULT '0',
  `HED_PROC_ID` int NOT NULL DEFAULT '0',
  `HED_SUP_DEDUCT` decimal(15,2) NOT NULL DEFAULT '0.00',
  `HED_APP_DEDUCT` decimal(15,2) DEFAULT '0.00',
  `HED_APP_REMARKS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `HED_NORMAL_RATE` decimal(15,2) NOT NULL DEFAULT '0.00',
  `HED_SPEC_RATE` decimal(15,2) NOT NULL DEFAULT '0.00',
  `HED_DED_ID` int DEFAULT '0',
  PRIMARY KEY (`HED_ID`,`HED_ID_SRNO`),
  KEY `Index_2` (`HED_INTIMATION_ID`),
  KEY `Idx_EXP_ID` (`HED_EXP_ID`),
  KEY `Idx_PROC_ID` (`HED_PROC_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `hosp_exp_head`
--

DROP TABLE IF EXISTS `hosp_exp_head`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hosp_exp_head` (
  `HEH_EXP_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `HEH_EXP_DESC` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `HEH_EXP_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `HEH_DISP_ORDER` int NOT NULL,
  `HEH_FOR_IP` int DEFAULT '1',
  `HEH_FOR_OPD` int DEFAULT '1',
  `HEH_DISP_MEMBER` int DEFAULT '1',
  PRIMARY KEY (`HEH_EXP_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `hosp_revenue_dtls`
--

DROP TABLE IF EXISTS `hosp_revenue_dtls`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hosp_revenue_dtls` (
  `hrd_office_id` varchar(6) NOT NULL,
  `hrd_rev_fy` int NOT NULL,
  `hrd_rev_amt` decimal(15,2) DEFAULT '0.00',
  `hrd_mrk_dt` date DEFAULT NULL,
  `hrd_lstupdt_dt` datetime DEFAULT NULL,
  `hrd_lstupdt_usr` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`hrd_office_id`,`hrd_rev_fy`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `hosp_stats`
--

DROP TABLE IF EXISTS `hosp_stats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hosp_stats` (
  `HS_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `HS_PROC_DATE` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `icd_master`
--

DROP TABLE IF EXISTS `icd_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `icd_master` (
  `ICD_CODE` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `ICD_DESC` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `ICD_INTERNAL_CODE` int unsigned NOT NULL,
  `ICD_LEVEL` int unsigned NOT NULL,
  `ICD_PARENT` int unsigned NOT NULL,
  `ICD_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`ICD_CODE`),
  KEY `Index_2` (`ICD_LEVEL`),
  KEY `Index_3` (`ICD_PARENT`),
  KEY `Index_4` (`ICD_INTERNAL_CODE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ifa_allot`
--

DROP TABLE IF EXISTS `ifa_allot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ifa_allot` (
  `IA_CLAIM_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `IA_ALLOT_ID` int DEFAULT NULL,
  `IA_STAGE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `IA_STATUS` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `IA_ACCEPT_DATE` datetime NOT NULL,
  `IA_CLAIM_AMT` double(10,2) NOT NULL,
  `IA_SANCTION_AMT` double(10,2) NOT NULL,
  `IA_AMOUNT` double(10,2) NOT NULL,
  PRIMARY KEY (`IA_CLAIM_ID`),
  KEY `Idx_Allot_Id` (`IA_ALLOT_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ifa_allot_summary`
--

DROP TABLE IF EXISTS `ifa_allot_summary`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ifa_allot_summary` (
  `IAS_ID` int NOT NULL AUTO_INCREMENT,
  `IAS_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `IAS_DATE` datetime NOT NULL,
  `IAS_PAT_TYPE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `IAS_STATUS` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `IAS_CLAIM_TYPE` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `IAS_ALLOTED` int DEFAULT '0',
  `IAS_PERC` int NOT NULL DEFAULT '0',
  `IAS_PROC` int DEFAULT '0',
  `IAS_ESCLATE` int DEFAULT '0',
  `IAS_FWD_CFA` int DEFAULT '0',
  PRIMARY KEY (`IAS_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=1567 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ifa_events`
--

DROP TABLE IF EXISTS `ifa_events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ifa_events` (
  `IE_EVENT_ID` int NOT NULL AUTO_INCREMENT,
  `IE_CLAIM_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `IE_PROC_ID` int NOT NULL,
  `IE_ESCLATE` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '0',
  `IE_DATE` datetime NOT NULL,
  `IE_GROUP_ID` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `IE_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `IE_REMARKS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `IE_AMOUNT` int NOT NULL DEFAULT '0',
  `IE_IP_ADDRESS` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `IE_REVERT` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`IE_EVENT_ID`),
  KEY `Idx_Claim_Id` (`IE_CLAIM_ID`),
  KEY `Idx_User_Id` (`IE_USER_ID`) /*!80000 INVISIBLE */,
  KEY `Idx_Proc_Id` (`IE_PROC_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=1087263 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ifa_period`
--

DROP TABLE IF EXISTS `ifa_period`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ifa_period` (
  `IP_ID` int NOT NULL AUTO_INCREMENT,
  `IP_FROM_DATE` date NOT NULL,
  `IP_TO_DATE` date DEFAULT NULL,
  `IP_ACTIVE` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`IP_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ifa_process`
--

DROP TABLE IF EXISTS `ifa_process`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ifa_process` (
  `IP_CLAIM_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `IP_ALLOT_ID` int NOT NULL DEFAULT '0',
  `IP_PROC_ID` int NOT NULL,
  `IP_DATE` datetime NOT NULL,
  `IP_GROUP_ID` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `IP_NMI_BY` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `IP_EVENT_ID` int DEFAULT NULL,
  `IP_CFA_CHECK` int DEFAULT '0',
  `IP_AMOUNT` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`IP_CLAIM_ID`),
  KEY `idx_allot` (`IP_ALLOT_ID`),
  KEY `idx_proc_id` (`IP_PROC_ID`),
  KEY `idx_cfa_check` (`IP_CFA_CHECK`),
  KEY `idx_nmi_by` (`IP_NMI_BY`),
  KEY `idx_group_id` (`IP_GROUP_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ifa_setting`
--

DROP TABLE IF EXISTS `ifa_setting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ifa_setting` (
  `IFS_ID` int NOT NULL AUTO_INCREMENT,
  `IFS_PERIOD_ID` int NOT NULL,
  `IFS_GROUP_ID` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `IFS_STATUS_ID` int NOT NULL DEFAULT '0',
  `IFS_NEXT_GROUP_ID` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `IFS_ESCLATE_NUM` int DEFAULT '0',
  `IFS_ESCLATE_MODE` int DEFAULT '0',
  `IFS_IS_FINAL` int DEFAULT '0',
  `IFS_ACCEPT` int DEFAULT '0',
  `IFS_ORDER_ID` int DEFAULT '0',
  `IFS_START` int DEFAULT '0',
  `IFS_NMI` int DEFAULT '0',
  `IFS_REPLY` int DEFAULT '0',
  `IFS_MODE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`IFS_ID`),
  KEY `Idx_Reply` (`IFS_REPLY`),
  KEY `Idx_NMI` (`IFS_NMI`),
  KEY `Idx_Next_Group` (`IFS_NEXT_GROUP_ID`),
  KEY `Idx_Start` (`IFS_START`),
  KEY `Idx_Group_Id` (`IFS_GROUP_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ifa_status`
--

DROP TABLE IF EXISTS `ifa_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ifa_status` (
  `IS_ID` int NOT NULL,
  `IS_DESC` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `IS_DISPLAY` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`IS_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ifa_timing`
--

DROP TABLE IF EXISTS `ifa_timing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ifa_timing` (
  `IT_ID` int NOT NULL AUTO_INCREMENT,
  `IP_ESC_DATE` date DEFAULT NULL,
  `IP_MODE` varchar(1) DEFAULT 'R',
  `IT_START_TIME` datetime NOT NULL,
  `IT_END_TIME` datetime DEFAULT NULL,
  `IT_COUNT` int DEFAULT '0',
  `IT_EXCEP` text,
  PRIMARY KEY (`IT_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `inv_proc_cert`
--

DROP TABLE IF EXISTS `inv_proc_cert`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inv_proc_cert` (
  `IPC_OFFICE_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `IPC_VALID_ID` int NOT NULL,
  `IPC_PROC_ID` int NOT NULL,
  `IPC_HOSP_USER` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `IPC_ENTRY_DATE` datetime DEFAULT NULL,
  `IPC_CONFIRM` int DEFAULT '0',
  `IPC_RC_USER` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `IPC_CONFIRM_DATE` datetime DEFAULT NULL,
  PRIMARY KEY (`IPC_OFFICE_ID`,`IPC_VALID_ID`,`IPC_PROC_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `inv_proc_detail`
--

DROP TABLE IF EXISTS `inv_proc_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inv_proc_detail` (
  `IPD_HEADER_ID` int unsigned NOT NULL,
  `IPD_ID` int unsigned NOT NULL AUTO_INCREMENT,
  `IPD_RATE_FOR` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'E',
  `IPD_SRNO` varchar(10) NOT NULL DEFAULT '0',
  `IPD_DESC` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `IPD_CODE` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `IPD_SUFIX` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'A',
  `IPD_TYPE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'L',
  `IPD_MODE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'L',
  `IPD_GENDER` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `IPD_PACK_APP` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'N',
  PRIMARY KEY (`IPD_ID`),
  UNIQUE KEY `IPD_CODE_UNIQUE` (`IPD_CODE`),
  KEY `Idx_IPD_Srno` (`IPD_SRNO`)
) ENGINE=InnoDB AUTO_INCREMENT=12051 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `inv_proc_header`
--

DROP TABLE IF EXISTS `inv_proc_header`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inv_proc_header` (
  `IPH_ID` int unsigned NOT NULL AUTO_INCREMENT,
  `IPH_HEADER` varchar(400) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `IPH_START` int unsigned DEFAULT '0',
  `IPH_END` int unsigned DEFAULT '0',
  `IPH_HEAD_TYPE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'P',
  `IPH_GROUP` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `IPH_PRIORITY` int unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`IPH_ID`),
  KEY `Idx_Proc_Header` (`IPH_HEAD_TYPE`)
) ENGINE=InnoDB AUTO_INCREMENT=258 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `inv_proc_rate_list`
--

DROP TABLE IF EXISTS `inv_proc_rate_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inv_proc_rate_list` (
  `IPRL_REGION_ID` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `IPRL_ID` int unsigned NOT NULL,
  `IPRL_NABH_RATE` decimal(10,2) DEFAULT '0.00',
  `IPRL_NON_NABH_RATE` decimal(10,2) DEFAULT '0.00',
  `IPRL_SUPER_SPEC_RATE` decimal(10,2) DEFAULT '0.00',
  `IPRL_NC` decimal(10,2) DEFAULT '0.00',
  `IPRL_C` decimal(10,2) DEFAULT '0.00',
  `IPRL_B` decimal(10,2) DEFAULT '0.00',
  `IPRL_A` decimal(10,2) DEFAULT '0.00',
  `IPRL_D` decimal(10,2) DEFAULT '0.00',
  `IPRL_FN` decimal(10,2) DEFAULT '0.00',
  `IPRLREFER` int unsigned DEFAULT '0',
  `IPRL_FROM_DATE` date NOT NULL,
  `IPRL_TO_DATE` date DEFAULT NULL,
  `IPRL_MAIN` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`IPRL_MAIN`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `last_tran_details`
--

DROP TABLE IF EXISTS `last_tran_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `last_tran_details` (
  `LTD_TRAN_TYPE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `LTD_LAST_NO` int unsigned NOT NULL,
  `LTD_TRAN_DESC` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `LTD_TRAN_TYPE_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`LTD_TRAN_TYPE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `leave_master`
--

DROP TABLE IF EXISTS `leave_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `leave_master` (
  `LM_ID` int NOT NULL AUTO_INCREMENT,
  `LM_NAME` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `LM_AT_WORK` int NOT NULL DEFAULT '1',
  `LM_ACTIVE` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`LM_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `login_type`
--

DROP TABLE IF EXISTS `login_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `login_type` (
  `LT_ID` int NOT NULL,
  `LT_TYPE` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`LT_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `manual_recovery`
--

DROP TABLE IF EXISTS `manual_recovery`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `manual_recovery` (
  `MR_ID` int NOT NULL,
  `MR_HOSPITAL_ID` int NOT NULL,
  `MR_INIT_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MR_DATE` date NOT NULL,
  `MR_REASON` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `MR_AMOUNT` double DEFAULT '0',
  `MR_RECOVERED` double DEFAULT '0',
  `MR_STATUS` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MR_STATUS_DATE` datetime DEFAULT NULL,
  `MR_APPR_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MR_CFA_REMARKS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  PRIMARY KEY (`MR_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `manual_recovery_details`
--

DROP TABLE IF EXISTS `manual_recovery_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `manual_recovery_details` (
  `MRD_ID` int NOT NULL,
  `MRD_RECOV_FROM` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `MRD_SETTLEMENT_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MRD_RECOVER_AMT` decimal(14,2) DEFAULT '0.00',
  PRIMARY KEY (`MRD_ID`,`MRD_RECOV_FROM`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `manual_settlement`
--

DROP TABLE IF EXISTS `manual_settlement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `manual_settlement` (
  `MS_CLAIM_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `MS_DATE` date NOT NULL,
  `MS_HOSPITAL_ID` int NOT NULL,
  `MS_HOSPITAL_NAME` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MS_HOSP_ADD1` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MS_HOSP_ADD2` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MS_HOSP_ADD3` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MS_HOSP_CITY` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MS_HOSP_STATE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MS_HOSP_STATE` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MS_HOSP_PIN` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MS_HOSP_PAN` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MS_REGION_ID` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MS_BANK_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MS_BANK_BRANCH` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MS_IFSC_CODE` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MS_MICR_CODE` varchar(9) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MS_ACC_NUMBER` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MS_CLAIM_AMT` double NOT NULL,
  `MS_APPROVED_AMT` double NOT NULL,
  `MS_ENTRY_USERID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MS_APPROVAL_STATUS` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MS_APPROVAL_REMARKS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `MS_APPROVAL_TIME` datetime DEFAULT NULL,
  `MS_APP_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MS_SETTLMENT_ID` decimal(10,0) DEFAULT NULL,
  `MS_SETTLE_DATE` datetime DEFAULT NULL,
  `MS_FINAL_SETTLE_DT` datetime DEFAULT NULL,
  PRIMARY KEY (`MS_CLAIM_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `member_claim_waiver`
--

DROP TABLE IF EXISTS `member_claim_waiver`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `member_claim_waiver` (
  `MCW_CLAIM_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `MCW_APPLY_ID` int DEFAULT '0',
  `MCW_APPLY_DATE` datetime NOT NULL,
  `MCW_ADMISSION_DATE` datetime DEFAULT NULL,
  `MCW_EIR_DATE` datetime DEFAULT NULL,
  `MCW_DOD` date DEFAULT NULL,
  `MCW_WO_REFERRAL` int DEFAULT '0',
  `MCW_32KB` int NOT NULL DEFAULT '0',
  `MCW_DOC_SUBMIT_DATE` date DEFAULT NULL,
  `MCW_DELAY_ID` int DEFAULT '0',
  `MCW_DELAY_REASON` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `MCW_WAIVER_ID` int NOT NULL DEFAULT '0',
  `MCW_CUR_PROC` int DEFAULT '0',
  `MCW_PROC_COMMENT` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `MCW_REQUERY_ID` int DEFAULT '0',
  `MCW_GROUP_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MCW_REQUERY_BY` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MCW_REJ_COUNT` int DEFAULT '0',
  `MCW_REJ_BY` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MCW_PROCESS_USER` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MCW_PROCESS_DATE` datetime DEFAULT NULL,
  `MCW_IP_ADDRESS` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MCW_BENF_ID` int DEFAULT '0',
  `MCW_DEP_ID` int DEFAULT '0',
  `MCW_EVENT_ID` int DEFAULT NULL,
  PRIMARY KEY (`MCW_CLAIM_ID`,`MCW_WAIVER_ID`),
  UNIQUE KEY `unique_id` (`MCW_APPLY_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `member_feedback`
--

DROP TABLE IF EXISTS `member_feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `member_feedback` (
  `MF_CLAIM_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `MF_REF_NUMBER` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MF_GEN_DATE` datetime NOT NULL,
  `MF_REPLY_DATE` datetime DEFAULT NULL,
  `MF_IP_ADDRESS` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MF_MIN_RATE` int DEFAULT '0',
  `MF_MAX_RATE` int DEFAULT '0',
  PRIMARY KEY (`MF_CLAIM_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `member_permit_process`
--

DROP TABLE IF EXISTS `member_permit_process`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `member_permit_process` (
  `MPP_ID` int NOT NULL,
  `MPP_MAJOR` int DEFAULT '0',
  `MPP_GROUP_ID` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MPP_STATUS_ID` int DEFAULT NULL,
  `MPP_NEXT_GROUP_ID` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MPP_IS_START` int DEFAULT '0',
  `MPP_IS_NMI` int DEFAULT '0',
  `MPP_IS_REPLY` int DEFAULT '0',
  `MPP_IS_ACCEPT` int DEFAULT '0',
  `MPP_IS_FINAL` int DEFAULT '0',
  PRIMARY KEY (`MPP_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `member_permit_status`
--

DROP TABLE IF EXISTS `member_permit_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `member_permit_status` (
  `MPS_ID` int NOT NULL,
  `MPS_DESC` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`MPS_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `member_request`
--

DROP TABLE IF EXISTS `member_request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `member_request` (
  `MR_ID` int NOT NULL,
  `MR_REQUERY_ID` int DEFAULT '0',
  `MR_BENF_ID` int NOT NULL,
  `MR_PARENT_OIC` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MR_CLAIM_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MR_REQ_DATE` datetime DEFAULT NULL,
  `MR_HOSP_NAME` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MR_INIT_BY` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MR_PAT_TYPE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MR_ADMIT_DATE` date DEFAULT NULL,
  `MR_CATG_ID` int DEFAULT NULL,
  `MR_TREATMENT` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `MR_VISIT_REASON` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `MR_PROC_REM` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `MR_COMMENTS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `MR_PROC_DATE` datetime DEFAULT NULL,
  `MR_GROUP_ID` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MR_PERMIT_ID` int DEFAULT NULL,
  `MR_NMI_BY` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MR_DRAFT_SAVE` int NOT NULL DEFAULT '1',
  `MR_ACTIVE` int DEFAULT '1',
  PRIMARY KEY (`MR_ID`),
  UNIQUE KEY `MR_CLAIM_ID_UNIQUE` (`MR_CLAIM_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `member_request_events`
--

DROP TABLE IF EXISTS `member_request_events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `member_request_events` (
  `MRE_APPLY_ID` int NOT NULL DEFAULT '0',
  `MRE_REQUERY_ID` int NOT NULL DEFAULT '0',
  `MRE_GROUP_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `MRE_DATE` datetime DEFAULT NULL,
  `MRE_REASON` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `MRE_COMMENTS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `MRE_PERMIT_ID` int DEFAULT '0',
  `MRE_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`MRE_APPLY_ID`,`MRE_REQUERY_ID`,`MRE_GROUP_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `member_waiver_events`
--

DROP TABLE IF EXISTS `member_waiver_events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `member_waiver_events` (
  `MWE_CLAIM_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MWE_APPLY_ID` int NOT NULL DEFAULT '0',
  `MWE_GROUP_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MWE_DATE` datetime DEFAULT NULL,
  `MWE_REASON` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `MWE_COMMENTS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `MWE_WAIVER_ID` int NOT NULL DEFAULT '0',
  `MWE_STATUS` int DEFAULT '0',
  `MWE_USER_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MWE_EVENT_ID` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`MWE_APPLY_ID`,`MWE_EVENT_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `menu_header`
--

DROP TABLE IF EXISTS `menu_header`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `menu_header` (
  `mh_group_id` int unsigned NOT NULL DEFAULT '0',
  `mh_header` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`mh_group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mm_menu_master`
--

DROP TABLE IF EXISTS `mm_menu_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mm_menu_master` (
  `MM_LEVEL_1` int NOT NULL DEFAULT '0',
  `MM_LEVEL_2` int NOT NULL DEFAULT '0',
  `MM_LEVEL_3` int NOT NULL DEFAULT '0',
  `MM_LEVEL_4` int NOT NULL DEFAULT '0',
  `MM_MENU_ITEM` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MM_MENU_LINK` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MM_ALWAYS_DISPLAY` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MM_ITEM_DESCRIPTION` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MM_HEAD_ID` int unsigned DEFAULT '0',
  `MM_ORDER_ID` int DEFAULT '1',
  `MM_MENU_ACTION` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MM_DAYS_LIMIT` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`MM_LEVEL_1`,`MM_LEVEL_2`,`MM_LEVEL_3`,`MM_LEVEL_4`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `neft_details`
--

DROP TABLE IF EXISTS `neft_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `neft_details` (
  `nd_settlement_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `nd_region_id` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `nd_micr_no` varchar(9) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `nd_neft_ref_no` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `nd_neft_amount` decimal(15,2) DEFAULT NULL,
  `nd_neft_date` datetime NOT NULL,
  `nd_remarks` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `nd_ip_address` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `nd_user_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `nd_tran_date` datetime NOT NULL,
  `nd_chq_date` datetime NOT NULL,
  `nd_settled_claims` int NOT NULL,
  `nd_settlement_amount` decimal(15,2) DEFAULT NULL,
  `nd_settlement_UTIFees` decimal(15,2) DEFAULT NULL,
  `nd_settlement_date` datetime NOT NULL,
  PRIMARY KEY (`nd_settlement_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `new_patient_register`
--

DROP TABLE IF EXISTS `new_patient_register`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `new_patient_register` (
  `PTR_CARD_NUMBER` int NOT NULL DEFAULT '0',
  `PTR_CARD_ID` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `PTR_BEN_ID` bigint NOT NULL DEFAULT '0',
  `PTR_BENEFICIARY_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_PATIENT_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_SERVICE_TYPE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_SERVICE_RANK` int DEFAULT '0',
  `PTR_SERVICE_NO` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_UID_NUMBER` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_UID_STATUS` int DEFAULT '0',
  `PTR_DOB` date DEFAULT NULL,
  `PTR_SEX` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_RELATION_ID` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_PHONE_NO` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_MOBILE` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_EMAIL` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_ADDRESS1` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_ADDRESS2` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_ADDRESS3` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_CITY` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_STATE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_PIN` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_CARD_ROOM_TYPE` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_CR_USER` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_CR_DATE` datetime NOT NULL,
  `PTR_IP_ADDRESS` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_MAIN_CLINIC_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`PTR_CARD_ID`),
  UNIQUE KEY `uq_benf_id` (`PTR_BEN_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `nmi_summary`
--

DROP TABLE IF EXISTS `nmi_summary`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nmi_summary` (
  `NS_OFFICE_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `NS_STAGE` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `1_COUNT` int NOT NULL,
  `1_AMT` double NOT NULL,
  `2_COUNT` int NOT NULL,
  `2_AMT` double NOT NULL,
  `3_COUNT` int NOT NULL,
  `3_AMT` double NOT NULL,
  `4_COUNT` int NOT NULL,
  `4_AMT` double NOT NULL,
  `5_COUNT` int NOT NULL,
  `5_AMT` double NOT NULL,
  `6_COUNT` int NOT NULL,
  `6_AMT` double NOT NULL,
  PRIMARY KEY (`NS_OFFICE_ID`,`NS_STAGE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `notice_list`
--

DROP TABLE IF EXISTS `notice_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notice_list` (
  `NL_NOT_TYPE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `NL_NOT_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `NL_NOT_SHORT_DESC` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `NL_NOT_FILE_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `NL_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'Y',
  `NL_NOT_DESC` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  PRIMARY KEY (`NL_NOT_ID`) USING BTREE,
  KEY `FK_notice_list_1` (`NL_NOT_TYPE_ID`),
  CONSTRAINT `FK_notice_list_1` FOREIGN KEY (`NL_NOT_TYPE_ID`) REFERENCES `notice_type` (`NT_NOT_TYPE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `notice_type`
--

DROP TABLE IF EXISTS `notice_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notice_type` (
  `NT_NOT_TYPE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `NT_NOT_TYPE_DESC` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `NT_NOT_TYPE_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'Y',
  PRIMARY KEY (`NT_NOT_TYPE_ID`),
  KEY `Idx_Not_Active` (`NT_NOT_TYPE_ACTIVE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `offc_bed_typ_mstr`
--

DROP TABLE IF EXISTS `offc_bed_typ_mstr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `offc_bed_typ_mstr` (
  `obtm_typ_id` int NOT NULL AUTO_INCREMENT,
  `obtm_typ_descp` varchar(100) DEFAULT NULL,
  `obtm_typ_status` int DEFAULT NULL,
  `obtm_typ_crt_dt` date DEFAULT NULL,
  `obtm_lstupdt_usr` varchar(30) DEFAULT NULL,
  `obtm_lstupdt_dt` datetime DEFAULT NULL,
  `obtm_order` int NOT NULL DEFAULT '99',
  PRIMARY KEY (`obtm_typ_id`),
  UNIQUE KEY `obtm_inx001` (`obtm_typ_descp`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `offc_bsc_info`
--

DROP TABLE IF EXISTS `offc_bsc_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `offc_bsc_info` (
  `OBI_ID` int NOT NULL AUTO_INCREMENT,
  `obi_OFFC_ID` varchar(6) NOT NULL,
  `obi_bsc_inf_typ` int NOT NULL,
  `obi_CNT` int DEFAULT NULL,
  `obi_actv_frm_dt` date NOT NULL,
  `obi_actv_to_dt` date DEFAULT NULL,
  `obi_lstupdt_usr` varchar(30) DEFAULT NULL,
  `obi_lstupdt_dt` datetime DEFAULT NULL,
  PRIMARY KEY (`OBI_ID`),
  UNIQUE KEY `unq_index` (`obi_OFFC_ID`,`obi_bsc_inf_typ`,`obi_actv_frm_dt`,`obi_actv_to_dt`)
) ENGINE=InnoDB AUTO_INCREMENT=126 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `office_emp_purpose`
--

DROP TABLE IF EXISTS `office_emp_purpose`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `office_emp_purpose` (
  `OEP_OFFICE_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `OEP_ID` int unsigned NOT NULL,
  `OEP_PURPOSE` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  PRIMARY KEY (`OEP_OFFICE_ID`,`OEP_ID`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `office_holiday`
--

DROP TABLE IF EXISTS `office_holiday`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `office_holiday` (
  `OH_ID` int NOT NULL,
  `OH_OFFICE_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`OH_ID`,`OH_OFFICE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `office_master`
--

DROP TABLE IF EXISTS `office_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `office_master` (
  `OM_OFFICE_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `OM_OFFICE_NAME` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_OFFICE_ADD1` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_OFFICE_ADD2` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_OFFICE_ADD3` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_OFFICE_CITY` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_OFFICE_STATE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_OFFICE_PIN` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_OFFICE_PHONE` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_OFFICE_FAX` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_OFFICE_EMAIL` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_OFFICE_ALTER_EMAIL` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_OFFICE_CONTACT` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_OFFICE_CGHS_CITY_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_RATE_REGION` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_OFFICE_CON_DESG` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_OFFICE_PAN` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_OFFICE_STAX_NO` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_OFFICE_ENTITY_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_OFFICE_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_REG_DT` datetime NOT NULL,
  `OM_TAX_EXEMPT` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_CGHS_DIS_PERC` decimal(5,2) NOT NULL,
  `OM_OFFICE_TAN_NO` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_OFFICE_STD` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_NABH` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_NABL` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_SUPER` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_HOSP_TYPE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_OFFICE_PAOCD` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_OFFICE_DDOCD` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_OFFICE_PAOREG` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_OFFICE_DDOREG` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_ACTUAL_REG_DT` datetime DEFAULT NULL,
  `OM_HOSP_TYPES` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_CREATED_BY` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_IP_ADDRESS` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_CATG_ID` int unsigned DEFAULT '0',
  `OM_CONTACT_LEVEL_1` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_PHONE_LEVEL_1` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_EMAIL_LEVEL_1` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_CONTACT_LEVEL_2` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_PHONE_LEVEL_2` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_EMAIL_LEVEL_2` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_CONTACT_LEVEL_3` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_PHONE_LEVEL_3` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_EMAIL_LEVEL_3` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_SOURCE_POLY_ID` varchar(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_NODAL_CLINIC` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_MH_ID` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OM_TIER_ID` int DEFAULT '0',
  `OM_EMPL_ID` varchar(30) DEFAULT NULL,
  `OM_EMPANEL_NO` varchar(45) DEFAULT NULL,
  `OM_GSTNO` varchar(15) DEFAULT NULL,
  `OM_EXT_API` int DEFAULT '0',
  `OM_REF_ISSUE` int DEFAULT '0',
  `OM_DIVERT_OIC` varchar(5) DEFAULT NULL,
  PRIMARY KEY (`OM_OFFICE_ID`),
  KEY `FK_office_entity_Id` (`OM_OFFICE_ENTITY_ID`),
  KEY `FK_office_master_2` (`OM_OFFICE_STATE_ID`),
  KEY `Idx_CGHS_City_Id` (`OM_OFFICE_CGHS_CITY_ID`) USING BTREE,
  KEY `Idx_Rate_Region` (`OM_RATE_REGION`),
  KEY `idx_source_poly` (`OM_SOURCE_POLY_ID`),
  KEY `Idx_Catg_Id` (`OM_CATG_ID`),
  CONSTRAINT `FK_CGHS_CITY_ID` FOREIGN KEY (`OM_OFFICE_CGHS_CITY_ID`) REFERENCES `cghs_region_master` (`CRM_CITY_ID`),
  CONSTRAINT `FK_STATE_ID` FOREIGN KEY (`OM_OFFICE_STATE_ID`) REFERENCES `state_master` (`SM_STATE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `office_reg_valdate`
--

DROP TABLE IF EXISTS `office_reg_valdate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `office_reg_valdate` (
  `ORV_OFFICE_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `ORV_VAL_TYPE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'M',
  `ORV_ID` int NOT NULL DEFAULT '0',
  `ORV_VAL_FROM` date NOT NULL,
  `ORV_VAL_TO` date NOT NULL,
  `ORV_FULL` int NOT NULL DEFAULT '1',
  `ORV_TRAN_NO` int NOT NULL,
  `ORV_CREATE_BY` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ORV_CREATE_DATE` datetime NOT NULL,
  `ORV_CREATE_IP` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ORV_UPDATED_BY` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ORV_UPDATE_DATE` datetime NOT NULL,
  `ORV_UPDATE_IP` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ORV_MOU_FILENAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ORV_REMARK` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  PRIMARY KEY (`ORV_OFFICE_ID`,`ORV_VAL_TYPE`,`ORV_VAL_FROM`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `opd_ph_answers`
--

DROP TABLE IF EXISTS `opd_ph_answers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `opd_ph_answers` (
  `opd_ans_id` int unsigned NOT NULL DEFAULT '0',
  `opd_ans_anyhistory` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'M',
  `opd_ans_details` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `opd_claim_id` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`opd_claim_id`,`opd_ans_id`) USING BTREE,
  KEY `FK_opd_ph_answers_1` (`opd_ans_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='InnoDB free: 11264 kB';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `opd_ph_question`
--

DROP TABLE IF EXISTS `opd_ph_question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `opd_ph_question` (
  `opd_question_id` int unsigned NOT NULL DEFAULT '0',
  `opd_questions` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `opd_active` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'Y',
  PRIMARY KEY (`opd_question_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ot_setup`
--

DROP TABLE IF EXISTS `ot_setup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ot_setup` (
  `OT_ID` int NOT NULL AUTO_INCREMENT,
  `OT_EMPTYPE` int DEFAULT NULL,
  `OT_DAY` int DEFAULT NULL,
  `OT_FULLDAY` int DEFAULT '0',
  `OT_FROM_TIME` time DEFAULT NULL,
  `OT_TO_TIME` time DEFAULT NULL,
  `OT_FINISH_REG` int DEFAULT '0',
  `OT_SCH_TIME` int NOT NULL DEFAULT '1',
  `OT_ACTIVE` int DEFAULT '1',
  PRIMARY KEY (`OT_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `other_last_tran_details`
--

DROP TABLE IF EXISTS `other_last_tran_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `other_last_tran_details` (
  `LTD_TRAN_TYPE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `LTD_LAST_NO` int unsigned NOT NULL,
  `LTD_TRAN_DESC` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `LTD_TRAN_TYPE_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`LTD_TRAN_TYPE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `other_recovery`
--

DROP TABLE IF EXISTS `other_recovery`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `other_recovery` (
  `OR_CLAIM_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `OR_RECOV_FROM` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `OR_SETTLEMENT_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OR_RECOVER_AMT` decimal(14,2) DEFAULT '0.00',
  `OR_REMARK` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  PRIMARY KEY (`OR_CLAIM_ID`,`OR_RECOV_FROM`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `otp_generator`
--

DROP TABLE IF EXISTS `otp_generator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `otp_generator` (
  `OG_ID` int NOT NULL AUTO_INCREMENT,
  `OG_SECURITY_CODE` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OG_CARD_ID` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OG_MOBILE_NUM` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OG_OTP` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OG_GEN_TIME` datetime DEFAULT NULL,
  `OG_VALID_TIME` datetime DEFAULT NULL,
  `OG_RECV_TIME` datetime DEFAULT NULL,
  `OG_OTP_SUCC` int DEFAULT '0',
  `OG_IP_ADDRESS` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`OG_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=1699972 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `par_ext_duration`
--

DROP TABLE IF EXISTS `par_ext_duration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `par_ext_duration` (
  `PED_DAYS` int unsigned NOT NULL DEFAULT '0',
  `PED_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'Y',
  PRIMARY KEY (`PED_DAYS`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `parameter_master`
--

DROP TABLE IF EXISTS `parameter_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parameter_master` (
  `PM_ID` int unsigned NOT NULL AUTO_INCREMENT,
  `PM_DESC` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PM_UNIT` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`PM_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `parameter_range`
--

DROP TABLE IF EXISTS `parameter_range`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parameter_range` (
  `PS_RANGE_ID` int unsigned NOT NULL DEFAULT '0',
  `PS_ID` int unsigned NOT NULL DEFAULT '0',
  `PS_FROM_DATE` date NOT NULL,
  `PS_TO_DATE` date DEFAULT NULL,
  `PS_FROM_RANGE` decimal(10,0) DEFAULT '0',
  `PS_TO_RANGE` decimal(10,0) DEFAULT '0',
  `PS_SHORT_CODE` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PS_MIN_LIMIT` int NOT NULL DEFAULT '0',
  `PS_MAX_LIMIT` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`PS_RANGE_ID`),
  KEY `Index_2` (`PS_ID`),
  KEY `Index_3` (`PS_FROM_RANGE`),
  KEY `Index_4` (`PS_TO_RANGE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `parametric_attributes`
--

DROP TABLE IF EXISTS `parametric_attributes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parametric_attributes` (
  `PA_ID` int NOT NULL,
  `PA_ATTRIBUTE` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PA_TYPE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`PA_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `parametric_values`
--

DROP TABLE IF EXISTS `parametric_values`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parametric_values` (
  `PV_ID` int NOT NULL,
  `PV_GROUP_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `PV_FROM_DATE` date NOT NULL,
  `PV_TO_DATE` date DEFAULT NULL,
  `PV_VALUE` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`PV_ID`,`PV_GROUP_ID`,`PV_FROM_DATE`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `passwordpolicy`
--

DROP TABLE IF EXISTS `passwordpolicy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `passwordpolicy` (
  `pw_expiry` int NOT NULL DEFAULT '0',
  `pw_history` int NOT NULL DEFAULT '0',
  `ps_min_length` int NOT NULL DEFAULT '0',
  `pw_man_special` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `pw_special_chars` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `pw_man_numeric` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `pw_man_upper` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `pw_change_before` int DEFAULT '0',
  `pw_login_attempts` int DEFAULT '3',
  `pw_from_date` date NOT NULL DEFAULT '0000-00-00',
  `pw_to_date` date DEFAULT NULL,
  PRIMARY KEY (`pw_from_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `patient_register`
--

DROP TABLE IF EXISTS `patient_register`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patient_register` (
  `PTR_CARD_ID` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `PTR_BEN_ID` bigint NOT NULL DEFAULT '0',
  `PTR_BENEFICIARY_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_PATIENT_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_SERVICE_TYPE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_SERVICE_RANK` int DEFAULT '0',
  `PTR_SERVICE_NO` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_UID_NUMBER` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_UID_STATUS` int DEFAULT '0',
  `PTR_DOB` date DEFAULT NULL,
  `PTR_SEX` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_RELATION_ID` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_PHONE_NO` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_MOBILE` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_EMAIL` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_ADDRESS1` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_ADDRESS2` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_ADDRESS3` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_CITY` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_STATE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_PIN` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_CARD_ROOM_TYPE` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_CR_USER` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PTR_CR_DATE` datetime NOT NULL,
  `PTR_IP_ADDRESS` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`PTR_CARD_ID`),
  UNIQUE KEY `uq_benf_id` (`PTR_BEN_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `patient_type`
--

DROP TABLE IF EXISTS `patient_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patient_type` (
  `PT_TYPE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `PT_TYPE_DESC` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PT_TYPE_CODE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PT_TYPE_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`PT_TYPE_ID`),
  UNIQUE KEY `Index_2` (`PT_TYPE_CODE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pay_mode`
--

DROP TABLE IF EXISTS `pay_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pay_mode` (
  `PM_PAY_MODE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '0',
  `PM_PAY_MODE_DESC` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PM_PAY_MODE_CODE` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PM_PAY_MODE_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`PM_PAY_MODE_ID`),
  KEY `Index_2` (`PM_PAY_MODE_CODE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `payment_instruction`
--

DROP TABLE IF EXISTS `payment_instruction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment_instruction` (
  `PI_REC_ID` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_PAY_VAL_DT` datetime NOT NULL,
  `PI_PROD_CODE` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_DEB_AC_NO` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_BEN_CODE` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_BEN_NAME` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_INSTR_REF_NO` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_INSTR_AMT` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_PAY_LOC_CODE` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_PAY_BRANCH_CODE` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_BEN_BANK_CODE` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_BEN_BANK_BRC_CODE` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_BEN_AC_NO` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_BEN_AC_TYPE` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_BEN_ADD1` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_BEN_ADD2` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_BEN_ADD3` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_BEN_ADD4` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_BEN_ZIP_CODE` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_DEL_MODE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_OTC_PER` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_DISP_TO` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_DISP_TO_BRC_CODE` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_DISP_LOC_CODE` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_DISP_TO_ADD1` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_DISP_TO_ADD2` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_DISP_TO_ADD3` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_DISP_TO_ADD4` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_DISP_TO_ZIP_CODE` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_CHQ_NO` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_ISSUE_REF_NO` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_WAR_NO` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_FOLIO_NO` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_ENRC_TXT1` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_ENCR_TXT2` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_ENCR_TXT3` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_ENCR_TXT4` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_ENCR_TXT5` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_ENCR_TXT6` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_ENCR_TXT7` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_ENCR_TXT8` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_ENCR_TXT9` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_ENCR_TXT10` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PI_SETTLEMENT_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pend_claims`
--

DROP TABLE IF EXISTS `pend_claims`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pend_claims` (
  `REGION_ID` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OFFICE_ID` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PATIENT_TYPE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ADM_TYPE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `REIM_TYPE` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CLAIM_STAGE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CLAIM_STATUS` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MOD_DATE` datetime NOT NULL,
  `ACC_DATE` datetime DEFAULT NULL,
  `ENTITY_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `NET_AMT` int DEFAULT '0',
  `SUP_AMT` int DEFAULT '0',
  `APP_AMT` int DEFAULT '0',
  `CURR_RATIO` decimal(10,2) DEFAULT '1.00',
  `DOC_RECD` int DEFAULT '0',
  `DOC_VERIFY` int DEFAULT '0',
  KEY `idx_stage` (`CLAIM_STAGE`),
  KEY `idx_status` (`CLAIM_STATUS`),
  KEY `idx_entity` (`ENTITY_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pend_group_details`
--

DROP TABLE IF EXISTS `pend_group_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pend_group_details` (
  `REGION_ID` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `OFFICE_ID` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PATIENT_TYPE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ADM_TYPE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `REIM_TYPE` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CLAIM_STAGE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `CLAIM_STATUS` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `MOD_DATE` datetime NOT NULL,
  `ACC_DATE` datetime DEFAULT NULL,
  `ENTITY_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `NET_AMT` int DEFAULT '0',
  `SUP_AMT` int DEFAULT '0',
  `APP_AMT` int DEFAULT '0',
  `GROUP_ID` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  KEY `idx_stage` (`CLAIM_STAGE`),
  KEY `idx_status` (`CLAIM_STATUS`),
  KEY `idx_entity` (`ENTITY_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pend_schd`
--

DROP TABLE IF EXISTS `pend_schd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pend_schd` (
  `PS_ID` int NOT NULL AUTO_INCREMENT,
  `PS_DATE` date NOT NULL,
  `PS_START_TIME` datetime NOT NULL,
  `PS_END_TIME` datetime DEFAULT NULL,
  `PS_RC_REC` int DEFAULT '0',
  `PS_OFF_REC` int DEFAULT '0',
  PRIMARY KEY (`PS_ID`),
  UNIQUE KEY `PS_DATE_UNIQUE` (`PS_DATE`)
) ENGINE=InnoDB AUTO_INCREMENT=536 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pendency_master`
--

DROP TABLE IF EXISTS `pendency_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pendency_master` (
  `PM_ID` int NOT NULL AUTO_INCREMENT,
  `PM_ENTITY_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PM_STAGE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PM_STATUS` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PM_DESP_ID` int NOT NULL DEFAULT '0',
  `PM_GROUP_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '0',
  `PM_BPA_ZERO` int DEFAULT '0',
  `PM_FROM_AMT` int DEFAULT '0',
  `PM_TO_AMT` int DEFAULT '0',
  `PM_NXT_GROUP_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PM_IS_FINAL` int DEFAULT '0',
  `PM_IS_ACCEPT` int DEFAULT '0',
  `PM_IS_NMI` int DEFAULT '0',
  `PM_IS_REVIEW` int DEFAULT '0',
  `PM_IS_REPLY` int DEFAULT '0',
  `PM_NMI_LIMIT` int DEFAULT '0',
  `PM_DISPLAY` int DEFAULT '1',
  `PM_ORDER` int DEFAULT '0',
  `PM_DOC_RECD` int DEFAULT '0',
  `PM_DOC_VERIFY` int DEFAULT '1',
  PRIMARY KEY (`PM_ID`),
  UNIQUE KEY `idx_unique` (`PM_ENTITY_ID`,`PM_STAGE`,`PM_STATUS`,`PM_BPA_ZERO`,`PM_FROM_AMT`),
  KEY `idx_stage` (`PM_STAGE`),
  KEY `idx_status` (`PM_STATUS`),
  KEY `idx_entity` (`PM_ENTITY_ID`),
  KEY `idx_amt` (`PM_FROM_AMT`),
  KEY `idx_toamt` (`PM_TO_AMT`),
  KEY `idx_next_group` (`PM_NXT_GROUP_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=179 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phy_instr_det`
--

DROP TABLE IF EXISTS `phy_instr_det`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `phy_instr_det` (
  `PID_TRAN_NO` decimal(10,0) NOT NULL,
  `PID_INSTR_NO` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PID_INSTR_DT` date DEFAULT NULL,
  `PID_INSTR_TYPE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PID_INSTR_AMOUNT` decimal(15,2) NOT NULL,
  `PID_DRAWEE_BANK` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PID_INSTR_REMARK` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `PID_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PID_TRAN_DATE` datetime NOT NULL,
  `PID_IP_ADDRESS` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`PID_TRAN_NO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Physical Instrument Details';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phy_instr_mode`
--

DROP TABLE IF EXISTS `phy_instr_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `phy_instr_mode` (
  `PIM_INSTR_MODE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '0',
  `PIM_INSTR_MODE_DESC` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PIM_INSTR_MODE_CODE` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PIM_INSTR_MODE_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`PIM_INSTR_MODE_ID`),
  KEY `Idx_MODE_CODE` (`PIM_INSTR_MODE_CODE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pndgrprt`
--

DROP TABLE IF EXISTS `pndgrprt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pndgrprt` (
  `clm_id` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `bnfry_nm` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ptnt_nm` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `card_no` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `srvc_no` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `pty_typ` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `loc` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `hosp_nm` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `admtn_dt` datetime DEFAULT NULL,
  `submtn_dt` datetime DEFAULT NULL,
  `clm_amt` decimal(16,2) DEFAULT NULL,
  `submt_to` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `rcpt_dt` datetime DEFAULT NULL,
  `rcpt_frm` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `stg` varchar(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pre_auth`
--

DROP TABLE IF EXISTS `pre_auth`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pre_auth` (
  `PA_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PA_DATE` datetime DEFAULT NULL,
  `PA_DIAGNOSIS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `PA_EST_COST` decimal(15,2) DEFAULT NULL,
  `PA_CASE_SUMMARY` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `PA_TREAT_MODALITY` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `PA_TREAT_FINALITY` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PA_TREAT_TIME` int DEFAULT '0',
  `PA_DOCTORS` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PA_PAT_VISIT_DATE` date DEFAULT NULL,
  `PA_TREAT_AUTH` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `PA_TREAT_EFFECT` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `PA_DIAG_RELEVANCE` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `PA_EXT_STAY_REASON` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `PA_EXP_FINALITY_DT` date DEFAULT NULL,
  `PA_REMARK` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `PA_APP_REMARK` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `PA_APPROVED` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PA_APP_BY` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PA_ANY_ATTACHMENT` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PA_AUTH_ID` int NOT NULL DEFAULT '0',
  `PA_AUTH_FLAG` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'P',
  PRIMARY KEY (`PA_AUTH_ID`),
  KEY `FK_pre_auth_1` (`PA_INTIMATION_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='InnoDB free: 6144 kB';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pre_exist_ailment`
--

DROP TABLE IF EXISTS `pre_exist_ailment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pre_exist_ailment` (
  `PEA_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `PEA_AILMENT_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `PEA_IS_AILMENT` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PEA_AILMENT_DETAILS` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PEA_ENHANCE_ID` int unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`PEA_INTIMATION_ID`,`PEA_AILMENT_ID`,`PEA_ENHANCE_ID`) USING BTREE,
  KEY `FK_pre_exist_ailment_1` (`PEA_AILMENT_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `prior_app_setting`
--

DROP TABLE IF EXISTS `prior_app_setting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prior_app_setting` (
  `PAS_GROUP_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `PAS_STAGE` int NOT NULL,
  `PAS_NEXT_GROUP` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PAS_FINAL` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`PAS_GROUP_ID`,`PAS_STAGE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `prior_approval`
--

DROP TABLE IF EXISTS `prior_approval`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prior_approval` (
  `PA_CLAIM_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `PA_APPLY_DATE` datetime NOT NULL,
  `PA_HOSPITAL` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PA_REASON` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PA_REIM_TYPE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PA_ESTIMATE_COST` double NOT NULL DEFAULT '0',
  `PA_REQUERY_ID` int DEFAULT '0',
  `PA_GROUP_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PA_REQUERY_BY` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PA_PROCESS_USER` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PA_PROCESS_STAGE` int DEFAULT '0',
  `PA_PROCESS_DATE` datetime DEFAULT NULL,
  `PA_FINAL_STAGE` int NOT NULL DEFAULT '0',
  `PA_IP_ADDRESS` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`PA_CLAIM_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `prior_approval_events`
--

DROP TABLE IF EXISTS `prior_approval_events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prior_approval_events` (
  `PAE_CLAIM_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `PAE_REQUERY_ID` int NOT NULL DEFAULT '0',
  `PAE_GROUP_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `PAE_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PAE_STATUS` int NOT NULL DEFAULT '0',
  `PAE_DATE` datetime NOT NULL,
  `PAE_REPLY` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `PAE_PROCESS_REMARKS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `PAE_IP_ADDRESS` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`PAE_CLAIM_ID`,`PAE_REQUERY_ID`,`PAE_GROUP_ID`,`PAE_STATUS`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `procdlog`
--

DROP TABLE IF EXISTS `procdlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `procdlog` (
  `vseq` int NOT NULL AUTO_INCREMENT,
  `v_file_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `v_field_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `v_field_value` varchar(5000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`vseq`)
) ENGINE=InnoDB AUTO_INCREMENT=12177030 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `process_alert`
--

DROP TABLE IF EXISTS `process_alert`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `process_alert` (
  `PA_GROUP_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `PA_FROM_DATE` date NOT NULL,
  `PA_TO_DATE` date DEFAULT NULL,
  `PA_PATIENT_TYPE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `PA_STAGE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `PA_LIMIT` int NOT NULL,
  `PA_DIFF_TYPE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'D',
  `PA_DAYS_TYPE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`PA_GROUP_ID`,`PA_FROM_DATE`,`PA_PATIENT_TYPE`,`PA_STAGE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `prop_treatment`
--

DROP TABLE IF EXISTS `prop_treatment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prop_treatment` (
  `PT_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `PT_TRTYPE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `PR_IS_TREATMENT` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PR_TR_DETAILS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `PR_ENHANCE_ID` int NOT NULL DEFAULT '0',
  `PR_PRE_AUTH_ID` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`PT_INTIMATION_ID`,`PT_TRTYPE_ID`,`PR_ENHANCE_ID`,`PR_PRE_AUTH_ID`),
  KEY `FK_prop_treatment_1` (`PT_TRTYPE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rank_master`
--

DROP TABLE IF EXISTS `rank_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rank_master` (
  `rm_service_code` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'A',
  `rm_rank_id` int unsigned NOT NULL,
  `rm_rank_def` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `RM_SINFO_ID` int DEFAULT '0',
  `rm_active` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'Y',
  `rm_room_type_id` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`rm_service_code`,`rm_rank_id`) USING BTREE,
  KEY `Index_2` (`rm_rank_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rates_master`
--

DROP TABLE IF EXISTS `rates_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rates_master` (
  `RM_CAT_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `RM_CAT_SUB_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `RM_CAT_DESC` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `RM_RATE` decimal(15,2) NOT NULL,
  `RM_CAT_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `RM_REGION_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `RM_RATE_TYPE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`RM_CAT_ID`,`RM_CAT_SUB_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `recovery_type`
--

DROP TABLE IF EXISTS `recovery_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recovery_type` (
  `RT_ID` int unsigned NOT NULL AUTO_INCREMENT,
  `RT_DESC` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `RT_FINANCE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'Y',
  `RT_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'Y',
  PRIMARY KEY (`RT_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `red_tax_rate`
--

DROP TABLE IF EXISTS `red_tax_rate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `red_tax_rate` (
  `RTR_RATE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `RTR_PERIOD_FR` date NOT NULL,
  `RTR_PERIOD_TO` date NOT NULL,
  `RTR_SER_TAX` decimal(10,3) DEFAULT NULL,
  `RTR_ECESS` decimal(10,3) DEFAULT '0.000',
  `RTR_HSCESS` decimal(10,3) DEFAULT '0.000',
  `RTR_SBCESS` decimal(10,3) DEFAULT '0.000',
  `RTR_KKCESS` decimal(10,3) DEFAULT '0.000',
  `RTR_TAX_TYPE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `RTR_OFFICE_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `RTR_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `RTR_UPDATE_DATE` datetime NOT NULL,
  `RTR_IP_ADDRESS` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `RTR_AMT_LIMIT` decimal(15,2) DEFAULT NULL,
  PRIMARY KEY (`RTR_RATE_ID`),
  KEY `Index_2` (`RTR_PERIOD_FR`),
  KEY `Index_3` (`RTR_PERIOD_TO`),
  KEY `Index_4` (`RTR_OFFICE_ID`),
  KEY `Index_5` (`RTR_TAX_TYPE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `referal_city`
--

DROP TABLE IF EXISTS `referal_city`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `referal_city` (
  `rc_region_id` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `rc_city_id` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `rc_city_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `rc_city_active` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'Y',
  PRIMARY KEY (`rc_city_id`) USING BTREE,
  KEY `Idx_Region_Id` (`rc_region_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `referal_details`
--

DROP TABLE IF EXISTS `referal_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `referal_details` (
  `REF_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `REF_NUMBER` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `REF_CGHS_REGION_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `REF_CGHS_DISP_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `REF_ISS_DATE` date DEFAULT NULL,
  `REF_ADV_BY` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `REF_APP_BY` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `REF_HOSPITAL_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `REF_ROOM_TYPE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `REF_VAL_DATE` date DEFAULT NULL,
  `REF_SESSIONS` int DEFAULT NULL,
  `REF_PROCEDURES` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `REF_ENTRY_BY` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'H',
  `REF_BAL_SESSION` int unsigned DEFAULT '0',
  `REF_ADM_PROCEDURES` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `REF_INV_PROCEDURES` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `REF_CON_PROCEDURES` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `REF_TRAVEL_REIMBURSE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `REF_ATTENDANT_REIMBURSE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `REF_PATIENT_TYPE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `REF_CITY_ID` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`REF_INTIMATION_ID`),
  KEY `Index_2` (`REF_CGHS_DISP_ID`),
  KEY `Idx_Ref_Iss_Date` (`REF_ISS_DATE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `referal_type`
--

DROP TABLE IF EXISTS `referal_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `referal_type` (
  `RT_TYPE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `RT_TYPE_DESC` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `RT_TYPE_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `RT_TYPE_CODE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`RT_TYPE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `referral_sessions`
--

DROP TABLE IF EXISTS `referral_sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `referral_sessions` (
  `RS_CLAIM_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `RS_REF_CLAIM_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `RS_DATE` datetime NOT NULL,
  PRIMARY KEY (`RS_CLAIM_ID`),
  KEY `IDX_REFCLAIM` (`RS_REF_CLAIM_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `region_budget_allocate`
--

DROP TABLE IF EXISTS `region_budget_allocate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `region_budget_allocate` (
  `RBA_REGION_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `RBA_BUDGET_AMOUNT` decimal(15,2) NOT NULL DEFAULT '0.00',
  PRIMARY KEY (`RBA_REGION_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `region_budget_details`
--

DROP TABLE IF EXISTS `region_budget_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `region_budget_details` (
  `RBD_TRAN_NO` int unsigned NOT NULL,
  `RBD_REGION_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `RBD_TRAN_DATE` date NOT NULL,
  `RBD_TRAN_AMOUNT` decimal(15,2) NOT NULL DEFAULT '0.00',
  `RBD_TRAN_TYPE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `RBD_REMARK` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `RBD_UPDATE_DATE` datetime NOT NULL,
  `RBD_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `RBD_IP_ADDRESS` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`RBD_TRAN_NO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `regionpendency_summary`
--

DROP TABLE IF EXISTS `regionpendency_summary`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `regionpendency_summary` (
  `rps_rcrd_no` bigint NOT NULL AUTO_INCREMENT,
  `rps_city_id` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `rps_city_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `rps_HOS_COUNT` int DEFAULT NULL,
  `rps_HOS_AMT` decimal(16,2) DEFAULT NULL,
  `rps_HOS_NMI_COUNT` int DEFAULT NULL,
  `rps_HOS_NMI_AMT` decimal(16,2) DEFAULT NULL,
  `rps_VER_COUNT` int DEFAULT NULL,
  `rps_VER_AMT` decimal(16,2) DEFAULT NULL,
  `rps_BPA_COUNT` int DEFAULT NULL,
  `rps_BPA_AMT` decimal(16,2) DEFAULT NULL,
  `rps_RC_COUNT` int DEFAULT NULL,
  `rps_RC_AMT` decimal(16,2) DEFAULT NULL,
  `rps_CORG_COUNT` int DEFAULT NULL,
  `rps_CORG_AMT` decimal(16,2) DEFAULT NULL,
  `rps_CFA_COUNT` int DEFAULT NULL,
  `rps_CFA_AMT` decimal(16,2) DEFAULT NULL,
  `rps_DYMD_COUNT` int DEFAULT NULL,
  `rps_DYMD_AMT` decimal(16,2) DEFAULT NULL,
  `rps_MD_COUNT` int DEFAULT NULL,
  `rps_MD_AMT` decimal(16,2) DEFAULT NULL,
  `rps_MOD_COUNT` int DEFAULT NULL,
  `rps_MOD_AMT` decimal(16,2) DEFAULT NULL,
  `rps_ACC_COUNT` int DEFAULT NULL,
  `rps_ACC_AMT` decimal(16,2) DEFAULT NULL,
  `rps_reprt_dt` date DEFAULT NULL,
  `rps_rp_exctn_dt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`rps_rcrd_no`),
  KEY `rps_ix001` (`rps_reprt_dt`,`rps_city_id`)
) ENGINE=InnoDB AUTO_INCREMENT=74926 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `reimb_recovery`
--

DROP TABLE IF EXISTS `reimb_recovery`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reimb_recovery` (
  `RR_RECOVERY_ID` int unsigned NOT NULL AUTO_INCREMENT,
  `RR_CLAIM_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `RR_SERVICE_NO` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `RR_RECOVERY_AMT` decimal(15,2) NOT NULL DEFAULT '0.00',
  `RR_RECOVERED_AMT` decimal(15,2) NOT NULL DEFAULT '0.00',
  `RR_BALANCE_AMT` decimal(15,2) NOT NULL DEFAULT '0.00',
  `RR_REMARK` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  PRIMARY KEY (`RR_RECOVERY_ID`),
  KEY `Idx_Service_No` (`RR_SERVICE_NO`)
) ENGINE=InnoDB AUTO_INCREMENT=275 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `reimb_recovery_details`
--

DROP TABLE IF EXISTS `reimb_recovery_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reimb_recovery_details` (
  `RRD_ID` int unsigned NOT NULL AUTO_INCREMENT,
  `RRD_RECOV_FROM` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `RRD_SETTLEMENT_ID` int unsigned DEFAULT NULL,
  `RRD_RECOVER_AMT` decimal(15,2) NOT NULL,
  PRIMARY KEY (`RRD_ID`,`RRD_RECOV_FROM`)
) ENGINE=InnoDB AUTO_INCREMENT=270 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `reimb_type`
--

DROP TABLE IF EXISTS `reimb_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reimb_type` (
  `RT_TYPE_ID` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `RT_TYPE_DESC` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `RT_TYPE_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `RT_EIR_REQ` int DEFAULT '1',
  PRIMARY KEY (`RT_TYPE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rej_settle_history`
--

DROP TABLE IF EXISTS `rej_settle_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rej_settle_history` (
  `RSH_SETTLEMENT_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `RSH_ENTITY_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `RSH_DATE` date NOT NULL,
  `RSH_REGION_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`RSH_SETTLEMENT_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `relation_master`
--

DROP TABLE IF EXISTS `relation_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `relation_master` (
  `RM_RELATION_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `RM_RELATION_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `RM_SINFO_ID` int DEFAULT '0',
  `RM_SINFO_RELATION_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `RM_RELATION_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`RM_RELATION_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `remark_type`
--

DROP TABLE IF EXISTS `remark_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `remark_type` (
  `RT_REM_TYPE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `RT_REM_TYPE_DESC` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `RT_REM_TYPE_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `RT_DISP_ORDER` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`RT_REM_TYPE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `report_param`
--

DROP TABLE IF EXISTS `report_param`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `report_param` (
  `RP_REP_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `RP_RANGE_FR` decimal(15,2) NOT NULL,
  `RP_RANGE_TO` decimal(15,2) NOT NULL,
  `RP_RANGE_AGE_FR` int unsigned NOT NULL DEFAULT '0',
  `RP_RANGE_AGE_TO` int unsigned NOT NULL DEFAULT '0',
  `RP_TRAN_ID` int unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`RP_TRAN_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `room_rates`
--

DROP TABLE IF EXISTS `room_rates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `room_rates` (
  `RR_TYPE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `RR_FROM_DATE` date NOT NULL,
  `RR_TO_DATE` date DEFAULT NULL,
  `RR_RATE` decimal(15,2) DEFAULT NULL,
  `RR_NABH` decimal(6,2) NOT NULL DEFAULT '0.00',
  `RR_NON_NABH` decimal(6,2) DEFAULT '0.00',
  `RR_CGHS_CODE` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `RR_TYPE_ID` int unsigned DEFAULT '0',
  `RR_REGION_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`RR_TYPE`,`RR_FROM_DATE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `room_type`
--

DROP TABLE IF EXISTS `room_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `room_type` (
  `RT_TYPE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `RT_TYPE_DESC` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `RT_TYPE_CODE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `RT_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `RR_DISPLAY_ORDER` int unsigned DEFAULT '1',
  `RT_ENTITLE` int DEFAULT '0',
  PRIMARY KEY (`RT_TYPE_ID`),
  KEY `Idx_Room_Active` (`RT_ACTIVE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `seq_mem_req`
--

DROP TABLE IF EXISTS `seq_mem_req`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seq_mem_req` (
  `SQ_REQ_ID` int NOT NULL AUTO_INCREMENT,
  `SQ_KEY` int NOT NULL,
  PRIMARY KEY (`SQ_REQ_ID`),
  UNIQUE KEY `SQ_KEY_UNIQUE` (`SQ_KEY`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `service_fees`
--

DROP TABLE IF EXISTS `service_fees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `service_fees` (
  `SF_FEES_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `SF_PERIOD_FR` date NOT NULL,
  `SF_PERIOD_TO` date NOT NULL,
  `SF_BILL_AMT_FR` decimal(15,2) NOT NULL,
  `SF_BILL_AMT_TO` decimal(15,2) NOT NULL,
  `SF_SER_FEES` decimal(15,5) NOT NULL,
  `SF_SOURCE_ENTITY_ID` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`SF_FEES_ID`),
  KEY `Index_2` (`SF_SOURCE_ENTITY_ID`),
  KEY `Index_3` (`SF_BILL_AMT_FR`),
  KEY `Index_4` (`SF_BILL_AMT_TO`),
  KEY `Index_5` (`SF_PERIOD_FR`),
  KEY `Index_6` (`SF_PERIOD_TO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `service_master`
--

DROP TABLE IF EXISTS `service_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `service_master` (
  `sm_code` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `sm_desc` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SM_SINFO_ID` int DEFAULT '0',
  `sm_active` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`sm_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `settlement_details`
--

DROP TABLE IF EXISTS `settlement_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `settlement_details` (
  `SD_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `SD_SUB_ENTITY_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SD_SUB_OFFICE_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SD_OFFICE_NAME` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SD_OFFICE_ADD1` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SD_OFFICE_ADD2` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SD_OFFICE_ADD3` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SD_OFFICE_CITY` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SD_OFFICE_STATE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SD_OFFICE_STATE` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SD_OFFICE_PIN` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SD_OFFICE_PAN` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SD_BANK_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SD_BANK_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SD_BANK_BRANCH` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SD_BANK_ADD1` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SD_BANK_ADD2` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SD_BANK_ADD3` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SD_BANK_CITY` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SD_BANK_STATE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SD_BANK_STATE` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SD_BANK_PIN` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SD_BANK_ACTYPE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SD_BANK_ACNO` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SD_BANK_MICR` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SD_BANK_IFSC` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SD_PAY_MODE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SD_CLAIM_AMT` decimal(15,2) DEFAULT NULL,
  `SD_UTI_APP_AMT` decimal(15,2) DEFAULT NULL,
  `SD_ACCEPT_DATE` datetime DEFAULT NULL,
  `SD_SETTLE_DATE` datetime DEFAULT NULL,
  `SD_CGHS_DIS_PER` decimal(5,2) DEFAULT NULL,
  `SD_CGHS_DIS_AMT` decimal(15,2) DEFAULT NULL,
  `SD_RECOUP_CLAIM_AMT` decimal(15,2) DEFAULT NULL,
  `SD_HOS_SER_RATE` decimal(10,3) DEFAULT NULL,
  `SD_HOS_SER` decimal(15,2) DEFAULT NULL,
  `SD_HOS_ECESS` decimal(15,2) DEFAULT NULL,
  `SD_HOS_HSCESS` decimal(15,2) DEFAULT NULL,
  `SD_HOS_TOT_TAX` decimal(15,2) DEFAULT NULL,
  `SD_HOS_UTI_FEE` decimal(15,2) DEFAULT NULL,
  `SD_BPA_PENALITY` decimal(15,2) DEFAULT NULL,
  `SD_HOS_UTI_SER` decimal(15,2) DEFAULT NULL,
  `SD_HOS_UTI_CGST` decimal(15,2) DEFAULT '0.00',
  `SD_HOS_UTI_SGST` decimal(15,2) DEFAULT '0.00',
  `SD_HOS_UTI_IGST` decimal(15,2) DEFAULT '0.00',
  `SD_HOS_UTI_ECESS` decimal(15,2) DEFAULT NULL,
  `SD_HOS_UTI_HSCESS` decimal(15,2) DEFAULT NULL,
  `SD_HOS_UTI_SBCESS` decimal(15,2) DEFAULT NULL,
  `SD_HOS_UTI_KKCESS` decimal(15,2) DEFAULT NULL,
  `SD_HOS_UTI_TOT_TAX` decimal(15,2) DEFAULT NULL,
  `SD_HOS_UTI_NET_PAY` decimal(15,2) DEFAULT NULL,
  `SD_HOS_UTI_NET_PAY_INCL_SER_TAX` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SD_HOS_UTI_TDS` decimal(15,2) DEFAULT NULL,
  `SD_HOS_UTI_GST_TDS` decimal(15,2) NOT NULL DEFAULT '0.00',
  `SD_HOS_UTI_NET_FEES` decimal(15,2) DEFAULT NULL,
  `SD_HOS_NET_PAY` decimal(15,2) DEFAULT NULL,
  `SD_CGHS_UTI_FEE` decimal(15,2) DEFAULT NULL,
  `SD_CGHS_UTI_SER` decimal(15,2) DEFAULT NULL,
  `SD_CGHS_UTI_ECESS` decimal(15,2) DEFAULT NULL,
  `SD_CGHS_UTI_HSCESS` decimal(15,2) DEFAULT NULL,
  `SD_CGHS_UTI_TOT_TAX` decimal(15,2) DEFAULT NULL,
  `SD_CGHS_UTI_NET_PAY` decimal(15,2) DEFAULT NULL,
  `SD_HOS_RECOV` decimal(15,2) DEFAULT NULL,
  `SD_HOS_NET_PAID` decimal(15,2) DEFAULT NULL,
  `SD_PROCESS_TRAN_NO` decimal(10,0) DEFAULT NULL,
  `SD_SETTLEMENT_ID` decimal(10,0) DEFAULT NULL,
  `SD_FINAL_SETTLE_DT` datetime DEFAULT NULL,
  `SD_FINAL_SETTLE_REMARK` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `SD_LAST_UPDATED` datetime DEFAULT NULL,
  `SD_UPDATED_BY` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SD_TAX_EXEMPT` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SD_BATCH_NO` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SD_BATCH_DATE` date DEFAULT NULL,
  `SD_PAYEE_NAME` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SD_BATCH_REFNO` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SD_RECOUP_AMT` decimal(15,2) DEFAULT '0.00',
  `SD_CGHS_RECOV` decimal(15,2) DEFAULT '0.00',
  `SD_RECOUP_DATE` date DEFAULT NULL,
  `SD_REJECT_MARK` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SD_RECOUP_REMARK` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SD_CLOSED` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'N',
  PRIMARY KEY (`SD_INTIMATION_ID`),
  KEY `Index_2` (`SD_SETTLEMENT_ID`),
  KEY `Index_3` (`SD_SUB_OFFICE_ID`),
  KEY `Index_4` (`SD_SUB_ENTITY_ID`),
  KEY `Index_5` (`SD_SETTLE_DATE`),
  KEY `Index_6` (`SD_FINAL_SETTLE_DT`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='InnoDB free: 6144 kB; (`SD_INTIMATION_ID`) REFER `cghs/claim';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `settlement_doc_reco`
--

DROP TABLE IF EXISTS `settlement_doc_reco`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `settlement_doc_reco` (
  `SDR_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `SDR_FINAL_SETTLE_DT` date NOT NULL,
  `SDR_SET_INT_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SDR_SENT_DATE` date DEFAULT NULL,
  `SDR_LIST_NAME` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SDR_FLAG` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`SDR_INTIMATION_ID`),
  KEY `Idx_SDR_INT_ID` (`SDR_SET_INT_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `settlement_last_tran_details`
--

DROP TABLE IF EXISTS `settlement_last_tran_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `settlement_last_tran_details` (
  `LTD_TRAN_TYPE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `LTD_LAST_NO` int unsigned NOT NULL,
  `LTD_TRAN_DESC` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `LTD_TRAN_TYPE_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`LTD_TRAN_TYPE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `settlement_stat`
--

DROP TABLE IF EXISTS `settlement_stat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `settlement_stat` (
  `SS_YEAR` int NOT NULL,
  `SS_MONTH` int NOT NULL,
  `SS_FY_YEAR` int NOT NULL DEFAULT '0',
  `SS_PAT_TYPE_ID` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `SS_ENTITY_ID` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `SS_REF_TYPE_ID` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `SS_REGION_ID` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `SS_OFFICE_ID` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `SS_GENDER` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `SS_RELATION_ID` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `SS_ROOM_CATG` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `SS_CLAIM_CNT` int NOT NULL DEFAULT '0',
  `SS_CLAIM_AMT` bigint NOT NULL DEFAULT '0',
  `SS_APPR_AMT` bigint NOT NULL DEFAULT '0',
  `SS_DED_AMT` bigint NOT NULL DEFAULT '0',
  PRIMARY KEY (`SS_YEAR`,`SS_MONTH`,`SS_PAT_TYPE_ID`,`SS_ENTITY_ID`,`SS_REF_TYPE_ID`,`SS_REGION_ID`,`SS_OFFICE_ID`,`SS_GENDER`,`SS_RELATION_ID`,`SS_ROOM_CATG`,`SS_FY_YEAR`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `settlement_valdate`
--

DROP TABLE IF EXISTS `settlement_valdate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `settlement_valdate` (
  `SV_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `SV_FIRST_VAL_DATE` datetime DEFAULT NULL,
  `SV_PROV_BPA_FEE` decimal(15,2) NOT NULL,
  `SV_PROV_BPA_SER_TAX` decimal(15,2) NOT NULL,
  `SV_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SV_PAID_DT` datetime DEFAULT NULL,
  `SV_VOUCHER_NO` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`SV_INTIMATION_ID`) USING BTREE,
  KEY `Idx_Val_Date` (`SV_FIRST_VAL_DATE`) USING BTREE,
  KEY `Idx_User_Id` (`SV_USER_ID`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_reco`
--

DROP TABLE IF EXISTS `sms_reco`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sms_reco` (
  `SBPR_PCODE` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SBPR_ACODE` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SBPR_MOBILE` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SBPR_SENDER_ID` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SBPR_AIR2WEB_ACCEPTED_DATE` datetime DEFAULT NULL,
  `SBPR_CARRIER_ACCEPTED_TIME` datetime DEFAULT NULL,
  `SBPR_STATUS` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SBPR_STATUS_ID` decimal(20,0) DEFAULT NULL,
  `SBPR_CARRIER_DELVERED_TIME` datetime DEFAULT NULL,
  `SBPR_CARRIER_STATUS` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SBPR_STATUS_DESC` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SBPR_MESSAGE_TEXT` varchar(4000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SBPR_AKN_ID` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SBPR_TRANS_ID` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  KEY `NDX_AKN_UPLOAD` (`SBPR_AKN_ID`,`SBPR_AIR2WEB_ACCEPTED_DATE`),
  KEY `NDX_UPLOAD` (`SBPR_AIR2WEB_ACCEPTED_DATE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_transaction`
--

DROP TABLE IF EXISTS `sms_transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sms_transaction` (
  `ST_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `ST_DATE` datetime NOT NULL,
  `ST_ACK_ID` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ST_TRAN_ID` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ST_INT_STAGE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ST_INT_STATUS` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ST_MOBILE` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ST_MESSAGE` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `ST_MSG_ID` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ST_DLR_TIME` datetime DEFAULT NULL,
  `ST_SMS_STATUS` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ST_ERR_CODE` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ST_SMS_DETAIL` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  PRIMARY KEY (`ST_INTIMATION_ID`,`ST_DATE`),
  KEY `Idx_Tran_Id` (`ST_TRAN_ID`),
  KEY `Idx_MOBILE` (`ST_MOBILE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `standard_remarks`
--

DROP TABLE IF EXISTS `standard_remarks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `standard_remarks` (
  `SR_REM_TYPE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `SR_REM_DESC` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SR_REM_TEXT` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `VR_REM_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`SR_REM_TYPE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `state_district_master`
--

DROP TABLE IF EXISTS `state_district_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `state_district_master` (
  `DSM_STATE_CODE` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DSM_STATE_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DSM_DIST_CODE` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DSM_DIST_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DSM_SUB_DIST_CODE` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DSM_SUB_DIST_VER` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DSM_SUB_DIST_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DSM_SUB_DIST_NAME_LOCAL` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DSM_CENSUS_2001_CODE` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DSM_CENSUS_2011_CODE` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  KEY `Idx_State_Code` (`DSM_STATE_CODE`),
  KEY `Idx_Dist_Code` (`DSM_DIST_CODE`),
  KEY `Idx_Sub_Dist_Code` (`DSM_SUB_DIST_CODE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `state_master`
--

DROP TABLE IF EXISTS `state_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `state_master` (
  `SM_STATE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `SM_STATE_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `ST_SINFO_ID` int DEFAULT '0',
  `SM_COUNTRY_ID` int DEFAULT '1',
  `SM_ISO_CODE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SM_IS_UT` int DEFAULT '0',
  `SM_IT_CODE` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SM_TIN_NUM` int NOT NULL DEFAULT '0',
  `SM_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`SM_STATE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `status_master`
--

DROP TABLE IF EXISTS `status_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `status_master` (
  `SM_STATUS_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `SM_STATUS_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SM_STATUS_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`SM_STATUS_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `statuswise_remarks`
--

DROP TABLE IF EXISTS `statuswise_remarks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `statuswise_remarks` (
  `SR_STATUS_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `SR_REMARK_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `SR_REMARK_DESC` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SR_REMARK_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SR_TO_STAGE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SR_TO_STATUS` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SR_DASHBOARD` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'Y',
  `SR_INOUT_TYPE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'A',
  `SR_STAGE_STATUS_REMARK` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`SR_STATUS_ID`,`SR_REMARK_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `stay_extension`
--

DROP TABLE IF EXISTS `stay_extension`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stay_extension` (
  `SE_APPLY_ID` int NOT NULL,
  `SE_CLAIM_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SE_REQUERY_ID` int DEFAULT '0',
  `SE_APPLY_DATE` datetime NOT NULL,
  `SE_EXT_ID` int NOT NULL DEFAULT '0',
  `SE_REASON` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `SE_HOSP_REMARKS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `SE_PROPOSE_DOD` date DEFAULT NULL,
  `SE_APPROVED_DOD` date DEFAULT NULL,
  `SE_GROUP_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SE_PROCESS_USER` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SE_STAGE_ID` int DEFAULT '0',
  `SE_PROCESS_STAGE` int DEFAULT '0',
  `SE_PROCESS_DATE` datetime DEFAULT NULL,
  `SE_FINAL_APP` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'N',
  `SE_REQUERY_BY` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SE_IP_ADDRESS` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SE_ACTIVE` int DEFAULT '1',
  `SE_FINAL_AUTH` int DEFAULT '0',
  PRIMARY KEY (`SE_APPLY_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `stay_extension_events`
--

DROP TABLE IF EXISTS `stay_extension_events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stay_extension_events` (
  `SEE_ID` int NOT NULL,
  `SEE_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SEE_REQUERY_ID` int NOT NULL DEFAULT '0',
  `SEE_GROUP_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `SEE_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SEE_PROP_DOD` date DEFAULT NULL,
  `SEE_APPR_DOD` date DEFAULT NULL,
  `SEE_STAGE_ID` int DEFAULT '0',
  `SEE_STATUS` int DEFAULT '0',
  `SEE_DATE` datetime NOT NULL,
  `SEE_REPLY` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `SEE_HOSP_REMARKS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `SEE_PROCESS_REMARKS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `SEE_IP_ADDRESS` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SEE_REVERT` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'N',
  PRIMARY KEY (`SEE_ID`,`SEE_REQUERY_ID`,`SEE_GROUP_ID`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `stayext_status_master`
--

DROP TABLE IF EXISTS `stayext_status_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stayext_status_master` (
  `SSM_ID` int NOT NULL,
  `SSM_STATUS` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`SSM_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sub_category`
--

DROP TABLE IF EXISTS `sub_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sub_category` (
  `sub_cat_id` int unsigned NOT NULL AUTO_INCREMENT,
  `sub_cat_desc` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `sub_cat_active` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`sub_cat_id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sub_district_master`
--

DROP TABLE IF EXISTS `sub_district_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sub_district_master` (
  `SDM_CODE` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `SDM_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SDM_DIST_CODE` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`SDM_CODE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `suppliment_claim`
--

DROP TABLE IF EXISTS `suppliment_claim`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `suppliment_claim` (
  `SC_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `SC_SUPP_ID` int NOT NULL,
  `SC_CLAIM_AMT` double NOT NULL DEFAULT '0',
  `SC_SANCTION_AMT` double NOT NULL DEFAULT '0',
  `SC_ADDEDUM_AMT` double NOT NULL DEFAULT '0',
  `SC_JUSTIFY` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `SC_STAGE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SC_STATUS` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SC_INIT_DATE` datetime NOT NULL,
  `SC_START_APP_DATE` datetime DEFAULT NULL,
  `SC_LAST_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SC_LAST_PROC_DATE` datetime DEFAULT NULL,
  `SC_LAST_RECOM_AMT` double DEFAULT '0',
  `SC_SETTLEMENT_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SC_FINAL_SETTLE_DT` date DEFAULT NULL,
  PRIMARY KEY (`SC_INTIMATION_ID`,`SC_SUPP_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `suppliment_process`
--

DROP TABLE IF EXISTS `suppliment_process`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `suppliment_process` (
  `SP_ID` int NOT NULL,
  `SP_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SP_SUPP_ID` int NOT NULL,
  `SP_GROUP_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SP_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SP_PROC_STATUS` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SP_PROC_DATE` datetime NOT NULL,
  `SP_RECOM_AMT` decimal(10,2) NOT NULL,
  `SP_PROC_REMARKS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `SP_IN_PROCESS` int NOT NULL DEFAULT '0',
  `SP_REVERT` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'N',
  PRIMARY KEY (`SP_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `suppliment_remarks`
--

DROP TABLE IF EXISTS `suppliment_remarks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `suppliment_remarks` (
  `SR_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SR_SUPP_ID` int DEFAULT '0',
  `SR_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SR_USER_REMARKS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `SR_UPDATE_DATE` datetime NOT NULL,
  `SR_INT_STAGE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SR_INT_STATUS` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SR_IP_ADDRESS` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SR_AUTO_UPDATE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `SR_CHANGE_ID` int unsigned DEFAULT NULL,
  `SR_REQUEST_ID` int unsigned NOT NULL DEFAULT '0',
  KEY `FK_claim_remarks_1` (`SR_INTIMATION_ID`) USING BTREE,
  KEY `Index_2` (`SR_UPDATE_DATE`),
  KEY `Index_3` (`SR_USER_ID`),
  KEY `idx_SR_int_stage` (`SR_INT_STAGE`),
  KEY `idx_SR_int_status` (`SR_INT_STATUS`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tariff_rates`
--

DROP TABLE IF EXISTS `tariff_rates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tariff_rates` (
  `TR_CODE` int unsigned NOT NULL AUTO_INCREMENT,
  `TR_REGION_ID` int unsigned NOT NULL,
  `TR_CAT_ID` int unsigned NOT NULL,
  `TR_RT_TYPE_ID` int unsigned NOT NULL,
  `TR_PROC_CODE` int unsigned NOT NULL,
  `TR_SUB_CAT_CODE` int unsigned NOT NULL,
  `TR_RATE` int unsigned NOT NULL,
  `TR_REMARKS` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`TR_CODE`)
) ENGINE=InnoDB AUTO_INCREMENT=62401 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tat_monitor`
--

DROP TABLE IF EXISTS `tat_monitor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tat_monitor` (
  `tm_scheme` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `tm_date` date NOT NULL,
  `tm_ip_cnt` int unsigned NOT NULL,
  `tm_ip_amt` decimal(15,2) NOT NULL,
  `tm_op_cnt` int unsigned NOT NULL,
  `tm_op_amt` decimal(15,2) NOT NULL,
  PRIMARY KEY (`tm_scheme`,`tm_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tax_rate`
--

DROP TABLE IF EXISTS `tax_rate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tax_rate` (
  `TR_RATE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `TR_PERIOD_FR` date NOT NULL,
  `TR_PERIOD_TO` date NOT NULL,
  `TR_SER_TAX` decimal(10,2) NOT NULL,
  `TR_ECESS` decimal(10,2) NOT NULL,
  `TR_HSCESS` decimal(10,2) NOT NULL,
  `TR_SBCESS` decimal(10,2) NOT NULL,
  `TR_KKCESS` decimal(10,2) NOT NULL,
  `TR_GSTTDS` decimal(10,2) NOT NULL DEFAULT '0.00',
  `TR_TAX_TYPE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`TR_RATE_ID`),
  KEY `Index_2` (`TR_TAX_TYPE`),
  KEY `Index_3` (`TR_PERIOD_FR`),
  KEY `Index_4` (`TR_PERIOD_TO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tds_challan_det`
--

DROP TABLE IF EXISTS `tds_challan_det`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tds_challan_det` (
  `TCD_TRAN_ID` int unsigned NOT NULL,
  `TCD_CGHS_CITY_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `TCD_MONTH` int unsigned DEFAULT NULL,
  `TCD_YEAR` int unsigned DEFAULT NULL,
  `TCD_FY` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `TCD_INSTR_TYPE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `TCD_INSTR_NO` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `TCD_INSTR_DT` date DEFAULT NULL,
  `TCD_INSTR_AMOUNT` decimal(15,2) DEFAULT NULL,
  `TCD_DRAWEE_BANK` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `TCD_BSR_CODE` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `TCD_DEPOSITED_DATE` date DEFAULT NULL,
  `TCD_CHALLAN_NO` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `TCD_DEDUCTEE_TYPE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `TCD_SUB_ENTITY_ID` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`TCD_TRAN_ID`),
  UNIQUE KEY `Index_2` (`TCD_CGHS_CITY_ID`,`TCD_MONTH`,`TCD_YEAR`,`TCD_DEDUCTEE_TYPE`,`TCD_SUB_ENTITY_ID`) USING BTREE,
  KEY `Idx_Instr_Type` (`TCD_INSTR_TYPE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `temp_bpa_serfee_reco`
--

DROP TABLE IF EXISTS `temp_bpa_serfee_reco`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `temp_bpa_serfee_reco` (
  `bsr_settlement_id` decimal(10,0) NOT NULL,
  `bsr_region_id` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `bsr_ser_fee` decimal(15,2) NOT NULL DEFAULT '0.00',
  `bsr_ser_fee_recvd` decimal(15,2) NOT NULL DEFAULT '0.00',
  `bsr_credit_date` datetime NOT NULL,
  `bsr_neft_ref_no` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `bsr_neft_amount` decimal(15,2) DEFAULT '0.00',
  `bsr_voucher_no` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `bsr_gst_tds` decimal(15,2) DEFAULT '0.00',
  `bsr_diff_fee` decimal(15,2) DEFAULT '0.00',
  `bsr_user_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `bsr_update_date` datetime NOT NULL,
  `bsr_ip_address` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`bsr_settlement_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `temp_claims`
--

DROP TABLE IF EXISTS `temp_claims`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `temp_claims` (
  `TC_CLAIM_ID` varchar(15) NOT NULL,
  `TC_TIER_ID` int NOT NULL,
  `TC_ACCR` varchar(1) NOT NULL,
  `TC_STAGE` varchar(3) DEFAULT NULL,
  `TC_STATUS` varchar(3) DEFAULT NULL,
  `TC_KEEP` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`TC_CLAIM_ID`,`TC_KEEP`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `temp_extra_exp`
--

DROP TABLE IF EXISTS `temp_extra_exp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `temp_extra_exp` (
  `TXP_OFFICE_ID` varchar(10) NOT NULL,
  `TXP_CLAIM_ID` varchar(15) DEFAULT NULL,
  `TXP_ID` decimal(10,0) NOT NULL DEFAULT '0',
  `TXP_SRNO` int NOT NULL DEFAULT '0',
  `TXP_PROC_ID` int NOT NULL DEFAULT '0',
  `TXP_CAT_ID` varchar(10) DEFAULT NULL,
  `TXP_HOS_RATE` decimal(15,2) DEFAULT NULL,
  `TXP_NON_ACCR_RATE` decimal(10,2) DEFAULT NULL,
  `TXP_DIFF_RATE` decimal(16,2) DEFAULT NULL,
  `TXP_DIFF_AMT` decimal(31,4) DEFAULT NULL,
  `TXP_STAGE` varchar(3) DEFAULT NULL,
  `TXP_STATUS` varchar(3) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `temp_extra_rates`
--

DROP TABLE IF EXISTS `temp_extra_rates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `temp_extra_rates` (
  `TER_CLAIM_ID` varchar(10) NOT NULL,
  `TER_OFFICE_ID` varchar(10) NOT NULL,
  `TER_ACCR` varchar(1) NOT NULL,
  `TER_DIFF_AMT` int DEFAULT NULL,
  `TER_DIFF_CNT` int DEFAULT NULL,
  `TER_TIER_ID` int DEFAULT NULL,
  `TER_STAGE` varchar(3) DEFAULT NULL,
  `TER_STATUS` varchar(3) DEFAULT NULL,
  PRIMARY KEY (`TER_CLAIM_ID`,`TER_ACCR`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `temp_sett_proc_discard`
--

DROP TABLE IF EXISTS `temp_sett_proc_discard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `temp_sett_proc_discard` (
  `SR_NO` int NOT NULL DEFAULT '0',
  `CLAIM_ID` varchar(15) NOT NULL,
  `CLAIM_AMT` int DEFAULT '0',
  `OFFICE_NAME` varchar(100) DEFAULT NULL,
  `RUNNING_AMT` int DEFAULT '0',
  PRIMARY KEY (`SR_NO`),
  UNIQUE KEY `idx_claim` (`CLAIM_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `transaction_history`
--

DROP TABLE IF EXISTS `transaction_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transaction_history` (
  `TH_TRAN_NO` int unsigned DEFAULT '0',
  `TH_TIME` datetime DEFAULT NULL,
  `TH_IS_MAIN_MENU` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'N',
  `TH_TRAN_DETAILS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `TH_ERROR_ID` decimal(10,0) DEFAULT '0',
  KEY `Index_1` (`TH_TRAN_NO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `treatment_details`
--

DROP TABLE IF EXISTS `treatment_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `treatment_details` (
  `TD_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `TD_TRTYPE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `TD_IS_TREATMENT` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `TD_TR_DETAILS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  PRIMARY KEY (`TD_INTIMATION_ID`,`TD_TRTYPE_ID`),
  KEY `FK_treatment_details_1` (`TD_TRTYPE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `treatment_type`
--

DROP TABLE IF EXISTS `treatment_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `treatment_type` (
  `TT_TRTYPE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `TT_TRTYPE_DESC` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `TT_TRTYPE_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`TT_TRTYPE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `treatment_waiver`
--

DROP TABLE IF EXISTS `treatment_waiver`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `treatment_waiver` (
  `TW_ID` int NOT NULL,
  `TW_DESC` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `TW_MAJOR` int NOT NULL DEFAULT '0',
  `TW_ACTIVE` int DEFAULT '1',
  `TW_ORDER` int DEFAULT '1',
  PRIMARY KEY (`TW_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `uid_status`
--

DROP TABLE IF EXISTS `uid_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `uid_status` (
  `US_ID` int NOT NULL,
  `US_DESC` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `US_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'Y',
  `US_DISP_ORDER` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`US_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `unlist_proc_summary`
--

DROP TABLE IF EXISTS `unlist_proc_summary`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `unlist_proc_summary` (
  `UPS_ID` int NOT NULL,
  `UPS_CLAIM_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UPS_APPLY_DATE` datetime DEFAULT NULL,
  `UPS_GROUP_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UPS_PROC_DATE` datetime DEFAULT NULL,
  `UPS_NODAL_CLINIC` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UPS_MH` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UPS_IS_TRANSFER` int DEFAULT '0',
  `UPS_APPX_HOSP` int DEFAULT '0',
  `UPS_APPX_NODAL` int DEFAULT '0',
  `UPS_APPX_MH` int DEFAULT '0',
  PRIMARY KEY (`UPS_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `unlisted_procedure`
--

DROP TABLE IF EXISTS `unlisted_procedure`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `unlisted_procedure` (
  `UP_APPLY_ID` int NOT NULL,
  `UP_CLAIM_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UP_ID` int DEFAULT NULL,
  `UP_APPLY_DATE` datetime NOT NULL,
  `UP_PROCEDURE` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UP_REASON` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `UP_UNITS` int NOT NULL DEFAULT '0',
  `UP_SANC_UNITS` int NOT NULL DEFAULT '0',
  `UP_ESTIMATE_COST` double NOT NULL DEFAULT '0',
  `UP_SANC_COST` double NOT NULL DEFAULT '0',
  `UP_TOTAL_COST` double NOT NULL DEFAULT '0',
  `UP_SANC_TOTAL` double NOT NULL DEFAULT '0',
  `UP_REQUERY_ID` int DEFAULT '0',
  `UP_GROUP_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UP_PROCESS_USER` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UP_PROCESS_STAGE` int DEFAULT '0',
  `UP_PROCESS_DATE` datetime DEFAULT NULL,
  `UP_RATE_SRNO` int DEFAULT '0',
  `UP_EXP_SRNO` int DEFAULT '0',
  `UP_IP_ADDRESS` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`UP_APPLY_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `unlisted_process_events`
--

DROP TABLE IF EXISTS `unlisted_process_events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `unlisted_process_events` (
  `UPE_APPLY_ID` int NOT NULL DEFAULT '0',
  `UPE_INTIMATION_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UPE_ID` int DEFAULT NULL,
  `UPE_REQUERY_ID` int NOT NULL DEFAULT '0',
  `UPE_GROUP_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `UPE_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UPE_STATUS` int DEFAULT '0',
  `UPE_DATE` datetime NOT NULL,
  `UPE_REPLY` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `UPE_REPLY_COST` double DEFAULT '0',
  `UPE_REPLY_UNIT` int DEFAULT '0',
  `UPE_REPLY_AMOUNT` double DEFAULT '0',
  `UPE_PROCESS_REMARKS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `UPE_IP_ADDRESS` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UPE_REVERT` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'N',
  PRIMARY KEY (`UPE_APPLY_ID`,`UPE_REQUERY_ID`,`UPE_GROUP_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ur_user_rights`
--

DROP TABLE IF EXISTS `ur_user_rights`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ur_user_rights` (
  `UR_USER_TYPE` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `UR_LEVEL_1` int NOT NULL,
  `UR_LEVEL_2` int NOT NULL,
  `UR_LEVEL_3` int NOT NULL,
  `UR_LEVEL_4` int NOT NULL,
  `UR_GRP_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `UR_RESTRICTED_USER` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UR_NOTVALID_USER` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UR_PILOT_REGION` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UR_PILOT_OFFICE` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`UR_USER_TYPE`,`UR_GRP_ID`,`UR_LEVEL_1`,`UR_LEVEL_2`,`UR_LEVEL_3`,`UR_LEVEL_4`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_allot_archiwe`
--

DROP TABLE IF EXISTS `user_allot_archiwe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_allot_archiwe` (
  `UAA_TRACKING_ID` bigint unsigned NOT NULL,
  `UAA_USER` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UAA_DATE` datetime NOT NULL,
  `UAA_USER_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UAA_PATIENT_TYPE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UAA_FROM_AMT` decimal(10,0) unsigned DEFAULT '0',
  `UAA_TO_AMT` decimal(10,0) unsigned DEFAULT '0',
  `UAA_CLAIM_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UAA_CLAIM_AMT` decimal(10,0) NOT NULL,
  `UAA_CURRENT_STAGE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UAA_CURRENT_STATUS` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UAA_ACCEPT_DATE` datetime NOT NULL,
  `UAA_PROCESS_STAGE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UAA_PROCESS_STATUS` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UAA_START_TIME` datetime DEFAULT NULL,
  `UAA_END_TIME` datetime DEFAULT NULL,
  `UAA_ACTION_MODE` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UAA_ACTION_DATE` date DEFAULT NULL,
  `UAA_NEW_ALLOTEE` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UAA_ACTION_BY` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UAA_CATG_ID` int NOT NULL DEFAULT '0',
  `UAA_RANGE_ID` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`UAA_TRACKING_ID`),
  KEY `Idx_Claim_Id` (`UAA_CLAIM_ID`),
  KEY `Idx_User` (`UAA_USER`),
  KEY `Idx_Date` (`UAA_DATE`),
  KEY `Idx_Action` (`UAA_ACTION_DATE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_allot_setup`
--

DROP TABLE IF EXISTS `user_allot_setup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_allot_setup` (
  `UAS_USER_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `UAS_IP_CASE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'N',
  `UAS_OPD_CASE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'N',
  `UAS_FROM_DATE` date DEFAULT NULL,
  `UAS_TO_DATE` date DEFAULT NULL,
  `UAS_IPD_RANGE` int NOT NULL DEFAULT '0',
  `UAS_OPD_RANGE` int NOT NULL DEFAULT '0',
  `UAS_TIME_START` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UAS_TIME_END` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UAS_PER_DAY_ALLOCATE` int unsigned DEFAULT '0',
  `UAS_MAC_ADDR` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UAS_UPDATE_ON` datetime DEFAULT NULL,
  `UAS_UPDATE_BY` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`UAS_USER_ID`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_allot_tracking`
--

DROP TABLE IF EXISTS `user_allot_tracking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_allot_tracking` (
  `UAT_TRACKING_ID` bigint unsigned DEFAULT NULL,
  `UAT_USER` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UAT_DATE` datetime NOT NULL,
  `UAT_PATIENT_TYPE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UAT_FROM_AMT` decimal(10,0) unsigned DEFAULT '0',
  `UAT_TO_AMT` decimal(10,0) unsigned DEFAULT '0',
  `UAT_CLAIM_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `UAT_CLAIM_AMT` decimal(10,0) DEFAULT '0',
  `UAT_CURRENT_STAGE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UAT_CURRENT_STATUS` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UAT_ACCEPT_DATE` datetime NOT NULL,
  `UAT_PROC_STATUS` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'P',
  `UAT_START_TIME` datetime DEFAULT NULL,
  `UAT_END_TIME` datetime DEFAULT NULL,
  `UAT_TRANSFER_ON` datetime DEFAULT NULL,
  `UAT_TRANSFER_BY` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UAT_RANGE_ID` int NOT NULL DEFAULT '0',
  `UAT_CATG_ID` int NOT NULL DEFAULT '0',
  `UAT_PRIORITY` int unsigned NOT NULL DEFAULT '99',
  `UAT_PROC_MODE` int DEFAULT '1',
  PRIMARY KEY (`UAT_CLAIM_ID`),
  KEY `Idx_UAT_User` (`UAT_USER`),
  KEY `Idx_UAT_Proc_Status` (`UAT_PROC_STATUS`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_allot_weekly_off`
--

DROP TABLE IF EXISTS `user_allot_weekly_off`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_allot_weekly_off` (
  `UAW_SETUP_ID` int unsigned NOT NULL DEFAULT '0',
  `UAW_MON` int DEFAULT '-1',
  `UAW_TUE` int DEFAULT '-1',
  `UAW_WED` int DEFAULT '-1',
  `UAW_THUS` int DEFAULT '-1',
  `UAW_FRI` int DEFAULT '-1',
  `UAW_SAT` int DEFAULT '-1',
  `UAW_SUN` int DEFAULT '-1',
  PRIMARY KEY (`UAW_SETUP_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_details`
--

DROP TABLE IF EXISTS `user_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_details` (
  `UD_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `UD_ID` int NOT NULL DEFAULT '0',
  `UD_GROUP_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UD_ENTITY_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UD_PWD` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'Y',
  `UD_LOGIN_STATUS` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UD_USER_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UD_EMAIL_ID` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UD_PHONE_NO` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UD_LOGIN_DATE` datetime DEFAULT NULL,
  `UD_LAST_TRAN_ID` bigint unsigned DEFAULT '0',
  `UD_LOGIN_ATTEMPT` int DEFAULT NULL,
  `UD_PWD_CHANGE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UD_USER_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'Y',
  `UD_OFFICE_ID` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UD_CERTIFICATE_SERIAL` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UD_ISSUER_ID` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UD_UNIQUE_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UD_PASSWORD_EXPIRY` date DEFAULT NULL,
  `UD_CREATE_DATE` datetime NOT NULL,
  `UD_CLOSED_DATE` datetime DEFAULT NULL,
  `UD_SEC_QUE_ID` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '0',
  `UD_SEC_QUE_ANS` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UD_EMAIL_ID_VER` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'N',
  `UD_EMAIL_VER_TRAN` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UD_EMAIL_VER_CODE` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UD_REG_IP_ADDRESS` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UD_USER_DESIG` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UD_USER_RANK` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UD_MAC_ADDRESS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `UD_MAC_ADDRESS_2` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `UD_MAC_MAPPING` int unsigned DEFAULT '0',
  `UD_LOGIN_AFTER` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UD_LOGOUT_BEFORE` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UD_PRE_ALLOTED` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'N',
  `UD_ALREADY_LOGIN` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'N',
  `UD_LOGIN_VERIFY` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'N',
  `UD_SECRET_CODE` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UD_BPA_CENTRE_ID` int NOT NULL DEFAULT '0',
  `UD_CERT_FILE` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UD_USR_RL` int unsigned DEFAULT NULL,
  `UD_USR_TL` int unsigned DEFAULT NULL,
  `UD_USR_PL` int unsigned DEFAULT NULL,
  `UD_EMP_TYPE` int DEFAULT '0',
  `UD_EMP_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`UD_USER_ID`),
  KEY `FK_user_details_1` (`UD_GROUP_ID`),
  KEY `FK_user_details_2` (`UD_ENTITY_ID`),
  KEY `FK_user_details_3` (`UD_OFFICE_ID`),
  CONSTRAINT `FK_ENTITY_ID` FOREIGN KEY (`UD_ENTITY_ID`) REFERENCES `user_entity` (`UE_ENTITY_ID`),
  CONSTRAINT `FK_GROUP_ID` FOREIGN KEY (`UD_GROUP_ID`) REFERENCES `user_group` (`UG_GROUP_ID`),
  CONSTRAINT `FK_OFFICE_ID` FOREIGN KEY (`UD_OFFICE_ID`) REFERENCES `office_master` (`OM_OFFICE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_entity`
--

DROP TABLE IF EXISTS `user_entity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_entity` (
  `UE_ENTITY_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `UE_ENTITY_DESC` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UE_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`UE_ENTITY_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_group`
--

DROP TABLE IF EXISTS `user_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_group` (
  `UG_GROUP_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `UG_GROUP_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UG_SHORT_CODE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UG_GROUP_ENTITY_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UG_GROUP_LEVEL` int NOT NULL,
  `UG_GROUP_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UG_AMT_LOWER_LIMIT` decimal(15,2) NOT NULL,
  `UG_AMT_UPPER_LIMIT` decimal(15,2) NOT NULL,
  `UG_INT_STAGE_CODE` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UG_REGION_MODE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'N',
  `UG_SESSION_LIMIT` int unsigned NOT NULL DEFAULT '30',
  `UG_MULTIPLE_LOGIN` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'N',
  PRIMARY KEY (`UG_GROUP_ID`),
  KEY `FK_user_group_1` (`UG_GROUP_ENTITY_ID`),
  KEY `Idx_Region_Mode` (`UG_REGION_MODE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_group_queue`
--

DROP TABLE IF EXISTS `user_group_queue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_group_queue` (
  `UGQ_GROUP_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `UGQ_INT_STAGE` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `UGQ_INT_STATUS` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `UGQ_PENDING_AT` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`UGQ_GROUP_ID`,`UGQ_INT_STAGE`,`UGQ_INT_STATUS`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_history`
--

DROP TABLE IF EXISTS `user_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_history` (
  `UH_ID` int NOT NULL AUTO_INCREMENT,
  `UH_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UH_MODE` int DEFAULT '0',
  `UH_DONE_BY` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UH_DATE` datetime NOT NULL,
  `UH_PREV_VALUE` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UH_IP_ADDRESS` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UH_UPD_REF` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  PRIMARY KEY (`UH_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=212514 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_over_time`
--

DROP TABLE IF EXISTS `user_over_time`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_over_time` (
  `UOT_ID` int NOT NULL AUTO_INCREMENT,
  `UOT_USER` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UOT_DATE` datetime NOT NULL,
  `UOT_RANGE_ID` int NOT NULL DEFAULT '0',
  `UOT_CLAIM_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UOT_CLAIM_AMT` decimal(10,0) DEFAULT '0',
  `UOT_STAGE` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UOT_STATUS` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UOT_START_TIME` datetime DEFAULT NULL,
  `UOT_END_TIME` datetime DEFAULT NULL,
  PRIMARY KEY (`UOT_ID`),
  KEY `Idx_UOT_CLAIM` (`UOT_CLAIM_ID`),
  KEY `Idx_UOT_User` (`UOT_USER`),
  KEY `Idx_End_Time` (`UOT_END_TIME`)
) ENGINE=InnoDB AUTO_INCREMENT=4265537 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_password_history`
--

DROP TABLE IF EXISTS `user_password_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_password_history` (
  `uph_user_id` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `uph_password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `uph_change_on` datetime NOT NULL,
  `uph_updated_by` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `uph_update_IP` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  KEY `Idx_User_Id` (`uph_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_profile_parameter`
--

DROP TABLE IF EXISTS `user_profile_parameter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_profile_parameter` (
  `UPP_ID` int NOT NULL AUTO_INCREMENT,
  `UPP_VALUE` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `UPP_STORE_PREV` int DEFAULT '0',
  PRIMARY KEY (`UPP_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_security_question`
--

DROP TABLE IF EXISTS `user_security_question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_security_question` (
  `USQ_QUE_ID` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `USQ_QUESTION` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `USQ_QUE_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`USQ_QUE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_sequence`
--

DROP TABLE IF EXISTS `user_sequence`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_sequence` (
  `ID` bigint NOT NULL DEFAULT '0',
  `MIN_VALUE` int NOT NULL DEFAULT '0',
  `MAX_VALUE` bigint NOT NULL DEFAULT '0',
  `RESET_ON_MAX` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'N',
  `RESET_FREQUENCY` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'N',
  `LAST_ACCESS_ON` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `verifier_remarks`
--

DROP TABLE IF EXISTS `verifier_remarks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `verifier_remarks` (
  `VR_REM_TYPE_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `VR_REM_DESC` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `VR_REM_ACTIVE` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`VR_REM_TYPE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `waiver_appr_process`
--

DROP TABLE IF EXISTS `waiver_appr_process`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `waiver_appr_process` (
  `WAP_ID` int NOT NULL,
  `WAP_CRITERIA_ID` int NOT NULL,
  `WAP_GROUP_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `WAP_STATUS_ID` int DEFAULT '0',
  `WAP_NEXT_GROUP_ID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `WAP_IS_FINAL` int DEFAULT '0',
  `WAP_ACCEPT` int DEFAULT '0',
  `WAP_ORDER_ID` int DEFAULT '0',
  `WAP_REPLY_NMI` int DEFAULT '0',
  `WAP_APPLY_STAGE` int DEFAULT '0',
  `WAP_NMI` int DEFAULT '0',
  `WAP_REPLY_REJECT` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`WAP_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `waiver_criteria`
--

DROP TABLE IF EXISTS `waiver_criteria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `waiver_criteria` (
  `WC_ID` int NOT NULL AUTO_INCREMENT,
  `WC_TYPE_ID` int DEFAULT '0',
  `WC_START_DATE` date NOT NULL,
  `WC_END_DATE` date DEFAULT NULL,
  `WC_FROM` int NOT NULL,
  `WC_TO` int NOT NULL,
  `WC_UNIT` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'D',
  `WC_DISCHARED` int DEFAULT '1',
  `WC_WO_REFERRAL` int DEFAULT '0',
  `WC_CLAIM_SUBMIT` int DEFAULT '0',
  `WC_WAIVER_REQD` int DEFAULT '0',
  `WC_NOT_ALLOW` int DEFAULT '0',
  `WC_REASON` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `WC_IP` int NOT NULL DEFAULT '1',
  `WC_OP` int NOT NULL DEFAULT '1',
  `WC_PH` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`WC_ID`),
  UNIQUE KEY `UNIQ_KEY` (`WC_START_DATE`,`WC_END_DATE`,`WC_DISCHARED`,`WC_CLAIM_SUBMIT`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `waiver_status_master`
--

DROP TABLE IF EXISTS `waiver_status_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `waiver_status_master` (
  `WSM_ID` int NOT NULL,
  `WSM_STATUS` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `WSM_ACTIVE` int DEFAULT '1',
  PRIMARY KEY (`WSM_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `waiver_types`
--

DROP TABLE IF EXISTS `waiver_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `waiver_types` (
  `WT_ID` int NOT NULL,
  `WT_NAME` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `WT_PRIORITY` int NOT NULL DEFAULT '3',
  `WT_ACTIVE` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`WT_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `web_direct_access`
--

DROP TABLE IF EXISTS `web_direct_access`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `web_direct_access` (
  `WDA_ID` int NOT NULL AUTO_INCREMENT,
  `WDA_USER_ID` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `WDA_MAC_ADDRESS` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `WDA_CHECK_IN` datetime DEFAULT NULL,
  PRIMARY KEY (`WDA_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=32339 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `web_referral`
--

DROP TABLE IF EXISTS `web_referral`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `web_referral` (
  `WR_REFERENCE_NO` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `WR_CLAIM_ID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `WR_HOSPITAL_ID` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `WR_POLYCLINIC_ID` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `WR_DATE` datetime NOT NULL,
  `WR_USER_ID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `WR_IP_ADDRESS` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`WR_REFERENCE_NO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping routines for database 'ECHS'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-06-02 17:04:31
