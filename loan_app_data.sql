-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: loan_app
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `data`
--

DROP TABLE IF EXISTS `data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `data` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `marital_status` varchar(20) DEFAULT NULL,
  `dependents` int DEFAULT NULL,
  `education` varchar(50) DEFAULT NULL,
  `employment_status` varchar(50) DEFAULT NULL,
  `residential_status` varchar(50) DEFAULT NULL,
  `annual_income` decimal(15,2) DEFAULT NULL,
  `monthly_income` decimal(15,2) DEFAULT NULL,
  `credit_score` int DEFAULT NULL,
  `existing_loans` int DEFAULT NULL,
  `total_existing_loan_amount` decimal(15,2) DEFAULT NULL,
  `loan_amount_requested` decimal(15,2) DEFAULT NULL,
  `loan_term` int DEFAULT NULL,
  `loan_purpose` varchar(100) DEFAULT NULL,
  `bank_account_history` int DEFAULT NULL,
  `eligibility` varchar(20) DEFAULT NULL,
  `confidence` float DEFAULT NULL,
  `suggested_amount` decimal(15,2) DEFAULT NULL,
  `final_eligibility` varchar(20) DEFAULT NULL,
  `final_confidence` float DEFAULT NULL,
  `approved_amount` decimal(15,2) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=88 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data`
--

