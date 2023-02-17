# imports
from abc import ABC

from river.datasets import base


class ChangePointDataset(base.FileDataset, ABC):
    def __init__(self, annotations, **desc):
        super().__init__(**desc)
        self._annotations = annotations

    @property
    def annotations(self):
        return self._annotations

    def annotations_aggregated(self, annotator_aggregation):
        if annotator_aggregation == "union":
            annotations = set()
            for annotator in self._annotations:
                annotations.update(self._annotations[annotator])
        elif annotator_aggregation == "intersection":
            annotations = set(self._annotations[0])
            for annotator in self._annotations:
                annotations.intersection_update(self._annotations[annotator])
        elif annotator_aggregation == "majority":
            annotations = {}
            for annotator in self._annotations:
                for change_point in self._annotations[annotator]:
                    if change_point in annotations:
                        annotations[change_point] += 1
                    else:
                        annotations[change_point] = 1
            annotations = {change_point for change_point, count in annotations.items() if
                           count > len(self._annotations) / 2}
        else:
            raise ValueError("Unknown annotator aggregation method.")
        return annotations
