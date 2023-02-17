from evaluation.evaluate import benchmark
from methods import ZeroPredictor, NaiveCPD
from metrics.changepoints import F1, Covering
from datasets import UKCoalEmploy, BrentSpotPrice, Bitcoin
from datasets.airline_passengers import AirlinePassengers

if __name__ == "__main__":
    datasets = [UKCoalEmploy(), BrentSpotPrice(), Bitcoin()]
    # datasets = [AirlinePassengers()]
    metrics = F1() + Covering()
    print(benchmark(ZeroPredictor(), datasets, metrics))
    print(benchmark(NaiveCPD(lookback_window=5, alpha=0.1), datasets, metrics))
