DROP TABLE IF EXISTS RISQUES;
DROP TABLE IF EXISTS CATEGORIESMATERIEL;
DROP TABLE IF EXISTS RESERVELABORATOIRE;
DROP TABLE IF EXISTS STOCKLABORATOIRE;
DROP TABLE IF EXISTS ENVOIFOURNISSEUR;
DROP TABLE IF EXISTS BONCOMMANDE;
DROP TABLE IF EXISTS SUIVICOMMANDE;
DROP TABLE IF EXISTS AJOUTERMATERIEL;
DROP TABLE IF EXISTS DEMANDE;
DROP TABLE IF EXISTS ETATCOMMANDE;
DROP TABLE IF EXISTS RECHERCHEMATERIELS;
DROP TABLE IF EXISTS MATERIELUNIQUE;
DROP TABLE IF EXISTS MATERIEL;
DROP TABLE IF EXISTS ARCHIVECOMMANDE;
DROP TABLE IF EXISTS FOURNISSEUR;
DROP TABLE IF EXISTS RANGEMENT;
DROP TABLE IF EXISTS CATEGORIE;
DROP TABLE IF EXISTS DOMAINE;
DROP TABLE IF EXISTS RISQUE;
DROP TABLE IF EXISTS FDS;
DROP TABLE IF EXISTS STATUT;
DROP TABLE IF EXISTS UTILISATEUR;


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
    unique(nomCategorie),
    primary key(idCategorie)
);

create table RISQUE(
    idRisque int not null auto_increment,
    nomRisque varchar(50) not null,
    pictogramme mediumblob,
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

create table RANGEMENT(
    idRangement int not null auto_increment,
    endroit varchar(50) not null,
    position varchar(50),
    unique(endroit),
    primary key(idRangement)
):

create table MATERIEL(
    referenceMateriel int not null,
    idFDS int references FDS,
    nomMateriel varchar(50) not null,
    caracteristiquesComplementaires varchar(2000),
    informationsComplementairesEtSecurite varchar(2000),
    unique(nomMateriel),
    primary key (referenceMateriel)
);

create table MATERIELUNIQUE(
    idMaterielUnique int not null auto_increment,
    referenceMateriel int not null references MATERIEL,
    idRangement int not null references RANGEMENT,
    dateReception datetime not null,
    commentaireMateriel varchar(100),
    quantiteApproximative float,
    datePeremption datetime,
    primary key(idMaterielUnique)
);

create table CATEGORIESMATERIEL(
    idMateriel int not null references MATERIEL,
    idCategorie int not null references CATEGORIE,
    primary key(idMateriel, idCategorie)
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

create table DEMANDE(
    idDemande int not null auto_increment,
    idUtilisateur int not null references UTILISATEUR,
    descriptionDemande varchar(2000),
    primary key(idDemande)
);

create table AJOUTERMATERIEL(
    idDemande int not null references DEMANDE,
    idMateriel int not null references MATERIEL,
    quantite int not null,
    primary key(idDemande, idMateriel)
);

create table ETATCOMMANDE(
    idEtat int not null auto_increment,
    nomEtat varchar(50) not null,
    primary key(idEtat)
);

create table BONCOMMANDE(
    idBonCommande int not null auto_increment,
    idDemande int not null references DEMANDE,
    idEtat int not null references ETATCOMMANDE,
    dateCommande datetime not null,
    primary key(idBonCommande)
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

create table ARCHIVECOMMANDE(
    numColis int not null,
    idFournisseur int not null,
    nomFournisseur varchar(50) not null,
    adresseFournisseur varchar(50) not null,
    mailFournisseur varchar(50) not null,
    telFournisseur varchar(10) not null,
    facture varchar(50) not null,
    primary key(numColis)
);