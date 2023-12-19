

DROP TABLE IF EXISTS RISQUES;
DROP TABLE IF EXISTS RESERVELABORATOIRE;
DROP TABLE IF EXISTS STOCKLABORATOIRE;
DROP TABLE IF EXISTS ENVOIFOURNISSEUR;
DROP TABLE IF EXISTS SUIVICOMMANDE;
DROP TABLE IF EXISTS AJOUTERMATERIEL;
DROP TABLE IF EXISTS RECHERCHEMATERIELS;
DROP TABLE IF EXISTS ALERTESENCOURS ;
DROP TABLE IF EXISTS MATERIELUNIQUE;
DROP TABLE IF EXISTS COMMANDE;
DROP TABLE IF EXISTS BONCOMMANDETEST;
DROP TABLE IF EXISTS MATERIEL;
DROP TABLE IF EXISTS ARCHIVECOMMANDE;
DROP TABLE IF EXISTS ARCHIVEBONCOMMANDE;
DROP TABLE IF EXISTS ARCHIVECOMMANDEANCIEN;
DROP TABLE IF EXISTS FOURNISSEUR;
DROP TABLE IF EXISTS RANGEMENT;
DROP TABLE IF EXISTS ENDROIT;
DROP TABLE IF EXISTS CATEGORIE;
DROP TABLE IF EXISTS DOMAINE;
DROP TABLE IF EXISTS RISQUE;
DROP TABLE IF EXISTS FDS;
DROP TABLE IF EXISTS BONCOMMANDE;
DROP TABLE IF EXISTS DEMANDE;
DROP TABLE IF EXISTS ETATCOMMANDE;
DROP TABLE IF EXISTS STATUT;
DROP TABLE IF EXISTS UTILISATEUR;
DROP TABLE IF EXISTS TYPESALERTES;
DROP TABLE IF EXISTS 2FA;

create table STATUT(
    idStatut int not null,
    nomStatut varchar(50) not null,
    primary key(idStatut)
);

create table UTILISATEUR(
    idUtilisateur int not null auto_increment,
    idStatut int  not null references STATUT,
    nom varchar(50) not null,
    prenom varchar(50) not null,
    email varchar(50) not null,
    motDePasse varchar(100) not null,
    primary key(idUtilisateur)
);

create table DOMAINE(
    idDomaine int not null auto_increment,
    nomDomaine varchar(50) not null,
    unique(nomDomaine),
    primary key(idDomaine)
);

create table CATEGORIE(
    idCategorie int not null auto_increment,
    idDomaine int not null references DOMAINE,
    nomCategorie varchar(50) not null,
    primary key(idCategorie)
);

create table RISQUE(
    idRisque int not null auto_increment,
    nomRisque varchar(50) not null,
    primary key(idRisque)
);

create table FDS(
    idFDS int not null auto_increment,
    nomFDS varchar(50) not null,
    primary key(idFDS)
);

create table RISQUES(
    idFDS int not null references FDS,
    idRisque int not null references RISQUE,
    primary key(idFDS, idRisque)
);

create table ENDROIT(
    idEndroit int not null auto_increment,
    endroit varchar(50) not null,
    unique(endroit),
    primary key(idEndroit)
);

create table RANGEMENT(
    idRangement int not null auto_increment,
    idEndroit int not null references ENDROIT,
    position varchar(50) not null,
    primary key(idRangement)
);

create table MATERIEL(
    idMateriel int not null auto_increment,
    referenceMateriel varchar(50) not null,
    idFDS int references FDS,
    nomMateriel varchar(50) not null,
    idCategorie int not null references CATEGORIE,
    seuilAlerte int,
    caracteristiquesComplementaires varchar(2000),
    informationsComplementairesEtSecurite varchar(2000),
    unique(nomMateriel),
    unique(referenceMateriel),
    primary key (idMateriel)
);

create table MATERIELUNIQUE(
    idMaterielUnique int not null auto_increment,
    idMateriel int not null references MATERIEL,
    idRangement int not null references RANGEMENT,
    dateReception datetime not null,
    commentaireMateriel varchar(100),
    quantiteApproximative float,
    datePeremption datetime,
    primary key(idMaterielUnique)
);

