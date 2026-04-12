class BurstPredictor:
    """
    Predicts the next CPU burst time using Exponential Moving Average (EMA).

    Formula:  Predicted_next = alpha * actual_burst + (1 - alpha) * old_prediction

    This allows the scheduler to pre-set the right CPU frequency BEFORE a
    process starts executing — avoiding wasteful frequency ramp-ups.

    alpha = 0.5 means equal weight to recent and historical bursts.
    Higher alpha → reacts faster to changes.
    Lower alpha  → smoother, more stable predictions.
    """

    def __init__(self, alpha=0.5):
        self.alpha       = alpha
        self.history     = {}      # pid -> list of past burst times
        self.predictions = {}      # pid -> last predicted burst

    def update(self, pid, actual_burst):
        """Record an actual burst and update the prediction."""
        if pid not in self.history:
            self.history[pid]     = []
            self.predictions[pid] = actual_burst   # Bootstrap with actual

        self.history[pid].append(actual_burst)
        old = self.predictions[pid]
        new = self.alpha * actual_burst + (1 - self.alpha) * old
        self.predictions[pid] = new
        return round(new, 2)

    def predict(self, pid, default_burst):
        """Return predicted burst. Falls back to default_burst if unseen."""
        return round(self.predictions.get(pid, default_burst), 2)

    def get_accuracy(self, pid):
        """Returns average prediction accuracy (%) for a process."""
        if pid not in self.history or len(self.history[pid]) < 2:
            return None
        actuals = self.history[pid]
        pred    = actuals[0]
        errors  = []
        for actual in actuals[1:]:
            if actual > 0:
                errors.append(abs(actual - pred) / actual * 100)
            pred = self.alpha * actual + (1 - self.alpha) * pred
        return round(100 - sum(errors) / len(errors), 2) if errors else 100.0
