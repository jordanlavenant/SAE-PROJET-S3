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
DROP TABLE IF EXISTS MATERIEL;
DROP TABLE IF EXISTS RISQUES;
DROP TABLE IF EXISTS FDS;
DROP TABLE IF EXISTS RISQUE;
DROP TABLE IF EXISTS DOMAINE;
DROP TABLE IF EXISTS CATEGORIE;
DROP TABLE IF EXISTS UTILISATEUR;
DROP TABLE IF EXISTS STATUT;
DROP TABLE IF EXISTS RECHERCHEMATERIELS;
DROP TABLE IF EXISTS ARCHIVECOMMANDE;

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


create table CATEGORIE(
    idCategorie int not null auto_increment,
    nomCategorie varchar(50) not null,
    unique(nomCategorie),
    primary key(idCategorie)
);

create table DOMAINE(
    idDomaine int not null auto_increment,
    nomDomaine varchar(50) not null,
    unique(nomDomaine),
    primary key(idDomaine)
);

create table RISQUE(
    idRisque int not null auto_increment,
    nomRisque varchar(50) not null,
    pictogramme varchar(2000),
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
    idDomaine int not null references DOMAINE,
    idCategorie int not null references CATEGORIE,
    idFDS int not null references FDS,
    nomMateriel varchar(50) not null,
    primary key (idMateriel)
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
    prixTotalCommande float not null,
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
    materielRecherche varchar(50),
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

INSERT INTO STATUT (idStatut, nomStatut, consultation, reservation, commander, creationUilisateur, modificationUtilisateur) VALUES
(1, 'Administrateur', true, true, true, true, true),
(2, 'Professeur/Laborantin', true, true, false, true, true),
(3, 'Gestionnaire', true, false, true, true, true);

INSERT INTO UTILISATEUR (idStatut, nom, prenom, email, motDePasse) VALUES 
(1, 'John', 'Doe', 'john.doe@example.com', 'motdepasse1'),
(2, 'Jane', 'Smith', 'jane.smith@example.com', 'motdepasse2'),
(3, 'Alice', 'Johnson', 'alice.johnson@example.com', 'motdepasse3');

INSERT INTO CATEGORIE (idCategorie, nomCategorie) VALUES
(1, 'Électronique'),
(2, 'Chimie'),
(3, 'Biologie'),
(4, 'Informatique');

INSERT INTO DOMAINE (idDomaine, nomDomaine) VALUES
(1, 'Informatique'),
(2, 'Médecine'),
(3, 'Chimie'),
(4, 'Biologie');

INSERT INTO RISQUE (idRisque, nomRisque, pictogramme) VALUES
(1, 'Toxicité', 'toxic.png'),
(2, 'Feu', 'fire.png'),
(3, 'Radiation', 'radiation.png');

INSERT INTO FDS (idFDS, nomFDS) VALUES
(1, 'FDS-001'),
(2, 'FDS-002'),
(3, 'FDS-003');

INSERT INTO RISQUES (idFDS, idRisque) VALUES
(1, 1),
(2, 2),
(3, 3);

INSERT INTO MATERIEL (idMateriel, idDomaine, idCategorie, idFDS, nomMateriel) VALUES
(1, 1, 1, 1, 'Ordinateur'),
(2, 2, 3, 2, 'Réactif chimique'),
(3, 4, 4, 3, 'Microscope');

INSERT INTO DATEPEREMPTION (idMateriel, datePeremption) VALUES
(2, '2023-12-31'),
(3, '2024-06-30');

INSERT INTO STOCKLABORATOIRE (idStock, idMateriel, quantiteLaboratoire) VALUES
(1, 1, 50),
(2, 2, 100),
(3, 3, 10);

INSERT INTO FOURNISSEUR (nomFournisseur, adresseFournisseur, mailFournisseur, telFournisseur) VALUES
('Fournisseur A', '123 Rue Fournisseur', 'fournisseur.a@example.com', '1234567890'),
('Fournisseur B', '456 Rue Fournisseur', 'fournisseur.b@example.com', '9876543210'),
('Fournisseur C', '789 Rue Fournisseur', 'fournisseur.c@example.com', '5555555555');

INSERT INTO MATERIELFOURNISSEUR (idMateriel, idFournisseur, prixMateriel, stockFournisseur) VALUES
(1, 1, 800.0, 100),
(2, 2, 50.0, 200),
(3, 3, 1200.0, 20);

INSERT INTO DEMANDE (idDemande, idUtilisateur) VALUES
(1, 1),
(2, 2),
(3, 3);

INSERT INTO AJOUTERMATERIEL (idDemande, idMateriel, quantite) VALUES
(1, 1, 10),
(2, 2, 5),
(3, 3, 2);

INSERT INTO ETATCOMMANDE (idEtat, nomEtat) VALUES
(1, 'En attente'),
(2, 'En cours'),
(3, 'Terminée');

INSERT INTO BONCOMMANDE (idBonCommande, idDemande, idEtat, prixTotalCommande, dateCommande) VALUES
(1, 1, 1, 1000.0, '2023-10-15 10:00:00'),
(2, 2, 2, 500.0, '2023-10-16 11:30:00'),
(3, 3, 3, 2400.0, '2023-10-17 14:15:00');

INSERT INTO SUIVICOMMANDE (idBonCommande, localisation, numColis) VALUES
(1, 'Entrepôt A', 12345),
(2, 'Entrepôt B', 54321),
(3, 'Entrepôt C', 98765);

INSERT INTO RECHERCHEMATERIELS (materielRecherche) VALUES
('Microscope'),
('Réactif chimique');

INSERT INTO ENVOIFOURNISSEUR (idBonCommande, idFournisseur, facture) VALUES
(1, 1, 'Facture-001.pdf'),
(2, 2, 'Facture-002.pdf'),
(3, 3, 'Facture-003.pdf');

INSERT INTO RECHERCHEMATERIELS(materielRecherche) 
VALUES  ('Tubes à essai'),
        ('Tubes à essai à fond plat'),
        ('Tubes à essai à fond rond'),
        ('Tubes à essai à col large'),
        ('Fioles coniques'),
        ('Fioles Erlenmeyer'),
        ('Béchers'),
        ('Béchers Griffin'),
        ('Pipettes graduées'),
        ('Pipettes volumétriques'),
        ('Pipettes Pasteur'),
        ('Burettes'),
        ('Cylindres gradués'),
        ('Boîtes de Pétri'),
        ('Capsules de pesée'),
        ('Éprouvettes'),
        ('Flacons compte-gouttes'),
        ('Fioles à vide'),
        ('Fioles à col large'),
        ('Fioles à col long'),
        ('Fioles de réaction'),
        ('Ballons de réaction'),
        ('Réacteurs à pression'),
        ('Réacteurs à micro-ondes'),
        ('Cuvettes de spectrophotomètre'),
        ('Cuvettes de fluorimètre'),
        ('Cuvettes de polarimètre'),
        ('Cuvettes de conductimètre'),
        ('Cuvettes de viscosimètre'),
        ('Filtres Buchner'),
        ('Entonnoirs'),
        ('Colonnes de chromatographie'),
        ('Ampoules à décanter'),
        ('Thermomètres de laboratoire'),
        ("Deshydrateurs d'air"),
        ('Mortiers et pilons'),
        ('Plaques de Petri'),
        ('Bains-marie'),
        ('Autoclaves'),
        ('Agitateurs magnétiques'),
        ('Agitateurs à hélice'),
        ('Agitateurs vortex'),
        ('Agitateurs à plaques chauffantes'),
        ('Agitateurs à ultrasons'),
        ('Réfrigérants à condenseur'),
        ('Réfrigérants à colonne'),
        ('Réfrigérants à serpentin'),
        ('Colonnes de fractionnement'),
        ('Support universel'),
        ('Pinces, supports et trépieds'),
        ('Pinces de fixation'),
        ('Bouchons en caoutchouc'),
        ('Bouchons en liège'),
        ('Récipients pour stockage'),
        ('Seringues'),
        ('Flacons laveurs'),
        ('Tubes capillaires'),
        ('Tubes Nessler'),
        ('Tubes de centrifugation'),
        ('Boîtes cryogéniques'),
        ('Flacons de stockage');