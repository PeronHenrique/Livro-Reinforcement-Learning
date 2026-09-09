from .random_generator import RandomGenerator

# Class for bandit with N arms estatic values and updates estimates by by weighted sum. 
# Can receive a initial value to witch the estimate to all actions is initialized 
# Choose action based on episolon-greed method
class E_Greedy_Weighted_Bandit:
    rng: RandomGenerator
    n: int
    values: list[float]
    optimal: int
    estimates: list[float]
    weight: float
    epsilon: float

    def __init__(self, n: int, epsilon: float, seed: int, 
                 initial_value: float = 0, weight: float = 0.1):
        self.rng = RandomGenerator(seed)
        self.n = n
        self.values = [self.rng.normal() for _ in range(n)]
        self.optimal = self.values.index(max(self.values))
        self.estimates = [initial_value for _ in range(n)]
        self.weight = weight
        self.epsilon = epsilon
        self.log = dict()

    # Value of action + noise
    def reward_action(self, a: int) -> float:
        if a >= self.n:
            raise ValueError("Action index out of range")

        return self.values[a] + self.rng.normal()

    # Execute one turn of action and updates estimate of values
    def do_action(self) -> tuple[int, float]:
        #explore
        a: int = self.rng.integer(0, self.n - 1)
        if not self.rng.chance(self.epsilon):
            #exploit
            a = self.estimates.index(max(self.estimates))

        # do the action
        reward: float = self.reward_action(a)

        #update estimate
        self.estimates[a] += self.weight * (reward - self.estimates[a])
        return (a, reward)
