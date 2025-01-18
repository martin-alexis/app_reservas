CREATE DATABASE  IF NOT EXISTS `booking_app` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `booking_app`;
-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: localhost    Database: booking_app
-- ------------------------------------------------------
-- Server version	8.0.39

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
-- Table structure for table `booking_statuses`
--

DROP TABLE IF EXISTS `booking_statuses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `booking_statuses` (
  `id_booking_statuses` int NOT NULL AUTO_INCREMENT,
  `status` varchar(45) NOT NULL,
  PRIMARY KEY (`id_booking_statuses`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `booking_statuses`
--

LOCK TABLES `booking_statuses` WRITE;
/*!40000 ALTER TABLE `booking_statuses` DISABLE KEYS */;
/*!40000 ALTER TABLE `booking_statuses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bookings`
--

DROP TABLE IF EXISTS `bookings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bookings` (
  `id_bookings` int NOT NULL AUTO_INCREMENT,
  `booking_creation_date` datetime NOT NULL,
  `booking_start_date` datetime NOT NULL,
  `booking_end_date` datetime NOT NULL,
  `total_amount` decimal(10,0) NOT NULL,
  `services_id` int NOT NULL,
  `users_id` int NOT NULL,
  `booking_statuses_id` int NOT NULL,
  PRIMARY KEY (`id_bookings`),
  KEY `fk_BOOKINGS_SERVICES1_idx` (`services_id`),
  KEY `fk_BOOKINGS_USERS1_idx` (`users_id`),
  KEY `fk_BOOKINGS_BOOKING_STATUSES1_idx` (`booking_statuses_id`),
  CONSTRAINT `fk_BOOKINGS_BOOKING_STATUSES1` FOREIGN KEY (`booking_statuses_id`) REFERENCES `booking_statuses` (`id_booking_statuses`),
  CONSTRAINT `fk_BOOKINGS_SERVICES1` FOREIGN KEY (`services_id`) REFERENCES `services` (`id_services`),
  CONSTRAINT `fk_BOOKINGS_USERS1` FOREIGN KEY (`users_id`) REFERENCES `users` (`id_users`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookings`
--

