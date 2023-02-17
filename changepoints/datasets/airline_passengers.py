from river import stream

# from . import base
from river.datasets import base
from .base import ChangePointDataset


class AirlinePassengers(ChangePointDataset):
    """JFK Airline Passengers

    References
    ----------
    [^1]: 
    """

    def __init__(self):
        super().__init__(
            annotations={
            "6": [
                299
            ],
            "7": [],
            "8": [
                302
            ],
            "9": [
                326,
                382
            ],
            "10": [
                296
            ]
	        },
            filename="airline_passengers.csv",
            task=base.REG,
            n_samples=1_584,
            n_features=2,
        )
        self._path = "./datasets/airline_passengers.csv"

    def __iter__(self):
        return stream.iter_csv(
            self._path,  # TODO: Must be changed for integration into river
            target=["Domestic Passengers","International Passengers","Total Passengers"],
            converters={
                "Airport Code": str,
                "Domestic Passengers": int,"International Passengers": int,"Total Passengers": int,
            },
            parse_dates={"date": "%Y-%b"},
        )
    