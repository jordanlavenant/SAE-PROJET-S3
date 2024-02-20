-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: mysql-blandeau.alwaysdata.net
-- Generation Time: Feb 19, 2024 at 04:11 PM
-- Server version: 10.6.16-MariaDB
-- PHP Version: 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `blandeau_gestlab19`
--

DELIMITER $$
--
-- Procedures
--
CREATE DEFINER=`blandeau`@`%` PROCEDURE `alertesPeremption` ()   BEGIN
    declare fini boolean default false ;
    declare idMu int ;

    declare idMateriels cursor for
        SELECT idMaterielUnique FROM MATERIELUNIQUE WHERE datePeremption <= CURDATE() ;

    declare continue handler for not found set fini = true ;
    
    open idMateriels ;
    while not fini do
        fetch idMateriels into idMu ;
        if not fini then 
            INSERT INTO ALERTESENCOURS VALUES(1, idMu) ;
        end if ;
    end while ;
    close idMateriels ;
end$$

CREATE DEFINER=`blandeau`@`%` PROCEDURE `alertesPeremptionDixJours` ()   BEGIN
    declare fini boolean default false ;
    declare idMu int ;

    declare idMateriels cursor for
        SELECT idMaterielUnique FROM MATERIELUNIQUE WHERE datePeremption > CURDATE() AND datePeremption <= CURDATE() + INTERVAL 10 DAY ;

    declare continue handler for not found set fini = true ;
    
    open idMateriels ;
    while not fini do
        fetch idMateriels into idMu ;
        if not fini then 
            INSERT INTO ALERTESENCOURS VALUES(2, idMu) ;
        end if ;
    end while ;
    close idMateriels ;
end$$

CREATE DEFINER=`blandeau`@`%` PROCEDURE `alertesQuantiteAZero` ()   BEGIN
    declare fini boolean default false ;
    declare idMu int ;

    declare idMateriels cursor for
        SELECT idMaterielUnique FROM MATERIELUNIQUE NATURAL JOIN MATERIEL WHERE quantiteApproximative > (seuilAlerte/4) AND quantiteApproximative = 0 ;
    declare continue handler for not found set fini = true ;
    
    open idMateriels ;
    while not fini do
        fetch idMateriels into idMu ;
        if not fini then 
            INSERT INTO ALERTESENCOURS VALUES(4, idMu) ;
        end if ;
    end while ;
    close idMateriels ;
end$$

CREATE DEFINER=`blandeau`@`%` PROCEDURE `alertesQuantiteSeuil` ()   BEGIN
    declare fini boolean default false ;
    declare idMu int ;

    declare idMateriels cursor for
        SELECT idMaterielUnique FROM MATERIELUNIQUE NATURAL JOIN MATERIEL WHERE quantiteApproximative <= (seuilAlerte/4) ;

    declare continue handler for not found set fini = true ;
    
    open idMateriels ;
    while not fini do
        fetch idMateriels into idMu ;
        if not fini then 
            INSERT INTO ALERTESENCOURS VALUES(3, idMu) ;
        end if ;
    end while ;
    close idMateriels ;
end$$

CREATE DEFINER=`blandeau`@`%` PROCEDURE `gestionAlertes` ()   BEGIN
    DELETE FROM ALERTESENCOURS ;
    call alertesPeremption() ;
    call alertesPeremptionDixJours() ;
    call alertesQuantiteAZero() ;
    call alertesQuantiteSeuil() ;
end$$

--
-- Functions
--
CREATE DEFINER=`blandeau`@`%` FUNCTION `demandesEnAttente` () RETURNS VARCHAR(255) CHARSET utf8mb4 COLLATE utf8mb4_general_ci  begin
    declare id int ;
    declare listeDemandes varchar(255) default '';
    declare fini boolean default false ;

    declare idDemandes cursor for 
        SELECT DEMANDE.idDemande FROM DEMANDE WHERE idEtatD = 2;

    declare continue handler for not found set fini = true ;
    open idDemandes ;
    while not fini do
        fetch idDemandes into id ;
        if not fini then 
            if listeDemandes = '' then 
                SET listeDemandes = id ;
            else 
                SET listeDemandes = concat(listeDemandes, ", ", id) ;
            end if ;
        end if ;
    end while ;
    close idDemandes ;

    return listeDemandes ;
end$$

CREATE DEFINER=`blandeau`@`%` FUNCTION `demandesEnAttenteAncien` () RETURNS VARCHAR(255) CHARSET utf8mb4 COLLATE utf8mb4_general_ci  begin
    declare id int ;
    declare listeDemandes varchar(255) default '';
    declare fini boolean default false ;

    declare idDemandes cursor for 
        SELECT DEMANDE.idDemande FROM DEMANDE JOIN BONCOMMANDE ON DEMANDE.idDemande = BONCOMMANDE.idDemande WHERE BONCOMMANDE.idEtat = 1 ;

    declare continue handler for not found set fini = true ;
    open idDemandes ;
    while not fini do
        fetch idDemandes into id ;
        if not fini then 
            if listeDemandes = '' then 
                SET listeDemandes = id ;
            else 
                SET listeDemandes = concat(listeDemandes, ", ", id) ;
            end if ;
        end if ;
    end while ;
    close idDemandes ;

    return listeDemandes ;
