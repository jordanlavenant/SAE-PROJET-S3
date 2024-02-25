-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: mysql-blandeau.alwaysdata.net
-- Generation Time: Feb 23, 2024 at 02:26 PM
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
-- Database: `blandeau_gestlab25`
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

INSERT INTO `2FA` (`email`, `uri`, `idUtilisateur`) VALUES
('erwan34230@gmail.com', 'ZXRI3DFAW2NDP3IYB75BYWMZZUGGTPYX', 16),
('jordan.lavenant@laposte.net', 'YFDQPDDP3EM2H3I5NKXOTMPYPT5BR5YQ', 14),
('kubik.deux@gmail.com', 'YQFFDFPMIFMSYPDDPVG7D5VI36IDCH3D', 18),
('kubikcube18@gmail.com', 'RXN2FXUYFXD5IN6Z7WM7QPQMPWVSOU6F', 15),
('leo.lucidor@gmail.com', 'KDKCGJ552QD7KP7S2IQBWQBWASCKNTGZ', 17),
('towkyofn@gmail.com', 'FMGOUYA6ZB4JPMTKIUQX6DYFEHORITPV', 19);

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

INSERT INTO `AJOUTERMATERIEL` (`idDemande`, `idMateriel`, `quantite`) VALUES
(104, 34, 1);

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

INSERT INTO `ALERTESENCOURS` (`idAlerte`, `idMaterielUnique`) VALUES
(1, 276),
(1, 277),
(1, 278),
(1, 279),
(1, 280),
(1, 281),
(1, 282),
(1, 283),
(1, 284),
(1, 285),
(1, 286),
(1, 287),
(1, 289);

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

INSERT INTO `ARCHIVEBONCOMMANDE` (`idArchiveBonCommande`, `idBonCommande`, `idEtat`, `idUtilisateur`, `dateArchiveBonCommande`) VALUES
(8, 27, 4, 2, '2024-01-11'),
(9, 32, 4, 2, '2024-01-15'),
(10, 33, 4, 2, '2024-01-15'),
(11, 40, 4, 2, '0000-00-00'),
(12, 50, 4, 17, '2024-02-23');

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

INSERT INTO `ARCHIVECOMMANDE` (`idArchiveBonCommande`, `idMateriel`, `quantite`) VALUES
(10, 34, 50),
(10, 35, 1),
(10, 38, 10),
(11, 34, 10),
(11, 36, 1),
(11, 38, 2),
(11, 39, 1),
(12, 40, 1);

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

INSERT INTO `BONCOMMANDE` (`idBonCommande`, `idEtat`, `idUtilisateur`, `dateBonCommande`) VALUES
(31, 1, 11, '2024-01-12'),
(48, 1, 14, '2024-02-22'),
(50, 4, 17, '2024-02-23'),
(51, 1, 17, '2024-02-23');

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

INSERT INTO `CATEGORIE` (`idCategorie`, `idDomaine`, `nomCategorie`) VALUES
(1, 1, 'Observation'),
(2, 1, 'Mesures'),
(3, 1, 'ExAO'),
(4, 1, 'Multimédia'),
(5, 1, 'Expérimentation'),
(6, 1, 'Divers'),
(7, 6, 'Verrerie'),
(8, 6, 'Associés'),
(9, 5, 'Produits organiques'),
(10, 5, 'Produits minéraux'),
(11, 5, 'Enzymes'),
(12, 5, 'Colorants'),
(13, 5, 'Entretien'),
(14, 5, 'Autres'),
(15, 3, 'Appareils de labo'),
(16, 3, 'Sécurité'),
(17, 3, 'Fournitures'),
(18, 3, 'Mobilier'),
(19, 3, 'Divers'),
(20, 4, 'Logiciels'),
(21, 4, 'DVD/VHS'),
(22, 4, 'Manuels scolaires'),
(23, 4, 'Livres scientifiques'),
(24, 4, 'Cartes/Posters'),
(25, 4, 'Divers'),
(26, 2, 'Générateurs'),
(27, 2, 'Mesures'),
(28, 2, 'Récepteurs'),
(29, 2, 'Connectique'),
(30, 2, 'Métaux'),
(31, 2, 'Divers');

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

