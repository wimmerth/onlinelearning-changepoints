import abc
import numbers

from . import base


class ChangePointDetector(base.Base):
    """A change point detector."""

    def __init__(self):
        self._change_point_detected = False
        self._change_point_score = 0.0

    def _reset(self):
        """Reset the change detector."""
        self._change_point_detected = False
        self._change_point_score = 0.0

    @property
    def change_point_detected(self) -> bool:
        """
        Returns True if a change point was detected.
        """
        return self.change_point_detected

    @property
    def change_point_score(self) -> float:
        """
        Returns the change point score.
        """
        return self._change_point_score

    @abc.abstractmethod
    def update(self, x: numbers.Number) -> "ChangePointDetector":
        """Update the change point detector with a single data point.

        Parameters
        ----------
        x
            Input value.

        Returns
        -------
        self

        """