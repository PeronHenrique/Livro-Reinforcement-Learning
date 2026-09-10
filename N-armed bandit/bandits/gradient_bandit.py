import math
from .random_generator import RandomGenerator

# Class for Gradient bandit with N arms estatic values.
class Gradient_Bandit:
    rng: RandomGenerator
    n: int
    values: list[float]
    optimal: int
    preferences: list[float]
    weight: float
    baseline: float
    use_baseline: bool

    def __init__(self, n: int, seed: int, 
                 weight: float = 0.1, use_baseline: bool = True, mean_value: float = 0):
        self.rng = RandomGenerator(seed)
        self.n = n
        self.values = [self.rng.normal(mean=mean_value) for _ in range(n)]
        self.optimal = self.values.index(max(self.values))
        self.preferences = [0.0 for _ in range(n)]
        self.weight = weight
        self.baseline = 0
        self.use_baseline = use_baseline

    # Value of action + noise
    def reward_action(self, a: int) -> float:
        if a >= self.n:
            raise ValueError("Action index out of range")

        return self.values[a] + self.rng.normal()

    def softmax_preferences(self) -> list[float]:
        max_pref = max(self.preferences)
        exp_preferences = [math.exp(p - max_pref) for p in self.preferences]
        total = sum(exp_preferences)
        return [p / total for p in exp_preferences]

    # Execute one turn of action and updates estimate of values
    def do_action(self, step:int) -> tuple[int, float]:
        #choose action
        prob = self.softmax_preferences()
        a = self.rng.choose(prob)

        # do the action
        reward: float = self.reward_action(a)
        self.baseline += (1/(step+1)) * (reward - self.baseline) if self.use_baseline == True else 0

        # updates preferences
        for i, h in enumerate(self.preferences):
            if i == a: 
                self.preferences[i] = h + self.weight*(reward - self.baseline)*(1-prob[i])
            else:
                self.preferences[i] = h - self.weight*(reward - self.baseline)*prob[i]

        return (a, reward)