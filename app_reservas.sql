CREATE DATABASE  IF NOT EXISTS `app_reservas` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `app_reservas`;
-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: localhost    Database: app_reservas
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
-- Table structure for table `calificaciones`
--

DROP TABLE IF EXISTS `calificaciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `calificaciones` (
  `id_calificaciones` int NOT NULL,
  `puntuacion` int NOT NULL,
  `comentario` varchar(45) NOT NULL,
  `fecha_creacion` datetime NOT NULL,
  `servicios_id` int NOT NULL,
  `usuarios_id` int NOT NULL,
  PRIMARY KEY (`id_calificaciones`),
  KEY `fk_CALIFICACIONES_SERVICIOS1_idx` (`servicios_id`),
  KEY `fk_CALIFICACIONES_USUARIOS1_idx` (`usuarios_id`),
  CONSTRAINT `fk_CALIFICACIONES_SERVICIOS1` FOREIGN KEY (`servicios_id`) REFERENCES `servicios` (`id_servicios`),
  CONSTRAINT `fk_CALIFICACIONES_USUARIOS1` FOREIGN KEY (`usuarios_id`) REFERENCES `usuarios` (`id_usuarios`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `calificaciones`
--

LOCK TABLES `calificaciones` WRITE;
/*!40000 ALTER TABLE `calificaciones` DISABLE KEYS */;
/*!40000 ALTER TABLE `calificaciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `disponibilidad_servicio`
--

