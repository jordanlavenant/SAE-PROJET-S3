# Manuel d'utilisation Import / Export BDD 

## Syntaxe

- Pour bien insérer en base de données, il faut données à l'application un fichier de type '.csv' qui aura comme convention :

--- 

    Pour représenter une table de la BDD* :

    "-NOM DE LA TABLE"

    Pour chaque attribut de la table en question* :

    "*ATTRIBUT"

    Et pour finir autant de ligne d'insertion que vout souhaiter (au moins 1 ligne)* :

    "cassandra.maupou@gmail.com,test,12"

    Ainsi tout cumulée une insertion ressemblera à ça :

    "-2FA
    *email
    *uri
    *idUtilisateur
    cassandra.maupou@gmail.com,test,12"

## Exemple d'un fichier CSV qui serait prêt à l'importation / ou qui vient d'être exporter

    -2FA
    *email
    *uri
    *idUtilisateur
    Exemple : cassandra.maupou@gmail.com,test,12
    
    -AJOUTERMATERIEL
    *idDemande
    *idMateriel
    *quantite
    Exemple : 26,36,2
    
    -ALERTESENCOURS
    *idAlerte
    *idMaterielUnique
    Exemple : 1,276
    
    -ARCHIVEBONCOMMANDE
    *idArchiveBonCommande
    *idBonCommande
    *idEtat
    *idUtilisateur
    *dateArchiveBonCommande
    Exemple : 1,2,4,3,2023-12-21
    
    -ARCHIVECOMMANDE
    *idArchiveBonCommande
    *idMateriel
    *quantite
    Exemple : 1,21,7
    
    -ARCHIVECOMMANDEANCIEN
    *numColis
    *idFournisseur
    *nomFournisseur
    *adresseFournisseur
    *mailFournisseur
    *telFournisseur
    *facture
    Exemple : 
    
    -BONCOMMANDE
    *idBonCommande
    *idEtat
    *idUtilisateur
    *dateBonCommande
    Exemple : 8,4,2,2023-12-22
    
    -CATEGORIE
    *idCategorie
    *idDomaine
    *nomCategorie
    Exemple : 1,1,Observation
    
    -COMMANDE
    *idBonCommande
    *idMateriel
    *quantite
    Exemple : 18,34,4
    
    -DEMANDE
    *idDemande
    *idUtilisateur
    *descriptionDemande
    *idEtatD
    Exemple : 26,11,,2
    
    -DOMAINE
    *idDomaine
    *nomDomaine
    Exemple : 1,Appareillage
    
    -ENDROIT
    *idEndroit
    *endroit
    Exemple : 6,008
    
    -ENVOIFOURNISSEUR
    *idBonCommande
    *idFournisseur
    *facture
    Exemple : 
    
    -ETATCOMMANDE
    *idEtat
    *nomEtat
    Exemple : 1,En attente de la validation du Gestionnaire
    
    -ETATDEMANDE
    *idEtatD
    *nomEtatD
    Exemple : 1,En attente de validation
    
    -FDS
    *idFDS
    *nomFDS
    Exemple : 29,Acide chloridrique
    
    -FOURNISSEUR
    *idFournisseur
    *nomFournisseur
    *adresseFournisseur
    *mailFournisseur
    *telFournisseur
    Exemple : 
    
    -MATERIEL
    *idMateriel
    *referenceMateriel
    *idFDS
    *nomMateriel
    *idCategorie
    *seuilAlerte
    *caracteristiquesComplementaires
    *informationsComplementairesEtSecurite
    Exemple : 34,REF123,24,Sulfate de cuivre anhydree,9,2,Sulfate de cuivre anhydre,Le sulfate de cuivre (II) anhydre est blanc et ne devient bleu que lorsqu'il est combiné avec des molécules d'eau
    
    -MATERIELUNIQUE
    *idMaterielUnique
    *idMateriel
    *idRangement
    *dateReception
    *commentaireMateriel
    *quantiteApproximative
    *datePeremption
    Exemple : 257,40,5,2024-02-19 00:00:00,un clavier supersonique,2.0,2024-07-20 00:00:00
    
    -RANGEMENT
    *idRangement
    *idEndroit
    *position
    Exemple : 1,1,haut
    
    -RECHERCHEMATERIELS
    *materielRecherche
    Exemple : Agitateurs à hélice
    
    -RESERVELABORATOIRE
    *idReserve
    *idMaterielUnique
    Exemple : 11,257

    -RISQUE
    *idRisque
    *nomRisque
    Exemple : 29,Comburant
    
    -RISQUES
    *idrisques
    *idFDS
    *idRisque
    Exemple : 440,29,35
    
    -STATUT
    *idStatut
    *nomStatut
    Exemple : 1,Administrateur
    
    -STOCKLABORATOIRE
    *idStock
    *idMateriel
    *quantiteLaboratoire
    Exemple : 26,40,20
    
    -SUIVICOMMANDE
    *idBonCommande
    *localisation
    *numColis
    
    -TYPESALERTES
    *idAlerte
    *descriptionAlerte
    Exemple : 1,Date de péremption dépassée
    
    -UTILISATEUR
    *idUtilisateur
    *idStatut
    *nom
    *prenom
    *email
    *motDePasse
    Exemple : 2,4,leo,lucidor,leo.lucidor@gmail.com,test
