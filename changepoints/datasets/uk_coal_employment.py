from river import stream

# from . import base
from river import base
from .base import ChangePointDataset

class UKCoalEmploy(ChangePointDataset):
    """Historic Employment in UK Coal Mines

    This is historic data obtained from the UK government.
	We use the employment column for the number of workers employed in the British coal mines
	Missing values in the data are replaced with the value of the preceding year.

    References
    ----------
    [^1]: https://www.gov.uk/government/statistical-data-sets/historical-coal-data-coal-production-availability-and-consumption
    """

    def __init__(self):
        super().__init__(
            annotations= ...,
            filename="uk_coal_employment.csv",
            task=base.REG,
            n_samples=105,
            n_features=1,
        )

    def _iter(self):
        return stream.iter_csv(
            self.path,
            target="Employment",
            converters={
                "Employment": int,
            },
            parse_dates={"Year": "%Y"},
        )