INSERT INTO `COMMANDE` (`idBonCommande`, `idMateriel`, `quantite`) VALUES
(48, 35, 1),
(50, 40, 1),
(51, 38, 2);

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

INSERT INTO `DEMANDE` (`idDemande`, `idUtilisateur`, `descriptionDemande`, `idEtatD`) VALUES
(30, 7, '', 2),
(32, 16, NULL, 1),
(33, 18, NULL, 1),
(34, 7, NULL, 2),
(35, 7, NULL, 2),
(36, 7, NULL, 2),
(38, 7, NULL, 2),
(39, 7, NULL, 2),
(40, 7, NULL, 2),
(100, 7, NULL, 2),
(101, 7, NULL, 2),
(104, 7, NULL, 2),
(106, 7, NULL, 1);

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

INSERT INTO `DOMAINE` (`idDomaine`, `nomDomaine`) VALUES
(1, 'Appareillage'),
(2, 'Électricité'),
(3, 'Matériel de laboratoire'),
(4, 'Médias'),
(5, 'Produits chimiques'),
(6, 'Verrerie et associés');

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

INSERT INTO `ENDROIT` (`idEndroit`, `endroit`) VALUES
(6, '8'),
(3, 'Armoire 1'),
(1, 'Étagère 1'),
(2, 'Étagère 2'),
(4, 'Etagere 5'),
(5, 'Salle 207'),
(7, 'test');

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

INSERT INTO `ETATCOMMANDE` (`idEtat`, `nomEtat`) VALUES
(1, 'En attente de la validation du Gestionnaire'),
(2, 'En cours de traitement'),
(3, 'Expédiée'),
(4, 'Livrée');

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

INSERT INTO `ETATDEMANDE` (`idEtatD`, `nomEtatD`) VALUES
(1, 'En attente de validation'),
(2, 'Envoyée');

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

INSERT INTO `FDS` (`idFDS`, `nomFDS`) VALUES
(29, 'Acide chloridrique'),
(25, 'Alimentation et Générateur de courant AC/DC'),
(33, 'AUTRE AUTRE BECHER'),
(32, 'AUTRE BECHER'),
(28, 'Becher 500ml'),
(26, 'Becher 800ml'),
(31, 'BECHERRRR'),
(30, 'clavier'),
(34, 'generateur test'),
(20, 'iPad'),
(8, 'iPhone'),
(11, 'JLK'),
(23, 'Microscope'),
(27, 'Pipette graduée'),
(24, 'Sulfate de cuivre anhydre'),
(21, 'test'),
(22, 'test2');

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

INSERT INTO `MATERIEL` (`idMateriel`, `referenceMateriel`, `idFDS`, `nomMateriel`, `idCategorie`, `seuilAlerte`, `caracteristiquesComplementaires`, `informationsComplementairesEtSecurite`) VALUES
(34, 'REF123', 24, 'Sulfate de cuivre anhydree', 9, 2, 'Sulfate de cuivre anhydre', 'Le sulfate de cuivre (II) anhydre est blanc et ne devient bleu que lorsqu\'il est combiné avec des molécules d\'eau'),
(35, 'ALR 3002M', 25, 'Alimentation et Générateur de courant AC/DC', 26, 1, 'Puissance : 120 Watts', ''),
(36, 'REF 4123', 26, 'Becher 800ml', 7, 1, 'Becher 800ml', 'aehahahahhaha'),
(38, 'REF 4122', 28, 'Becher 500ml', 7, 1, 'Becher 500ml', ''),
(39, 'REF 1111', 29, 'Acide chloridrique', 13, 1, '', ''),
(40, '6546', 30, 'clavier', 26, 2, 'ezrzet', 'rtert'),
(44, '1234', 34, 'generateur test', 26, 1, '', '');

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