LOCK TABLES `data` WRITE;
/*!40000 ALTER TABLE `data` DISABLE KEYS */;
INSERT INTO `data` VALUES (65,'Ramosh','Male',25,'Married',1,'Graduate','Employed','Family',600000.00,70000.00,720,0,0.00,500000.00,48,'Small Business Start-up',1,'Eligible',0.737319,NULL,'Eligible',0.737319,500000.00,'2025-08-29 19:12:05'),(66,'Ramosh','Male',25,'Married',1,'Graduate','Employed','Family',600000.00,70000.00,720,0,0.00,500000.00,48,'Small Business Start-up',1,'Eligible',0.737319,NULL,'Eligible',0.737319,500000.00,'2025-08-29 19:12:21'),(67,'Ramosh','Male',25,'Single',1,'Graduate','Employed','Own',335000.00,25000.00,350,0,0.00,600000.00,48,'Small Business Start-up',1,'Not Eligible',0.138452,299000.00,'Not Eligible',0.114424,NULL,'2025-08-29 19:13:53'),(68,'Ramosh','Male',25,'Single',1,'Graduate','Employed','Own',335000.00,25000.00,350,0,0.00,300000.00,48,'Small Business Start-up',1,'Eligible',0.114424,299000.00,'Eligible',0.114424,300000.00,'2025-08-29 19:14:14'),(69,'Ramosh','Male',25,'Single',1,'Graduate','Employed','Own',335000.00,25000.00,350,0,0.00,270000.00,48,'Small Business Start-up',1,'Eligible',0.117207,270000.00,'Eligible',0.117207,270000.00,'2025-08-29 19:14:32'),(70,'Ramosh','Male',25,'Single',1,'Graduate','Employed','Own',335000.00,25000.00,350,0,0.00,400000.00,48,'Small Business Start-up',1,'Not Eligible',0.124032,299000.00,'Not Eligible',0.114424,NULL,'2025-08-29 19:14:41'),(71,'Ramosh','Male',20,'Single',0,'Graduate','Employed','Own',700000.00,80000.00,700,0,0.00,500000.00,36,'Small Business Start-up',0,'Eligible',0.900293,NULL,'Eligible',0.900293,500000.00,'2025-08-31 18:56:54'),(72,'Ramosh','Male',20,'Single',0,'Graduate','Employed','Own',350000.00,25000.00,350,0,0.00,600000.00,12,'Small Business Start-up',0,'Not Eligible',0.171564,263000.00,'Not Eligible',0.163884,NULL,'2025-08-31 19:01:04'),(73,'Ramosh Samarawickrama','Male',20,'Single',1,'Graduate','Employed','Own',700000.00,80000.00,700,0,0.00,500000.00,36,'Small Business Start-up',1,'Eligible',0.860576,NULL,'Eligible',0.860576,500000.00,'2025-08-31 20:03:42'),(74,'Ramosh Samarawickrama','Male',20,'Single',1,'Graduate','Employed','Own',350000.00,25000.00,320,0,0.00,600000.00,36,'Small Business Start-up',1,'Not Eligible',0.201942,302000.00,'Not Eligible',0.219696,NULL,'2025-08-31 20:05:59'),(75,'Ramosh','Male',20,'Single',2,'Graduate','Employed','Own',600000.00,65000.00,750,0,0.00,600000.00,36,'Small Business Start-up',0,'Eligible',0.847858,NULL,'Eligible',0.847858,600000.00,'2025-09-03 16:38:53'),(76,'Ramosh','Male',20,'Single',2,'Graduate','Employed','Own',300000.00,25000.00,320,0,0.00,600000.00,36,'Small Business Start-up',0,'Not Eligible',0.301668,269000.00,'Not Eligible',0.252409,NULL,'2025-09-03 16:39:15'),(77,'Ramosh','Male',20,'Single',2,'Graduate','Employed','Own',300000.00,25000.00,320,0,0.00,250000.00,36,'Small Business Start-up',0,'Eligible',0.223147,250000.00,'Eligible',0.223147,250000.00,'2025-09-03 16:39:32'),(78,'Ramosh','Male',20,'Single',2,'Graduate','Employed','Own',300000.00,25000.00,320,0,0.00,200000.00,36,'Small Business Start-up',0,'Eligible',0.263431,200000.00,'Eligible',0.263431,200000.00,'2025-09-03 16:39:43'),(79,'Ramosh','Male',20,'Single',2,'Graduate','Employed','Own',300000.00,25000.00,320,0,0.00,600000.00,36,'Small Business Start-up',0,'Not Eligible',0.301668,269000.00,'Not Eligible',0.252409,NULL,'2025-09-03 16:41:15'),(80,'Ramosh','Male',20,'Single',0,'Graduate','Employed','Own',500000.00,25000.00,350,0,0.00,600000.00,12,'Small Business Start-up',0,'Not Eligible',0.170353,298000.00,'Not Eligible',0.149924,NULL,'2025-09-03 16:42:22'),(81,'Ramosh','Male',20,'Single',0,'Graduate','Employed','Own',100000.00,10000.00,300,0,0.00,600000.00,12,'Small Business Start-up',0,'Not Eligible',0.0780718,167000.00,'Not Eligible',0.052535,NULL,'2025-09-03 16:44:44'),(82,'Ramosh','Male',20,'Single',0,'Graduate','Employed','Own',100000.00,10000.00,300,0,0.00,600000.00,12,'Small Business Start-up',0,'Not Eligible',0.0780718,167000.00,'Not Eligible',0.052535,NULL,'2025-09-03 16:50:53'),(83,'Ramosh','Male',20,'Single',0,'Graduate','Employed','Own',100000.00,10000.00,300,0,0.00,100000.00,12,'Small Business Start-up',0,'Eligible',0.100415,100000.00,'Eligible',0.100415,100000.00,'2025-09-03 17:20:09'),(84,'Ramosh','Male',20,'Single',0,'Graduate','Employed','Own',350000.00,25000.00,350,0,0.00,600000.00,12,'Small Business Start-up',0,'Not Eligible',0.171564,263000.00,'Not Eligible',0.163884,NULL,'2025-09-03 17:20:35'),(85,'Ramosh','Male',20,'Single',0,'Graduate','Employed','Own',100000.00,10000.00,300,0,0.00,150000.00,12,'Small Business Start-up',0,'Eligible',0.0991807,150000.00,'Eligible',0.0991807,150000.00,'2025-09-03 17:23:24'),(86,'Ramosh','Male',20,'Single',0,'Graduate','Employed','Own',100000.00,10000.00,300,0,0.00,500000.00,12,'Small Business Start-up',0,'Not Eligible',0.0703773,167000.00,'Not Eligible',0.052535,NULL,'2025-09-03 17:23:36'),(87,'Ramosh','Male',20,'Single',0,'Graduate','Employed','Own',100000.00,10000.00,300,0,0.00,165000.00,12,'Small Business Start-up',0,'Eligible',0.052535,165000.00,'Eligible',0.052535,165000.00,'2025-09-03 17:23:52');
/*!40000 ALTER TABLE `data` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-09-07  0:40:57