end$$

CREATE DEFINER=`blandeau`@`%` FUNCTION `nombreDemandesEnAttente` () RETURNS VARCHAR(255) CHARSET utf8mb4 COLLATE utf8mb4_general_ci  begin
    declare id int ;
    declare listeDemandes varchar(255) default '';
    declare fini boolean default false ;

    declare idDemandes cursor for 
        SELECT COUNT(DEMANDE.idDemande) FROM DEMANDE ;

    declare continue handler for not found set fini = true ;
    open idDemandes ;
    while not fini do
        fetch idDemandes into id ;
        if not fini then 
            SET listeDemandes = id ;
        end if ;
    end while ;
    close idDemandes ;

    return listeDemandes ;
end$$

CREATE DEFINER=`blandeau`@`%` FUNCTION `nombreDemandesEnAttenteAncien` () RETURNS VARCHAR(255) CHARSET utf8mb4 COLLATE utf8mb4_general_ci  begin
    declare id int ;
    declare listeDemandes varchar(255) default '';
    declare fini boolean default false ;

    declare idDemandes cursor for 
        SELECT COUNT(DEMANDE.idDemande) FROM DEMANDE JOIN BONCOMMANDE ON DEMANDE.idDemande = BONCOMMANDE.idDemande WHERE BONCOMMANDE.idEtat = 1 ;

    declare continue handler for not found set fini = true ;
    open idDemandes ;
    while not fini do
        fetch idDemandes into id ;
        if not fini then 
            SET listeDemandes = id ;
        end if ;
    end while ;
    close idDemandes ;

    return listeDemandes ;
end$$

CREATE DEFINER=`blandeau`@`%` FUNCTION `recupereidMateriel` (`idMU` INT) RETURNS INT(11)  BEGIN
declare idM int;
SELECT idMateriel INTO idM FROM MATERIELUNIQUE WHERE idMaterielUnique = idMU ;
return idM;
end$$

CREATE DEFINER=`blandeau`@`%` FUNCTION `recupereStockLabo` (`idM` INT) RETURNS INT(11)  BEGIN
declare stock float;
SELECT quantiteLaboratoire INTO stock FROM STOCKLABORATOIRE WHERE idMateriel = idM ;
return stock;
end$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `2FA`
--

