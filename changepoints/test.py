from evaluation.evaluate import benchmark
from methods import ZeroPredictor, NaiveCPD, WATCH, ECDAS
from metrics.changepoints import F1, Covering
from datasets import *

if __name__ == "__main__":
    datasets = [Occupancy(), BrentSpotPrice(), Bitcoin(), UKCoalEmploy(), AirlinePassengers(), RunLog()]
    metrics = F1() + Covering()
    print(benchmark(ZeroPredictor(), datasets, metrics, to_csv="test.csv"))
    print(benchmark(NaiveCPD(lookback_window=7, alpha=0.1), datasets, metrics, to_csv="test.csv",
                    include_csv_header=False))
    print(benchmark(WATCH(batch_size=16, min_distr_size=64, max_distr_size=256, epsilon=1), datasets, metrics, to_csv="test.csv",
                    include_csv_header=False))
    print(benchmark(ECDAS(window_size=25), datasets, metrics, to_csv="test.csv"))
