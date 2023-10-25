--emailUtilisateurUnique

INSERT INTO UTILISATEUR (idStatut, nom, prenom, email, motDePasse) VALUES 
(1, 'Dupont', 'Dupond', 'john.doe@example.com', 'mdp');

UPDATE UTILISATEUR SET email = 'john.doe@example.com' WHERE idUtilisateur = 2 ;

--insereSommeCommandeUpdate
SELECT * FROM DEMANDE ;

UPDATE AJOUTERMATERIEL SET quantite = 4 WHERE idDemande = 2 ;

DELETE FROM AJOUTERMATERIEL WHERE idMateriel = 2 AND idDemande = 1 ;

--verificationStockFournisseur
SELECT * FROM MATERIELFOURNISSEUR ;

UPDATE AJOUTERMATERIEL SET quantite = 100 WHERE idDemande = 1 AND idMateriel = 1;

UPDATE AJOUTERMATERIEL SET quantite = 5 WHERE idDemande = 1 AND idMateriel = 1;

UPDATE AJOUTERMATERIEL SET quantite = 15 WHERE idDemande = 1 AND idMateriel = 1;

DELETE FROM AJOUTERMATERIEL WHERE idMateriel = 1 AND idDemande = 1 ;

--modifsSurDemande
INSERT INTO AJOUTERMATERIEL (idDemande, idMateriel, idFournisseur, quantite) VALUES (2, 4, 3, 1);

UPDATE AJOUTERMATERIEL SET quantite = 1 WHERE idDemande = 2 ;

--modificationStockLabo
UPDATE BONCOMMANDE SET idEtat = 3 WHERE idDemande = 2 ;