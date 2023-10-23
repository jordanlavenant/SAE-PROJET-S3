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


create table STATUT(
    idSt int not null,
    nomSt varchar(50),
    primary key(idSt)
);


create table UTILISATEUR(
    idUt int not null,
    nom varchar(50),
    prenom varchar(50),
    email varchar(50),
    mdp varchar(50),
    idSt int references STATUT(idSt),
    primary key(idUt, idSt)
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
    idFournisseur int not null,
    nomFournisseur varchar(50),
    adresseFournisseur varchar(50),
    mailFournisseur varchar(50),
    telFournisseur varchar(50),
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



insert into statut (idSt, nomSt) values 
    (1,'Proffesseur'),
    (2,'Utilisateur'),
    (3,'Gestionnaire'),
    (4,'Gestionnaire/Proffesseur');


insert into utilisateur (idUt, nom, prenom, email, mdp, idSt) values 
    (1,'Jean', 'Dupont', 'jean.dupont@example.com', 'azerty', 1),
    (2,'Pierre', 'Dupont', 'dupont@gmail.com', "azerty" , 2);

insert into reservation (idReser,date_debut, date_fin, quantiteR) values 
    (1,'2023-10-23', '2023-10-25', 10);

insert into categorie (idCat,nomCat) values 
    (1,'Matériaux de laboratoire');

insert into domaine (idDom,nomDom) values 
    (1,'Verre');

insert into materiaux (idMat, nomMat, idDom, idCat) values 
    (1,'becher', 1, 1);

insert into stock (idMat, quantite) values 
    (1, 100);

insert into date_peremption (idMat, date_peremption) values
    (1, '2024-10-23');

insert into fds (idDfs,nomFds) values 
    (1,'Fiche de données de sécurité du becher');

insert into commander (idCommande, idMat, idUt, quantiteC, prix, dateCommande,facture) values 
    (1, 1, 1, 10, 100, '2023-10-23', 'facture_123456789.pdf');

insert into fournisseur (idFournisseur,nomFournisseur, adresseFournisseur, mailFournisseur, telFournisseur)
values (1,'Leroy Merlin', '123 rue de la Paix, 75008 Paris', 'contact@leroymerlin.fr', '01 42 56 78 90');

insert into prix_materiel (idMat, idFournisseur, prix) values 
    (1, 1, 10);

insert into suivi_commande (idSuivi,idCommande, localisation, numColis)
values (1,1,'Orléans', 123456789);

insert into etat(idEtat, nomEtat) 
values (1, 'En prepatation'),
       (2, 'En cours de livraison'),
       (3, 'Livree');

insert into etat_commande (idSuivi, idEtat)
values (1, 1);

insert into risque (idRisque, idDfs, nomRisque, pictogramme) 
values (1, 1, 'Risque de coupure', 'https://th.bing.com/th/id/R.a05094b9f26eb64def392d54b291bea0?rik=3jSRK00M7%2fDYuQ&pid=ImgRaw&r=0')