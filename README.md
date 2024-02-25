# PROJET - SEMESTRE 3

# Sujet 1 : GestLab

## Versions

* Version actuelle : v3.0 le 23/02/2024
* v2.0 le 10/11/2023
* v1.0 le 27/10/2023

## Membres 

LUCIDOR Léo  
LALLIER Anna  
PILET Colin  
BLANDEAU Erwan  
LAVENANT Jordan  

## Prérequis

    virtualenv -p python3 venv
    source venv/bin/activate

    pip install -r requirements.txt

## Démarrage de l'application


Pour démarrer l'application, exécutez la commande suivante :

```
flask run
```

## Présentation du sujet

Projet proposé par les professeurs de Sciences Physiques du Lycée François VILLON à BEAUGENCY.

Dans le cadre de leur activité, les professeurs de Sciences Physiques du Lycée François VILLON à BEAUGENCY doivent partager un seul et unique laboratoire, avec l’aide de laborantins. Ils doivent par conséquent se partager l’appareillage, la verrerie et les accessoires associés, le matériel électrique, les produits chimiques, le matériel de laboratoire et différents médias. Pour faciliter la gestion de tous ces matériels, les professeurs ont donc évoqué le besoin de la création d’un outil.

## Fonctionnalitées demandées

* GestLab nécessite la création d’une base de données.

* Le matériel est listé avec saisie assistée. La liste est classée par domaines et catégories.

* La base de données sera en ligne, c’est-à-dire, consultable et modifiable à partir de n’importe quel poste informatique qui possède un accès internet et l’application web(depuis l’établissement, le domicile).
* Un moteur de recherche interne permet un accès rapide au matériel souhaité.
* Plusieurs modes de recherche seraient appréciés.

* Un gestionnaire de comptes permet d’attribuer un accès intégral (divers droits de modification ou non) ou en consultation seulement.

* La base de données peut être accessible à une tierce personne, autre que des professeurs de sciences physiques (gestionnaire du Lycée par exemple pour les commandes auprès de fournisseurs externes)

* On affichera les objets (matériels) du couple domaine/catégorie sélectionné et prévoir l’impression de cet état

* L’outil doit permettre d’afficher la liste des matériels marqués par une alerte péremption ou une alerte de quantité (permet de voir les matériels périmés ou à recommander).

* L’outil doit permettre d’afficher la liste des matériels accompagnés par une FDS. Le gestionnaire serait ravi d’y intégrer les fournisseurs et les bons de commande associés pour la bonne gestion des stocks et le suivi des commandes.

## Tâches réalisées

### Semaine du 23/10/2023
- Différents diagrammes réalisés
- MCD et base de données commencée et actualisée chaque jour
- Creation des fonctions pour se connecter
- Création des fonctions pour hash les mots de passe
- Creation des procedures et triggers
- Création des maquettes
- Création des fonctions requêtes afin de rendre l'implémentation du site fonctionnelle (tout au long des semaines)
- Début de l'implémentation des maquettes

### Semaine du 06/11/2023

- Harmonisation des maquettes et de l'implémentation des vues (tout au long de la deuxieme semaine)
- Authentification à 2 facteurs via l'api de Google
- Génération d'un fichier PDF récapitulatif d'un bon de commande
- Gestions des stocks (insertions, modifications, suppresions)
- Gestions des demandes, commandes et bons de commandes
- Gestions des alertes
- Gestions des signalement sur des matériels
- Gestion des commentaires 
- Gestion de l'adresse mail de l'application 

### Semaine du 19/02/2024

- Ajout du booléen themeLight dans la table UTILISATEUR pour garder le thème choisi par l’utilisateur en mémoire
- Harmonisation des templates pour une homogénéisation des pages entres-elles, et interface et expérience utilisateur renforcée
- Fonctionnalité d’importation et d’exportation de fichiers .csv, avec possibilité de remplacer les données existantes ou non et possibilités de Drag & Drop.
- Affichages des statuts des utilisateurs dans l’onglet “Consultation des statuts”
- Popups de confirmation pour les actions jugées sensibles (suppressions, réinitialisation, valider…)
- Pagination diverses



## Problèmes rencontrés

- Mauvaise compréhension de certaines notions du sujet qui nous ont mener à avancer dans la mauvaise direction, dû à un manque de renseignement de notre part
- Redirections entres les vues parfois très complexes, et peu rigoureux
- Factorisation du modèles et des contrôleurs très imparfaites
- Possibilités de modifier le mot de passe de tous les utilisateurs si on avait leur adresse-mail correspondante => Authentification à 2 facteurs

## Identifiants pour se connecter

Compte adminitrateur  

> ``erwan.blandeau28@gmail.com``  
``erwan``

Compte gestionnaire 
> ``leo.lucidor@gmail.com``  
``leo``

Compte professeur  
> ``anna.lallier@gmail.com``  
``anna``  

Compte laborantin  
> ``colin.pilet1@gmail.com``  
``colin``

## Crédits

* Toggle dark mode inspiré par [Scodoc Notes](https://github.com/SebL68/Scodoc_Notes)
