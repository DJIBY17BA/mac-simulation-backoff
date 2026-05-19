# Importation de la classe Simulator
# qui contient toute la logique de simulation
from simulator import Simulator


# Création d'un objet Simulator
sim = Simulator(
    
    # Nombre de stations dans le système
    N=3,
    
    # Capacité maximale du système
    K=5,
    
    # Taux d'arrivée des clients / transactions
    lambd=0.5,
    
    # Temps moyen de service
    tau=0.5,
    
    # Temps maximal de simulation
    T_max=10,
    
    # Nombre maximal d'itérations / essais
    i_max=10
)

# Lancement de la simulation
sim.run()