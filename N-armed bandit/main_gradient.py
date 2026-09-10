# python -m venv .venv
# .venv/Scripts/Activate.ps1
from plot import plot
from bandits.gradient_bandit import Gradient_Bandit

BANDITS: int = 2000
STEPS: int = 1000

def main():
    seed = 123
    bandits_01_T_4 : list[Gradient_Bandit] = [Gradient_Bandit(n=10, seed=seed+i, weight=0.1, use_baseline= True, mean_value=4) 
                                                for i in range(BANDITS)]
    bandits_01_T_0 : list[Gradient_Bandit] = [Gradient_Bandit(n=10, seed=seed+i, weight=0.1, use_baseline= True, mean_value=0) 
                                                for i in range(BANDITS)]
    bandits_04_T_4 : list[Gradient_Bandit] = [Gradient_Bandit(n=10, seed=seed+i, weight=0.4, use_baseline= True, mean_value=4) 
                                                for i in range(BANDITS)]
    bandits_01_F_4 : list[Gradient_Bandit] = [Gradient_Bandit(n=10, seed=seed+i, weight=0.1, use_baseline=False, mean_value=4) 
                                                for i in range(BANDITS)]
    bandits_01_F_0 : list[Gradient_Bandit] = [Gradient_Bandit(n=10, seed=seed+i, weight=0.1, use_baseline=False, mean_value=0) 
                                                for i in range(BANDITS)]
    bandits_04_F_4 : list[Gradient_Bandit] = [Gradient_Bandit(n=10, seed=seed+i, weight=0.4, use_baseline=False, mean_value=4) 
                                                for i in range(BANDITS)]

    # Median reward that the bandits received each step 
    median_01_T_4: list[float] = [0 for _ in range(STEPS)]
    median_01_T_0: list[float] = [0 for _ in range(STEPS)]
    median_04_T_4: list[float] = [0 for _ in range(STEPS)]
    median_01_F_4: list[float] = [0 for _ in range(STEPS)]
    median_01_F_0: list[float] = [0 for _ in range(STEPS)]
    median_04_F_4: list[float] = [0 for _ in range(STEPS)]

    # Percentual of times that the bandits choose the optimal action in each step
    optimal_01_T_4: list[float] = [0 for _ in range(STEPS)]
    optimal_01_T_0: list[float] = [0 for _ in range(STEPS)]
    optimal_04_T_4: list[float] = [0 for _ in range(STEPS)]
    optimal_01_F_4: list[float] = [0 for _ in range(STEPS)]
    optimal_01_F_0: list[float] = [0 for _ in range(STEPS)]
    optimal_04_F_4: list[float] = [0 for _ in range(STEPS)]
    
    for step in range(STEPS):
        if step % (STEPS/20) == 0: print(f"{step*100/STEPS}%")
        for bandit in bandits_01_T_4:
            a, r = bandit.do_action(step)
            median_01_T_4[step] += r/BANDITS
            optimal_01_T_4[step] += 1/BANDITS if a == bandit.optimal else 0

        for bandit in bandits_01_T_0:
            a, r = bandit.do_action(step)
            median_01_T_0[step] += r/BANDITS
            optimal_01_T_0[step] += 1/BANDITS if a == bandit.optimal else 0

        for bandit in bandits_04_T_4:
            a, r = bandit.do_action(step)
            median_04_T_4[step] += r/BANDITS
            optimal_04_T_4[step] += 1/BANDITS if a == bandit.optimal else 0

        for bandit in bandits_01_F_4:
            a, r = bandit.do_action(step)
            median_01_F_4[step] += r/BANDITS
            optimal_01_F_4[step] += 1/BANDITS if a == bandit.optimal else 0

        for bandit in bandits_01_F_0:
            a, r = bandit.do_action(step)
            median_01_F_0[step] += r/BANDITS
            optimal_01_F_0[step] += 1/BANDITS if a == bandit.optimal else 0

        for bandit in bandits_04_F_4:
            a, r = bandit.do_action(step)
            median_04_F_4[step] += r/BANDITS
            optimal_04_F_4[step] += 1/BANDITS if a == bandit.optimal else 0

    median_values = [median_01_T_4, median_01_T_0, median_04_T_4, median_01_F_4, median_01_F_0, median_04_F_4]
    optimal_values = [optimal_01_T_4, optimal_01_T_0, optimal_04_T_4, optimal_01_F_4, optimal_01_F_0, optimal_04_F_4]
    labels = [
            "a=0.1 - Baseline=T - Mean Value=4",
            "a=0.1 - Baseline=T - Mean Value=0",
            "a=0.4 - Baseline=T - Mean Value=4",
            "a=0.1 - Baseline=T - Mean Value=4",
            "a=0.1 - Baseline=F - Mean Value=4",
            "a=0.1 - Baseline=F - Mean Value=0",
            "a=0.4 - Baseline=F - Mean Value=4",
        ]

    plot(
        [median_values[i] for i in [0, 2, 3, 5]],
        [labels[i] for i in [0, 2, 3, 5]],
        "Median Reward Each Step",
        "Median Reward",
        "res/grad/median_reward baseline.svg"
    )
    
    plot(
        [optimal_values[i] for i in [0, 2, 3, 5]],
        [labels[i] for i in [0, 2, 3, 5]],
        "Optimal Action Each Step",
        "Percentual of Optimal Action",
        "res/grad/optimal_action baseline.svg"
    )

    plot(
        [median_values[i] for i in [0, 1, 3, 4]],
        [labels[i] for i in [0, 1, 3, 4]],
        "Median Reward Each Step",
        "Median Reward",
        "res/grad/median_reward mean value.svg"
    )
    
    plot(
        [optimal_values[i] for i in [0, 1, 3, 4]],
        [labels[i] for i in [0, 1, 3, 4]],
        "Optimal Action Each Step",
        "Percentual of Optimal Action",
        "res/grad/optimal_action mean value.svg"
    )

if __name__ == "__main__":
    main()