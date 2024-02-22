# Manuel d'utilisation du module Import / Export CSV

Vous trouverez dans ce manuel d'utilisation les informations nécessaires pour exporter et importer des données dans le logiciel GESTLAB.

## I. Importer des données

Votre fichier doit respecter les conventions demandées par l'application. Vous trouverez ci-dessous une explication de la syntaxe ainsi qu'un exemple de fichier CSV qui respecte ces conventions.

L'application permet d'importer les données *d'un seul fichier CSV à la fois*.

Vous povez aussi modifier directement l'exemple nommé `data_exemple.csv` qui vous a été fourni avec ce manuel d'utilisation.

### Remplacer les données existantes

Lors de l'import d'un fichier CSV, vous pouvez choisir de remplacer les données existantes par les nouvelles données. Si vous ne cochez pas cette case, les données seront ajoutées à celles déjà existantes dans la base de données.

**Pensez à exporter les données via le module "Exporter" avant d'importer un fichier CSV, si vous souhaitez conserver une sauvegarde de vos données actuelles.**

### Syntaxe

Afin de bien insérer vos données dans le logiciel GESTLAB, il vous faudra donner à l'application un fichier de type `.csv` qui aura comme convention :

---

    Pour représenter une table de la BDD* :

    "-NOM DE LA TABLE"

    Pour chaque attribut de la table en question* :

    "*ATTRIBUT"

    Et pour finir autant de lignes d'insertion que vous souhaitez (au moins 1 ligne)* :

    "dupont.dupond@gmail.com,mdp,1"

    Exemple d'insertion :

    "-2FA
    *email
    *uri
    *idUtilisateur
    dupont.dupond@gmail.com,mdp,1"

## II. Exporter des données

Pour exporter des données, il vous suffit de cliquer sur le bouton "Exporter" dans le menu "CSV" de l'application. Vous pourrez ensuite choisir les données que vous voulez exporter (ou tout exporter) et le fichier sera automatiquement téléchargé sur votre ordinateur.

Vous pouvez utiliser ces exports de données comme une sauvegarde de votre base de données, ou pour les modifier et les réimporter dans l'application.

## III. Annexe

### Exemple d'un fichier CSV qui serait prêt à l'importation / ou qui vient d'être exporté à partir du module "Exporter un fichier CSV"

    -2FA
    *email
    *uri
    *idUtilisateur
    dupont.dupond@gmail.com,mdp,1

    -AJOUTERMATERIEL
    *idDemande
    *idMateriel
    *quantite
    26,36,2

    -ALERTESENCOURS
    *idAlerte
    *idMaterielUnique
    1,276

    -ARCHIVEBONCOMMANDE
    *idArchiveBonCommande
    *idBonCommande
    *idEtat
    *idUtilisateur
    *dateArchiveBonCommande
    1,2,4,3,2023-12-21

    -ARCHIVECOMMANDE
    *idArchiveBonCommande
    *idMateriel
    *quantite
    1,21,7

    -ARCHIVECOMMANDEANCIEN
    *numColis
    *idFournisseur
    *nomFournisseur
    *adresseFournisseur
    *mailFournisseur
    *telFournisseur
    *facture

    -BONCOMMANDE
    *idBonCommande
    *idEtat
    *idUtilisateur
    *dateBonCommande
    8,4,2,2023-12-22

    -CATEGORIE
    *idCategorie
    *idDomaine
    *nomCategorie
    1,1,Observation

    -COMMANDE
    *idBonCommande
    *idMateriel
    *quantite
    18,34,4

    -DEMANDE
    *idDemande
    *idUtilisateur
    *descriptionDemande
    *idEtatD
    26,11,,2

    -DOMAINE
    *idDomaine
    *nomDomaine
    1,Appareillage

    -ENDROIT
    *idEndroit
    *endroit
    6,008

    -ENVOIFOURNISSEUR
    *idBonCommande
    *idFournisseur
    *facture

    -ETATCOMMANDE
    *idEtat
    *nomEtat
    1,En attente de la validation du Gestionnaire

    -ETATDEMANDE
    *idEtatD
    *nomEtatD
    1,En attente de validation

    -FDS
    *idFDS
    *nomFDS
    29,Acide chloridrique

    -FOURNISSEUR
    *idFournisseur
    *nomFournisseur
    *adresseFournisseur
    *mailFournisseur
    *telFournisseur

    -MATERIEL
    *idMateriel
    *referenceMateriel
    *idFDS
    *nomMateriel
    *idCategorie
    *seuilAlerte
    *caracteristiquesComplementaires
    *informationsComplementairesEtSecurite
    34,REF123,24,Sulfate de cuivre anhydree,9,2,Sulfate de cuivre anhydre,Le sulfate de cuivre (II) anhydre est blanc et ne devient bleu que lorsqu'il est combiné avec des molécules d'eau

    -MATERIELUNIQUE
    *idMaterielUnique
    *idMateriel
    *idRangement
    *dateReception
    *commentaireMateriel
    *quantiteApproximative
    *datePeremption
    257,40,5,2024-02-19 00:00:00,un clavier supersonique,2.0,2024-07-20 00:00:00

    -RANGEMENT
    *idRangement
    *idEndroit
    *position
    1,1,haut

    -RECHERCHEMATERIELS
    *materielRecherche
    Agitateurs à hélice

    -RESERVELABORATOIRE
    *idReserve
    *idMaterielUnique
    11,257

    -RISQUE
    *idRisque
    *nomRisque
    29,Comburant

    -RISQUES
    *idrisques
    *idFDS
    *idRisque
    440,29,35

    -STATUT
    *idStatut
    *nomStatut
    1,Administrateur

    -STOCKLABORATOIRE
    *idStock
    *idMateriel
    *quantiteLaboratoire
    26,40,20

    -SUIVICOMMANDE
    *idBonCommande
    *localisation
    *numColis

    -TYPESALERTES
    *idAlerte
    *descriptionAlerte
    1,Date de péremption dépassée

    -UTILISATEUR
    *idUtilisateur
    *idStatut
    *nom
    *prenom
    *email
    *motDePasse
    2,4,dupond,dupond,dupond@gmail.com,mdp
