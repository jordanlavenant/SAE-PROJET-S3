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
    idCategorie int not null,
    nomCategorie varchar(50) not null,
    unique(nomCategorie),
    primary key(idCategorie)
);

create table DOMAINE(
    idDomaine int not null,
    nomDomaine varchar(50) not null,
    unique(nomDomaine),
    primary key(idDomaine)
);

create table RISQUE(
    idRisque int not null,
    nomRisque varchar(50) not null,
    pictogramme varchar(2000),
    primary key(idRisque)
);

create table FDS(
    idFDS int not null,
    nomFDS varchar(50) not null,
    primary key(idFDS)
);

create table RISQUES(
    idFDS int not null references FDS,
    idRisque varchar(50) not null references RISQUE,
    primary key(idFDS, idRisque)
);

create table MATERIEL(
    idMateriel int not null,
    idDomaine int not null references DOMAINE,
    idCategorie int not null references CATEGORIE,
    idFDS int not null references FDS,
    idFournisseur int not null references FOURNISSEUR,
    nomMateriel varchar(50) not null,
    primary key (idMateriel)
);

create table DATEPEREMPTION(
    idMateriel int not null references MATERIEL,
    datePeremption date not null,
    primary key(idMateriel, datePeremption)
);

create table STOCKLABORATOIRE(
    idStock int not null,
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
    idDemande int not null,
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
    idEtat int not null,
    nomEtat varchar(50) not null,
    primary key(idEtat)
)

create table BONCOMMANDE(
    idBonCommande int not null,
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
    primary key(idBonCommande, localisation)
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
);


insert into STATUT (idSt, nomSt) values 
    (1,'Professeur'),
    (2,'Administrateur'),
    (3,'Gestionnaire'),
    (4,'Laborantin');


insert into UTILISATEUR (idUt, nom, prenom, email, mdp, idSt) values 
    (1,'Jean', 'Dupont', 'jean.dupont@example.com', 'azerty', 1),
    (2,'Pierre', 'Dupont', 'dupont@gmail.com', "azerty" , 2);

insert into RESERVATION (idReser,date_debut, date_fin, quantiteR) values 
    (1,'2023-10-23', '2023-10-25', 10);

insert into CATEGORIE (idCat,nomCat) values 
    (1,'Matériaux de laboratoire');

insert into DOMAINE (idDom,nomDom) values 
    (1,'Verre');

insert into MATERIAUX (idMat, nomMat, idDom, idCat) values 
    (1,'becher', 1, 1);

insert into STOCK (idMat, quantite) values 
    (1, 100);

insert into DATE_PEREMPTION (idMat, date_peremption) values
    (1, '2024-10-23');

insert into FDS (idDfs,nomFds) values 
    (1,'Fiche de données de sécurité du becher');

insert into COMMANDER (idCommande, idMat, idUt, quantiteC, prix, dateCommande,facture) values 
    (1, 1, 1, 10, 100, '2023-10-23', 'facture_123456789.pdf');

insert into FOURNISSEUR (idFournisseur,nomFournisseur, adresseFournisseur, mailFournisseur, telFournisseur)
values (1,'Leroy Merlin', '123 rue de la Paix, 75008 Paris', 'contact@leroymerlin.fr', '01 42 56 78 90');

insert into PRIX_MATERIEL (idMat, idFournisseur, prix) values 
    (1, 1, 10);

insert into SUIVI_COMMANDE (idSuivi,idCommande, localisation, numColis)
values (1,1,'Orléans', 123456789);

insert into ETAT(idEtat, nomEtat) 
values (1, 'En prepatation'),
       (2, 'En cours de livraison'),
       (3, 'Livree');

insert into ETAT_COMMANDE (idSuivi, idEtat)
values (1, 1);

insert into RISQUE (idRisque, idDfs, nomRisque, pictogramme) 
values (1, 1, 'Risque de coupure', 'https://th.bing.com/th/id/R.a05094b9f26eb64def392d54b291bea0?rik=3jSRK00M7%2fDYuQ&pid=ImgRaw&r=0')

INSERT INTO MATERIAUX_RECHERCHE (nomMatRech) 
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