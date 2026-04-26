#  Simulation MAC - Exponential Backoff

##  Description du projet

Ce projet consiste à simuler un protocole d'accès au canal (MAC - Medium Access Control) basé sur un mécanisme de **backoff exponentiel**.

Plusieurs stations tentent d’émettre des paquets sur un canal partagé. Lorsque plusieurs stations émettent en même temps, une collision se produit et les transmissions échouent. Les stations attendent alors un temps aléatoire avant de réessayer.

L'objectif est d'analyser les performances du système (débit, pertes, etc.) en fonction de différents paramètres.


##  Hypothèses du modèle

Afin de compléter les éléments non précisés dans l’énoncé, les hypothèses suivantes ont été adoptées :

- La simulation est réalisée en **événements discrets**
- Après une collision, le paquet **reste en file** et sera retransmis
- Les collisions sont détectées **instantanément**
- Une station ne peut avoir **qu'une seule tentative d’émission à la fois**
- Une limite maximale du nombre de retransmissions est fixée à : i_max = 10

Ces hypothèses permettent de simplifier le modèle tout en conservant son comportement principal.


##  Structure du projet
main.py : point d’entrée du programme

simulator.py : logique principale de la simulation

station.py : définition des stations (file, état…)

event.py : définition des événements (ARRIVE, TRY, FINISH)
requirements.txt


---

##  Fonctionnement du simulateur

Le simulateur est basé sur une **liste d’événements triée par temps**.

Trois types d’événements sont utilisés :

- `ARRIVE` : arrivée d’un paquet dans une station
- `TRY` : tentative d’émission d’un paquet
- `FINISH` : fin d’une transmission

Le fonctionnement est le suivant :

1. On initialise les premiers événements (arrivées)
2. À chaque étape :
   - On récupère l’événement le plus proche dans le temps
   - On met à jour le temps de simulation
   - On traite l’événement
   - On génère de nouveaux événements

Ce mécanisme permet de simuler efficacement l’évolution du système.

---

##  Exécution du projet

### 1. Prérequis

- Python 3.x installé

### 2. Lancer la simulation

Dans le terminal : python main.py

---

##  Objectifs du projet

Le simulateur permettra d’étudier :

- Le **débit** du système (nombre de paquets transmis avec succès)
- Le **taux de perte** (paquets rejetés car file pleine)
- L’évolution du nombre de paquets dans le système

Des expériences seront réalisées en faisant varier :

- le nombre de stations `N`
- le taux d’arrivée `λ`

---

##  Remarque

Ce projet est une simplification des protocoles réels comme Ethernet (CSMA/CD), permettant de mieux comprendre les mécanismes de gestion des collisions dans les réseaux.


  