DROP TABLE IF EXISTS `disponibilidad_servicio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `disponibilidad_servicio` (
  `id_disponibilidad_servicio` int NOT NULL AUTO_INCREMENT,
  `estado` varchar(45) NOT NULL,
  PRIMARY KEY (`id_disponibilidad_servicio`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `disponibilidad_servicio`
--

LOCK TABLES `disponibilidad_servicio` WRITE;
/*!40000 ALTER TABLE `disponibilidad_servicio` DISABLE KEYS */;
/*!40000 ALTER TABLE `disponibilidad_servicio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estados_pago`
--

DROP TABLE IF EXISTS `estados_pago`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estados_pago` (
  `id_estados_pago` int NOT NULL AUTO_INCREMENT,
  `estado` varchar(45) NOT NULL,
  PRIMARY KEY (`id_estados_pago`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estados_pago`
--

LOCK TABLES `estados_pago` WRITE;
/*!40000 ALTER TABLE `estados_pago` DISABLE KEYS */;
/*!40000 ALTER TABLE `estados_pago` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estados_reserva`
--

DROP TABLE IF EXISTS `estados_reserva`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estados_reserva` (
  `id_estados_reserva` int NOT NULL AUTO_INCREMENT,
  `estado` varchar(45) NOT NULL,
  PRIMARY KEY (`id_estados_reserva`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estados_reserva`
--

LOCK TABLES `estados_reserva` WRITE;
/*!40000 ALTER TABLE `estados_reserva` DISABLE KEYS */;
/*!40000 ALTER TABLE `estados_reserva` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pagos`
--

DROP TABLE IF EXISTS `pagos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pagos` (
  `id_pagos` int NOT NULL,
  `fecha_pago` datetime NOT NULL,
  `monto` decimal(10,0) NOT NULL,
  `reservas_id` int NOT NULL,
  `estados_pago_id` int NOT NULL,
  PRIMARY KEY (`id_pagos`),
  KEY `fk_PAGOS_RESERVAS1_idx` (`reservas_id`),
  KEY `fk_PAGOS_ESTADOS_PAGO1_idx` (`estados_pago_id`),
  CONSTRAINT `fk_PAGOS_ESTADOS_PAGO1` FOREIGN KEY (`estados_pago_id`) REFERENCES `estados_pago` (`id_estados_pago`),
  CONSTRAINT `fk_PAGOS_RESERVAS1` FOREIGN KEY (`reservas_id`) REFERENCES `reservas` (`id_reservas`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pagos`
--

LOCK TABLES `pagos` WRITE;
/*!40000 ALTER TABLE `pagos` DISABLE KEYS */;
/*!40000 ALTER TABLE `pagos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reservas`
--

DROP TABLE IF EXISTS `reservas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reservas` (
  `id_reservas` int NOT NULL AUTO_INCREMENT,
  `fecha_creacion_reserva` datetime NOT NULL,
  `fecha_inicio_reserva` datetime NOT NULL,
  `fecha_fin_reserva` datetime NOT NULL,
  `monto_total` decimal(10,0) NOT NULL,
  `servicios_id` int NOT NULL,
  `usuarios_id` int NOT NULL,
  `estados_reserva_id` int NOT NULL,
  PRIMARY KEY (`id_reservas`),
  KEY `fk_RESERVAS_SERVICIOS1_idx` (`servicios_id`),
  KEY `fk_RESERVAS_USUARIOS1_idx` (`usuarios_id`),
  KEY `fk_RESERVAS_ESTADOS_RESERVA1_idx` (`estados_reserva_id`),
  CONSTRAINT `fk_RESERVAS_ESTADOS_RESERVA1` FOREIGN KEY (`estados_reserva_id`) REFERENCES `estados_reserva` (`id_estados_reserva`),
  CONSTRAINT `fk_RESERVAS_SERVICIOS1` FOREIGN KEY (`servicios_id`) REFERENCES `servicios` (`id_servicios`),
  CONSTRAINT `fk_RESERVAS_USUARIOS1` FOREIGN KEY (`usuarios_id`) REFERENCES `usuarios` (`id_usuarios`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reservas`
--

LOCK TABLES `reservas` WRITE;
/*!40000 ALTER TABLE `reservas` DISABLE KEYS */;
/*!40000 ALTER TABLE `reservas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id_roles` int NOT NULL AUTO_INCREMENT,
  `tipo` varchar(45) NOT NULL,
  PRIMARY KEY (`id_roles`),
  UNIQUE KEY `tipo_UNIQUE` (`tipo`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (7,'ADMIN'),(8,'CLIENTE'),(9,'PROVEEDOR');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `servicios`
--

DROP TABLE IF EXISTS `servicios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `servicios` (
  `id_servicios` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `descripcion` varchar(255) NOT NULL,
  `precio` decimal(10,0) NOT NULL,
  `ubicacion` varchar(45) NOT NULL,
  `tipos_servicio_id` int NOT NULL,
  `usuarios_proveedores_id` int NOT NULL,
  `disponibilidad_servicio_id` int NOT NULL,
  PRIMARY KEY (`id_servicios`),
  KEY `fk_SERVICIOS_TIPOS_SERVICIO1_idx` (`tipos_servicio_id`),
  KEY `fk_SERVICIOS_USUARIOS1_idx` (`usuarios_proveedores_id`),
  KEY `fk_servicios_disponibilidad_servicio1_idx` (`disponibilidad_servicio_id`),
  CONSTRAINT `fk_servicios_disponibilidad_servicio1` FOREIGN KEY (`disponibilidad_servicio_id`) REFERENCES `disponibilidad_servicio` (`id_disponibilidad_servicio`),
  CONSTRAINT `fk_SERVICIOS_TIPOS_SERVICIO1` FOREIGN KEY (`tipos_servicio_id`) REFERENCES `tipos_servicio` (`id_tipos_servicio`),
  CONSTRAINT `fk_SERVICIOS_USUARIOS1` FOREIGN KEY (`usuarios_proveedores_id`) REFERENCES `usuarios` (`id_usuarios`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicios`
--

LOCK TABLES `servicios` WRITE;
/*!40000 ALTER TABLE `servicios` DISABLE KEYS */;
/*!40000 ALTER TABLE `servicios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipos_servicio`
--

DROP TABLE IF EXISTS `tipos_servicio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipos_servicio` (
  `id_tipos_servicio` int NOT NULL AUTO_INCREMENT,
  `tipo` varchar(45) NOT NULL,
  PRIMARY KEY (`id_tipos_servicio`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipos_servicio`
--

LOCK TABLES `tipos_servicio` WRITE;
/*!40000 ALTER TABLE `tipos_servicio` DISABLE KEYS */;
INSERT INTO `tipos_servicio` VALUES (7,'INDUMENTARIA'),(8,'VEHICULOS'),(9,'ALOJAMIENTO');
/*!40000 ALTER TABLE `tipos_servicio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipos_usuario`
--

DROP TABLE IF EXISTS `tipos_usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipos_usuario` (
  `id_tipos_usuario` int NOT NULL AUTO_INCREMENT,
  `tipo` varchar(45) NOT NULL,
  PRIMARY KEY (`id_tipos_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipos_usuario`
--

LOCK TABLES `tipos_usuario` WRITE;
/*!40000 ALTER TABLE `tipos_usuario` DISABLE KEYS */;
INSERT INTO `tipos_usuario` VALUES (5,'PARTICULAR'),(6,'EMPRESA');
/*!40000 ALTER TABLE `tipos_usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id_usuarios` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `correo` varchar(45) NOT NULL,
  `contrasena` varchar(255) NOT NULL,
  `telefono` varchar(45) NOT NULL,
  `tipos_usuario_id` int NOT NULL,
  PRIMARY KEY (`id_usuarios`),
  UNIQUE KEY `correo_UNIQUE` (`correo`),
  UNIQUE KEY `telefono_UNIQUE` (`telefono`),
  KEY `fk_USUARIOS_TIPOS_USUARIO1_idx` (`tipos_usuario_id`),
  CONSTRAINT `fk_USUARIOS_TIPOS_USUARIO1` FOREIGN KEY (`tipos_usuario_id`) REFERENCES `tipos_usuario` (`id_tipos_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (17,'Alexis Damian Martin','rgonza@jjs.com','scrypt:32768:8:1$iXh4XFglPRvfPSC1$50c46f89263dc1bee99dbd8060fb3d517c07ee1686e2326ed0902e363a954e4ceb7a7b07c3ee5746b7b2d4c9f636223b1e26671eefe05b0edf77cc9d5e9ede9f','3329601836',5);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios_tiene_roles`
--

DROP TABLE IF EXISTS `usuarios_tiene_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios_tiene_roles` (
  `id_usuarios_tiene_roles` int NOT NULL AUTO_INCREMENT,
  `usuarios_id` int NOT NULL,
  `roles_id` int NOT NULL,
  PRIMARY KEY (`id_usuarios_tiene_roles`),
  KEY `fk_USUARIOS_tiene_ROLES_ROLES1_idx` (`roles_id`),
  KEY `fk_USUARIOS_tiene_ROLES_USUARIOS_idx` (`usuarios_id`),
  CONSTRAINT `fk_USUARIOS_tiene_ROLES_ROLES1` FOREIGN KEY (`roles_id`) REFERENCES `roles` (`id_roles`),
  CONSTRAINT `fk_USUARIOS_tiene_ROLES_USUARIOS` FOREIGN KEY (`usuarios_id`) REFERENCES `usuarios` (`id_usuarios`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios_tiene_roles`
--

LOCK TABLES `usuarios_tiene_roles` WRITE;
/*!40000 ALTER TABLE `usuarios_tiene_roles` DISABLE KEYS */;
INSERT INTO `usuarios_tiene_roles` VALUES (9,17,8),(10,17,9);
/*!40000 ALTER TABLE `usuarios_tiene_roles` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-29 11:11:43
