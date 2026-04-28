import math
import statistics
import matplotlib.pyplot as plt

from simulator import Simulator


# ========================
# COURBES
# ========================

def plot_throughput_over_time():
    sim = Simulator(N=5, K=10, lambd=0.5, tau=0.5, T_max=200, i_max=10)
    result = sim.run()

    plt.figure()
    plt.plot(result["times"], result["throughputs"])
    plt.xlabel("Temps")
    plt.ylabel("n(t)/t")
    plt.title("Débit en fonction du temps")
    plt.grid(True)


def plot_mean_clients_over_time():
    sim = Simulator(N=5, K=10, lambd=0.5, tau=0.5, T_max=200, i_max=10)
    result = sim.run()

    plt.figure()
    plt.plot(result["times"], result["mean_clients_history"])
    plt.xlabel("Temps")
    plt.ylabel("Nombre moyen de clients")
    plt.title("Nombre moyen de clients en fonction du temps")
    plt.grid(True)


def plot_throughput_vs_lambda():
    lambdas = [0.1, 0.2, 0.4, 0.6, 0.8, 1.0, 1.5, 2.0]
    throughputs = []

    for lambd in lambdas:
        sim = Simulator(N=5, K=10, lambd=lambd, tau=0.5, T_max=500, i_max=10)
        result = sim.run()
        throughputs.append(result["throughput"])

    plt.figure()
    plt.plot(lambdas, throughputs, marker="o")
    plt.xlabel("lambda")
    plt.ylabel("Débit")
    plt.title("Débit en fonction de lambda")
    plt.grid(True)


def plot_throughput_vs_N():
    Ns = [1, 2, 3, 5, 8, 10, 15, 20]
    throughputs = []

    for N in Ns:
        sim = Simulator(N=N, K=10, lambd=0.5, tau=0.5, T_max=500, i_max=10)
        result = sim.run()
        throughputs.append(result["throughput"])

    plt.figure()
    plt.plot(Ns, throughputs, marker="o")
    plt.xlabel("Nombre de stations N")
    plt.ylabel("Débit")
    plt.title("Débit en fonction de N")
    plt.grid(True)


# ========================
# IC 95%
# ========================

def confidence_interval_95(values):
    mean = statistics.mean(values)

    if len(values) < 2:
        return mean, mean, mean

    std = statistics.stdev(values)
    margin = 1.96 * std / math.sqrt(len(values))

    return mean, mean - margin, mean + margin


def find_best_N_with_confidence():
    Ns = [1, 2, 3, 5, 8, 10, 15, 20]
    repetitions = 20
    results = []

    for N in Ns:
        throughputs = []

        for _ in range(repetitions):
            sim = Simulator(N=N, K=10, lambd=0.5, tau=0.5, T_max=500, i_max=10)
            result = sim.run()
            throughputs.append(result["throughput"])

        mean, low, high = confidence_interval_95(throughputs)
        results.append((N, mean, low, high))

        print(f"N={N} | débit moyen={mean:.4f} | IC 95%=[{low:.4f}, {high:.4f}]")

    best = max(results, key=lambda x: x[1])

    print("\n=== Meilleur N ===")
    print(f"N optimal = {best[0]}")
    print(f"Débit moyen = {best[1]:.4f}")
    print(f"IC 95% = [{best[2]:.4f}, {best[3]:.4f}]")


# ========================
# MODE
# ========================

MODE = "PLOT"  # "PLOT" pour les courbes, "IC" pour les intervalles de confiance

if __name__ == "__main__":
    if MODE == "PLOT":
        plot_throughput_over_time()
        plot_mean_clients_over_time()
        plot_throughput_vs_lambda()
        plot_throughput_vs_N()
        plt.show()

    elif MODE == "IC":
        find_best_N_with_confidence()