INSERT INTO `MATERIELUNIQUE` (`idMaterielUnique`, `idMateriel`, `idRangement`, `dateReception`, `commentaireMateriel`, `quantiteApproximative`, `datePeremption`) VALUES
(255, 34, 1, '2024-01-14 00:00:00', '', 1, '2024-07-26 00:00:00'),
(256, 34, 1, '2024-01-14 00:00:00', '', 1, '2024-07-26 00:00:00'),
(257, 40, 5, '2024-02-19 00:00:00', 'un clavier supersonique', 2, '2024-07-20 00:00:00'),
(258, 40, 5, '2024-02-19 00:00:00', 'un clavier supersonique', 2, '2024-07-20 00:00:00'),
(259, 40, 5, '2024-02-19 00:00:00', 'un clavier supersonique', 2, '2024-07-20 00:00:00'),
(260, 40, 5, '2024-02-19 00:00:00', 'un clavier supersonique', 2, '2024-07-20 00:00:00'),
(261, 40, 5, '2024-02-19 00:00:00', 'un clavier supersonique', 2, '2024-07-20 00:00:00'),
(262, 40, 5, '2024-02-19 00:00:00', 'un clavier supersonique', 2, '2024-07-20 00:00:00'),
(263, 40, 5, '2024-02-19 00:00:00', 'un clavier supersonique', 2, '2024-07-20 00:00:00'),
(264, 40, 5, '2024-02-19 00:00:00', 'un clavier supersonique', 2, '2024-07-20 00:00:00'),
(265, 40, 5, '2024-02-19 00:00:00', 'un clavier supersonique', 2, '2024-07-20 00:00:00'),
(266, 40, 5, '2024-02-19 00:00:00', 'un clavier supersonique', 2, '2024-07-20 00:00:00'),
(267, 40, 5, '2024-02-19 00:00:00', 'un clavier supersonique', 2, '2024-07-20 00:00:00'),
(268, 40, 5, '2024-02-19 00:00:00', 'un clavier supersonique', 2, '2024-07-20 00:00:00'),
(269, 40, 5, '2024-02-19 00:00:00', 'un clavier supersonique', 2, '2024-07-20 00:00:00'),
(270, 40, 5, '2024-02-19 00:00:00', 'un clavier supersonique', 2, '2024-07-20 00:00:00'),
(271, 40, 5, '2024-02-19 00:00:00', 'un clavier supersonique', 2, '2024-07-20 00:00:00'),
(272, 40, 5, '2024-02-19 00:00:00', 'un clavier supersonique', 2, '2024-07-20 00:00:00'),
(273, 40, 5, '2024-02-19 00:00:00', 'un clavier supersonique', 2, '2024-07-20 00:00:00'),
(274, 40, 5, '2024-02-19 00:00:00', 'un clavier supersonique', 2, '2024-07-20 00:00:00'),
(275, 40, 5, '2024-02-19 00:00:00', 'un clavier supersonique', 2, '2024-07-20 00:00:00'),
(276, 40, 8, '2024-02-19 00:00:00', 'un clavier supersonique', 2, '2024-02-20 00:00:00'),
(277, 36, 3, '2024-02-19 00:00:00', '', 1, '2024-02-20 00:00:00'),
(278, 36, 3, '2024-02-19 00:00:00', '', 1, '2024-02-20 00:00:00'),
(279, 36, 3, '2024-02-19 00:00:00', '', 1, '2024-02-20 00:00:00'),
(280, 36, 3, '2024-02-19 00:00:00', '', 1, '2024-02-20 00:00:00'),
(281, 36, 3, '2024-02-19 00:00:00', '', 1, '2024-02-20 00:00:00'),
(282, 36, 3, '2024-02-19 00:00:00', '', 1, '2024-02-20 00:00:00'),
(283, 36, 3, '2024-02-19 00:00:00', '', 1, '2024-02-20 00:00:00'),
(284, 36, 3, '2024-02-19 00:00:00', '', 1, '2024-02-20 00:00:00'),
(285, 36, 3, '2024-02-19 00:00:00', '', 1, '2024-02-20 00:00:00'),
(286, 36, 3, '2024-02-19 00:00:00', '', 1, '2024-02-20 00:00:00'),
(287, 35, 6, '2024-02-19 00:00:00', '', 1, '2024-02-20 00:00:00'),
(289, 38, 3, '2024-02-22 00:00:00', 'un becher ta vu', 1, '2024-02-23 00:00:00'),
(291, 35, 8, '2024-02-23 00:00:00', '', 1, '2024-11-24 00:00:00'),
(292, 35, 8, '2024-02-23 00:00:00', '', 1, '2024-11-24 00:00:00');

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

