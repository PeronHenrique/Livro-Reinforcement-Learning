# python -m venv .venv
from bandit import E_Bandit

BANDITS: int = 2000
STEPS: int = 1000

def main():
    seed = 123
    bandits_0_1 = [E_Bandit(n=10, epsilon=0.1, seed=seed*2+i) for i in range(BANDITS)]
    bandits_0_01 = [E_Bandit(n=10, epsilon=0.01, seed=seed*3+i) for i in range(BANDITS)]
    bandits_greedy = [E_Bandit(n=10, epsilon=0.0, seed=seed*1+i) for i in range(BANDITS)]
    
    for bandit in bandits_greedy:
        for _ in range(STEPS):
            bandit.do_action()

    for bandit in bandits_0_1:
        for _ in range(STEPS):
            bandit.do_action()

    for bandit in bandits_0_01:
        for _ in range(STEPS):
            bandit.do_action()

if __name__ == "__main__":
    main()