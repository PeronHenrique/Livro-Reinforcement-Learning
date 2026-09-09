from random_generator import RandomGenerator

class E_Bandit:
    rng: RandomGenerator
    n: int
    values: list[float]
    estimates: list[float]
    counts: list[int]
    epsilon: float
    # dict: {step: (action, reward)}
    log: dict[int, tuple[int, float]]
    step: int

    def __init__(self, n: int, epsilon: float, seed: int, initial_value: float = 0):
        self.rng = RandomGenerator(seed)
        self.n = n
        self.values = [self.rng.normal() for _ in range(n)]
        self.estimate = [initial_value for _ in range(n)]
        self.counts = [0 for _ in range(n)]
        self.epsilon = epsilon
        self.log = dict()
        self.step = 0

    # Value of action + noise
    def reward_action(self, a: int) -> float:
        if a >= self.n:
            raise ValueError("Action index out of range")

        self.counts[a] += 1
        return self.values[a] + self.rng.normal()

    # Execute one turn of action and updates estimate of values
    def do_action(self):
        a: int = -1
        if self.rng.chance(self.epsilon):
            #explore
            a = self.rng.integer(0, self.n - 1)
        else:
            #exploit
            a = self.estimate.index(max(self.estimate))

        # do the action
        reward: float = self.reward_action(a)
        self.step += 1
        self.log[self.step] = (a, reward)

        #update estimate
        self.estimate[a] += (1 / self.counts[a]) * (reward - self.estimate[a])
