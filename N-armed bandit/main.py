# python -m venv .venv
from bandit import E_Bandit

BANDITS: int = 2000
STEPS: int = 1000

def main():
    seed = 123
    bandits_0_1 =       [E_Bandit(n= 10, epsilon= 0.10, seed= seed+i) for i in range(BANDITS)]
    bandits_0_01 =      [E_Bandit(n= 10, epsilon= 0.01, seed= seed+i) for i in range(BANDITS)]
    bandits_greedy =    [E_Bandit(n= 10, epsilon= 0.00, seed= seed+i) for i in range(BANDITS)]
    
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