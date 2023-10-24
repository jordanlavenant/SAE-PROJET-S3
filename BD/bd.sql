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
(1, 'Doe', 'John', 'john.doe@example.com', 'motdepasse1'),
(2, 'Smith', 'Jane', 'jane.smith@example.com', 'motdepasse2'),
(3, 'Johnson', 'Alice', 'alice.johnson@example.com', 'motdepasse3');

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

INSERT IGNORE INTO RECHERCHEMATERIELS (materielRecherche) VALUES
("Tubes à essai"),
("Tubes à essai à fond plat"),
("Tubes à essai à fond rond"),
("Tubes à essai à col large"),
("Fioles coniques"),
("Fioles Erlenmeyer"),
("Béchers"),
("Béchers Griffin"),
("Pipettes graduées"),
("Pipettes volumétriques"),
("Pipettes Pasteur"),
("Burettes"),
("Cylindres gradués"),
("Boîtes de Pétri"),
("Capsules de pesée"),
("Éprouvettes"),
("Flacons compte-gouttes"),
("Fioles à vide"),
("Fioles à col large"),
("Fioles à col long"),
("Fioles de réaction"),
("Ballons de réaction"),
("Réacteurs à pression"),
("Réacteurs à micro-ondes"),
("Cuvettes de spectrophotomètre"),
("Cuvettes de fluorimètre"),
("Cuvettes de polarimètre"),
("Cuvettes de conductimètre"),
("Cuvettes de viscosimètre"),
("Filtres Buchner"),
("Entonnoirs"),
("Colonnes de chromatographie"),
("Ampoules à décanter"),
("Thermomètres de laboratoire"),
("Deshydrateurs d'air"),
("Mortiers et pilons"),
("Plaques de Petri"),
("Bains-marie"),
("Autoclaves"),
("Agitateurs magnétiques"),
("Agitateurs à hélice"),
("Agitateurs vortex"),
("Agitateurs à plaques chauffantes"),
("Agitateurs à ultrasons"),
("Réfrigérants à condenseur"),
("Réfrigérants à colonne"),
("Réfrigérants à serpentin"),
("Colonnes de fractionnement"),
("Support universel"),
("Pinces, supports et trépieds"),
("Pinces de fixation"),
("Bouchons en caoutchouc"),
("Bouchons en liège"),
("Récipients pour stockage"),
("Seringues"),
("Flacons laveurs"),
("Tubes capillaires"),
("Tubes Nessler"),
("Tubes de centrifugation"),
("Boîtes cryogéniques"),
("Flacons de stockage");

-- Liste d'appareillages
INSERT IGNORE INTO RECHERCHEMATERIELS (materielRecherche) VALUES
("Microscopes (optiques, électroniques, à force atomique, etc.)"),
("Télescopes (astronomiques, terrestres, radio, etc.)"),
("Spectromètres (spectromètres de masse, spectroscopes, spectromètres UV-Vis, etc.)"),
("Oscilloscopes"),
("Voltmètres"),
("Ampèremètres"),
("Multimètres"),
("Générateurs de signaux"),
("Analyseurs de réseaux"),
("Détecteurs de rayonnement (comme les compteurs Geiger-Müller)"),
("Chambres à vide"),
("Interféromètres"),
("Appareils de diffraction (diffraction de rayons X, diffraction de neutrons, etc.)"),
("Analyseurs de particules (comme les spectromètres de masse et les spectromètres de temps de vol)"),
("Radiographes (radiographes médicaux, radiographes industriels, etc.)"),
("Caméras thermiques (thermographie)"),
("Calorimètres"),
("Photodétecteurs (photodiodes, photomultiplicateurs, etc.)"),
("Analyseurs de gaz"),
("Générateurs d'ondes électromagnétiques (micro-ondes, radiofréquences, etc.)"),
("Sonomètres (pour mesurer l'intensité sonore)"),
("Analyseurs de vibrations"),
("Pompes à vide"),
("Analyseurs de pression"),
("Analyseurs de température (thermomètres, thermocouples, etc.)"),
("Balances de précision"),
("Dynamomètres (pour mesurer les forces)"),
("Microbalance (pour mesurer de petites masses)"),
("Microdureté-testeurs"),
("Rhéomètres (pour mesurer la viscosité des fluides)"),
("Spectromètres Raman"),
("Spectromètres Mössbauer"),
("Appareils de magnétométrie"),
("Cryostats (pour des températures très basses)"),
("Magnétomètres (pour mesurer les champs magnétiques)"),
("Accélérateurs de particules"),
("Spectromètres de résonance magnétique nucléaire (RMN)"),
("Spectromètres de résonance paramagnétique électronique (RPE)"),
("Appareils de mesure de l'indice de réfraction"),
("Générateurs d'ultrasons"),
("Appareils de mesure de la conductivité électrique"),
("Appareils de mesure de la permittivité électrique"),
("Plaques d'alimentation électrique"),
("Analyseurs de perturbations électromagnétiques");

