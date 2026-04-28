from simulator import Simulator

from simulator import Simulator

sim = Simulator(
    N=3,
    K=5,
    lambd=0.5,
    tau=0.5,
    T_max=10,
    i_max=10
)

sim.run()