# Classe représentant une station du réseau
class Station:
    
    # Constructeur de la station
    def __init__(self, station_id, K):
        
        # Identifiant unique de la station
        self.id = station_id
        
        # Capacité maximale de la file d’attente
        self.K = K

        # Nombre de paquets actuellement dans la file
        self.queue = 0
        
        # État de retransmission / niveau de backoff
        # Commence à 1
        self.state = 1

        # Indique si la station est en train de transmettre
        self.transmitting = False
        
        # Indique si une tentative de transmission
        # est déjà programmée
        self.try_scheduled = False
        
        # Identifiant de la transmission en cours
        self.current_tx_id = 0