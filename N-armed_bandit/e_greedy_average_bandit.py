from random_generator import RandomGenerator

# Class for bandit with N arms estatic values and updates estimates by average. 
# Can receive a initial value to witch the estimate to all actions is initialized 
class E_Greedy_Average_Bandit:
    rng: RandomGenerator
    n: int
    values: list[float]
    optimal: int
    estimates: list[float]
    counts: list[int]
    epsilon: float

    def __init__(self, n: int, epsilon: float, seed: int, initial_value: float = 0):
        self.rng = RandomGenerator(seed)
        self.n = n
        self.values = [self.rng.normal() for _ in range(n)]
        self.optimal = self.values.index(max(self.values))
        self.estimate = [initial_value for _ in range(n)]
        self.counts = [0 for _ in range(n)]
        self.epsilon = epsilon

    # Value of action + noise
    def reward_action(self, a: int) -> float:
        if a >= self.n:
            raise ValueError("Action index out of range")

        self.counts[a] += 1
        return self.values[a] + self.rng.normal()

    # Execute one turn of action and updates estimate of values
    def do_action(self) -> tuple[int, float]:
        #explore
        a: int = self.rng.integer(0, self.n - 1)
        if not self.rng.chance(self.epsilon):
            #exploit
            a = self.estimate.index(max(self.estimate))

        # do the action
        reward: float = self.reward_action(a)

        #update estimate
        self.estimate[a] += (1 / self.counts[a]) * (reward - self.estimate[a])
        return (a, reward)
