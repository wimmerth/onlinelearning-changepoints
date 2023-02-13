# from river.changepoints.base import ChangePointDetector
from .base import ChangePointDetector


class ZeroPredictor(ChangePointDetector):

    def __init__(self):
        super().__init__()

    def update(self, x, t) -> "ChangePointDetector":
        # This predictor never predicts a change pointa
        return self
