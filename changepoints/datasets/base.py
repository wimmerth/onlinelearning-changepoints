### imports
from river import base
# import pandas as pd

class ChangePointDataset(base.FileDataset):
    def __init__(self, annotations, **desc):
        super().__init__(**desc)
        self._annotations = annotations

    @property
    def annotations(self):
        return self._annotations

    @annotations.setter
    def annotations(self, annotations):
        self._annotations = annotations

################################################################
# dataset name
# annotations or annotations path
# dataset path
# in the __init__ method we load the dataset and the annotations specific to our dataset