CREATE DATABASE SSO;
USE SSO;
DROP TABLE IF EXISTS `AppRequests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `AppRequests` (
  `UserName` varchar(100) DEFAULT NULL,
  `AppName` varchar(100) DEFAULT NULL,
  `OrgName` varchar(100) DEFAULT NULL
) ;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `AppRequests` WRITE;
/*!40000 ALTER TABLE `AppRequests` DISABLE KEYS */;
/*!40000 ALTER TABLE `AppRequests` ENABLE KEYS */;
UNLOCK TABLES;

DROP TABLE IF EXISTS `AppUsers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `AppUsers` (
  `AppName` varchar(100) NOT NULL,
  `Users` varchar(100) NOT NULL
) ;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `AppUsers`
--

LOCK TABLES `AppUsers` WRITE;
/*!40000 ALTER TABLE `AppUsers` DISABLE KEYS */;
INSERT INTO `AppUsers` VALUES ('TestAppLocal','dvana1'),('TestApp2','dvana1');
/*!40000 ALTER TABLE `AppUsers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Apps`
--

DROP TABLE IF EXISTS `Apps`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Apps` (
  `AppName` varchar(100) NOT NULL,
  `Redirect_URL` varchar(100) NOT NULL,
  `Org` varchar(100) NOT NULL,
  PRIMARY KEY (`AppName`)
) ;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Apps`
--

LOCK TABLES `Apps` WRITE;
/*!40000 ALTER TABLE `Apps` DISABLE KEYS */;
INSERT INTO `Apps` VALUES ('TestApp2','http://54.87.197.101/home/','SSO Boys'),('TestAppLocal','http://18.215.163.142/home/','SSO Boys');
/*!40000 ALTER TABLE `Apps` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Organizations`
--

DROP TABLE IF EXISTS `Organizations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Organizations` (
  `OrgName` varchar(100) NOT NULL,
  `OwnerUser` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`OrgName`)
);
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Organizations`
--

LOCK TABLES `Organizations` WRITE;
/*!40000 ALTER TABLE `Organizations` DISABLE KEYS */;
INSERT INTO `Organizations` VALUES ('SSO Boys','dvana1'),('testEncrypt','dvana34');
/*!40000 ALTER TABLE `Organizations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Users`
--

DROP TABLE IF EXISTS `Users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Users` (
  `UserName` varchar(100) NOT NULL,
  `Password` varchar(100) NOT NULL,
  `FirstName` varchar(100) NOT NULL,
  `LastName` varchar(100) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `AccountType` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `Organization` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`UserName`)
);
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Users`
--

LOCK TABLES `Users` WRITE;
/*!40000 ALTER TABLE `Users` DISABLE KEYS */;
INSERT INTO `Users` VALUES ('dvana1','$2b$12$A4NgGGdEYZphw01F2jTk0eapPRRtaqekKuzG6NWtn9/RzUJ4K3ZUy','David','dvdvdv','davidkennesaw@gmail.com','Owner','SSO Boys'),('dvana2','$2b$12$1eGjH0zQbT5tKhq8v3aPTu4.ARuAgVekP0pqPkb4V9nuZ8NqE3kHy','David','VanAsselberg','davidkennesaw@gmail.com','User','SSO Boys'),('dvana34','$2b$12$UvVf4oRDbPso5FUfMydIN.n94dU68m4sIPupmFoFq.IR9RazJnXXe','David','VanAsselberg','davidkennesaw@gmail.com','Owner','testEncrypt');
/*!40000 ALTER TABLE `Users` ENABLE KEYS */;
UNLOCK TABLES;

ALTER TABLE AppRequests
  ADD KEY `AppRequests_FK` (`AppName`),
  ADD KEY `AppRequests_FK_1` (`UserName`),
  ADD CONSTRAINT `AppRequests_FK` FOREIGN KEY (`AppName`) REFERENCES `Apps` (`AppName`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `AppRequests_FK_1` FOREIGN KEY (`UserName`) REFERENCES `Users` (`UserName`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE AppUsers
  ADD KEY `AppUsers_FK` (`Users`),
  ADD KEY `AppUsers_FK_1` (`AppName`),
  ADD CONSTRAINT `AppUsers_FK` FOREIGN KEY (`Users`) REFERENCES `Users` (`UserName`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `AppUsers_FK_1` FOREIGN KEY (`AppName`) REFERENCES `Apps` (`AppName`);

ALTER TABLE Apps
  ADD KEY `Apps_FK` (`Org`),
  ADD CONSTRAINT `Apps_FK` FOREIGN KEY (`Org`) REFERENCES `Organizations` (`OrgName`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE Organizations
  ADD KEY `Organizations_FK` (`OwnerUser`),
  ADD CONSTRAINT `Organizations_FK` FOREIGN KEY (`OwnerUser`) REFERENCES `Users` (`UserName`);
