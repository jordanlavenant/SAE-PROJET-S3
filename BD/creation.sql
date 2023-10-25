DROP TABLE IF EXISTS ENVOIFOURNISSEUR;
DROP TABLE IF EXISTS RECHERCHEMATERIELS;
DROP TABLE IF EXISTS SUIVICOMMANDE;
DROP TABLE IF EXISTS BONCOMMANDE;
DROP TABLE IF EXISTS ETATCOMMANDE;
DROP TABLE IF EXISTS AJOUTERMATERIEL;
DROP TABLE IF EXISTS DEMANDE;
DROP TABLE IF EXISTS MATERIELFOURNISSEUR;
DROP TABLE IF EXISTS FOURNISSEUR;
DROP TABLE IF EXISTS STOCKLABORATOIRE;
DROP TABLE IF EXISTS DATEPEREMPTION;
DROP TABLE IF EXISTS CATEGORIESMATERIEL ;
DROP TABLE IF EXISTS MATERIEL;
DROP TABLE IF EXISTS RISQUES;
DROP TABLE IF EXISTS FDS;
DROP TABLE IF EXISTS RISQUE;
DROP TABLE IF EXISTS CATEGORIE;
DROP TABLE IF EXISTS DOMAINE;
DROP TABLE IF EXISTS UTILISATEUR;
DROP TABLE IF EXISTS STATUT;
DROP TABLE IF EXISTS RECHERCHEMATERIELS;
DROP TABLE IF EXISTS ARCHIVECOMMANDE;
DROP TABLE IF EXISTS debug_table ;
DROP TABLE IF EXISTS debug_table_prix ;
DROP TABLE IF EXISTS debug_table_id ;

create table STATUT(
    idStatut int not null,
    nomStatut varchar(50) not null,
    consultation boolean not null,
    reservation boolean not null,
    commander boolean not null,
    creationUilisateur boolean not null,
    modificationUtilisateur boolean not null,
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

create table MATERIEL(
    idMateriel int not null auto_increment,
    idFDS int references FDS,
    nomMateriel varchar(50) not null,
    primary key (idMateriel)
);

create table CATEGORIESMATERIEL(
    idMateriel int not null references MATERIEL,
    idCategorie int not null references CATEGORIE,
    primary key(idMateriel, idCategorie)
);

create table DATEPEREMPTION(
    idMateriel int not null references MATERIEL,
    datePeremption date not null,
    primary key(idMateriel, datePeremption)
);

create table STOCKLABORATOIRE(
    idStock int not null auto_increment,
    idMateriel int not null references MATERIEL,
    quantiteLaboratoire int,
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

create table MATERIELFOURNISSEUR(
    idMateriel int not null references MATERIEL,
    idFournisseur int not null references FOURNISSEUR,
    prixMateriel double not null,
    stockFournisseur int not null,
    primary key(idMateriel, idFournisseur)
);

create table DEMANDE(
    idDemande int not null auto_increment,
    idUtilisateur int not null references UTILISATEUR,
    prixTotalDemande float not null,
    primary key(idDemande)
);

create table AJOUTERMATERIEL(
    idDemande int not null references DEMANDE,
    idMateriel int not null references MATERIEL,
    idFournisseur int not null references FOURNISSEUR,
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