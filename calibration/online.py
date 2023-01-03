"""
This module contains an implementation of

Kuleshov, Volodymyr, and Stefano Ermon. "Reliable confidence estimation via online learning."
arXiv preprint arXiv:1607.03594 (2016): 2586-2594.
"""


class MeanCalibrator:
    def __init__(self, n_bins=15, alpha=0.5):
        self.n_bins = n_bins
        self.bin_means = {}
        self.alpha = alpha

    def fit_one(self, y_pred, y_true):
        if not int(y_pred * self.n_bins) in self.bin_means:
            self.bin_means[int(y_pred * self.n_bins)] = y_true
        else:
            self.bin_means[int(y_pred * self.n_bins)] = self.bin_means[int(y_pred * self.n_bins)] * (1 - self.alpha) + y_true * self.alpha

    def predict_one(self, y_pred):
        if not int(y_pred * self.n_bins) in self.bin_means:
            return y_pred
        else:
            return self.bin_means[int(y_pred * self.n_bins)]

    def fit(self, y_pred, y_true):
        for i in range(len(y_pred)):
            self.fit_one(y_pred[i], y_true[i])

    def predict(self, y_pred):
        return [self.predict_one(y) for y in y_pred]

    def reset(self):
        self.bin_means = {}
