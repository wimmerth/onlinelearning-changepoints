# from river.changepoints.methods.base import ChangePointDetector
from methods.base import ChangePointDetector


class NaiveCPD(ChangePointDetector):
    """A change point detector that uses a linear regression over a specified lookback window to predict
    the next value and then compares the prediction with the actual value. If the actual value is too
    far from the prediction, a change point is detected."""

    def __init__(self, lookback_window, alpha=0.1, **kwargs):
        super().__init__(**kwargs)
        self.lookback_window = lookback_window
        self.alpha = alpha
        self.lookback_values = []

    def update(self, x, t) -> "ChangePointDetector":

        if t > self.lookback_window:
            # Linear regression without using numpy
            mean_x = sum(range(1, len(self.lookback_values) + 1)) / len(self.lookback_values)
            mean_y = sum(self.lookback_values) / len(self.lookback_values)
            numerator = sum([(i + 1 - mean_x) * (y - mean_y) for i, y in enumerate(self.lookback_values)])
            denominator = sum([(i + 1 - mean_x) ** 2 for i in range(len(self.lookback_values))])
            slope = numerator / denominator
            intercept = mean_y - slope * mean_x
            y_pred = slope * t + intercept

            var_y = sum([(y - mean_y) ** 2 for y in self.lookback_values]) / (len(self.lookback_values) - 1)

            if y_pred - self.alpha * var_y < x < y_pred + self.alpha * var_y:
                self._change_point_detected = False
            else:
                self._change_point_detected = True
            self._change_point_score = abs(x - y_pred) / var_y
            self.lookback_values.pop(0)

        self.lookback_values.append(x)
        return self

    def _reset(self):
        super()._reset()
        self.lookback_values = []

    def is_multivariate(self):
        return False
