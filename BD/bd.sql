drop table ETAT_COMMANDE;
drop table ETAT;
drop table PRIX_MATERIEL;
drop table SUIVI_COMMANDE;
drop table FOURNISSEUR;
drop table COMMANDER;
drop table RISQUE;
drop table FDS;
drop table DATE_PEREMPTION;
drop table STOCK;
drop table MATERIAUX;
drop table DOMAINE;
drop table CATEGORIE;
drop table RESERVATION;
drop table UTILISATEUR;
drop table STATUT;

create table DROITS(
    consultation boolean,
    reservation boolean,
    commander boolean,
    creation_utilisateur boolean,
    modifier_utilisateur boolean,

)

create table STATUT(
    idSt int not null,
    nomSt varchar(50),
    primary key(idSt)
);


create table UTILISATEUR(
    idUt int not null auto_increment,
    nom varchar(50),
    prenom varchar(50),
    email varchar(50),
    mdp varchar(100),
    idSt int references STATUT(idSt),
    unique(email),
    primary key(idUt)
);

create table RESERVATION(
    idReser int not null,
    date_debut date,
    date_fin date,
    quantiteR int not null,
    primary key(idReser)
);


create table CATEGORIE(
    idCat int not null,
    nomCat varchar(50),
    primary key(idCat)
);

create table DOMAINE(
    idDom int not null,
    nomDom varchar(50),
    primary key(idDom)
);

create table MATERIAUX(
    idMat int not null,
    nomMat varchar(50),
    idDom int references DOMAINE(idDom),
    idCat int references CATEGORIE(idCat),
    primary key (idMat)
);

create table STOCK(
    idMat int not null references MATERIAUX(idMat),
    quantite int not null,
    primary key(idMat)
);

create table DATE_PEREMPTION(
    idMat int not null references MATERIAUX(idMat),
    date_peremption date ,
    primary key(idMat)
);

create table FDS(
    idDfs int not null,
    nomFds varchar(50),
    primary key(idDfs)
);

create table RISQUE(
    idRisque int not null,
    idDfs int not null references FDS(idDfs),
    nomRisque varchar(50),
    pictogramme varchar(2000),
    primary key(idRisque)
);


create table COMMANDER(
    idCommande int not null,
    idMat int references MATERIAUX(idMat),
    idUt int references UTILISATEUR(idUt),
    quantiteC int not null,
    prix float not null,
    dateCommande date,
    facture varchar(4000),
    primary key(idCommande)
);

create table FOURNISSEUR(
    idFournisseur int not null auto_increment,
    nomFournisseur varchar(50),
    adresseFournisseur varchar(50),
    mailFournisseur varchar(50),
    telFournisseur varchar(50),
    unique(mailFournisseur, telFournisseur, nomFournisseur, adresseFournisseur),

    primary key(idFournisseur)
);

create table SUIVI_COMMANDE(
    idSuivi int not null,
    idCommande int references COMMANDER(idCommande),
    localisation varchar(50),
    numColis int not null,
    primary key(idSuivi)
);

create table PRIX_MATERIEL(
    idMat int not null references MATERIAUX(idMat),
    idFournisseur int not null references FOURNISSEUR(idFournisseur),
    prix float,
    primary key(idMat,idFournisseur)
);

create table ETAT (
    idEtat int not null,
    nomEtat varchar(50),
    primary key(idEtat)
);

create table ETAT_COMMANDE (
    idSuivi int  references SUIVI_COMMANDE(idSuivi),
    idEtat int  references ETAT(idEtat),
    primary key(idSuivi)
);

create table MATERIAUX_RECHERCHE(
    nomMatRech varchar(50),
    primary key(nomMatRech)
);

create table ALERTES (
    idAlerte int not null,
    idMat int references DATE_PEREMPTION(idMat),
    quantite int not null,
    primary key(idAlerte)
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