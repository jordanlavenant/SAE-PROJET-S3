# PROJET - SEMESTRE 3

# Sujet 1 : GestLab

## Versions

* Version actuelle : v1.0 le 27/10/2023

## Membres 

LUCIDOR Léo  
LALLIER Anna  
PILET Colin  
BLANDEAU Erwan  
LAVENANT Jordan  

## Prérequis

    virtualenv -p python3 venv
    source venv/bin/activate

    pip install flask
    pip install python-dotenv
    pip install PyYAML
    pip install bootstrap-flask
    pip install flask-sqlalchemy
    pip install flask-wtf
    pip install flask-login
    pip install werkzeug

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

- Différents diagrammes réalisés à partir du 23/10/2023
- MCD et base de données commencée le 23/10/2023 et actualisée chaque jour
- Creation des fonctions pour se connecter à partir du 23/10/2023
- Création des fonctions pour hash les mots de passe 24/10/2023
- Creation des procedures et triggers à partir du 24/10/2023
- Création des maquettes à partir du 24/10/2023
- Création des fonctions requêtes afin de rendre l'implémentation du site fonctionnelle (tout au long de la semaine)
- Début de l'implémentation des maquettes à partir du 24/10/2023

## Problèmes rencontrés

- Mauvaise compréhension de certaines notions du sujet qui nous ont mener à avancer dans la mauvaise direction, dû à un manque de renseignement de notre part

## Identifiants pour se connecter

Compte adminitrateur  
> ``leo@``  
``leo``

Compte gestionnaire 
> ``gest@``  
``gest``

Compte professeur  
> ``proff@``  
``proff``  

Compte laborantin  
> ``labo@``  
``labo``
