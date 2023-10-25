

INSERT INTO STATUT (idStatut, nomStatut, consultation, reservation, commander, creationUilisateur, modificationUtilisateur) VALUES
(1, 'Administrateur', true, true, true, true, true),
(2, 'Professeur/Laborantin', true, true, false, true, true),
(3, 'Gestionnaire', true, false, true, true, true);

INSERT INTO UTILISATEUR (idStatut, nom, prenom, email, motDePasse) VALUES 
(1, 'John', 'Doe', 'john.doe@example.com', 'motdepasse1'),
(2, 'Jane', 'Smith', 'jane.smith@example.com', 'motdepasse2'),
(3, 'Alice', 'Johnson', 'alice.johnson@example.com', 'motdepasse3');

INSERT INTO DOMAINE (idDomaine, nomDomaine) VALUES
(1, 'Physique'),
(2, 'Chimie');

INSERT INTO CATEGORIE (idCategorie, idDomaine, nomCategorie) VALUES
(1, 1, 'Matériel électrique'),
(2, 2, 'Produits chimiques'),
(3, 1, 'Appareillage'),
(4, 2, 'Matériel de laboratoire'),
(5, 2, 'Accessoires associés au matériel de laboratoire'),
(6, 1, 'Médias'),
(7, 2, 'Verrerie');

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

INSERT INTO MATERIEL (idMateriel, idFDS, nomMateriel) VALUES
(1, 1,'Disjoncteur électrique'),
(2, 1, 'Acide sulfurique'),
(3, null, 'Oscilloscope'),
(4, null, 'Érlenmeyer en verre'),
(5, null, 'Pipette graduée'),
(6, null, "DVD éducatif sur l'électricité"),
(7, null, 'Becher en verre'),
(8, null, 'Multimètre numérique'),
(9, 2, 'Hydroxyde de sodium (Soude caustique)'),
(10, null, 'Générateur de signaux'),
(11, null, 'Burette en verre'),
(12, null, 'Pipette Pasteur en plastique'),
(13, null, 'CD-ROM de simulation de réactions chimiques'),
(14, null, 'Pissette en verre');

INSERT INTO CATEGORIESMATERIEL (idMateriel, idCategorie) VALUES
(1, 1),
(8, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(9, 2),
(10, 3),
(11, 4),
(12, 5),
(13, 6),
(14, 7);

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
(3, 3, 1200.0, 20),
(4, 3, 900.0, 50),
(5, 1, 60.0, 150),
(6, 2, 1300.0, 30) ;

INSERT INTO DEMANDE (idDemande, idUtilisateur, prixTotalDemande) VALUES
(1, 1, 0),
(2, 2, 0);

INSERT INTO AJOUTERMATERIEL (idDemande, idMateriel, idFournisseur, quantite) VALUES
(1, 1, 1, 10),
(1, 2, 2, 5),
(2, 3, 3, 2);

INSERT INTO ETATCOMMANDE (idEtat, nomEtat) VALUES
(1, 'En attente'),
(2, 'En cours'),
(3, 'Terminée');

INSERT INTO BONCOMMANDE (idBonCommande, idDemande, idEtat, dateCommande) VALUES
(1, 1, 1, '2023-10-15 10:00:00'),
(2, 2, 2,'2023-10-16 11:30:00');
--(3, 3, 3, '2023-10-17 14:15:00');

INSERT INTO SUIVICOMMANDE (idBonCommande, localisation, numColis) VALUES
(1, 'Entrepôt A', 12345),
(2, 'Entrepôt B', 54321);
--(3, 'Entrepôt C', 98765);

INSERT INTO ENVOIFOURNISSEUR (idBonCommande, idFournisseur, facture) VALUES
(1, 1, 'Facture-001.pdf'),
(2, 2, 'Facture-002.pdf');
--(3, 3, 'Facture-003.pdf');

INSERT INTO RECHERCHEMATERIELS(materielRecherche) 
VALUES  ('Microscope'),
        ('Réactif chimique'),
        ('Tubes à essai'),
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