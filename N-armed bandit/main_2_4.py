# Exercise 2.4 (programming):
# Design and conduct an experiment to demonstrate the difficulties that sample-average methods have for nonstationary problems. 
# Use a modified version of the 10-armed testbed in which all the q(a) start out equal and then take independent random walks. 
# Prepare plots like Figure 2.1 for an action-value method using sample averages, incrementally computed by α = 1/k, 
# and another action-value method using a constant step-size parameter, α = 0.1. 
# Use ε = 0.1 and, if necessary, runs longer than 1000 plays.

# python -m venv .venv
# .venv/Scripts/Activate.ps1
import random
from plot import plot
from bandits.e_greedy_average_bandit import E_Greedy_Average_Bandit
from bandits.e_greedy_weighted_bandit import E_Greedy_Weighted_Bandit 
from bandits.ucb_bandit import UCB_Bandit 
from bandits.gradient_bandit import Gradient_Bandit

BANDITS: int = 500
STEPS: int = 1000
rng = random.Random(456)

def random_walk_values(values: list[float]) -> None:
    for i in range(len(values)):
        values[i] += rng.gauss(0, 0.2)


def main():
    seed = 123
    bandits_avg: list[E_Greedy_Average_Bandit] = [E_Greedy_Average_Bandit(n=10, epsilon=0.1, seed=seed+i) for i in range(BANDITS)]
    bandits_wgt: list[E_Greedy_Weighted_Bandit] = [E_Greedy_Weighted_Bandit(n=10, epsilon=0.1, seed=seed+i) for i in range(BANDITS)]
    bandits_ucb: list[UCB_Bandit] = [UCB_Bandit(n=10, c=1, seed=seed+i) for i in range(BANDITS)]
    bandits_grad: list[Gradient_Bandit] = [Gradient_Bandit(n=10, seed=seed+i) for i in range(BANDITS)]

    # Median reward that the bandits received each step 
    median_avg: list[float] = [0 for _ in range(STEPS)]
    median_wgt: list[float] = [0 for _ in range(STEPS)]
    median_ucb: list[float] = [0 for _ in range(STEPS)]
    median_grad: list[float] = [0 for _ in range(STEPS)]

    # Percentual of times that the bandits choose the optimal action in each step
    optimal_avg: list[float] = [0 for _ in range(STEPS)]
    optimal_wgt: list[float] = [0 for _ in range(STEPS)]
    optimal_ucb: list[float] = [0 for _ in range(STEPS)]
    optimal_grad: list[float] = [0 for _ in range(STEPS)]
    
    for step in range(STEPS):
        if step % (STEPS/20) == 0: print(f"{step*100/STEPS}%")

        for bandit in bandits_avg:
            a, r = bandit.do_action()
            median_avg[step] += r/BANDITS
            optimal_avg[step] += 1/BANDITS if a == bandit.values.index(max(bandit.values)) else 0
            random_walk_values(bandit.values)

        for bandit in bandits_wgt:
            a, r = bandit.do_action()
            median_wgt[step] += r/BANDITS
            optimal_wgt[step] += 1/BANDITS if a == bandit.values.index(max(bandit.values)) else 0
            random_walk_values(bandit.values)

        for bandit in bandits_ucb:
            a, r = bandit.do_action(step)
            median_ucb[step] += r/BANDITS
            optimal_ucb[step] += 1/BANDITS if a == bandit.values.index(max(bandit.values)) else 0
            random_walk_values(bandit.values)

        for bandit in bandits_grad:
            a, r = bandit.do_action(step)
            median_grad[step] += r/BANDITS
            optimal_grad[step] += 1/BANDITS if a == bandit.values.index(max(bandit.values)) else 0
            random_walk_values(bandit.values)

    median_values = [median_avg, median_wgt, median_ucb, median_grad]
    optimal_values = [optimal_avg, optimal_wgt, optimal_ucb, optimal_grad]
    labels = ["Average", "Weighted", "UCB-Bandit", "Gradient"]

    plot(
        median_values,
        labels,
        "Median Reward Each Step",
        "Median Reward",
        "res/2_4/median_reward.svg"
    )    

    plot(
        optimal_values,
        labels,
        "Optimal Action Each Step",
        "Percentual of Optimal Action",
        "res/2_4/optimal_action.svg"
    )

if __name__ == "__main__":
    main()