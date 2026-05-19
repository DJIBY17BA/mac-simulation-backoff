import math
import statistics
import matplotlib.pyplot as plt

# Importation de la classe Simulator
# qui contient toute la logique de simulation
from simulator import Simulator


# ========================
# COURBES
# ========================

# Fonction qui affiche l'évolution du débit au cours du temps
def plot_throughput_over_time():
    
    # Création du simulateur avec les paramètres :
    # N = nombre de stations
    # K = capacité
    # lambd = taux d'arrivée
    # tau = temps moyen de service
    # T_max = durée maximale de simulation
    # i_max = nombre max d'itérations
    sim = Simulator(N=5, K=10, lambd=0.5, tau=0.5, T_max=200, i_max=10)
    
    # Lancement de la simulation
    result = sim.run()

    # Création d'une nouvelle figure
    plt.figure()
    
    # Affichage du débit en fonction du temps
    plt.plot(result["times"], result["throughputs"])
    
    # Labels des axes
    plt.xlabel("Temps")
    plt.ylabel("n(t)/t")
    
    # Titre du graphique
    plt.title("Débit en fonction du temps")
    
    # Affichage de la grille
    plt.grid(True)


# Fonction qui affiche le nombre moyen de clients au cours du temps
def plot_mean_clients_over_time():
    
    sim = Simulator(N=5, K=10, lambd=0.5, tau=0.5, T_max=200, i_max=10)
    result = sim.run()

    plt.figure()
    
    # Courbe du nombre moyen de clients
    plt.plot(result["times"], result["mean_clients_history"])
    
    plt.xlabel("Temps")
    plt.ylabel("Nombre moyen de clients")
    plt.title("Nombre moyen de clients en fonction du temps")
    plt.grid(True)


# Fonction qui étudie l'influence de lambda sur le débit
def plot_throughput_vs_lambda():
    
    # Liste des différentes valeurs de lambda à tester
    lambdas = [0.1, 0.2, 0.4, 0.6, 0.8, 1.0, 1.5, 2.0]
    
    # Liste qui stockera les débits obtenus
    throughputs = []

    # Boucle sur chaque valeur de lambda
    for lambd in lambdas:
        
        # Création du simulateur
        sim = Simulator(N=5, K=10, lambd=lambd, tau=0.5, T_max=500, i_max=10)
        
        # Exécution de la simulation
        result = sim.run()
        
        # Ajout du débit obtenu dans la liste
        throughputs.append(result["throughput"])

    plt.figure()
    
    # Tracé des résultats
    plt.plot(lambdas, throughputs, marker="o")
    
    plt.xlabel("lambda")
    plt.ylabel("Débit")
    plt.title("Débit en fonction de lambda")
    plt.grid(True)


# Fonction qui étudie l'influence du nombre de stations N
def plot_throughput_vs_N():
    
    # Différentes valeurs de N à tester
    Ns = [1, 2, 3, 5, 8, 10, 15, 20]
    
    throughputs = []

    # Boucle sur les valeurs de N
    for N in Ns:
        
        sim = Simulator(N=N, K=10, lambd=0.5, tau=0.5, T_max=500, i_max=10)
        result = sim.run()
        
        # Sauvegarde du débit
        throughputs.append(result["throughput"])

    plt.figure()
    
    plt.plot(Ns, throughputs, marker="o")
    
    plt.xlabel("Nombre de stations N")
    plt.ylabel("Débit")
    plt.title("Débit en fonction de N")
    plt.grid(True)


# ========================
# INTERVALLE DE CONFIANCE 95%
# ========================

# Fonction qui calcule un intervalle de confiance à 95%
def confidence_interval_95(values):
    
    # Calcul de la moyenne
    mean = statistics.mean(values)

    # Si on a moins de 2 valeurs
    # impossible de calculer un écart-type
    if len(values) < 2:
        return mean, mean, mean

    # Calcul de l'écart-type
    std = statistics.stdev(values)
    
    # Calcul de la marge d'erreur
    margin = 1.96 * std / math.sqrt(len(values))

    # Retour :
    # moyenne, borne basse, borne haute
    return mean, mean - margin, mean + margin


# Fonction qui cherche la meilleure valeur de N
# avec intervalle de confiance
def find_best_N_with_confidence():
    
    # Valeurs de N testées
    Ns = [1, 2, 3, 5, 8, 10, 15, 20]
    
    # Nombre de répétitions pour chaque simulation
    repetitions = 20
    
    # Liste des résultats
    results = []

    # Boucle sur chaque valeur de N
    for N in Ns:
        
        throughputs = []

        # Répétition des simulations
        for _ in range(repetitions):
            
            sim = Simulator(N=N, K=10, lambd=0.5, tau=0.5, T_max=500, i_max=10)
            result = sim.run()
            
            # Sauvegarde du débit
            throughputs.append(result["throughput"])

        # Calcul de l'IC 95%
        mean, low, high = confidence_interval_95(throughputs)
        
        # Sauvegarde des résultats
        results.append((N, mean, low, high))

        # Affichage des résultats
        print(f"N={N} | débit moyen={mean:.4f} | IC 95%=[{low:.4f}, {high:.4f}]")

    # Recherche du meilleur N
    # max selon le débit moyen
    best = max(results, key=lambda x: x[1])

    print("\n=== Meilleur N ===")
    print(f"N optimal = {best[0]}")
    print(f"Débit moyen = {best[1]:.4f}")
    print(f"IC 95% = [{best[2]:.4f}, {best[3]:.4f}]")


# ========================
# MODE D'EXÉCUTION
# ========================

# Choix du mode :
# "PLOT" => afficher les graphiques
# "IC" => calculer les intervalles de confiance
MODE = "PLOT"


# Point d'entrée principal du programme
if __name__ == "__main__":
    
    # Si le mode est PLOT
    if MODE == "PLOT":
        
        # Génération des différents graphiques
        plot_throughput_over_time()
        plot_mean_clients_over_time()
        plot_throughput_vs_lambda()
        plot_throughput_vs_N()
        
        # Affichage des figures
        plt.show()

    # Si le mode est IC
    elif MODE == "IC":
        
        # Recherche du meilleur N
        find_best_N_with_confidence()