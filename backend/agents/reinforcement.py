def score_from_result(correct, response_time, avg_time, hints, failure):
    if correct and response_time is not None and avg_time is not None and response_time <= avg_time:
        return 1.0
    if correct:
        return 0.8
    if failure == "partial":
        return 0.5
    if failure == "wrong":
        return 0.2
    return 0.0


def apply_prediction_error(memory, low, high, actual, obj):
    if actual is None:
        return

    if actual < low:
        error = actual - low
    elif actual > high:
        error = actual - high
    else:
        return

    severity = abs(error)

    if error < 0:
        # actual is below lower bound -> worsen memory
        obj.decay_rate = (obj.decay_rate or 0.1) * (1 + severity)
        obj.reinforcement_gain = (obj.reinforcement_gain or 0.2) * (1 - 0.5 * severity)
        obj.fatigue_modifier = (obj.fatigue_modifier or 1.0) * (1 + 0.3 * severity)
    else:
        # actual above upper bound -> improve memory
        obj.decay_rate = (obj.decay_rate or 0.1) * max(0.0, (1 - 0.7 * severity))
        obj.reinforcement_gain = (obj.reinforcement_gain or 0.2) * (1 + 0.5 * severity)
        obj.stability_factor = (obj.stability_factor or 1.0) * (1 + 0.4 * severity)
