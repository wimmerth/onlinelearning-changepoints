# from river.changepoints.methods.base import ChangePointDetector
from methods.base import ChangePointDetector

from collections import deque
from numbers import Number
from typing import Any, Dict, List, Tuple, Type, Union

import networkx as nx
import numpy as np
from typing_extensions import Literal


# import stats
from abc import ABC, abstractmethod
from collections import Counter, defaultdict
from math import sqrt
from typing import Dict

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Union

import numpy as np


class Scaler(ABC):
    @abstractmethod
    def scale(self, x: Dict[str, float]):
        pass

    def __repr__(self) -> str:
        return self.__class__.__name__


class StandardScaler(Scaler):
    def __init__(self):
        self._counts = Counter()
        self._means = defaultdict(float)
        self._variances = defaultdict(float)

    @abstractmethod
    def non_zero_div(x, y):
        try:
            return x/(y)
        except ZeroDivisionError:
            return 0

    def scale(self, x: Dict[str, float]):
        for k, v in x.items():
            self._counts[k] += 1
            prev_mean = self._means[k]
            self._means[k] += (v-prev_mean)/self._counts[k]
            self._variances[k] += (((v-prev_mean) *
                                   (v-self._means[k])) / self._counts[k])
        return {k: StandardScaler.non_zero_div(v-self._means[k], sqrt(self._variances[k])) for k, v in x.items()}
    
class ECDAS(ChangePointDetector):
    """A multivariate change point detector that compares the new points with a description of the current distribution. 
    A changepoint is detected if the distribution mean goes over a threshold."""

    def __init__(self,
                 num_features: Union[str, List[Union[str, Tuple[str, float]]]]=["feature1"],
                 cat_features: Union[str, List[Union[str, Tuple[str, float]]]]=[],
                 window_size: int=30,
                 num_scaler: Type[Scaler] = None,
                 cat_scaler: Type[Scaler] = None,
                 custom_start: int = None,
                 threshold: float = .9,
                 **kwargs):
        super().__init__(**kwargs)
        self.features = {0: (None,  # categorical window
                                NumericalWindow(num_features, window_size,
                                                None if not num_scaler else num_scaler()))}
        self._window_size = window_size
        self._num_scaler = num_scaler
        self._custom_start = custom_start if custom_start else window_size
        self.num_feature_count = len(num_features) if isinstance(
            num_features, list) else 1
        self.initialized = False
        # self.cat_feature_count = len(cat_features) if isinstance(
        #     cat_features, list) else 1

        # threshold detector
        self.detector = ThresholdChangeDetector(
            mean_threshold=threshold, window_size=window_size, min_samples=window_size)

    def update(self, x, t) -> "ChangePointDetector":
        self._change_point_detected = False
        # print(f"data: {x}, type: {type(x)}")
        if not isinstance(x, dict):
            x = {"feature1": x}
        if not self.initialized:
            num_features = list(x.keys())
            self.features = {0: (None,  # categorical window
                                NumericalWindow(num_features, self._window_size,
                                                None if not self._num_scaler else self._num_scaler()))}
            self.initialized = True
        node_id = False
        f = self.features[node_id if node_id else 0]
        _, num_window = f
        should_score = t+1 >= self._custom_start if not self._custom_start is None \
            else t+1 > self._window_size
        triggered = False
        num_avg, num_features, num_scores = num_window.learn_one(
            x, should_score)
        # same thing for categorical features
        # ...
        avg = num_avg  # + cat_features
        if should_score:
            # print("num scores", num_scores)
            triggered = self.detector.step(avg)
            self._change_point_detected = triggered
        # return triggered, avg, (0, None, None), (num_avg, num_features, num_scores)
        
        return self

    def _reset(self):
        super()._reset()
        self.lookback_values = []

    def is_multivariate(self):
        return True
    
    
class ThresholdChangeDetector:
    def __init__(self, mean_threshold: float, window_size: int = 10, min_samples: int = 100):
        assert .0 < mean_threshold < 1.
        self._changepoint = None
        self._min_samples = min_samples
        self._window = deque(maxlen=window_size)
        self._mean_threshold = mean_threshold
        self._min_samples = min_samples
        self._N = 0
        self._mean = 0

    def step(self, x: Number) -> bool:
        self._window.append(x)
        self._N += 1
        prev_mean = self._mean
        self._mean += (x - prev_mean) / self._N
        triggered = False
        if self._N > self._min_samples:
            window_mean = sum(self._window) / len(self._window)
            mean_ratio = window_mean / (self._mean + 1e-6)
            if any([mean_ratio > (1. + self._mean_threshold),
                    mean_ratio < (1. - self._mean_threshold)]):
                triggered = True
                self._changepoint = self._N
        return triggered


class Window(ABC):
    def __init__(self, features: Union[str, List[Union[str, Tuple[str, float]]]], size: int,  scaler: Scaler, p: float = .6):
        assert .0 < p < 1., "'p' threshold must be between 0 and 1."
        if isinstance(features, (str, tuple)):
            features = [features]
        features = [([*f]+[1.]*max(0, 2-len(f)))[:2] if isinstance(f, (tuple, list)) else (f, 1.)
                    for f in features]
        features, weights = zip(*features)
        self._features = np.asarray(features, dtype=object)
        self._weights = np.asarray(weights)
        self._index = 0
        self._scaler = scaler
        self._p = p
        self.size = size

    def extract_features(self, x: Dict):
        return {k: x[k] if k in x else .0 for k in self._features}

    @abstractmethod
    def _reference_average(self):
        pass

    @abstractmethod
    def _update(self, x: np.array):
        pass

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(features={len(self._features)}, size={self.size}, scaler={self._scaler}, p={self._p})'


class NumericalWindow(Window):
    def __init__(self, features: Union[str, List[Union[str, Tuple[str, float]]]], size: int, scaler: Scaler = None):
        super().__init__(features, size, scaler)
        shape = (size, len(self._features))
        self._reference = np.zeros(shape)
        self._current = np.zeros(shape)

    def _reference_average(self):
        return np.average(self._reference, axis=0) * self._weights

    def _update(self, x: np.array):
        if self._index < self._current.shape[0]:
            self._current[self._index] = x
            self._index += 1
        else:
            self._index = 0
            self._reference[:] = self._current
            self._current[self._index] = x
            self._current[self._index+1:] = 0

    # -> mean_score, features, score_per_feature

    def learn_one(self, x: Dict, should_score: bool = False) -> Tuple[float, np.ndarray, np.ndarray]:
        x = self.extract_features(x)
        if self._scaler:
            x = self._scaler.scale(x)
        x = np.fromiter(x.values(), dtype=np.float64)  # to numpy array
        self._update(x)
        out = np.zeros(len(self._features))
        if not should_score:
            return 0., self._features, out
        ref = self._reference_average()
        loss = Utils.rmse(ref, x) * self._weights
        out[:] = loss
        idx = np.argsort(out)[::-1]
        return np.mean(out, axis=0), self._features[idx], out[idx]
    
class Utils():
    def __init__(self) -> None:
        pass
    def rmse(y: np.ndarray, x: np.ndarray, expand: bool = True):
        if expand:
            y, x = np.expand_dims(y, 0), np.expand_dims(x, 0)
        return np.sqrt(np.mean((y-x)**2, axis=0))