-- Liste de matériel électrique
INSERT IGNORE INTO RECHERCHEMATERIELS (materielRecherche) VALUES
("Alimentations électriques (sources de courant continu et alternatif)"),
("Voltmètres"),
("Ampèremètres"),
("Multimètres (mesurent tension, courant et résistance)"),
("Générateurs de signaux électriques"),
("Oscilloscopes (pour visualiser des signaux électriques)"),
("Alimentations à découpage"),
("Transformateurs électriques"),
("Résistances variables (potentiomètres)"),
("Condensateurs"),
("Bobines d'inductance"),
("Commutateurs (interrupteurs, commutateurs rotatifs, etc.)"),
("Connecteurs électriques (bornes, prises bananes, etc.)"),
("Fils de connexion (pour réaliser des connexions électriques)"),
("Piles et batteries"),
("Dispositifs de protection électrique (fusibles, disjoncteurs)"),
("Boîtes de jonction"),
("Boîtiers électriques"),
("Capteurs électriques (capteurs de courant, capteurs de tension)"),
("Dispositifs de mise à la terre"),
("Équipement de câblage et d'interconnexion (câbles, adaptateurs, etc.)"),
("Commutateurs de sécurité (interrupteurs à clé, interrupteurs d'arrêt d'urgence)"),
("Minuteries et compteurs"),
("Variateurs de vitesse (pour contrôler la vitesse des moteurs électriques)"),
("Relais électromagnétiques"),
("Dispositifs de protection contre les surtensions"),
("Alimentations de laboratoire (pour fournir des tensions stabilisées)"),
("Appareils de mesure de puissance électrique"),
("Transducteurs électriques (pour convertir une grandeur physique en signal électrique)"),
("Appareils de mesure de résistance de terre"),
("Convertisseurs de fréquence (pour modifier la fréquence des signaux électriques)"),
("Capteurs de courant de fuite"),
("Analyseurs de réseau électrique (pour analyser la qualité de l'énergie électrique)"),
("Unités de mesure de courant de fuite (mesure de l'isolement électrique)"),
("Appareils de mesure de puissance optique (dans le cas de laboratoires de physique optique)"),
("Appareils de mesure de champ électrique et magnétique"),
("Plaques d'alimentation électrique"),
("Analyseurs de perturbations électromagnétiques");

-- Liste de produits chimiques
INSERT IGNORE INTO RECHERCHEMATERIELS (materielRecherche) VALUES
("Acides (acide sulfurique, acide nitrique, acide chlorhydrique, acide acétique, etc.)"),
("Bases (hydroxyde de sodium, hydroxyde de potassium, ammoniaque, etc.)"),
("Solvants (eau, éthanol, acétone, dichlorométhane, etc.)"),
("Réactifs chimiques (comme les réactifs de précipitation, réactifs d'oxydation, réactifs de réduction, etc.)"),
("Sel commun (chlorure de sodium)"),
("Sel de table (chlorure de sodium iodé)"),
("Acétone"),
("Éther diéthylique"),
("Benzène"),
("Tolène"),
("Alcool isopropylique"),
("Méthanol"),
("Acétate d'éthyle"),
("Acétate de butyle"),
("Péroxides organiques (par exemple, peroxyde d'hydrogène)"),
("Diéthyl éther"),
("Composés organiques (comme les cétones, les alcools, les acides carboxyliques, etc.)"),
("Réactifs de réduction (sodium borohydrure, lithium aluminium hydride, etc.)"),
("Réactifs de précipitation (chlorure d'argent, sulfate de baryum, etc.)"),
("Réactifs de chromatographie (par exemple, silice gel)"),
("Gélatine"),
("Réactifs de coloration (comme les indicateurs pH, les colorants)"),
("Cristaux de sels (pour la croissance de cristaux)"),
("Réactifs de revêtement (pour la préparation d'échantillons)"),
("Hydrogène"),
("Azote"),
("Gaz rares (argon, hélium, etc.)"),
("Gaz combustibles (méthane, propane, etc.)"),
("Gaz comprimés (air comprimé, dioxyde de carbone, etc.)"),
("Poudres de métaux (par exemple, poudre d'aluminium pour la thermite)"),
("Sulfure d'hydrogène"),
("Réactifs de fluoruration"),
("Réactifs de catalyse (comme les catalyseurs métalliques)"),
("Réactifs de résonance magnétique nucléaire (RMN)"),
("Réactifs de spectrométrie de masse"),
("Réactifs pour la détermination de la conductivité électrique"),
("Réactifs pour l'analyse de surface (par exemple, agents tensioactifs)"),
("Réactifs de protection contre les radiations (pour les expériences en rayonnement)");

-- Liste de matériel et média
INSERT IGNORE INTO RECHERCHEMATERIELS (materielRecherche) VALUES
("Appareils de mesure (voltmètres, ampèremètres, oscilloscopes, etc.)"),
("Microscopes (optiques, électroniques, etc.)"),
("Télescopes (astronomiques, terrestres, radio, etc.)"),
("Spectromètres (spectromètres de masse, spectroscopes, spectromètres UV-Vis, etc.)"),
("Oscilloscopes"),
("Caméras thermiques (thermographie)"),
("Calorimètres"),
("Générateurs de signaux électriques"),
("Équipement de câblage et d'interconnexion (câbles, adaptateurs, etc.)"),
("Appareils de mesure de puissance électrique"),
("Transformateurs électriques"),
("Condensateurs"),
("Bobines d'inductance"),
("Plaques d'alimentation électrique"),
("Support pour colonne de fractionnement"),
("Cylindres de gaz comprimé (azote, argon, etc.)"),
("Tubes à vide"),
("Compteurs Geiger-Müller"),
("Tubes capillaires"),
("Réflecteurs de lumière (miroirs, prismes, etc.)");

-- Liste de milieux
INSERT IGNORE INTO RECHERCHEMATERIELS (materielRecherche) VALUES
("Air"),
("Eau (distillée, déionisée, etc.)"),
("Huile (pour des expériences d'optique)"),
("Gaz rares (argon, hélium, etc.)"),
("Vide (dans des chambres à vide)"),
("Solides (différents types de matériaux, cristaux, métaux)"),
("Gaz (pour des expériences de chimie et de physique des gaz)"),
("Plasmas (dans certaines expériences de physique nucléaire et de fusion)"),
("Diélectriques (utilisés dans la polarisation électrique)"),
("Milieux de diffusion (pour la diffusion de la lumière)");
