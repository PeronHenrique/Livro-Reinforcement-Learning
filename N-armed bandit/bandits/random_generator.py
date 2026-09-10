import random

class RandomGenerator:
    def __init__(self, seed=None):
        self.rng = random.Random(seed)

    # Return random integer in range [a, b]
    def integer(self, min: int, max: int) -> int:
        return self.rng.randint(min, max)

    # Returns if a event with probality happens 
    def chance(self, probability: float) -> bool:
        return self.rng.random() < probability
    
    # Returns a random value based on a normal distribution with median and standart deviation 
    def normal(self, mean: float = 0, std_dev: float = 1) -> float:
        return self.rng.gauss(mean, std_dev)

    # Returns a index based on a list of weights
    def choose(self, weights: list[float]) -> int:
        return self.rng.choices(range(len(weights)), weights=weights)[0]