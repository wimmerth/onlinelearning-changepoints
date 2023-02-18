from river import stream

# from . import base
from river.datasets import base
from .base import ChangePointDataset


class Occupancy(ChangePointDataset):
    """ Interval Training Running Pace

        This dataset shows the pace of a runner during an interval training session, where a mobile application provides instructions on when to run and when to walk.
        Data obtained from the authors' RunDouble account for a run on 2018-07-31.
    """

    def __init__(self):
        super().__init__(
            annotations={
                "6": [
                    60,
                    96,
                    114,
                    174,
                    204,
                    240,
                    258,
                    317
                ],
                "7": [
                    60,
                    96,
                    114,
                    177,
                    204,
                    240,
                    258,
                    317
                ],
                "8": [
                    60,
                    96,
                    114,
                    174,
                    204,
                    240,
                    258,
                    317
                ],
                "10": [
                    2,
                    60,
                    96,
                    114,
                    174,
                    204,
                    240,
                    258,
                    317
                ],
                "12": []
            },
            filename="occupancy.csv",
            task=base.REG,
            n_samples=509,
            n_features=4,
        )
        self._path = "./datasets/occupancy.csv"

    def __iter__(self):
        return stream.iter_csv(
            self._path,  # TODO: Must be changed for integration into river
            target=["V1", "V2", "V3", "V4"],
            converters={
                "V1": float,
                "V2": float,
                "V3": float,
                "V4": float,
            },
            parse_dates={"time": "%Y-%m-%d %H:%M:%S"},
        )
