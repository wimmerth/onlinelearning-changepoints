from evaluation.evaluate import benchmark
from methods import ZeroPredictor
from metrics.changepoints import F1
from datasets import UKCoalEmploy

if __name__ == "__main__":
    print(benchmark(ZeroPredictor(), UKCoalEmploy(), F1()))
