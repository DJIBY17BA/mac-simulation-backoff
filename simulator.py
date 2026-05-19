# Importation du module heapq
# utilisé pour gérer une file de priorité (tas / heap)
import heapq

# Importation du module random
# utilisé pour générer des valeurs aléatoires
import random

# Importation des événements et constantes
from event import Event, ARRIVE, TRY, FINISH

# Importation de la classe Station
from station import Station


# Classe principale de simulation
class Simulator:
    
    # Constructeur de la classe
    def __init__(self, N, K, lambd, tau, T_max, i_max=10):
        
        # Nombre de stations
        self.N = N
        
        # Capacité maximale des files d’attente
        self.K = K
        
        # Taux d’arrivée des paquets
        self.lambd = lambd
        
        # Temps moyen utilisé pour le backoff
        self.tau = tau
        
        # Temps maximal de simulation
        self.T_max = T_max
        
        # Nombre maximal de tentatives avant abandon
        self.i_max = i_max

        # Temps courant de simulation
        self.time = 0.0
        
        # Liste des événements (file de priorité)
        self.events = []
        
        # Création des stations
        self.stations = [Station(i, K) for i in range(N)]

        # Indique si le canal est occupé
        self.channel_busy = False
        
        # ID de la station actuellement en transmission
        self.current_station_id = None
        
        # Compteur des transmissions
        self.tx_counter = 0

        # Nombre de paquets transmis avec succès
        self.success_packets = 0
        
        # Nombre de paquets perdus
        self.lost_packets = 0
        
        # Nombre total d’arrivées
        self.total_arrivals = 0

        # Historique des temps
        self.times = []
        
        # Historique du débit
        self.throughputs = []
        
        # Historique du nombre moyen de clients
        self.mean_clients_history = []
        
        # Historique du taux de perte
        self.loss_rates = []

    
    # Ajout d’un événement dans la file de priorité
    def add_event(self, event):
        heapq.heappush(self.events, event)

    
    # Planification d’un événement ARRIVE
    def schedule_arrive(self, station_id):
        
        # Génération d’un délai exponentiel
        delay = random.expovariate(self.lambd)
        
        # Ajout de l’événement
        self.add_event(Event(self.time + delay, ARRIVE, station_id))

    
    # Initialisation des premiers événements
    def init_events(self):
        for station in self.stations:
            self.schedule_arrive(station.id)

    
    # Retourne le nombre total de clients dans toutes les stations
    def total_clients(self):
        return sum(station.queue for station in self.stations)

    
    # Enregistrement des statistiques
    def record_stats(self):
        if self.time > 0:
            
            # Sauvegarde du temps
            self.times.append(self.time)
            
            # Débit = paquets réussis / temps
            self.throughputs.append(self.success_packets / self.time)
            
            # Nombre moyen de clients
            self.mean_clients_history.append(self.total_clients() / self.N)
            
            # Taux de perte
            self.loss_rates.append(
                self.lost_packets / self.total_arrivals if self.total_arrivals > 0 else 0
            )

    
    # Gestion du backoff exponentiel
    def schedule_backoff(self, station):
        
        # Si le nombre maximal de tentatives est atteint
        if station.state >= self.i_max:
            
            # Suppression du paquet
            if station.queue > 0:
                station.queue -= 1
            
            # Comptage comme paquet perdu
            self.lost_packets += 1
            
            # Réinitialisation de l’état
            station.state = 1
            station.try_scheduled = False
            station.transmitting = False
            station.current_tx_id = 0
            return

        # Calcul du backoff exponentiel
        mean_backoff = (2 ** station.state) * self.tau
        
        # Génération du délai aléatoire
        delay = random.expovariate(1 / mean_backoff)

        # Augmentation du niveau de collision
        station.state += 1
        
        # Indique qu’une tentative est programmée
        station.try_scheduled = True
        
        # Arrêt de la transmission actuelle
        station.transmitting = False
        station.current_tx_id = 0

        # Planification d’un nouvel essai
        self.add_event(Event(self.time + delay, TRY, station.id))

    
    # Gestion d’une arrivée de paquet
    def handle_arrive(self, event):
        
        # Récupération de la station
        station = self.stations[event.station_id]

        # Incrément du nombre d’arrivées
        self.total_arrivals += 1
        
        # Planification de la prochaine arrivée
        self.schedule_arrive(station.id)

        # Si la file est pleine
        if station.queue >= station.K:
            
            # Paquet perdu
            self.lost_packets += 1
            return

        # Ajout du paquet dans la file
        station.queue += 1

        # Si aucune tentative n’est déjà prévue
        if not station.try_scheduled and not station.transmitting:
            
            station.try_scheduled = True
            
            # Tentative immédiate de transmission
            self.add_event(Event(self.time, TRY, station.id))

    
    # Gestion d’une tentative de transmission
    def handle_try(self, event):
        
        station = self.stations[event.station_id]
        
        # La tentative programmée est maintenant exécutée
        station.try_scheduled = False

        # Si aucun paquet ou déjà en transmission
        if station.queue == 0 or station.transmitting:
            return

        # Si le canal est libre
        if not self.channel_busy:
            
            # Occupation du canal
            self.channel_busy = True
            self.current_station_id = station.id

            # Nouvelle transmission
            self.tx_counter += 1
            
            # Attribution d’un identifiant unique
            station.current_tx_id = self.tx_counter
            
            # La station transmet
            station.transmitting = True

            # Planification de la fin de transmission
            self.add_event(Event(self.time + 1, FINISH, station.id, station.current_tx_id))

        else:
            # =====================
            # COLLISION
            # =====================

            # Station déjà en transmission
            old_station = self.stations[self.current_station_id]

            # Annulation de sa transmission
            old_station.transmitting = False
            old_station.current_tx_id = 0

            # Libération du canal
            self.channel_busy = False
            self.current_station_id = None

            # Backoff des deux stations
            self.schedule_backoff(old_station)
            self.schedule_backoff(station)

    
    # Gestion de la fin de transmission
    def handle_finish(self, event):
        
        station = self.stations[event.station_id]

        # Ignore les anciens FINISH après collision
        if not station.transmitting:
            return

        # Ignore les événements obsolètes
        if event.tx_id != station.current_tx_id:
            return

        # Libération du canal
        self.channel_busy = False
        self.current_station_id = None

        # Fin de transmission
        station.transmitting = False
        station.current_tx_id = 0

        # Si un paquet existe dans la file
        if station.queue > 0:
            
            # Retrait du paquet transmis
            station.queue -= 1
            
            # Réinitialisation de l’état
            station.state = 1
            
            # Transmission réussie
            self.success_packets += 1

        # Si d’autres paquets restent
        if station.queue > 0 and not station.try_scheduled:
            
            station.try_scheduled = True
            
            # Nouvelle tentative immédiate
            self.add_event(Event(self.time, TRY, station.id))

    
    # Fonction principale de simulation
    def run(self):
        
        # Initialisation des événements
        self.init_events()

        # Tant qu’il reste des événements
        while self.events:
            
            # Récupération de l’événement prioritaire
            event = heapq.heappop(self.events)

            # Arrêt si temps maximal atteint
            if event.time > self.T_max:
                break

            # Mise à jour du temps courant
            self.time = event.time

            # Gestion selon le type d’événement
            if event.event_type == ARRIVE:
                self.handle_arrive(event)

            elif event.event_type == TRY:
                self.handle_try(event)

            elif event.event_type == FINISH:
                self.handle_finish(event)

            # Mise à jour des statistiques
            self.record_stats()

        # Résultats finaux
        return {
            "time": self.time,
            "success_packets": self.success_packets,
            "lost_packets": self.lost_packets,
            "total_arrivals": self.total_arrivals,

            # Débit final
            "throughput": self.success_packets / self.time if self.time > 0 else 0,

            # Taux de perte final
            "loss_rate": self.lost_packets / self.total_arrivals if self.total_arrivals > 0 else 0,

            # Historiques
            "times": self.times,
            "throughputs": self.throughputs,
            "mean_clients_history": self.mean_clients_history,
            "loss_rates": self.loss_rates,
        }