INSERT INTO `RANGEMENT` (`idRangement`, `idEndroit`, `position`) VALUES
(1, 1, 'haut'),
(2, 2, 'bas'),
(3, 3, 'gauche'),
(4, 2, 'droite'),
(5, 1, 'milieu'),
(6, 3, 'milieu'),
(7, 4, 'Rac 87'),
(8, 5, 'Tiroir du bureau'),
(9, 3, 'droite'),
(10, 6, 'bocale'),
(11, 7, 'test1');

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

INSERT INTO `RECHERCHEMATERIELS` (`materielRecherche`) VALUES
('Agitateurs à hélice'),
('Agitateurs à plaques chauffantes'),
('Agitateurs à ultrasons'),
('Agitateurs magnétiques'),
('Agitateurs vortex'),
('Ampoules à décanter'),
('Autoclaves'),
('Bains-marie'),
('Ballons de réaction'),
('Béchers'),
('Béchers Griffin'),
('Boîtes cryogéniques'),
('Boîtes de Pétri'),
('Bouchons en caoutchouc'),
('Bouchons en liège'),
('Burettes'),
('Capsules de pesée'),
('Colonnes de chromatographie'),
('Colonnes de fractionnement'),
('Cuvettes de conductimètre'),
('Cuvettes de fluorimètre'),
('Cuvettes de polarimètre'),
('Cuvettes de spectrophotomètre'),
('Cuvettes de viscosimètre'),
('Cylindres gradués'),
('Deshydrateurs d\'air'),
('Entonnoirs'),
('Éprouvettes'),
('Filtres Buchner'),
('Fioles à col large'),
('Fioles à col long'),
('Fioles à vide'),
('Fioles coniques'),
('Fioles de réaction'),
('Fioles Erlenmeyer'),
('Flacons compte-gouttes'),
('Flacons de stockage'),
('Flacons laveurs'),
('Microscope'),
('Mortiers et pilons'),
('Pinces de fixation'),
('Pinces supports et trépieds'),
('Pipettes graduées'),
('Pipettes Pasteur'),
('Pipettes volumétriques'),
('Plaques de Petri'),
('Réacteurs à micro-ondes'),
('Réacteurs à pression'),
('Réactif chimique'),
('Récipients pour stockage'),
('Réfrigérants à colonne'),
('Réfrigérants à condenseur'),
('Réfrigérants à serpentin'),
('Seringues'),
('Support universel'),
('Thermomètres de laboratoire'),
('Tubes à essai'),
('Tubes à essai à col large'),
('Tubes à essai à fond plat'),
('Tubes à essai à fond rond'),
('Tubes capillaires'),
('Tubes de centrifugation'),
('Tubes Nessler');

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

INSERT INTO `RESERVELABORATOIRE` (`idReserve`, `idMaterielUnique`) VALUES
(1, 289),
(3, 291),
(4, 292);

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

INSERT INTO `RISQUE` (`idRisque`, `nomRisque`) VALUES
(29, 'Comburant'),
(30, 'Danger incendie'),
(31, 'Explosif'),
(32, 'Effets graves sur la senté'),
(33, 'Altération de la santé humaine'),
(34, 'Gaz sous pression'),
(35, 'Corrosion'),
(36, 'Toxicité aquatique'),
(37, 'Toxicité aiguë');

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

INSERT INTO `RISQUES` (`idrisques`, `idFDS`, `idRisque`) VALUES
(440, 29, 35),
(445, 30, 35),
(455, 26, 33),
(456, 26, 34),
(457, 26, 35),
(458, 26, 37),
(468, 24, 29),
(469, 24, 30),
(470, 24, 33),
(471, 24, 34),
(472, 25, 32),
(473, 25, 34),
(474, 25, 36);

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

