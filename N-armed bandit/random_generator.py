import random

class RandomGenerator:
    def __init__(self, seed=None):
        self.rng = random.Random(seed)

    def integer(self, min: int, max: int) -> int:
        return self.rng.randint(min, max)

    def chance(self, probability: float) -> bool:
        return self.rng.random() < probability

    def normal(self, mean: float = 0, std_dev: float = 1) -> float:
        return self.rng.gauss(mean, std_dev)