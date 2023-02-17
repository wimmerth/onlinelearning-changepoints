from evaluation.evaluate import benchmark
from methods import ZeroPredictor, NaiveCPD
from metrics.changepoints import F1, Covering
from datasets import UKCoalEmploy, BrentSpotPrice, Bitcoin, AirlinePassengers

if __name__ == "__main__":
    print(benchmark(ZeroPredictor(), UKCoalEmploy(), F1()))
    print(benchmark(ZeroPredictor(), BrentSpotPrice(), F1()))
    print(benchmark(ZeroPredictor(), AirlinePassengers(), F1()))
    print(benchmark(NaiveCPD(lookback_window=5, alpha=0.1), Bitcoin(), F1()))
    print(benchmark(NaiveCPD(lookback_window=5, alpha=0.1), BrentSpotPrice(), F1()))
