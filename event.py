from dataclasses import dataclass

# Constantes représentant les différents types d'événements
ARRIVE = "ARRIVE"   # Transaction arrivée à une station
TRY = "TRY"         # Tentative de traitement / exécution
FINISH = "FINISH"   # Fin du traitement

# @dataclass permet de créer automatiquement
# le constructeur (__init__), le __repr__, etc.
# order=True permet de comparer et trier les objets Event
# automatiquement selon les attributs (dans l’ordre de déclaration)
@dataclass(order=True)
class Event:
    
    # Temps auquel l'événement se produit
    time: float
    
    # Type de l'événement (ARRIVE, TRY ou FINISH)
    event_type: str
    
    # Identifiant de la station concernée
    station_id: int
    
    # Identifiant de la transaction
    # Valeur par défaut = 0 si non précisée
    tx_id: int = 0