CREATE DATABASE  IF NOT EXISTS `taxi` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `taxi`;
-- MySQL dump 10.13  Distrib 5.7.9, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: taxi
-- ------------------------------------------------------
-- Server version	5.7.13-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `client`
--

DROP TABLE IF EXISTS `client`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `client` (
  `client_id` int(11) NOT NULL AUTO_INCREMENT,
  `account_no` varchar(45) NOT NULL,
  `first_name` varchar(45) NOT NULL,
  `last_name` varchar(45) NOT NULL,
  `phone_no` varchar(45) NOT NULL,
  `home_address` varchar(85) DEFAULT NULL,
  `home_zipcode` varchar(6) DEFAULT NULL,
  `pickup_address` varchar(85) DEFAULT NULL,
  `pickup_zipcode` varchar(6) DEFAULT NULL,
  `dropoff_address` varchar(85) DEFAULT NULL,
  `dropoff_zipcode` varchar(6) DEFAULT NULL,
  `payment_type` varchar(45) DEFAULT NULL,
  `payment_card` varchar(45) DEFAULT NULL,
  `payment_exp` datetime DEFAULT NULL,
  `raiting` varchar(45) DEFAULT NULL,
  `status` varchar(1) DEFAULT NULL,
  `last_update` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`client_id`),
  UNIQUE KEY `client_id_UNIQUE` (`client_id`),
  UNIQUE KEY `account_no_UNIQUE` (`account_no`),
  KEY `first_name_index` (`first_name`),
  KEY `last_name_index` (`last_name`),
  KEY `pnone_index` (`phone_no`),
  KEY `status` (`status`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `client`
--

LOCK TABLES `client` WRITE;
/*!40000 ALTER TABLE `client` DISABLE KEYS */;
INSERT INTO `client` VALUES (1,'1-001','Roger','Clements','613-2655587','5-999 Riverside Dr.','K1Z89F','5-999 Riverside Dr.','K1Z89F',NULL,NULL,NULL,NULL,NULL,NULL,'A','2017-05-24 00:39:38'),(2,'1-202','Barry','Bonds','613-5587878','555 Elgin St','K1R46T','555 Elgin St','K1R46T',NULL,NULL,NULL,NULL,NULL,NULL,'A','2017-05-24 00:39:38'),(3,'1-444','Andrew','McCutchen','613-789-2121',NULL,NULL,'888 Rideu St. Ottawa, ON',NULL,'Canadian Tire Centre',NULL,NULL,NULL,NULL,NULL,'A','2017-05-24 21:45:31');
/*!40000 ALTER TABLE `client` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-05-25 10:07:18
