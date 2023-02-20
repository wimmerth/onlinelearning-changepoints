from evaluation.evaluate import benchmark
from methods import ZeroPredictor, NaiveCPD
from metrics.changepoints import F1, Covering
from datasets import *

if __name__ == "__main__":
    datasets = [Occupancy(), BrentSpotPrice(), Bitcoin(), UKCoalEmploy(), AirlinePassengers(), RunLog()]
    metrics = F1() + Covering()
    print(benchmark(ZeroPredictor(), datasets, metrics, to_csv="test.csv"))
    print(benchmark(NaiveCPD(lookback_window=7, alpha=0.1), datasets, metrics, to_csv="test.csv",
                    include_csv_header=False))
