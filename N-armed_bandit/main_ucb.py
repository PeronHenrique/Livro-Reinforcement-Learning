# python -m venv .venv
# .venv/Scripts/Activate.ps1
from plot import plot
from bandits.e_greedy_weighted_bandit import E_Greedy_Weighted_Bandit
from bandits.e_greedy_average_bandit import E_Greedy_Average_Bandit
from bandits.ucb_bandit import UCB_Bandit

BANDITS: int = 2000
STEPS: int = 1000

def main():
    seed = 123
    bandits_0_10: list[E_Greedy_Average_Bandit] = [E_Greedy_Average_Bandit(n=10, epsilon=0.10, seed=seed+i) for i in range(BANDITS)]
    bandits_wgt_0_10: list[E_Greedy_Weighted_Bandit] = [E_Greedy_Weighted_Bandit(n=10, epsilon=0.10, seed=seed+i) for i in range(BANDITS)]
    bandits_ucb_1: list[UCB_Bandit] = [UCB_Bandit(n=10, c=1, seed=seed+i) for i in range(BANDITS)]
    bandits_ucb_2: list[UCB_Bandit] = [UCB_Bandit(n=10, c=2, seed=seed+i) for i in range(BANDITS)]

    # Median reward that the bandits received each step 
    median_0_10: list[float] = [0 for _ in range(STEPS)]
    median_wgt_0_10: list[float] = [0 for _ in range(STEPS)]
    median_ucb_1: list[float] = [0 for _ in range(STEPS)]
    median_ucb_2: list[float] = [0 for _ in range(STEPS)]

    # Percentual of times that the bandits choose the optimal action in each step
    optimal_0_10: list[float] = [0 for _ in range(STEPS)]
    optimal_wgt_0_10: list[float] = [0 for _ in range(STEPS)]
    optimal_ucb_1: list[float] = [0 for _ in range(STEPS)]
    optimal_ucb_2: list[float] = [0 for _ in range(STEPS)]
    
    for step in range(STEPS):
        if step % (STEPS/20) == 0: print(f"{step*100/STEPS}%")
        for bandit in bandits_0_10:
            a, r = bandit.do_action()
            median_0_10[step] += r/BANDITS
            optimal_0_10[step] += 1/BANDITS if a == bandit.optimal else 0

        for bandit in bandits_wgt_0_10:
            a, r = bandit.do_action()
            median_wgt_0_10[step] += r/BANDITS
            optimal_wgt_0_10[step] += 1/BANDITS if a == bandit.optimal else 0

        for bandit in bandits_ucb_1:
            a, r = bandit.do_action(step)
            median_ucb_1[step] += r/BANDITS
            optimal_ucb_1[step] += 1/BANDITS if a == bandit.optimal else 0

        for bandit in bandits_ucb_2:
            a, r = bandit.do_action(step)
            median_ucb_2[step] += r/BANDITS
            optimal_ucb_2[step] += 1/BANDITS if a == bandit.optimal else 0

    median_values = [median_0_10, median_wgt_0_10, median_ucb_1, median_ucb_2]
    optimal_values = [optimal_0_10, optimal_wgt_0_10, optimal_ucb_1, optimal_ucb_2]
    labels = ["Average - ε = 0.10", "Weighted - ε = 0.10", "ucb - c = 1", "ucb - c = 2"]

    plot(
        median_values,
        labels,
        "Median Reward Each Step",
        "Median Reward",
        "res/ucb/median_reward.svg"
    )
    
    plot(
        optimal_values,
        labels,
        "Optimal Action Each Step",
        "Percentual of Optimal Action",
        "res/ucb/optimal_action.svg"
    )

if __name__ == "__main__":
    main()