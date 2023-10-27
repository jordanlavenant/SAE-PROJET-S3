--emailUtilisateurUnique

INSERT INTO UTILISATEUR (idStatut, nom, prenom, email, motDePasse) VALUES 
(3, 'Dupont', 'Dupond', 'admin@example.com', 'mdp');

UPDATE UTILISATEUR SET email = 'admin@example.com' WHERE idUtilisateur = 2 ;
UPDATE UTILISATEUR SET nom = 'Yoyoyo' WHERE idUtilisateur = 2 ;

--modifsSurDemande

UPDATE DEMANDE SET descriptionDemande = 'blablabla' WHERE idDemande = 2 ;

--modificationStockLabo
UPDATE RESERVELABORATOIRE SET idMaterielUnique = 1 WHERE idReserve = 1 ;

--empecheSuppressionsStockLaboratoire
DELETE FROM STOCKLABORATOIRE where idStock = 1 ;