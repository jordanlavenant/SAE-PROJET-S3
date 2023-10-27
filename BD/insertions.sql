INSERT INTO DOMAINE (nomDomaine) VALUES
('Appareillage'),
('Électricité'),
('Matériel de laboratoire'),
('Médias'),
('Produits chimiques'),
('Verrerie et associés');

INSERT INTO CATEGORIE (idDomaine, nomCategorie) VALUES
(1, 'Observation'), 
(1, 'Mesures'), 
(1, 'ExAO'), 
(1, 'Multimédia'), 
(1, 'Expérimentation'), 
(1, 'Divers'),
(6, 'Verrerie'), 
(6, 'Associés'),
(5, 'Produits organiques'),
(5, 'Produits minéraux'),
(5, 'Enzymes'),
(5, 'Colorants'),
(5, 'Entretien'),
(5, 'Autres'),
(3, 'Appareils de labo'),
(3, 'Sécurité'),
(3, 'Fournitures'),
(3, 'Mobilier'),
(3, 'Divers'),
(4, 'Logiciels'),
(4, 'DVD/VHS'),
(4, 'Manuels scolaires'),
(4, 'Livres scientifiques'),
(4, 'Cartes/Posters'),
(4, 'Divers'),
(2, 'Générateurs'),
(2, 'Mesures'),
(2, 'Récepteurs'),
(2, 'Connectique'),
(2, 'Métaux'),
(2, 'Divers');

INSERT INTO STATUT (idStatut, nomStatut) VALUES
(1, 'Administrateur'),
(2, 'Professseur'),
(3, 'Laborantin'),
(4, 'Gestionnaire');

INSERT INTO UTILISATEUR (idStatut, nom, prenom, email, motDePasse) VALUES
(1, 'Admin', 'Admin', 'admin@example.com', 'motdepasseadmin'),
(2, 'Utilisateur', 'Standard', 'user@example.com', 'motdepasseuser');

INSERT INTO RISQUE (nomRisque) VALUES
('Toxicité'),
('Feu'),
('Radiation');

INSERT INTO FDS (nomFDS) VALUES
('FDS 1'),
('FDS 2'),
('FDS 3');

INSERT INTO RISQUES (idFDS, idRisque) VALUES
(1, 1),
(2, 2),
(3, 3);

INSERT INTO RANGEMENT (endroit, position) VALUES
('Étagère 1', 'haut'),
('Étagère 2', 'bas'),
('Armoire 1', 'gauche');

INSERT INTO MATERIEL (referenceMateriel, seuilAlerte, idFDS, nomMateriel, idCategorie, caracteristiquesComplementaires, informationsComplementairesEtSecurite) VALUES
('REF123', 1, 1, 'Microscope électronique', 1, 'Microscope électronique haute résolution', "Utilisé pour observer des échantillons à l'échelle microscopique."),
('REF456', 10, 2, 'Acide chlorhydrique', 5, "Solution d'acide chlorhydrique à 37%", 'Utilisé comme réactif de laboratoire.'),
('REF789', 1, null, 'Oscilloscope Tektronix TBS1052B', 1, 'Oscilloscope numérique à deux canaux', "Utilisé pour l'analyse de signaux électriques."),
('REF101', 1, null, 'Bécher en verre de 250 ml', 6, 'Bécher en verre borosilicaté', "Utilisé pour contenir des liquides en laboratoire."),
('REF202', 15, null, 'Pipette graduée en plastique 10 ml', 6, 'Pipette jetable à usage unique', 'Utilisée pour mesurer des volumes liquides avec précision.'),
('REF303', 1, null, "DVD éducatif sur l'électricité", 4, "DVD interactif d'enseignement", "Utilisé pour l'apprentissage des concepts électricité."),
('REF404', 1, null, 'Multimètre Fluke 87V', 2, 'Multimètre numérique professionnel', 'Utilisé pour la mesure de tensions, courants, et résistances électriques.'),
('REF505', 30, 3, 'Sulfate de cuivre', 3, 'Poudre cristalline bleue', 'Utilisé comme réactif chimique dans diverses expériences.'),
('REF606', 1, null, 'Générateur de signaux Rohde & Schwarz', 2, 'Générateur de signaux RF haute fréquence', 'Utilisé pour la génération de signaux électriques complexes.'),
('REF707', 1, null, 'Burette automatique en verre 50 ml', 6, "Burette en verre avec système d'étalonnage automatique", 'Utilisée pour doser des solutions avec précision.'),
('REF808', 5, null, 'Pipette Pasteur en plastique 3 ml', 6, 'Pipette jetable en plastique', 'Utilisée pour le transfert de petits volumes liquides.'),
('REF909', 1, null, 'Logiciel de modélisation moléculaire', 4, 'Logiciel de simulation chimique avancé', 'Utilisé pour la modélisation moléculaire et la simulation de réactions chimiques.'),
('REF1010', 1,  null, 'Pissette en verre 500 ml', 6, 'Pissette en verre classique', 'Utilisée pour le transfert de liquides en laboratoire.');

