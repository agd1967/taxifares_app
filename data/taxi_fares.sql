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
-- Table structure for table `fares`
--

DROP TABLE IF EXISTS `fares`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fares` (
  `fare_id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` varchar(45) NOT NULL,
  `passenger_name` varchar(45) NOT NULL,
  `phone_no` varchar(45) DEFAULT NULL,
  `pickup_address` varchar(45) NOT NULL,
  `pickup_datetime` datetime NOT NULL,
  `dropoff_address` varchar(45) DEFAULT NULL,
  `dropoff_datetime` datetime DEFAULT NULL,
  `status` varchar(1) DEFAULT NULL,
  `date_created` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `last_updated` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`fare_id`),
  UNIQUE KEY `fare_id_UNIQUE` (`fare_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fares`
--

LOCK TABLES `fares` WRITE;
/*!40000 ALTER TABLE `fares` DISABLE KEYS */;
INSERT INTO `fares` VALUES (1,'3','Andrew McCutchen','613-789-2121','888 Rideu St. Ottawa, ON','2017-05-23 17:23:00','Canadian Tire Centre',NULL,'D','2017-05-24 21:45:32','2017-05-24 23:20:55'),(2,'3','Andrew McCutchen','613-789-2121','888 Rideu St. Ottawa, ON','2017-05-24 18:35:00','None',NULL,'D','2017-05-24 22:36:04','2017-05-24 22:36:04'),(3,'1','Roger Clements','613-2655587','5-999 Riverside Dr.','2017-05-24 18:36:00','K1Z89F',NULL,'D','2017-05-24 22:36:36','2017-05-24 22:36:36'),(4,'3','Andrew McCutchen','613-789-2121','888 Rideu St. Ottawa, ON','2017-05-24 19:41:00','None',NULL,'D','2017-05-24 23:41:53','2017-05-24 23:41:53'),(5,'3','Andrew McCutchen','613-789-2121','Canadian Tire Centre','2017-05-24 21:01:00','None',NULL,'D','2017-05-25 01:02:08','2017-05-25 01:02:08'),(6,'3','Andrew McCutchen','613-789-2121','888 Rideu St. Ottawa, ON','2017-05-27 21:12:00','None',NULL,'D','2017-05-25 01:12:44','2017-05-25 01:12:44'),(7,'3','Andrew McCutchen','613-789-2121','888 Rideu St. Ottawa, ON','2017-05-24 09:13:00','None',NULL,'D','2017-05-25 01:13:45','2017-05-25 01:13:45'),(8,'3','Andrew McCutchen','613-789-2121','888 Rideu St. Ottawa, ON','2017-05-24 18:14:00','None',NULL,'D','2017-05-25 01:14:32','2017-05-25 01:14:32'),(9,'3','Andrew McCutchen','613-789-2121','888 Rideu St. Ottawa, ON','2017-05-24 23:14:00','None',NULL,'D','2017-05-25 01:15:06','2017-05-25 01:15:06');
/*!40000 ALTER TABLE `fares` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-05-25 10:07:15
