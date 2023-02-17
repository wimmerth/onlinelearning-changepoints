# from river.changepoints.methods.base import ChangePointDetector TODO: Change path for integration into river
from methods.base import ChangePointDetector
# import river.metrics.changepoints.base TODO: Change path for integration into river
import metrics.changepoints.base
# import river.datasets.changepoints.base TODO: Change path for integration into river
import datasets.base


def load_dataset(dataset: datasets.base.ChangePointDataset):
    """
    Load a changepoint dataset.
    :param dataset: The dataset to load.
    :return: A tuple containing the data and the annotations.
    """
    annotations = dataset.annotations
    return dataset, annotations


def run_method(method: ChangePointDetector, data: datasets.base.ChangePointDataset):
    """
    Run a changepoint detection method on a dataset.
    :param method: The method to run.
    :param data: The dataset to run the method on.
    :return: A list of change points.
    """
    changepoints = []
    n_obs = 0
    for t, (T, x) in enumerate(data, start=1):
        method.update(x, t)
        n_obs += 1
        if method.change_point_detected:
            changepoints.append(t)
    return changepoints, n_obs


def evaluate_method(changepoints: list,
                    annotations: list,
                    metric: metrics.changepoints.base.ChangePointMetric,
                    n_obs: int):
    """
    Evaluate a method on a dataset.
    :param changepoints: A list of change points.
    :param annotations: A list of annotations.
    :param metric: The metric to use for evaluation.
    :param n_obs: The number of observations in the dataset.
    :return: A dictionary containing the results.
    """
    return metric(changepoints, annotations, n_obs=n_obs)


def benchmark(
        method,
        dataset,
        metric):
    if not isinstance(dataset, datasets.base.ChangePointDataset):
        results = []
        for ds in dataset:
            results.append(benchmark(method, ds, metric))
        return results

    data, annotations = load_dataset(dataset)
    changepoints, n_obs = run_method(method, data)
    results = evaluate_method(annotations, changepoints, metric, n_obs=n_obs)
    return results
