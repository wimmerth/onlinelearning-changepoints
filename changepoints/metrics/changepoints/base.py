import abc
import operator

from river import base

# from river.changepoints.methods.base import ChangePointDetector TODO: Change path for integration into river
from methods.base import ChangePointDetector


class ChangePointMetric:
    """Mother class for all change point detection metrics."""

    def __init__(self, margin=5):
        self.margin = margin
        self.value = None

    @abc.abstractmethod
    def __call__(self, annotations, predictions):
        """Execute the metric"""

    def get(self) -> float:
        """Return the current value of the metric."""
        return self.value

    @property
    def bigger_is_better(self):
        """Indicate if a high value is better than a low one or not."""
        return True

    @staticmethod
    def works_with(model: base.Estimator) -> bool:
        """Indicates whether or not a metric can work with a given model."""
        return isinstance(model, ChangePointDetector)

    @property
    def works_with_weights(self) -> bool:
        """Indicate whether the model takes into consideration the effect of sample weights"""
        return False

    def is_better_than(self, other) -> bool:
        op = operator.gt if self.bigger_is_better else operator.lt
        return op(self.get(), other.get())

    def __gt__(self, other):
        return self.is_better_than(other)

    def __repr__(self):
        """Return the class name along with the current value of the metric."""
        return f"{self.__class__.__name__}: {self.get():{self._fmt}}".rstrip("0")

    def __str__(self):
        return repr(self)