INSERT INTO `STATUT` (`idStatut`, `nomStatut`) VALUES
(1, 'Administrateur'),
(2, 'Professseur'),
(3, 'Laborantin'),
(4, 'Gestionnaire');

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

INSERT INTO `STOCKLABORATOIRE` (`idStock`, `idMateriel`, `quantiteLaboratoire`) VALUES
(25, 34, 3),
(26, 40, 20),
(27, 36, 10),
(28, 35, 4),
(30, 38, 1);

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

INSERT INTO `TYPESALERTES` (`idAlerte`, `descriptionAlerte`) VALUES
(1, 'Date de péremption dépassée'),
(2, 'Date de péremption dépassée dans 10 jours'),
(3, 'Quantité en dessous du seuil minimal'),
(4, 'Quantité de l\'objet à 0');

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
  `motDePasse` varchar(100) NOT NULL,
  `themeLight` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `UTILISATEUR`
--

INSERT INTO `UTILISATEUR` (`idUtilisateur`, `idStatut`, `nom`, `prenom`, `email`, `motDePasse`, `themeLight`) VALUES
(1, 1, 'Admin', 'Admin', 'erwan.blandeau28@gmail.com', '3e296ab5e8a9c95df44c8839a3c42e3fb4614f25eedcdd5211b621b8b9f9f198', 1),
(7, 3, 'pilet', 'colin', 'colin.pilet1@gmail.com', '4c1001c251c1c923bca00789638afb17e908d526bf3e9975407c65d2b03f4b10', 1),
(11, 4, 'Erwan', 'Blandeau', 'erwan.blandeaujs@gmail.com', '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08', 1),
(14, 4, 'lavenant', 'jordan', 'jordan.lavenant@laposte.net', '136c67657614311f32238751044a0a3c0294f2a521e573afa8e496992d3786ba', 1),
(15, 3, 'lavenant', 'jordan', 'kubikcube18@gmail.com', '136c67657614311f32238751044a0a3c0294f2a521e573afa8e496992d3786ba', 1),
(16, 3, 'erwan', 'blandeau', 'erwan34230@gmail.com', '3fdf1e538b1e960a213f6f8ab3047c2dda161c54e7799e0501a413f4ee4fdb05', 1),
(17, 4, 'lucidor', 'leo', 'leo.lucidor@gmail.com', '8535e86c8118bbbb0a18ac72d15d3a2b37b18d1bce1611fc60165f322cf57386', 1),
(18, 3, 'test', 'test', 'kubik.deux@gmail.com', '6c00598a343908baa9e6b4527e35ebfdb69cdeb7479166755ef3a1eb7baf4fd0', 1),
(19, 2, 'prof', 'prof', 'towkyofn@gmail.com', '76a40438ab4dce4b55697502422e4e48de28c2ea11931b9ae10a3600e585a62e', 1);

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
  MODIFY `idArchiveBonCommande` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `BONCOMMANDE`
--
ALTER TABLE `BONCOMMANDE`
  MODIFY `idBonCommande` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=52;

--
-- AUTO_INCREMENT for table `CATEGORIE`
--
ALTER TABLE `CATEGORIE`
  MODIFY `idCategorie` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT for table `DEMANDE`
--
ALTER TABLE `DEMANDE`
  MODIFY `idDemande` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=107;

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
  MODIFY `idFDS` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT for table `FOURNISSEUR`
--
ALTER TABLE `FOURNISSEUR`
  MODIFY `idFournisseur` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `MATERIEL`
--
ALTER TABLE `MATERIEL`
  MODIFY `idMateriel` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;

--
-- AUTO_INCREMENT for table `MATERIELUNIQUE`
--
ALTER TABLE `MATERIELUNIQUE`
  MODIFY `idMaterielUnique` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=293;

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
  MODIFY `idrisques` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=475;

--
-- AUTO_INCREMENT for table `STOCKLABORATOIRE`
--
ALTER TABLE `STOCKLABORATOIRE`
  MODIFY `idStock` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `UTILISATEUR`
--
ALTER TABLE `UTILISATEUR`
  MODIFY `idUtilisateur` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

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
