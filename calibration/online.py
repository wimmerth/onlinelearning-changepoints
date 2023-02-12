"""
This module contains an implementation of

Kuleshov, Volodymyr, and Stefano Ermon. "Reliable confidence estimation via online learning."
arXiv preprint arXiv:1607.03594 (2016): 2586-2594.
"""
from river import linear_model
from river import optim

from sklearn.linear_model import LogisticRegression


class MeanCalibrator:
    """
    Return running mean of bin as calibrated score.
    """

    def __init__(self, n_bins=15, alpha=0.5, keep=0.1):
        assert 1 >= alpha >= 0, f"alpha should be a value between 0 and 1, but is {alpha}"
        assert 1 >= keep >= 0, f"keep should be a value between 0 and 1, but is {keep}"
        assert n_bins > 0, f"n_bins should be a positive integer, but is {n_bins}"

        self.n_bins = n_bins
        self.bin_means = {}
        self.alpha = alpha
        self.keep = keep

    def fit_one(self, y_pred, y_true):
        if not int(y_pred * self.n_bins) in self.bin_means:
            self.bin_means[int(y_pred * self.n_bins)] = y_true
        else:
            self.bin_means[int(y_pred * self.n_bins)] = self.bin_means[int(y_pred * self.n_bins)] * (
                        1 - self.alpha) + y_true * self.alpha

    def predict_one(self, y_pred):
        if not int(y_pred * self.n_bins) in self.bin_means:
            return y_pred
        else:
            return y_pred * self.keep + (1 - self.keep) * self.bin_means[int(y_pred * self.n_bins)]

    def fit(self, y_pred, y_true):
        for i in range(len(y_pred)):
            self.fit_one(y_pred[i], y_true[i])

    def predict(self, y_pred):
        return [self.predict_one(y) for y in y_pred]

    def reset(self):
        self.bin_means = {}


class PlattCalibrator:
    """
    Fit a Platt calibration to each bin.
    """

    def __init__(self, n_bins=15, keep=0.1):
        assert 1 >= keep >= 0, f"keep should be a value between 0 and 1, but is {keep}"
        assert n_bins > 0, f"n_bins should be a positive integer, but is {n_bins}"

        self.n_bins = n_bins
        self.bin_entries = {}
        self.keep = keep

    def fit_one(self, y_pred, y_true):
        if not int(y_pred * self.n_bins) in self.bin_entries:
            self.bin_entries[int(y_pred * self.n_bins)] = []
        self.bin_entries[int(y_pred * self.n_bins)].append((y_pred, y_true))

    def predict_one(self, y_pred):
        if not int(y_pred * self.n_bins) in self.bin_entries:
            return y_pred
        else:
            bin_entries = self.bin_entries[int(y_pred * self.n_bins)]
            if len(bin_entries) == 0:
                return y_pred
            else:
                return self.keep * y_pred + (1 - self.keep) * self.platt_fit(bin_entries)

    def platt_fit(self, bin_entries):
        # See https://en.wikipedia.org/wiki/Platt_scaling

        # Compute t+ and t-
        pos_sum = sum([y > 0 for _, y in bin_entries])
        neg_sum = len(bin_entries) - pos_sum
        t_pos = (pos_sum + 1) / (pos_sum + 2)
        t_neg = 1 / (neg_sum + 2)


class PlattCalibratorSklearn:
    """
    Fit a Platt calibration to each bin. Uses sklearn's LogisticRegression.
    """

    def __init__(self, n_bins=15, keep=0.1):
        assert 1 >= keep >= 0, f"keep should be a value between 0 and 1, but is {keep}"
        assert n_bins > 0, f"n_bins should be a positive integer, but is {n_bins}"

        self.n_bins = n_bins
        self.bin_entries = {}
        self.keep = keep
