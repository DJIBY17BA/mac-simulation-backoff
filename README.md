# Simulation MAC - Exponential Backoff

## Description

Ce projet consiste à simuler un protocole d’accès au canal (MAC - Medium Access Control) basé sur un mécanisme de backoff exponentiel.

Dans un réseau, plusieurs stations souhaitent transmettre des paquets sur un canal partagé. Lorsque deux stations émettent en même temps, une collision se produit, entraînant la perte des transmissions. Pour résoudre ce problème, chaque station attend un temps aléatoire avant de réémettre, ce temps augmentant après chaque collision.

L’objectif du projet est de modéliser ce système et d’analyser ses performances (débit, pertes, etc.) en fonction de différents paramètres.

---

## Hypothèses retenues

Les hypothèses suivantes ont été adoptées pour simplifier le modèle :

- La simulation est réalisée à événements discrets.
- Les arrivées de paquets suivent une loi exponentielle de paramètre λ.
- Chaque station possède une file d’attente de capacité limitée K.
- Les collisions sont détectées instantanément.
- Après une collision, le paquet reste dans la file et sera retransmis.
- Une station ne peut avoir qu’une seule tentative d’émission planifiée à la fois.
- Le nombre maximal de retransmissions est limité à `i_max = 10`.

---

## Structure du projet

```text
mac-simulation-backoff/
├── event.py          # Définition des événements
├── station.py        # Définition des stations
├── simulator.py      # Cœur du simulateur
├── experiments.py    # Génération des courbes
├── main.py           # Test simple
├── README.md         # Documentation
└── requirements.txt  # Dépendances

## 🔹 Événements

Trois types d’événements sont utilisés dans la simulation :

- `ARRIVE` : arrivée d’un paquet dans une station  
- `TRY` : tentative d’émission d’un paquet  
- `FINISH` : fin d’une transmission  

Chaque événement est caractérisé par :

- `time` : instant de l’événement  
- `event_type` : type d’événement  
- `station_id` : station concernée  

---

## 🔹 Station

Chaque station possède les attributs suivants :

- `id` : identifiant de la station  
- `K` : capacité maximale de la file  
- `queue` : nombre de paquets dans la file  
- `state` : état du backoff (nombre de collisions)  
- `transmitting` : indique si la station émet  
- `try_scheduled` : indique si une tentative est déjà programmée  

---

## 🔹 Simulateur

Le simulateur est basé sur une liste d’événements triée par temps à l’aide d’une file de priorité (`heapq`).

### Fonctionnement général :

1. Initialisation des premières arrivées de paquets  
2. Traitement des événements dans l’ordre chronologique  
3. Mise à jour du système après chaque événement  
4. Génération de nouveaux événements  

---

## 🔹 Fonctionnement du système

### Lorsqu’un paquet arrive (`ARRIVE`) :

- il est ajouté à la file si celle-ci n’est pas pleine  
- sinon, il est perdu  

### Lorsqu’une station tente d’émettre (`TRY`) :

- si le canal est libre → la transmission commence  
- sinon → collision → backoff exponentiel  

### Lorsqu’une transmission se termine (`FINISH`) :

- le paquet est transmis avec succès  
- la station peut tenter d’émettre à nouveau si des paquets restent  

---

## 🔹 Backoff exponentiel

Après chaque collision, une station attend un temps aléatoire avant de réessayer :

\[
t \sim \text{Exp}\left(\frac{1}{2^i \tau}\right)
\]

où :

- `i` est le nombre de collisions subies  
- `τ` est un paramètre de base  

Plus le nombre de collisions augmente, plus le temps d’attente devient long.

---

## 🔹 Paramètres du simulateur

- `N` : nombre de stations  
- `K` : taille de la file d’attente  
- `λ (lambd)` : taux d’arrivée des paquets  
- `τ (tau)` : paramètre du backoff  
- `T_max` : durée de simulation  
- `i_max` : nombre maximal de retransmissions  

---

## 🔹 Statistiques calculées

Le simulateur permet de mesurer :

- le nombre de paquets transmis avec succès  
- le nombre de paquets perdus  
- le débit du système  
- l’évolution du débit dans le temps  

Le débit est défini par :

```text
débit = nombre de paquets transmis / temps

## 🔹 Expériences réalisées

Le fichier `experiments.py` permet de générer les courbes suivantes :

- Débit \( n(t)/t \) en fonction du temps  
- Débit en fonction de \( \lambda \)  
- Débit en fonction du nombre de stations \( N \)  

Ces courbes permettent d’analyser le comportement du système et d’identifier des valeurs optimales.

---

## 🔹 Exécution

### Installer les dépendances :

```bash
pip install -r requirements.txt

## 🔹 Exécution

### Lancer le test simple :

```bash
python main.py

###Lancer les expériences :

python experiments.py

## Dépendances

Dans le fichier requirements.txt :

matplotlib

Les bibliothèques utilisées sont :

random : génération aléatoire
heapq : gestion des événements
matplotlib : tracé des courbes

##🔹 Conclusion

Ce projet permet de simuler un protocole MAC avec backoff exponentiel et d’étudier l’impact des paramètres sur les performances du système.

Les résultats obtenus montrent l’existence de conditions optimales maximisant le débit du système, en fonction du taux d’arrivée des paquets et du nombre de stations.