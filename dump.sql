CREATE DATABASE  IF NOT EXISTS `sklopime` /*!40100 DEFAULT CHARACTER SET utf8mb3 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `sklopime`;
-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: sklopime
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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=89 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add build',2,'add_build'),(2,'Can change build',2,'change_build'),(3,'Can delete build',2,'delete_build'),(4,'Can view build',2,'view_build'),(5,'Can add component',7,'add_component'),(6,'Can change component',7,'change_component'),(7,'Can delete component',7,'delete_component'),(8,'Can view component',7,'view_component'),(9,'Can add benchmark',1,'add_benchmark'),(10,'Can change benchmark',1,'change_benchmark'),(11,'Can delete benchmark',1,'delete_benchmark'),(12,'Can view benchmark',1,'view_benchmark'),(13,'Can add case',6,'add_case'),(14,'Can change case',6,'change_case'),(15,'Can delete case',6,'delete_case'),(16,'Can view case',6,'view_case'),(17,'Can add cpu',9,'add_cpu'),(18,'Can change cpu',9,'change_cpu'),(19,'Can delete cpu',9,'delete_cpu'),(20,'Can view cpu',9,'view_cpu'),(21,'Can add cpucooler',10,'add_cpucooler'),(22,'Can change cpucooler',10,'change_cpucooler'),(23,'Can delete cpucooler',10,'delete_cpucooler'),(24,'Can view cpucooler',10,'view_cpucooler'),(25,'Can add gpu',11,'add_gpu'),(26,'Can change gpu',11,'change_gpu'),(27,'Can delete gpu',11,'delete_gpu'),(28,'Can view gpu',11,'view_gpu'),(29,'Can add motherboard',12,'add_motherboard'),(30,'Can change motherboard',12,'change_motherboard'),(31,'Can delete motherboard',12,'delete_motherboard'),(32,'Can view motherboard',12,'view_motherboard'),(33,'Can add powersupply',13,'add_powersupply'),(34,'Can change powersupply',13,'change_powersupply'),(35,'Can delete powersupply',13,'delete_powersupply'),(36,'Can view powersupply',13,'view_powersupply'),(37,'Can add ram',14,'add_ram'),(38,'Can change ram',14,'change_ram'),(39,'Can delete ram',14,'delete_ram'),(40,'Can view ram',14,'view_ram'),(41,'Can add storage',15,'add_storage'),(42,'Can change storage',15,'change_storage'),(43,'Can delete storage',15,'delete_storage'),(44,'Can view storage',15,'view_storage'),(45,'Can add buildcomponent',3,'add_buildcomponent'),(46,'Can change buildcomponent',3,'change_buildcomponent'),(47,'Can delete buildcomponent',3,'delete_buildcomponent'),(48,'Can view buildcomponent',3,'view_buildcomponent'),(49,'Can add componentprice',8,'add_componentprice'),(50,'Can change componentprice',8,'change_componentprice'),(51,'Can delete componentprice',8,'delete_componentprice'),(52,'Can view componentprice',8,'view_componentprice'),(53,'Can add user profile',16,'add_userprofile'),(54,'Can change user profile',16,'change_userprofile'),(55,'Can delete user profile',16,'delete_userprofile'),(56,'Can view user profile',16,'view_userprofile'),(57,'Can add buildlikedislike',5,'add_buildlikedislike'),(58,'Can change buildlikedislike',5,'change_buildlikedislike'),(59,'Can delete buildlikedislike',5,'delete_buildlikedislike'),(60,'Can view buildlikedislike',5,'view_buildlikedislike'),(61,'Can add buildimage',4,'add_buildimage'),(62,'Can change buildimage',4,'change_buildimage'),(63,'Can delete buildimage',4,'delete_buildimage'),(64,'Can view buildimage',4,'view_buildimage'),(65,'Can add log entry',17,'add_logentry'),(66,'Can change log entry',17,'change_logentry'),(67,'Can delete log entry',17,'delete_logentry'),(68,'Can view log entry',17,'view_logentry'),(69,'Can add permission',19,'add_permission'),(70,'Can change permission',19,'change_permission'),(71,'Can delete permission',19,'delete_permission'),(72,'Can view permission',19,'view_permission'),(73,'Can add group',18,'add_group'),(74,'Can change group',18,'change_group'),(75,'Can delete group',18,'delete_group'),(76,'Can view group',18,'view_group'),(77,'Can add user',20,'add_user'),(78,'Can change user',20,'change_user'),(79,'Can delete user',20,'delete_user'),(80,'Can view user',20,'view_user'),(81,'Can add content type',21,'add_contenttype'),(82,'Can change content type',21,'change_contenttype'),(83,'Can delete content type',21,'delete_contenttype'),(84,'Can view content type',21,'view_contenttype'),(85,'Can add session',22,'add_session'),(86,'Can change session',22,'change_session'),(87,'Can delete session',22,'delete_session'),(88,'Can view session',22,'view_session');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$1200000$n8IOOEPus2aT36HlAMfNDo$zS+OkiSqVBP+B8O0DBK8ulB02XGvZLS/PqB7htBvPs4=',NULL,0,'cira','','','cira@test.com',0,1,'2026-07-13 13:13:48.852003'),(2,'pbkdf2_sha256$1200000$kiCR1fUScf9kWRcOGOEeKf$HSrgwTlmpU3g+GQidQGuJVAA0uyKCEJa7f4J5H9WaOI=',NULL,0,'cvetko','','','cvetko@test.com',0,1,'2026-07-13 13:13:49.207316'),(3,'pbkdf2_sha256$1200000$ZXbkA9h2ictVe4XdSYdVRu$IEwZzAIjlejycoXygZxeQ2yU5hhoS+qISVwlxIGWtjA=',NULL,0,'coa','','','coa@test.com',0,1,'2026-07-13 13:13:49.546538');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `benchmark`
--

DROP TABLE IF EXISTS `benchmark`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `benchmark` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `value` varchar(45) NOT NULL,
  `idBuild` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `benchmark_idBuild_47918f97_fk_build_id` (`idBuild`),
  CONSTRAINT `benchmark_idBuild_47918f97_fk_build_id` FOREIGN KEY (`idBuild`) REFERENCES `build` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `benchmark`
--

LOCK TABLES `benchmark` WRITE;
/*!40000 ALTER TABLE `benchmark` DISABLE KEYS */;
INSERT INTO `benchmark` VALUES (1,'Cinebench R23','14500',1),(2,'3DMark Time Spy','11000',1),(3,'Cinebench R23','18500',2),(4,'3DMark Time Spy','19500',2),(5,'Geekbench 6','27000',2),(6,'3DMark Time Spy','17500',3),(7,'Cinebench R23','15000',3),(8,'Cinebench R23','22000',4),(9,'Geekbench 6','25000',4),(10,'3DMark Time Spy','21000',5),(11,'Cinebench R23','18500',5),(12,'Geekbench 6','22000',6);
/*!40000 ALTER TABLE `benchmark` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `build`
--

DROP TABLE IF EXISTS `build`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `build` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `totalPrice` int NOT NULL,
  `numOfLikes` int NOT NULL,
  `numOfDislikes` int NOT NULL,
  `idUser` bigint NOT NULL,
  `description` longtext,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `build_idUser_fb1ecca1_fk_user_id` (`idUser`),
  CONSTRAINT `build_idUser_fb1ecca1_fk_user_id` FOREIGN KEY (`idUser`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `build`
--

LOCK TABLES `build` WRITE;
/*!40000 ALTER TABLE `build` DISABLE KEYS */;
INSERT INTO `build` VALUES (1,99500,1,0,1,'Affordable 1080p gaming configuration','Budget Gaming PC'),(2,84500,1,0,1,'Gaming and streaming setup','Streaming Beast'),(3,72000,1,0,2,'Balanced gaming computer','AMD Midrange Build'),(4,213000,0,1,2,'Workstation for development and editing','Intel Productivity PC'),(5,232500,1,0,3,'High refresh rate gaming PC','RTX Gaming Machine'),(6,197500,1,0,3,'Quiet computer for everyday work','Silent Office PC');
/*!40000 ALTER TABLE `build` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `buildcomponent`
--

DROP TABLE IF EXISTS `buildcomponent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `buildcomponent` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `idBuild` bigint NOT NULL,
  `idComponent` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `buildcomponent_idBuild_789c5e0b_fk_build_id` (`idBuild`),
  KEY `buildcomponent_idComponent_69507216_fk_component_id` (`idComponent`),
  CONSTRAINT `buildcomponent_idBuild_789c5e0b_fk_build_id` FOREIGN KEY (`idBuild`) REFERENCES `build` (`id`),
  CONSTRAINT `buildcomponent_idComponent_69507216_fk_component_id` FOREIGN KEY (`idComponent`) REFERENCES `component` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `buildcomponent`
--

LOCK TABLES `buildcomponent` WRITE;
/*!40000 ALTER TABLE `buildcomponent` DISABLE KEYS */;
INSERT INTO `buildcomponent` VALUES (1,1,1),(2,1,6),(3,1,7),(4,2,2),(5,2,4),(6,2,11),(7,3,1),(8,3,5),(9,3,9),(10,4,3),(11,4,10),(12,4,12),(13,5,2),(14,5,4),(15,5,8),(16,6,1),(17,6,11),(18,6,15);
/*!40000 ALTER TABLE `buildcomponent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `buildimage`
--

DROP TABLE IF EXISTS `buildimage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `buildimage` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `image` varchar(100) NOT NULL,
  `idBuild` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `buildimage_idBuild_5080ec5f_fk_build_id` (`idBuild`),
  CONSTRAINT `buildimage_idBuild_5080ec5f_fk_build_id` FOREIGN KEY (`idBuild`) REFERENCES `build` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `buildimage`
--

LOCK TABLES `buildimage` WRITE;
/*!40000 ALTER TABLE `buildimage` DISABLE KEYS */;
/*!40000 ALTER TABLE `buildimage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `buildlikedislike`
--

DROP TABLE IF EXISTS `buildlikedislike`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `buildlikedislike` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `like` int NOT NULL,
  `idBuild` bigint NOT NULL,
  `idUser` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `buildlikedislike_idBuild_c08f6f67_fk_build_id` (`idBuild`),
  KEY `buildlikedislike_idUser_dbbbd1ac_fk_user_id` (`idUser`),
  CONSTRAINT `buildlikedislike_idBuild_c08f6f67_fk_build_id` FOREIGN KEY (`idBuild`) REFERENCES `build` (`id`),
  CONSTRAINT `buildlikedislike_idUser_dbbbd1ac_fk_user_id` FOREIGN KEY (`idUser`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `buildlikedislike`
--

LOCK TABLES `buildlikedislike` WRITE;
/*!40000 ALTER TABLE `buildlikedislike` DISABLE KEYS */;
INSERT INTO `buildlikedislike` VALUES (1,1,3,1),(2,1,5,1),(3,1,1,2),(4,1,6,2),(5,1,2,3),(6,0,4,3);
/*!40000 ALTER TABLE `buildlikedislike` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `case`
--

DROP TABLE IF EXISTS `case`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `case` (
  `id` bigint NOT NULL,
  `color` varchar(45) NOT NULL,
  `dimensions` varchar(45) NOT NULL,
  `supportedMotherboards` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `case_id_7b8a5c4c_fk_component_id` FOREIGN KEY (`id`) REFERENCES `component` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `case`
--

LOCK TABLES `case` WRITE;
/*!40000 ALTER TABLE `case` DISABLE KEYS */;
INSERT INTO `case` VALUES (18,'Black','464x227x446','ATX,mATX,ITX'),(19,'White','453x230x466','ATX,mATX,ITX');
/*!40000 ALTER TABLE `case` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `component`
--

DROP TABLE IF EXISTS `component`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `component` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `description` varchar(255) NOT NULL,
  `imagePath` varchar(255) NOT NULL,
  `powerConsumption` int NOT NULL,
  `manufacturer` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `component_name_e850d9ab_uniq` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `component`
--

LOCK TABLES `component` WRITE;
/*!40000 ALTER TABLE `component` DISABLE KEYS */;
INSERT INTO `component` VALUES (1,'AMD Ryzen 5 7600','6 core AM5 gaming processor','cpu.png',65,'AMD'),(2,'AMD Ryzen 7 7800X3D','High end gaming CPU with 3D cache','cpu.png',120,'AMD'),(3,'Intel Core i5-14600KF','14th generation Intel gaming CPU','cpu.png',125,'Intel'),(4,'GIGABYTE GEFORCE RTX 5050 8GB ','NVIDIA RTX gaming GPU','gpu.png',220,'MSI'),(5,'ASUS PRIME GeForce RTX 5060 8GB','Budget RTX','gpu.png',260,'Sapphire'),(6,'ASUS Prime Radeon RX 9070 XT 16GB','GPUAMD Radeon gaming GPU','gpu.png',115,'ASUS'),(7,'KINGSTON FURY BEAST 32GB - KF556C40BBK2-32 ','DDR5 gaming memory kit','ram.png',10,'Kingston'),(8,'PATRIOT VIPER STEEL 32GB PVS432G360C8','Corsair DDR5 RAM','ram.png',10,'Corsair'),(9,'MSI MPG B850 EDGE TI ','AM5 DDR5 motherboard','mb.png',30,'MSI'),(10,'ASUS TUF Gaming B760-PLUS WiFi','Intel DDR5 motherboard','mb.png',35,'ASUS'),(11,'KINGSTON NV3 500GB 2280 4.0 SNV3S/500G','High performance NVMe SSD','ssd.png',8,'Samsung'),(12,'SAMSUNG 990 EVO PLUS 1TB 4.0 ','Gaming NVMe SSD','ssd.png',7,'Western Digital'),(13,'WESTERN DIGITAL Blue PC Desktop 2TB SATA III','Desktop HDD','hdd.png',6,'Seagate'),(14,'Corsair RM750e','750W Gold PSU','psu.png',0,'Corsair'),(15,'be quiet! Pure Power 12 M 750W','Silent modular PSU','psu.png',0,'be quiet!'),(16,'NZXT Kraken Elite 360 Black','Air CPU cooler','cooler.png',5,'DeepCool'),(17,'ARCTIC Freezer 36 Black Kuler','Dual tower air cooler','cooler.png',7,'Thermalright'),(18,'NZXT H3 FLOW BLACK','Airflow gaming case','case.png',0,'NZXT'),(19,'GIGABYTE C102 GLASS ICE ','Popular airflow case','case.png',0,'Corsair');
/*!40000 ALTER TABLE `component` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `componentprice`
--

DROP TABLE IF EXISTS `componentprice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `componentprice` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `shopName` varchar(45) NOT NULL,
  `link` varchar(255) NOT NULL,
  `price` int NOT NULL,
  `idComponent` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `componentprice_idComponent_a57536f1_fk_component_id` (`idComponent`),
  CONSTRAINT `componentprice_idComponent_a57536f1_fk_component_id` FOREIGN KEY (`idComponent`) REFERENCES `component` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `componentprice`
--

LOCK TABLES `componentprice` WRITE;
/*!40000 ALTER TABLE `componentprice` DISABLE KEYS */;
INSERT INTO `componentprice` VALUES (1,'Gigatron','https://gigatron.rs/proizvod/nzxt-h3-flow-black-5056547207988',9999,18),(2,'Gigatron','https://gigatron.rs/proizvod/gigabyte-c102-glass-ice-4719331554842',7999,19),(3,'Gigatron','https://gigatron.rs/proizvod/corsair-rm750e-750w-840006691082',15999,14),(4,'Gigatron','https://gigatron.rs/proizvod/be-quiet-pure-power-12-650w-4260052191170',12999,15),(5,'Gigatron','https://gigatron.rs/proizvod/patriot-viper-steel-32gb-ddr4-3600mhz-cl18-pvs432g360c8-ram-memorija-0814914026915',24999,8),(6,'Gigatron','https://gigatron.rs/proizvod/kingston-ddr5-2x16gb-5600mhz-740617325706',59999,7),(7,'Gigatron','https://gigatron.rs/proizvod/kingston-nv3-series-500gb-740617344806',13999,11),(8,'Gigatron','https://gigatron.rs/proizvod/samsung-ssd-990-evo-plus-1tb-8806095575674',22999,12),(9,'Gigatron','https://gigatron.rs/proizvod/western-digital-blue-2tb-sata-iii-3-5-wd20ezbx-hdd-718037877501',17999,13),(10,'Gigatron','https://gigatron.rs/proizvod/gigabyte-rtx-5050-wf2-oc-8gb-4719331356743',33999,4),(11,'Gigatron','https://gigatron.rs/proizvod/asus-rtx-5060-prime-oc-8gb-4711636057851',47999,5),(12,'Gigatron','https://gigatron.rs/proizvod/asus-rx-9070-prime-oc-16gb-4711387829592',94999,6),(13,'Gigatron','https://gigatron.rs/proizvod/asus-tuf-gaming-b760-plus-wifi-maticna-ploca-4711387095119',17999,10),(14,'Gigatron','https://gigatron.rs/proizvod/msi-mpg-b850-edge-ti-wifi-4711377290616',42999,9),(15,'Gigatron','https://gigatron.rs/proizvod/aio-kraken-elite-360-v2black-5056547204130',40999,16),(16,'Gigatron','https://gigatron.rs/proizvod/arctic-freezer-36-black-4895213704144',4499,17),(17,'Gigatron','https://gigatron.rs/proizvod/amd-ryzen-5-7600-3-8ghz-730143314572',21999,1),(18,'Gigatron','https://gigatron.rs/proizvod/amd-ryzen-7-7800x3d-4-2ghz-730143314930',49999,2),(19,'Gigatron','https://gigatron.rs/proizvod/intel-core-i5-12600kf-2-8ghz-4-9ghz-5032037234115',21999,3);
/*!40000 ALTER TABLE `componentprice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cpu`
--

DROP TABLE IF EXISTS `cpu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cpu` (
  `id` bigint NOT NULL,
  `coreCount` int NOT NULL,
  `threadCount` int NOT NULL,
  `clockSpeed` decimal(4,2) NOT NULL,
  `socket` varchar(45) NOT NULL,
  `integratedGPU` int NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `cpu_id_e5a1ef0e_fk_component_id` FOREIGN KEY (`id`) REFERENCES `component` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cpu`
--

LOCK TABLES `cpu` WRITE;
/*!40000 ALTER TABLE `cpu` DISABLE KEYS */;
INSERT INTO `cpu` VALUES (1,6,12,3.80,'AM5',1),(2,8,16,4.20,'AM5',1),(3,14,20,3.50,'LGA1700',0);
/*!40000 ALTER TABLE `cpu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cpucooler`
--

DROP TABLE IF EXISTS `cpucooler`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cpucooler` (
  `id` bigint NOT NULL,
  `coolerType` varchar(5) NOT NULL,
  `socket` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `cpucooler_id_14d6ce10_fk_component_id` FOREIGN KEY (`id`) REFERENCES `component` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cpucooler`
--

LOCK TABLES `cpucooler` WRITE;
/*!40000 ALTER TABLE `cpucooler` DISABLE KEYS */;
INSERT INTO `cpucooler` VALUES (16,'Air','AM5'),(17,'Air','AM5');
/*!40000 ALTER TABLE `cpucooler` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (17,'admin','logentry'),(1,'app','benchmark'),(2,'app','build'),(3,'app','buildcomponent'),(4,'app','buildimage'),(5,'app','buildlikedislike'),(6,'app','case'),(7,'app','component'),(8,'app','componentprice'),(9,'app','cpu'),(10,'app','cpucooler'),(11,'app','gpu'),(12,'app','motherboard'),(13,'app','powersupply'),(14,'app','ram'),(15,'app','storage'),(16,'app','userprofile'),(18,'auth','group'),(19,'auth','permission'),(20,'auth','user'),(21,'contenttypes','contenttype'),(22,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-07-13 13:12:41.158157'),(2,'auth','0001_initial','2026-07-13 13:12:41.458035'),(3,'admin','0001_initial','2026-07-13 13:12:41.535777'),(4,'admin','0002_logentry_remove_auto_add','2026-07-13 13:12:41.539776'),(5,'admin','0003_logentry_add_action_flag_choices','2026-07-13 13:12:41.544776'),(6,'app','0001_initial','2026-07-13 13:12:42.150397'),(7,'app','0002_alter_cpu_clockspeed','2026-07-13 13:12:42.189953'),(8,'app','0003_alter_component_imagepath','2026-07-13 13:12:42.220967'),(9,'app','0004_build_description_build_name_alter_benchmark_idbuild_and_more','2026-07-13 13:12:42.303446'),(10,'app','0005_alter_benchmark_idbuild_alter_build_iduser_and_more','2026-07-13 13:12:42.431877'),(11,'app','0006_alter_component_name','2026-07-13 13:12:42.450981'),(12,'contenttypes','0002_remove_content_type_name','2026-07-13 13:12:42.499118'),(13,'auth','0002_alter_permission_name_max_length','2026-07-13 13:12:42.545135'),(14,'auth','0003_alter_user_email_max_length','2026-07-13 13:12:42.585279'),(15,'auth','0004_alter_user_username_opts','2026-07-13 13:12:42.590785'),(16,'auth','0005_alter_user_last_login_null','2026-07-13 13:12:42.626606'),(17,'auth','0006_require_contenttypes_0002','2026-07-13 13:12:42.627606'),(18,'auth','0007_alter_validators_add_error_messages','2026-07-13 13:12:42.631605'),(19,'auth','0008_alter_user_username_max_length','2026-07-13 13:12:42.669620'),(20,'auth','0009_alter_user_last_name_max_length','2026-07-13 13:12:42.708639'),(21,'auth','0010_alter_group_name_max_length','2026-07-13 13:12:42.750660'),(22,'auth','0011_update_proxy_permissions','2026-07-13 13:12:42.759165'),(23,'auth','0012_alter_user_first_name_max_length','2026-07-13 13:12:42.792211'),(24,'sessions','0001_initial','2026-07-13 13:12:42.812191');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gpu`
--

DROP TABLE IF EXISTS `gpu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gpu` (
  `id` bigint NOT NULL,
  `chip` varchar(45) NOT NULL,
  `memCapacity` varchar(10) NOT NULL,
  `color` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `gpu_id_a2195328_fk_component_id` FOREIGN KEY (`id`) REFERENCES `component` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gpu`
--

LOCK TABLES `gpu` WRITE;
/*!40000 ALTER TABLE `gpu` DISABLE KEYS */;
INSERT INTO `gpu` VALUES (4,'RTX 4070 SUPER','12GB','Black'),(5,'RX 7800 XT','16GB','Black'),(6,'RTX 4060','8GB','White');
/*!40000 ALTER TABLE `gpu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `motherboard`
--

DROP TABLE IF EXISTS `motherboard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `motherboard` (
  `id` bigint NOT NULL,
  `socket` varchar(45) NOT NULL,
  `formFactor` varchar(45) NOT NULL,
  `ramSlots` int NOT NULL,
  `ramType` varchar(20) NOT NULL,
  `color` varchar(45) NOT NULL,
  `wifiChip` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `motherboard_id_83f9e233_fk_component_id` FOREIGN KEY (`id`) REFERENCES `component` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `motherboard`
--

LOCK TABLES `motherboard` WRITE;
/*!40000 ALTER TABLE `motherboard` DISABLE KEYS */;
INSERT INTO `motherboard` VALUES (9,'AM5','ATX',4,'DDR5','Black','Intel AX210'),(10,'LGA1700','ATX',4,'DDR5','Black','Intel WiFi 6');
/*!40000 ALTER TABLE `motherboard` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `powersupply`
--

DROP TABLE IF EXISTS `powersupply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `powersupply` (
  `id` bigint NOT NULL,
  `formFactor` varchar(45) NOT NULL,
  `efficiency` varchar(45) NOT NULL,
  `wattage` int NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `powersupply_id_6567167c_fk_component_id` FOREIGN KEY (`id`) REFERENCES `component` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `powersupply`
--

LOCK TABLES `powersupply` WRITE;
/*!40000 ALTER TABLE `powersupply` DISABLE KEYS */;
INSERT INTO `powersupply` VALUES (14,'ATX','80+ Gold',750),(15,'ATX','80+ Gold',750);
/*!40000 ALTER TABLE `powersupply` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ram`
--

DROP TABLE IF EXISTS `ram`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ram` (
  `id` bigint NOT NULL,
  `type` varchar(45) NOT NULL,
  `speed` int NOT NULL,
  `memCapacity` varchar(10) NOT NULL,
  `moduleNum` int NOT NULL,
  `color` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `ram_id_8d923cac_fk_component_id` FOREIGN KEY (`id`) REFERENCES `component` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ram`
--

LOCK TABLES `ram` WRITE;
/*!40000 ALTER TABLE `ram` DISABLE KEYS */;
INSERT INTO `ram` VALUES (7,'DDR5',6000,'32GB',2,'Black'),(8,'DDR5',5600,'32GB',2,'Black');
/*!40000 ALTER TABLE `ram` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `storage`
--

DROP TABLE IF EXISTS `storage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `storage` (
  `id` bigint NOT NULL,
  `type` varchar(3) NOT NULL,
  `slot` varchar(45) NOT NULL,
  `capacity` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `storage_id_eb4d08eb_fk_component_id` FOREIGN KEY (`id`) REFERENCES `component` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `storage`
--

LOCK TABLES `storage` WRITE;
/*!40000 ALTER TABLE `storage` DISABLE KEYS */;
INSERT INTO `storage` VALUES (11,'SSD','M.2','2TB'),(12,'SSD','M.2','1TB'),(13,'HDD','SATA','2TB');
/*!40000 ALTER TABLE `storage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `user_user_id_3ad375f5_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,1),(2,2),(3,3);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-07-13 16:00:16