INSERT INTO MATERIELUNIQUE (idMateriel, idRangement, dateReception, commentaireMateriel, quantiteApproximative, datePeremption) VALUES
(1, 1, '2023-10-26 10:00:00', 'Bon état', 1, NULL),
(2, 2, '2023-10-26 11:00:00', 'Pipettes neuves', 2, '2023-10-26'),
(2, 2, '2023-10-26 11:00:00', 'Pipettes neuves', 10, '2024-10-26'),
(3, 3, '2023-10-26 12:00:00', null, 1, NULL),
(2, 2, '2023-10-26 11:00:00', 'Pipettes neuves', 10, '2023-10-30') ;

--éviter les insertions manuelles sur stocklaboratoire, exceptionnel ici pour les tests sur les alertes
INSERT INTO STOCKLABORATOIRE(idMateriel, quantiteLaboratoire) VALUES
(3, 1),
(1, 0) ;

INSERT INTO FOURNISSEUR (nomFournisseur, adresseFournisseur, mailFournisseur, telFournisseur) VALUES
('Fournisseur 1', 'Adresse 1', 'fournisseur1@example.com', '1234567890'),
('Fournisseur 2', 'Adresse 2', 'fournisseur2@example.com', '9876543210');

INSERT INTO DEMANDE (idUtilisateur, descriptionDemande) VALUES
(2, 'Demande 1 de l''utilisateur standard'),
(2, 'Demande 2 de l''utilisateur standard');

INSERT INTO AJOUTERMATERIEL (idDemande, idMateriel, quantite) VALUES
(2, 2, 2);

--(1, 1, 2),
--(1, 2, 5),

INSERT INTO ETATCOMMANDE (nomEtat) VALUES
('En attente'),
('En cours de traitement'),
('Expédiée'),
('Livrée');

INSERT INTO BONCOMMANDE (idDemande, idEtat, dateCommande) VALUES
(1, 1, '2023-10-26 13:00:00'),
(2, 2, '2023-10-26 14:00:00');

INSERT INTO SUIVICOMMANDE (idBonCommande, localisation, numColis) VALUES
(1, 'Entrepôt 1', 12345),
(2, 'Entrepôt 2', 67890);

INSERT INTO ENVOIFOURNISSEUR (idBonCommande, idFournisseur, facture) VALUES
(1, 1, 'Facture 1'),
(2, 2, 'Facture 2');

INSERT INTO RESERVELABORATOIRE (idReserve, idMaterielUnique) VALUES
(1, 2),
(2, 3);

INSERT INTO TYPESALERTES (idAlerte, descriptionAlerte) VALUES 
(1, "Date de péremption dépassée"),
(2, "Date de péremption dépassée dans 10 jours"),
(3, "Quantité en dessous du seuil minimal"),
(4, "Quantité de l'objet à 0") ;



INSERT INTO RECHERCHEMATERIELS (materielRecherche) 
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