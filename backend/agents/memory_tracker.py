import math
from datetime import datetime


def decay(memory, decay_rate, stability, interference, days):
    return memory * math.exp(-decay_rate * stability * interference * days)


def predict_range(memory, decay_rate, days, uncertainty, interference, fatigue):
    predicted = memory * math.exp(-decay_rate * days)
    uncertainty_val = uncertainty * interference * fatigue
    return predicted - uncertainty_val, predicted + uncertainty_val


def half_life(decay_rate, stability, interference):
    if decay_rate * stability * interference == 0:
        return float('inf')
    return math.log(2) / (decay_rate * stability * interference)
