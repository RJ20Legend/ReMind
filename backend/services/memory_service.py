import math

def forgetting_curve(initial_strength: float, days: float, decay_rate: float = 0.1) -> float:
    return initial_strength * math.exp(-decay_rate * days)