create table RESERVELABORATOIRE(
    idReserve int not null auto_increment,
    idMaterielUnique int not null references MATERIELUNIQUE,
    primary key(idReserve, idMaterielUnique)
);

create table STOCKLABORATOIRE(
    idStock int not null auto_increment,
    idMateriel int not null references MATERIEL,
    quantiteLaboratoire int default 0 ,
    primary key(idStock)
);

create table FOURNISSEUR(
    idFournisseur int not null auto_increment,
    nomFournisseur varchar(50),
    adresseFournisseur varchar(50),
    mailFournisseur varchar(50),
    telFournisseur varchar(10),
    unique(mailFournisseur), 
    unique(telFournisseur),
    primary key(idFournisseur)
);

create table ETATCOMMANDE(
    idEtat int not null auto_increment,
    nomEtat varchar(50) not null,
    primary key(idEtat)
);


create table DEMANDE(
    idDemande int not null auto_increment,
    idUtilisateur int not null references UTILISATEUR,
    descriptionDemande varchar(2000),
    idEtatD int not null references ETATDEMANDE,
    primary key(idDemande)
);

create table AJOUTERMATERIEL(
    idDemande int not null references DEMANDE,
    idMateriel int not null references MATERIEL,
    quantite int not null,
    primary key(idDemande, idMateriel)
);


create table BONCOMMANDE(
    idBonCommande int not null auto_increment,
    idEtat int not null references ETATCOMMANDE,
    idUtilisateur int not null references UTILISATEUR,
    dateBonCommande date,
    primary key(idBonCommande)
);

create table ETATDEMANDE(
    idEtatD int not null auto_increment,
    nomEtatD varchar(50) not null,
    primary key(idEtat)
);

create table COMMANDE(
    idBonCommande int not null references BONCOMMANDE,
    idMateriel int not null references MATERIEL,
    quantite int not null,
    primary key(idBonCommande,idMateriel)
);

create table ARCHIVEBONCOMMANDE(
    idArchiveBonCommande int not null auto_increment,
    idBonCommande int  not null,
    idEtat int not null,
    idUtilisateur int not null,
    dateArchiveBonCommande date,
    primary key(idArchiveBonCommande)
);

create table ARCHIVECOMMANDE(
    idArchiveBonCommande int not null references ARCHIVEBONCOMMANDE,
    idMateriel int not null,
    quantite int not null,
    primary key(idArchiveBonCommande, idMateriel)
);

create table SUIVICOMMANDE(
    idBonCommande int references BONCOMMANDE,
    localisation varchar(50) not null,
    numColis int not null,
    primary key(idBonCommande, numColis)
);

create table RECHERCHEMATERIELS(
    materielRecherche varchar(200),
    primary key(materielRecherche)
);

create table ENVOIFOURNISSEUR(
    idBonCommande int not null references BONCOMMANDE,
    idFournisseur int not null references FOURNISSEUR,
    facture varchar(50) not null,
    primary key(idBonCommande, idFournisseur)
);

CREATE TABLE TYPESALERTES (
    idAlerte int not null,
    descriptionAlerte varchar(100) not null,
    primary key (idAlerte)
);

create table ARCHIVECOMMANDEANCIEN(
    numColis int not null,
    idFournisseur int not null,
    nomFournisseur varchar(50) not null,
    adresseFournisseur varchar(50) not null,
    mailFournisseur varchar(50) not null,
    telFournisseur varchar(10) not null,
    facture varchar(50) not null,
    primary key(numColis)
);

CREATE TABLE ALERTESENCOURS(
    idAlerte int not null references TYPESALERTES, 
    idMaterielUnique int not null references MATERIELUNIQUE,
    primary key(idAlerte, idMaterielUnique)
);

CREATE TABLE 2FA(
    email varchar(50) not null,
    uri varchar(200) not null,
    idUtilisateur int not null references UTILISATEUR,
    primary key(email, idUtilisateur)
) ;