CREATE TABLE `2FA` (
  `email` varchar(50) NOT NULL,
  `uri` varchar(200) NOT NULL,
  `idUtilisateur` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `2FA`
--


-- --------------------------------------------------------

--
-- Table structure for table `AJOUTERMATERIEL`
--

CREATE TABLE `AJOUTERMATERIEL` (
  `idDemande` int(11) NOT NULL,
  `idMateriel` int(11) NOT NULL,
  `quantite` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `AJOUTERMATERIEL`
--



-- --------------------------------------------------------

--
-- Table structure for table `ALERTESENCOURS`
--

CREATE TABLE `ALERTESENCOURS` (
  `idAlerte` int(11) NOT NULL,
  `idMaterielUnique` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ALERTESENCOURS`
--

-- --------------------------------------------------------

--
-- Table structure for table `ARCHIVEBONCOMMANDE`
--

CREATE TABLE `ARCHIVEBONCOMMANDE` (
  `idArchiveBonCommande` int(11) NOT NULL,
  `idBonCommande` int(11) NOT NULL,
  `idEtat` int(11) NOT NULL,
  `idUtilisateur` int(11) NOT NULL,
  `dateArchiveBonCommande` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ARCHIVEBONCOMMANDE`
--



--
-- Triggers `ARCHIVEBONCOMMANDE`
--
DELIMITER $$
CREATE TRIGGER `archivageCommandes` AFTER INSERT ON `ARCHIVEBONCOMMANDE` FOR EACH ROW BEGIN
    declare idA int ;
    declare idM int ;
    declare qte int ;
    declare fini BOOLEAN default false;

    declare infosCommandes cursor for
        SELECT A.idArchiveBonCommande, C.idMateriel, C.quantite FROM COMMANDE C INNER JOIN ARCHIVEBONCOMMANDE A ON C.idBonCommande = A.idBonCommande WHERE A.idArchiveBonCommande =  new.idArchiveBonCommande ;
    
    declare continue handler for not found set fini = true ;
    open infosCommandes ;
    while not fini do
        fetch infosCommandes into idA, idM, qte ;
        if not fini then
            INSERT INTO ARCHIVECOMMANDE(idArchiveBonCommande, idMateriel, quantite) VALUES (idA, idM, qte) ;
        end if ;
    end while ;
    close infosCommandes ;
end
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `ARCHIVECOMMANDE`
--

CREATE TABLE `ARCHIVECOMMANDE` (
  `idArchiveBonCommande` int(11) NOT NULL,
  `idMateriel` int(11) NOT NULL,
  `quantite` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ARCHIVECOMMANDE`
--


-- --------------------------------------------------------

--
-- Table structure for table `ARCHIVECOMMANDEANCIEN`
--

CREATE TABLE `ARCHIVECOMMANDEANCIEN` (
  `numColis` int(11) NOT NULL,
  `idFournisseur` int(11) NOT NULL,
  `nomFournisseur` varchar(50) NOT NULL,
  `adresseFournisseur` varchar(50) NOT NULL,
  `mailFournisseur` varchar(50) NOT NULL,
  `telFournisseur` varchar(10) NOT NULL,
  `facture` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `BONCOMMANDE`
--

CREATE TABLE `BONCOMMANDE` (
  `idBonCommande` int(11) NOT NULL,
  `idEtat` int(11) NOT NULL,
  `idUtilisateur` int(11) NOT NULL,
  `dateBonCommande` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `BONCOMMANDE`
--


--
-- Triggers `BONCOMMANDE`
--
DELIMITER $$
CREATE TRIGGER `archivageBonCommande` AFTER UPDATE ON `BONCOMMANDE` FOR EACH ROW BEGIN 
    declare idBC int;
    declare idE int ;
    declare idU int ;
    declare d date ;
    declare fini BOOLEAN default false;

    declare infosBonCommande cursor for
        SELECT * FROM BONCOMMANDE WHERE idBonCommande = new.idBonCommande and idEtat = 4 ;
    
    declare continue handler for not found set fini = true ;
    open infosBonCommande ;
    while not fini do
        fetch infosBonCommande into idBC, idE, idU, d ;
        if not fini then
            INSERT INTO ARCHIVEBONCOMMANDE (idBonCommande, idEtat, idUtilisateur, dateArchiveBonCommande) VALUES (idBC, idE, idU, d) ;
        end if ;
    end while ;
    close infosBonCommande ;
end
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `CATEGORIE`
--

CREATE TABLE `CATEGORIE` (
  `idCategorie` int(11) NOT NULL,
  `idDomaine` int(11) NOT NULL,
  `nomCategorie` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `CATEGORIE`
--
-- --------------------------------------------------------

--
-- Table structure for table `COMMANDE`
--

CREATE TABLE `COMMANDE` (
  `idBonCommande` int(11) NOT NULL,
  `idMateriel` int(11) NOT NULL,
  `quantite` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `COMMANDE`
--



-- --------------------------------------------------------

--
-- Table structure for table `DEMANDE`
--

CREATE TABLE `DEMANDE` (
  `idDemande` int(11) NOT NULL,
  `idUtilisateur` int(11) NOT NULL,
  `descriptionDemande` varchar(2000) DEFAULT NULL,
  `idEtatD` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `DEMANDE`
--

--
-- Triggers `DEMANDE`
--
DELIMITER $$
CREATE TRIGGER `modifsSurDemandeUpdate` BEFORE UPDATE ON `DEMANDE` FOR EACH ROW begin
    declare presente int;
    declare mes varchar(255);

    SELECT COUNT(ifnull(DEMANDE.idDemande, 0)) into presente FROM DEMANDE WHERE DEMANDE.idDemande = new.idDemande AND idEtatD = 2;

    if presente > 0 then
        set mes = concat("La modification ne peut être effectuée sur la demande (id demande : ", new.idDemande,") car celle-ci est associée à un bon de commande.");
        signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
    end if;
end
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `DOMAINE`
--

CREATE TABLE `DOMAINE` (
  `idDomaine` int(11) NOT NULL,
  `nomDomaine` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `DOMAINE`
--

-- --------------------------------------------------------

--
-- Table structure for table `ENDROIT`
--

CREATE TABLE `ENDROIT` (
  `idEndroit` int(11) NOT NULL,
  `endroit` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ENDROIT`
--


-- --------------------------------------------------------

--
-- Table structure for table `ENVOIFOURNISSEUR`
--

CREATE TABLE `ENVOIFOURNISSEUR` (
  `idBonCommande` int(11) NOT NULL,
  `idFournisseur` int(11) NOT NULL,
  `facture` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ETATCOMMANDE`
--

CREATE TABLE `ETATCOMMANDE` (
  `idEtat` int(11) NOT NULL,
  `nomEtat` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ETATCOMMANDE`
--

-- --------------------------------------------------------

--
-- Table structure for table `ETATDEMANDE`
--

CREATE TABLE `ETATDEMANDE` (
  `idEtatD` int(11) NOT NULL,
  `nomEtatD` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ETATDEMANDE`
--

-- --------------------------------------------------------

--
-- Table structure for table `FDS`
--

CREATE TABLE `FDS` (
  `idFDS` int(11) NOT NULL,
  `nomFDS` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `FDS`
--

-- --------------------------------------------------------

--
-- Table structure for table `FOURNISSEUR`
--

CREATE TABLE `FOURNISSEUR` (
  `idFournisseur` int(11) NOT NULL,
  `nomFournisseur` varchar(50) DEFAULT NULL,
  `adresseFournisseur` varchar(50) DEFAULT NULL,
  `mailFournisseur` varchar(50) DEFAULT NULL,
  `telFournisseur` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `MATERIEL`
--

CREATE TABLE `MATERIEL` (
  `idMateriel` int(11) NOT NULL,
  `referenceMateriel` varchar(50) NOT NULL,
  `idFDS` int(11) DEFAULT NULL,
  `nomMateriel` varchar(50) NOT NULL,
  `idCategorie` int(11) NOT NULL,
  `seuilAlerte` int(11) DEFAULT NULL,
  `caracteristiquesComplementaires` varchar(2000) DEFAULT NULL,
  `informationsComplementairesEtSecurite` varchar(2000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `MATERIEL`
--

-- --------------------------------------------------------

--
-- Table structure for table `MATERIELUNIQUE`
--

CREATE TABLE `MATERIELUNIQUE` (
  `idMaterielUnique` int(11) NOT NULL,
  `idMateriel` int(11) NOT NULL,
  `idRangement` int(11) NOT NULL,
  `dateReception` datetime NOT NULL,
  `commentaireMateriel` varchar(100) DEFAULT NULL,
  `quantiteApproximative` float DEFAULT NULL,
  `datePeremption` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `MATERIELUNIQUE`
--

-- --------------------------------------------------------

--
-- Table structure for table `RANGEMENT`
--

CREATE TABLE `RANGEMENT` (
  `idRangement` int(11) NOT NULL,
  `idEndroit` int(11) NOT NULL,
  `position` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `RANGEMENT`
--

-- --------------------------------------------------------

--
-- Table structure for table `RECHERCHEMATERIELS`
--

CREATE TABLE `RECHERCHEMATERIELS` (
  `materielRecherche` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `RECHERCHEMATERIELS`
--

-- --------------------------------------------------------

--
-- Table structure for table `RESERVELABORATOIRE`
--

CREATE TABLE `RESERVELABORATOIRE` (
  `idReserve` int(11) NOT NULL,
  `idMaterielUnique` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `RESERVELABORATOIRE`
--


--
-- Triggers `RESERVELABORATOIRE`
--
DELIMITER $$
CREATE TRIGGER `modificationStockLaboDelete` AFTER DELETE ON `RESERVELABORATOIRE` FOR EACH ROW BEGIN
    declare idM INT;
    declare stock INT;
    declare fini BOOLEAN default false;

    declare curseur cursor for
        SELECT idMateriel FROM MATERIELUNIQUE WHERE idMaterielUnique = old.idMaterielUnique;

    declare continue handler for not found set fini = true ;

    open curseur;

    boucle: loop
        fetch curseur into idM;
        if fini then
            LEAVE boucle;
        end if;

        SELECT quantiteLaboratoire INTO stock FROM STOCKLABORATOIRE WHERE idMateriel = idM;

        if stock - 1 > 0 then
            UPDATE STOCKLABORATOIRE SET quantiteLaboratoire = stock - 1 WHERE idMateriel = idM;
        end if;
    end loop;
    close curseur;
end
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `modificationStockLaboInsert` AFTER INSERT ON `RESERVELABORATOIRE` FOR EACH ROW BEGIN
    declare idM INT;
    declare stock INT;
    declare fini BOOLEAN default false;

    declare curseur cursor for
        SELECT idMateriel FROM MATERIELUNIQUE WHERE idMaterielUnique = new.idMaterielUnique;

    declare continue handler for not found set fini = true ;

    open curseur;

    boucle: loop
        fetch curseur into idM;
        if fini then
            LEAVE boucle;
        end if;

        SELECT quantiteLaboratoire INTO stock FROM STOCKLABORATOIRE WHERE idMateriel = idM;

        if stock is null then
            INSERT INTO STOCKLABORATOIRE (idMateriel, quantiteLaboratoire) VALUES (idM, 1);
        else
            UPDATE STOCKLABORATOIRE SET quantiteLaboratoire = stock + 1 WHERE idMateriel = idM;
        end if;
    end loop;
    close curseur;
end
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `modificationStockLaboUpdate` AFTER UPDATE ON `RESERVELABORATOIRE` FOR EACH ROW BEGIN
    declare idM INT;
    declare stock INT;
    declare fini BOOLEAN default false;

    declare curseur cursor for
        SELECT idMateriel FROM MATERIELUNIQUE WHERE idMaterielUnique = new.idMaterielUnique;

    declare continue handler for not found set fini = true ;

    open curseur;

    boucle: loop
        fetch curseur into idM;
        if fini then
            LEAVE boucle;
        end if;

        SELECT quantiteLaboratoire INTO stock FROM STOCKLABORATOIRE WHERE idMateriel = idM;

        if stock is null then
            INSERT INTO STOCKLABORATOIRE (idMateriel, quantiteLaboratoire) VALUES (idM, 1);
        else
            UPDATE STOCKLABORATOIRE SET quantiteLaboratoire = stock + 1 WHERE idMateriel = idM;
        end if;
    end loop;
    close curseur;
end
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `RISQUE`
--

CREATE TABLE `RISQUE` (
  `idRisque` int(11) NOT NULL,
  `nomRisque` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `RISQUE`
--



-- --------------------------------------------------------

--
-- Table structure for table `RISQUES`
--

CREATE TABLE `RISQUES` (
  `idrisques` int(11) NOT NULL,
  `idFDS` int(11) NOT NULL,
  `idRisque` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `RISQUES`
--

-- --------------------------------------------------------

--
-- Table structure for table `STATUT`
--

CREATE TABLE `STATUT` (
  `idStatut` int(11) NOT NULL,
  `nomStatut` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `STATUT`
--


-- --------------------------------------------------------

--
-- Table structure for table `STOCKLABORATOIRE`
--

CREATE TABLE `STOCKLABORATOIRE` (
  `idStock` int(11) NOT NULL,
  `idMateriel` int(11) NOT NULL,
  `quantiteLaboratoire` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `STOCKLABORATOIRE`
--


-- --------------------------------------------------------

--
-- Table structure for table `SUIVICOMMANDE`
--

CREATE TABLE `SUIVICOMMANDE` (
  `idBonCommande` int(11) NOT NULL,
  `localisation` varchar(50) NOT NULL,
  `numColis` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `TYPESALERTES`
--

CREATE TABLE `TYPESALERTES` (
  `idAlerte` int(11) NOT NULL,
  `descriptionAlerte` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `TYPESALERTES`
--


-- --------------------------------------------------------

--
-- Table structure for table `UTILISATEUR`
--

CREATE TABLE `UTILISATEUR` (
  `idUtilisateur` int(11) NOT NULL,
  `idStatut` int(11) NOT NULL,
  `nom` varchar(50) NOT NULL,
  `prenom` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `motDePasse` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `UTILISATEUR`
--


--
-- Triggers `UTILISATEUR`
--
DELIMITER $$
CREATE TRIGGER `emailUtilisateurUniqueInsert` BEFORE INSERT ON `UTILISATEUR` FOR EACH ROW begin
    declare compteur int;
    declare mes varchar(255);
    SELECT COUNT(*) INTO compteur from UTILISATEUR WHERE email = new.email;
    if compteur > 0 then
        set mes = concat("L'email ", new.email, " est déjà utilisé.");
        signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
    end if;
end
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `emailUtilisateurUniqueUpdate` BEFORE UPDATE ON `UTILISATEUR` FOR EACH ROW begin
    declare compteur int;
    declare mes varchar(255);
    SELECT COUNT(*) INTO compteur from UTILISATEUR WHERE email = new.email;
    if compteur > 0 then
        if old.email <> new.email then 
            set mes = concat("L'email ", new.email, " est déjà utilisé.");
        signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
        end if;
    end if;
end
$$
DELIMITER ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `2FA`
--
ALTER TABLE `2FA`
  ADD PRIMARY KEY (`email`,`idUtilisateur`),
  ADD KEY `idUtilisateur` (`idUtilisateur`);

--
-- Indexes for table `AJOUTERMATERIEL`
--
ALTER TABLE `AJOUTERMATERIEL`
  ADD PRIMARY KEY (`idDemande`,`idMateriel`),
  ADD KEY `idMateriel` (`idMateriel`);

--
-- Indexes for table `ALERTESENCOURS`
--
ALTER TABLE `ALERTESENCOURS`
  ADD PRIMARY KEY (`idAlerte`,`idMaterielUnique`),
  ADD KEY `idMaterielUnique` (`idMaterielUnique`);

--
-- Indexes for table `ARCHIVEBONCOMMANDE`
--
ALTER TABLE `ARCHIVEBONCOMMANDE`
  ADD PRIMARY KEY (`idArchiveBonCommande`);

--
-- Indexes for table `ARCHIVECOMMANDE`
--
ALTER TABLE `ARCHIVECOMMANDE`
  ADD PRIMARY KEY (`idArchiveBonCommande`,`idMateriel`);

--
-- Indexes for table `ARCHIVECOMMANDEANCIEN`
--
ALTER TABLE `ARCHIVECOMMANDEANCIEN`
  ADD PRIMARY KEY (`numColis`);

--
-- Indexes for table `BONCOMMANDE`
--
ALTER TABLE `BONCOMMANDE`
  ADD PRIMARY KEY (`idBonCommande`),
  ADD KEY `idEtat` (`idEtat`),
  ADD KEY `idUtilisateur` (`idUtilisateur`);

--
-- Indexes for table `CATEGORIE`
--
ALTER TABLE `CATEGORIE`
  ADD PRIMARY KEY (`idCategorie`),
  ADD KEY `idDomaine` (`idDomaine`);

--
-- Indexes for table `COMMANDE`
--
ALTER TABLE `COMMANDE`
  ADD PRIMARY KEY (`idBonCommande`,`idMateriel`),
  ADD KEY `idMateriel` (`idMateriel`);

--
-- Indexes for table `DEMANDE`
--
ALTER TABLE `DEMANDE`
  ADD PRIMARY KEY (`idDemande`),
  ADD KEY `idUtilisateur` (`idUtilisateur`),
  ADD KEY `idEtatD` (`idEtatD`);

--
-- Indexes for table `DOMAINE`
--
ALTER TABLE `DOMAINE`
  ADD PRIMARY KEY (`idDomaine`),
  ADD UNIQUE KEY `nomDomaine` (`nomDomaine`);

--
-- Indexes for table `ENDROIT`
--
ALTER TABLE `ENDROIT`
  ADD PRIMARY KEY (`idEndroit`),
  ADD UNIQUE KEY `endroit` (`endroit`);

--
-- Indexes for table `ENVOIFOURNISSEUR`
--
ALTER TABLE `ENVOIFOURNISSEUR`
  ADD PRIMARY KEY (`idBonCommande`,`idFournisseur`),
  ADD KEY `idFournisseur` (`idFournisseur`);

--
-- Indexes for table `ETATCOMMANDE`
--
ALTER TABLE `ETATCOMMANDE`
  ADD PRIMARY KEY (`idEtat`);

--
-- Indexes for table `ETATDEMANDE`
--
ALTER TABLE `ETATDEMANDE`
  ADD PRIMARY KEY (`idEtatD`);

--
-- Indexes for table `FDS`
--
ALTER TABLE `FDS`
  ADD PRIMARY KEY (`idFDS`),
  ADD UNIQUE KEY `nomFDS` (`nomFDS`);

--
-- Indexes for table `FOURNISSEUR`
--
ALTER TABLE `FOURNISSEUR`
  ADD PRIMARY KEY (`idFournisseur`),
  ADD UNIQUE KEY `mailFournisseur` (`mailFournisseur`),
  ADD UNIQUE KEY `telFournisseur` (`telFournisseur`);

--
-- Indexes for table `MATERIEL`
--
ALTER TABLE `MATERIEL`
  ADD PRIMARY KEY (`idMateriel`),
  ADD UNIQUE KEY `nomMateriel` (`nomMateriel`),
  ADD UNIQUE KEY `referenceMateriel` (`referenceMateriel`),
  ADD KEY `idFDS` (`idFDS`),
  ADD KEY `idCategorie` (`idCategorie`);

--
-- Indexes for table `MATERIELUNIQUE`
--
ALTER TABLE `MATERIELUNIQUE`
  ADD PRIMARY KEY (`idMaterielUnique`),
  ADD KEY `idMateriel` (`idMateriel`),
  ADD KEY `idRangement` (`idRangement`);

--
-- Indexes for table `RANGEMENT`
--
ALTER TABLE `RANGEMENT`
  ADD PRIMARY KEY (`idRangement`),
  ADD KEY `idEndroit` (`idEndroit`);

--
-- Indexes for table `RECHERCHEMATERIELS`
--
ALTER TABLE `RECHERCHEMATERIELS`
  ADD PRIMARY KEY (`materielRecherche`);

--
-- Indexes for table `RESERVELABORATOIRE`
--
ALTER TABLE `RESERVELABORATOIRE`
  ADD PRIMARY KEY (`idReserve`,`idMaterielUnique`),
  ADD KEY `idMaterielUnique` (`idMaterielUnique`);

--
-- Indexes for table `RISQUE`
--
ALTER TABLE `RISQUE`
  ADD PRIMARY KEY (`idRisque`);

--
-- Indexes for table `RISQUES`
--
ALTER TABLE `RISQUES`
  ADD PRIMARY KEY (`idrisques`),
  ADD KEY `idFDS` (`idFDS`),
  ADD KEY `idRisque` (`idRisque`);

--
-- Indexes for table `STATUT`
--
ALTER TABLE `STATUT`
  ADD PRIMARY KEY (`idStatut`);

--
-- Indexes for table `STOCKLABORATOIRE`
--
ALTER TABLE `STOCKLABORATOIRE`
  ADD PRIMARY KEY (`idStock`),
  ADD KEY `idMateriel` (`idMateriel`);

--
-- Indexes for table `SUIVICOMMANDE`
--
ALTER TABLE `SUIVICOMMANDE`
  ADD PRIMARY KEY (`idBonCommande`,`numColis`);

--
-- Indexes for table `TYPESALERTES`
--
ALTER TABLE `TYPESALERTES`
  ADD PRIMARY KEY (`idAlerte`);

--
-- Indexes for table `UTILISATEUR`
--
ALTER TABLE `UTILISATEUR`
  ADD PRIMARY KEY (`idUtilisateur`),
  ADD KEY `idStatut` (`idStatut`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `ARCHIVEBONCOMMANDE`
--
ALTER TABLE `ARCHIVEBONCOMMANDE`
  MODIFY `idArchiveBonCommande` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `BONCOMMANDE`
--
ALTER TABLE `BONCOMMANDE`
  MODIFY `idBonCommande` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT for table `CATEGORIE`
--
ALTER TABLE `CATEGORIE`
  MODIFY `idCategorie` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT for table `DEMANDE`
--
ALTER TABLE `DEMANDE`
  MODIFY `idDemande` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `DOMAINE`
--
ALTER TABLE `DOMAINE`
  MODIFY `idDomaine` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `ENDROIT`
--
ALTER TABLE `ENDROIT`
  MODIFY `idEndroit` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `ETATCOMMANDE`
--
ALTER TABLE `ETATCOMMANDE`
  MODIFY `idEtat` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `ETATDEMANDE`
--
ALTER TABLE `ETATDEMANDE`
  MODIFY `idEtatD` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `FDS`
--
ALTER TABLE `FDS`
  MODIFY `idFDS` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `FOURNISSEUR`
--
ALTER TABLE `FOURNISSEUR`
  MODIFY `idFournisseur` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `MATERIEL`
--
ALTER TABLE `MATERIEL`
  MODIFY `idMateriel` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT for table `MATERIELUNIQUE`
--
ALTER TABLE `MATERIELUNIQUE`
  MODIFY `idMaterielUnique` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=292;

--
-- AUTO_INCREMENT for table `RANGEMENT`
--
ALTER TABLE `RANGEMENT`
  MODIFY `idRangement` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `RESERVELABORATOIRE`
--
ALTER TABLE `RESERVELABORATOIRE`
  MODIFY `idReserve` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=116;

--
-- AUTO_INCREMENT for table `RISQUE`
--
ALTER TABLE `RISQUE`
  MODIFY `idRisque` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;

--
-- AUTO_INCREMENT for table `RISQUES`
--
ALTER TABLE `RISQUES`
  MODIFY `idrisques` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=459;

--
-- AUTO_INCREMENT for table `STOCKLABORATOIRE`
--
ALTER TABLE `STOCKLABORATOIRE`
  MODIFY `idStock` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT for table `UTILISATEUR`
--
ALTER TABLE `UTILISATEUR`
  MODIFY `idUtilisateur` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `2FA`
--
ALTER TABLE `2FA`
  ADD CONSTRAINT `2FA_ibfk_1` FOREIGN KEY (`idUtilisateur`) REFERENCES `UTILISATEUR` (`idUtilisateur`);

--
-- Constraints for table `AJOUTERMATERIEL`
--
ALTER TABLE `AJOUTERMATERIEL`
  ADD CONSTRAINT `AJOUTERMATERIEL_ibfk_1` FOREIGN KEY (`idDemande`) REFERENCES `DEMANDE` (`idDemande`),
  ADD CONSTRAINT `AJOUTERMATERIEL_ibfk_2` FOREIGN KEY (`idMateriel`) REFERENCES `MATERIEL` (`idMateriel`);

--
-- Constraints for table `ALERTESENCOURS`
--
ALTER TABLE `ALERTESENCOURS`
  ADD CONSTRAINT `ALERTESENCOURS_ibfk_1` FOREIGN KEY (`idAlerte`) REFERENCES `TYPESALERTES` (`idAlerte`),
  ADD CONSTRAINT `ALERTESENCOURS_ibfk_2` FOREIGN KEY (`idMaterielUnique`) REFERENCES `MATERIELUNIQUE` (`idMaterielUnique`);

--
-- Constraints for table `ARCHIVECOMMANDE`
--
ALTER TABLE `ARCHIVECOMMANDE`
  ADD CONSTRAINT `ARCHIVECOMMANDE_ibfk_1` FOREIGN KEY (`idArchiveBonCommande`) REFERENCES `ARCHIVEBONCOMMANDE` (`idArchiveBonCommande`);

--
-- Constraints for table `BONCOMMANDE`
--
ALTER TABLE `BONCOMMANDE`
  ADD CONSTRAINT `BONCOMMANDE_ibfk_1` FOREIGN KEY (`idEtat`) REFERENCES `ETATCOMMANDE` (`idEtat`),
  ADD CONSTRAINT `BONCOMMANDE_ibfk_2` FOREIGN KEY (`idUtilisateur`) REFERENCES `UTILISATEUR` (`idUtilisateur`);

--
-- Constraints for table `CATEGORIE`
--
ALTER TABLE `CATEGORIE`
  ADD CONSTRAINT `CATEGORIE_ibfk_1` FOREIGN KEY (`idDomaine`) REFERENCES `DOMAINE` (`idDomaine`);

--
-- Constraints for table `COMMANDE`
--
ALTER TABLE `COMMANDE`
  ADD CONSTRAINT `COMMANDE_ibfk_1` FOREIGN KEY (`idBonCommande`) REFERENCES `BONCOMMANDE` (`idBonCommande`),
  ADD CONSTRAINT `COMMANDE_ibfk_2` FOREIGN KEY (`idMateriel`) REFERENCES `MATERIEL` (`idMateriel`);

--
-- Constraints for table `DEMANDE`
--
ALTER TABLE `DEMANDE`
  ADD CONSTRAINT `DEMANDE_ibfk_1` FOREIGN KEY (`idUtilisateur`) REFERENCES `UTILISATEUR` (`idUtilisateur`),
  ADD CONSTRAINT `DEMANDE_ibfk_2` FOREIGN KEY (`idEtatD`) REFERENCES `ETATDEMANDE` (`idEtatD`);

--
-- Constraints for table `ENVOIFOURNISSEUR`
--
ALTER TABLE `ENVOIFOURNISSEUR`
  ADD CONSTRAINT `ENVOIFOURNISSEUR_ibfk_1` FOREIGN KEY (`idBonCommande`) REFERENCES `BONCOMMANDE` (`idBonCommande`),
  ADD CONSTRAINT `ENVOIFOURNISSEUR_ibfk_2` FOREIGN KEY (`idFournisseur`) REFERENCES `FOURNISSEUR` (`idFournisseur`);

--
-- Constraints for table `MATERIEL`
--
ALTER TABLE `MATERIEL`
  ADD CONSTRAINT `MATERIEL_ibfk_1` FOREIGN KEY (`idFDS`) REFERENCES `FDS` (`idFDS`),
  ADD CONSTRAINT `MATERIEL_ibfk_2` FOREIGN KEY (`idCategorie`) REFERENCES `CATEGORIE` (`idCategorie`);

--
-- Constraints for table `MATERIELUNIQUE`
--
ALTER TABLE `MATERIELUNIQUE`
  ADD CONSTRAINT `MATERIELUNIQUE_ibfk_1` FOREIGN KEY (`idMateriel`) REFERENCES `MATERIEL` (`idMateriel`),
  ADD CONSTRAINT `MATERIELUNIQUE_ibfk_2` FOREIGN KEY (`idRangement`) REFERENCES `RANGEMENT` (`idRangement`);

--
-- Constraints for table `RANGEMENT`
--
ALTER TABLE `RANGEMENT`
  ADD CONSTRAINT `RANGEMENT_ibfk_1` FOREIGN KEY (`idEndroit`) REFERENCES `ENDROIT` (`idEndroit`);

--
-- Constraints for table `RESERVELABORATOIRE`
--
ALTER TABLE `RESERVELABORATOIRE`
  ADD CONSTRAINT `RESERVELABORATOIRE_ibfk_1` FOREIGN KEY (`idMaterielUnique`) REFERENCES `MATERIELUNIQUE` (`idMaterielUnique`);

--
-- Constraints for table `RISQUES`
--
ALTER TABLE `RISQUES`
  ADD CONSTRAINT `RISQUES_ibfk_1` FOREIGN KEY (`idFDS`) REFERENCES `FDS` (`idFDS`),
  ADD CONSTRAINT `RISQUES_ibfk_2` FOREIGN KEY (`idRisque`) REFERENCES `RISQUE` (`idRisque`);

--
-- Constraints for table `STOCKLABORATOIRE`
--
ALTER TABLE `STOCKLABORATOIRE`
  ADD CONSTRAINT `STOCKLABORATOIRE_ibfk_1` FOREIGN KEY (`idMateriel`) REFERENCES `MATERIEL` (`idMateriel`);

--
-- Constraints for table `SUIVICOMMANDE`
--
ALTER TABLE `SUIVICOMMANDE`
  ADD CONSTRAINT `SUIVICOMMANDE_ibfk_1` FOREIGN KEY (`idBonCommande`) REFERENCES `BONCOMMANDE` (`idBonCommande`);

--
-- Constraints for table `UTILISATEUR`
--
ALTER TABLE `UTILISATEUR`
  ADD CONSTRAINT `UTILISATEUR_ibfk_1` FOREIGN KEY (`idStatut`) REFERENCES `STATUT` (`idStatut`);

DELIMITER $$
--
-- Events
--
CREATE DEFINER=`blandeau`@`%` EVENT `insereAlertesAuto` ON SCHEDULE EVERY 1 MINUTE STARTS '2023-12-21 15:26:08' ON COMPLETION NOT PRESERVE ENABLE DO BEGIN
    DELETE FROM ALERTESENCOURS ;
    INSERT INTO debug VALUES ("test") ;
    call alertesPeremption() ;
    call alertesPeremptionDixJours() ;
    call alertesQuantiteAZero() ;
    call alertesQuantiteSeuil() ;
end$$

DELIMITER ;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
