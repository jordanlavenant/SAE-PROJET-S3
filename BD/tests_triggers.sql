--emailUtilisateurUnique

INSERT INTO UTILISATEUR (idStatut, nom, prenom, email, motDePasse) VALUES 
(3, 'Dupont', 'Dupond', 'admin@example.com', 'mdp');

UPDATE UTILISATEUR SET email = 'admin@example.com' WHERE idUtilisateur = 2 ;

--modifsSurDemande

UPDATE DEMANDE SET descriptionDemande = 'blablabla' WHERE idDemande = 2 ;

--modificationStockLabo
UPDATE BONCOMMANDE SET idEtat = 3 WHERE idDemande = 2 ;