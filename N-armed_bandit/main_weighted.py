# python -m venv .venv
# .venv/Scripts/Activate.ps1
from plot import plot
from bandits.e_greedy_weighted_bandit import E_Greedy_Weighted_Bandit

BANDITS: int = 2000
STEPS: int = 1000

def main():
    seed = 123
    bandits_0_00: list[E_Greedy_Weighted_Bandit] = [E_Greedy_Weighted_Bandit(n=10, epsilon=0.00, seed=seed+i) for i in range(BANDITS)]
    bandits_0_01: list[E_Greedy_Weighted_Bandit] = [E_Greedy_Weighted_Bandit(n=10, epsilon=0.01, seed=seed+i) for i in range(BANDITS)]
    bandits_0_10: list[E_Greedy_Weighted_Bandit] = [E_Greedy_Weighted_Bandit(n=10, epsilon=0.10, seed=seed+i) for i in range(BANDITS)]
    bandits_opt_0_00: list[E_Greedy_Weighted_Bandit] = [E_Greedy_Weighted_Bandit(n=10, epsilon=0.00, seed=seed+i, initial_value=5) for i in range(BANDITS)]
    bandits_opt_0_01: list[E_Greedy_Weighted_Bandit] = [E_Greedy_Weighted_Bandit(n=10, epsilon=0.01, seed=seed+i, initial_value=5) for i in range(BANDITS)]
    bandits_opt_0_10: list[E_Greedy_Weighted_Bandit] = [E_Greedy_Weighted_Bandit(n=10, epsilon=0.10, seed=seed+i, initial_value=5) for i in range(BANDITS)]

    # Median reward that the bandits received each step 
    median_0_00: list[float] = [0 for _ in range(STEPS)]
    median_0_01: list[float] = [0 for _ in range(STEPS)]
    median_0_10: list[float] = [0 for _ in range(STEPS)]
    median_opt_0_00: list[float] = [0 for _ in range(STEPS)]
    median_opt_0_01: list[float] = [0 for _ in range(STEPS)]
    median_opt_0_10: list[float] = [0 for _ in range(STEPS)]

    # Percentual of times that the bandits choose the optimal action in each step
    optimal_0_00: list[float] = [0 for _ in range(STEPS)]
    optimal_0_01: list[float] = [0 for _ in range(STEPS)]
    optimal_0_10: list[float] = [0 for _ in range(STEPS)]
    optimal_opt_0_00: list[float] = [0 for _ in range(STEPS)]
    optimal_opt_0_01: list[float] = [0 for _ in range(STEPS)]
    optimal_opt_0_10: list[float] = [0 for _ in range(STEPS)]
    
    for step in range(STEPS):
        if step % (STEPS/20) == 0: print(f"{step*100/STEPS}%")
        for bandit in bandits_0_00:
            a, r = bandit.do_action()
            median_0_00[step] += r/BANDITS
            optimal_0_00[step] += 1/BANDITS if a == bandit.optimal else 0

        for bandit in bandits_0_01:
            a, r = bandit.do_action()
            median_0_01[step] += r/BANDITS
            optimal_0_01[step] += 1/BANDITS if a == bandit.optimal else 0

        for bandit in bandits_0_10:
            a, r = bandit.do_action()
            median_0_10[step] += r/BANDITS
            optimal_0_10[step] += 1/BANDITS if a == bandit.optimal else 0

        for bandit in bandits_opt_0_00:
            a, r = bandit.do_action()
            median_opt_0_00[step] += r/BANDITS
            optimal_opt_0_00[step] += 1/BANDITS if a == bandit.optimal else 0

        for bandit in bandits_opt_0_01:
            a, r = bandit.do_action()
            median_opt_0_01[step] += r/BANDITS
            optimal_opt_0_01[step] += 1/BANDITS if a == bandit.optimal else 0

        for bandit in bandits_opt_0_10:
            a, r = bandit.do_action()
            median_opt_0_10[step] += r/BANDITS
            optimal_opt_0_10[step] += 1/BANDITS if a == bandit.optimal else 0

    median_values = [median_0_00, median_0_01, median_0_10, 
                     median_opt_0_00, median_opt_0_01, median_opt_0_10]
    optimal_values = [optimal_0_00, optimal_0_01, optimal_0_10, 
                      optimal_opt_0_00, optimal_opt_0_01, optimal_opt_0_10]
    labels = ["iv = 0 - ε = 0.00", "iv = 0 - ε = 0.01", "iv = 0 - ε = 0.10", 
                      "iv = 5 - ε = 0.00", "iv = 5 - ε = 0.01", "iv = 5 - ε = 0.10"]

    plot(
        median_values,
        labels,
        "Median Reward Each Step",
        "Median Reward",
        "res/wgt/median_reward.svg"
    )
    
    plot(
        optimal_values,
        labels,
        "Optimal Action Each Step",
        "Percentual of Optimal Action",
        "res/wgt/optimal_action.svg"
    )

    plot(
        median_values[:3],
        labels[:3],
        "Median Reward Each Step",
        "Median Reward",
        "res/wgt/median_reward iv=0.svg"
    )

    plot(
        optimal_values[:3],
        labels[:3],
        "Optimal Action Each Step",
        "Percentual of Optimal Action",
        "res/wgt/optimal_action iv=0.svg"
    )

    plot(
        median_values[3:],
        labels[3:],
        "Median Reward Each Step",
        "Median Reward",
        "res/wgt/median_reward iv=5.svg"
    )

    plot(
        optimal_values[3:],
        labels[3:],
        "Optimal Action Each Step",
        "Percentual of Optimal Action",
        "res/wgt/optimal_action iv=5.svg"
    )

    
    plot(
        optimal_values[2:4],
        labels[2:4],
        "Optimal Action Each Step",
        "Percentual of Optimal Action",
        "res/wgt/optimal_action livro.svg"
    )


if __name__ == "__main__":
    main()