LOCK TABLES `bookings` WRITE;
/*!40000 ALTER TABLE `bookings` DISABLE KEYS */;
/*!40000 ALTER TABLE `bookings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment_statuses`
--

DROP TABLE IF EXISTS `payment_statuses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment_statuses` (
  `id_payment_statuses` int NOT NULL AUTO_INCREMENT,
  `status` varchar(45) NOT NULL,
  PRIMARY KEY (`id_payment_statuses`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_statuses`
--

LOCK TABLES `payment_statuses` WRITE;
/*!40000 ALTER TABLE `payment_statuses` DISABLE KEYS */;
/*!40000 ALTER TABLE `payment_statuses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments`
--

DROP TABLE IF EXISTS `payments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payments` (
  `id_payments` int NOT NULL,
  `payment_date` datetime NOT NULL,
  `amount` decimal(10,0) NOT NULL,
  `bookings_id` int NOT NULL,
  `payment_statuses_id` int NOT NULL,
  PRIMARY KEY (`id_payments`),
  KEY `fk_PAYMENTS_BOOKINGS1_idx` (`bookings_id`),
  KEY `fk_PAYMENTS_PAYMENT_STATUSES1_idx` (`payment_statuses_id`),
  CONSTRAINT `fk_PAYMENTS_BOOKINGS1` FOREIGN KEY (`bookings_id`) REFERENCES `bookings` (`id_bookings`),
  CONSTRAINT `fk_PAYMENTS_PAYMENT_STATUSES1` FOREIGN KEY (`payment_statuses_id`) REFERENCES `payment_statuses` (`id_payment_statuses`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments`
--

LOCK TABLES `payments` WRITE;
/*!40000 ALTER TABLE `payments` DISABLE KEYS */;
/*!40000 ALTER TABLE `payments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ratings`
--

DROP TABLE IF EXISTS `ratings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ratings` (
  `id_ratings` int NOT NULL,
  `score` int NOT NULL,
  `comment` varchar(45) NOT NULL,
  `creation_date` datetime NOT NULL,
  `services_id` int NOT NULL,
  `users_id` int NOT NULL,
  PRIMARY KEY (`id_ratings`),
  KEY `fk_RATINGS_SERVICES1_idx` (`services_id`),
  KEY `fk_RATINGS_USERS1_idx` (`users_id`),
  CONSTRAINT `fk_RATINGS_SERVICES1` FOREIGN KEY (`services_id`) REFERENCES `services` (`id_services`),
  CONSTRAINT `fk_RATINGS_USERS1` FOREIGN KEY (`users_id`) REFERENCES `users` (`id_users`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ratings`
--

LOCK TABLES `ratings` WRITE;
/*!40000 ALTER TABLE `ratings` DISABLE KEYS */;
/*!40000 ALTER TABLE `ratings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id_roles` int NOT NULL AUTO_INCREMENT,
  `type` varchar(45) NOT NULL,
  PRIMARY KEY (`id_roles`),
  UNIQUE KEY `type_UNIQUE` (`type`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (4,'ADMIN'),(5,'CLIENTE'),(6,'PROVEEDOR');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `service_availability`
--

DROP TABLE IF EXISTS `service_availability`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `service_availability` (
  `id_service_availability` int NOT NULL AUTO_INCREMENT,
  `status` varchar(45) NOT NULL,
  PRIMARY KEY (`id_service_availability`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `service_availability`
--

LOCK TABLES `service_availability` WRITE;
/*!40000 ALTER TABLE `service_availability` DISABLE KEYS */;
INSERT INTO `service_availability` VALUES (1,'DISPONIBLE'),(2,'AGOTADO'),(3,'PROXIMAMENTE');
/*!40000 ALTER TABLE `service_availability` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `service_types`
--

DROP TABLE IF EXISTS `service_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `service_types` (
  `id_service_types` int NOT NULL AUTO_INCREMENT,
  `type` varchar(45) NOT NULL,
  PRIMARY KEY (`id_service_types`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `service_types`
--

LOCK TABLES `service_types` WRITE;
/*!40000 ALTER TABLE `service_types` DISABLE KEYS */;
INSERT INTO `service_types` VALUES (4,'INDUMENTARIA'),(5,'VEHICULOS'),(6,'ALOJAMIENTO');
/*!40000 ALTER TABLE `service_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `services`
--

DROP TABLE IF EXISTS `services`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `services` (
  `id_services` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `description` varchar(255) NOT NULL,
  `price` decimal(10,0) NOT NULL,
  `location` varchar(45) NOT NULL,
  `service_types_id` int NOT NULL,
  `users_providers_id` int NOT NULL,
  `service_availability_id` int NOT NULL,
  PRIMARY KEY (`id_services`),
  KEY `fk_SERVICES_SERVICE_TYPES1_idx` (`service_types_id`),
  KEY `fk_SERVICES_USERS1_idx` (`users_providers_id`),
  KEY `fk_services_service_availability1_idx` (`service_availability_id`),
  CONSTRAINT `fk_services_service_availability1` FOREIGN KEY (`service_availability_id`) REFERENCES `service_availability` (`id_service_availability`),
  CONSTRAINT `fk_SERVICES_SERVICE_TYPES1` FOREIGN KEY (`service_types_id`) REFERENCES `service_types` (`id_service_types`),
  CONSTRAINT `fk_SERVICES_USERS1` FOREIGN KEY (`users_providers_id`) REFERENCES `users` (`id_users`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `services`
--

LOCK TABLES `services` WRITE;
/*!40000 ALTER TABLE `services` DISABLE KEYS */;
INSERT INTO `services` VALUES (3,'vendo moto','corolla 1.5',1500,'tota',6,16,2);
/*!40000 ALTER TABLE `services` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_types`
--

DROP TABLE IF EXISTS `user_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_types` (
  `id_user_types` int NOT NULL AUTO_INCREMENT,
  `type` varchar(45) NOT NULL,
  PRIMARY KEY (`id_user_types`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_types`
--

LOCK TABLES `user_types` WRITE;
/*!40000 ALTER TABLE `user_types` DISABLE KEYS */;
INSERT INTO `user_types` VALUES (3,'EMPRESA'),(4,'PARTICULAR');
/*!40000 ALTER TABLE `user_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id_users` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `password` varchar(255) NOT NULL,
  `phone` varchar(45) NOT NULL,
  `user_types_id` int NOT NULL,
  PRIMARY KEY (`id_users`),
  UNIQUE KEY `email_UNIQUE` (`email`),
  UNIQUE KEY `phone_UNIQUE` (`phone`),
  KEY `fk_USERS_USER_TYPES1_idx` (`user_types_id`),
  CONSTRAINT `fk_USERS_USER_TYPES1` FOREIGN KEY (`user_types_id`) REFERENCES `user_types` (`id_user_types`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (16,'John Doe','john.do2ee@example.com','scrypt:32768:8:1$3alEsVbRIcUUTJkA$a95bb6501051259b975bdf6c6cff748045621f275b17f7bdb5f89ee5ed64f6e5db52cfcaca4ecb2ba20e148850ccc516e866cff4d0dd54ea55b3de7968a671c6','123245627890',3);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_has_roles`
--

DROP TABLE IF EXISTS `users_has_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_has_roles` (
  `id_users_has_roles` int NOT NULL AUTO_INCREMENT,
  `users_id` int NOT NULL,
  `roles_id` int NOT NULL,
  PRIMARY KEY (`id_users_has_roles`),
  KEY `fk_USERS_has_ROLES_ROLES1_idx` (`roles_id`),
  KEY `fk_USERS_has_ROLES_USERS_idx` (`users_id`),
  CONSTRAINT `fk_USERS_has_ROLES_ROLES1` FOREIGN KEY (`roles_id`) REFERENCES `roles` (`id_roles`),
  CONSTRAINT `fk_USERS_has_ROLES_USERS` FOREIGN KEY (`users_id`) REFERENCES `users` (`id_users`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_has_roles`
--

LOCK TABLES `users_has_roles` WRITE;
/*!40000 ALTER TABLE `users_has_roles` DISABLE KEYS */;
INSERT INTO `users_has_roles` VALUES (8,16,6);
/*!40000 ALTER TABLE `users_has_roles` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-18 18:58:48
