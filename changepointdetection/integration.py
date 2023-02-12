"""
A wrapper for a new change point detector implemented with river.

This file is a modified version of the template file given by:
    Author: G.J.J. van den Burg
    Date: 2020-05-07
    License: MIT
    Copyright: 2020, The Alan Turing Institute
"""

import argparse
import time

from cpdbench_utils import load_dataset, exit_success, exit_with_error, make_param_dict, exit_with_timeout
from multiprocessing import Process, Manager

TIMEOUT = 60 * 30  # 30 minutes

METHODS = {
    # TODO: add methods (is this the best way to access the different modules?)
}


def parse_args():
    parser = argparse.ArgumentParser(description="Wrapper for any change point detector implemented with river.")
    parser.add_argument(
        "-i", "--input", help="path to the input data file", required=True
    )
    parser.add_argument("-o", "--output", help="path to the output file")
    parser.add_argument("--use-timeout", action="store_true")

    parser.add_argument("-m", "--method", help="change point detection method (class name)", required=True)

    # TODO: How do we handle the different parameters for different algorithms? How do we parse these arbitrary parameters in a kwargs dict?

    # OPTION 1: Use a config file
    # parser.add_argument("--config", help="path to the config file for the method (in YAML format)")

    # OPTION 2: A little hacky, but we can use the `nargs` argument to parse a list of parameters
    # parser.add_argument("--parameters", nargs="+", help="list of parameters for the method")

    # OPTION 3: Also hacky: use parse_known_args() to parse the parameters and then manually parse the rest
    # parsed, unparsed = parser.parse_known_args()
    # for arg in unparsed:
    #     if arg.startswith(("-", "--")):
    #       parser.add_argument(arg.split("=")[0])

    return parser.parse_args()


def run_method(mat, parameters, **kwargs):
    """
    Run the change point detector.

    :param mat: A T x d matrix of observations.
    :param parameters: A dictionary of parameters for the change point detector.
    :return: A change point detector object.
    """
    model = METHODS[parameters["method"]](parameters, **kwargs)
    change_points = []
    for t in range(mat.shape[0]):
        model.update(mat[t, :], t + 1)
        if model.change_point_detected():
            # make sure locations are 0-based and integer!
            change_points.append(t)
    return model, change_points


def wrap_with_timeout(args, kwargs, limit):
    """
    Run a change point detector with a timeout.

    :param args: Arguments to pass to the change point detector.
    :param kwargs: Keyword arguments to pass to the change point detector.
    :param limit: Timeout in seconds.
    :return: A tuple containing the change point detector and a string indicating the status.
    """

    def wrapper(args, return_dict, **kwargs):
        """
        Wrapper function to run the change point detector in a separate process.
        """
        detector, change_points = run_method(*args, **kwargs)  # TODO
        return_dict["detector"] = detector
        return_dict["change_points"] = change_points

    manager = Manager()
    return_dict = manager.dict()

    p = Process(target=wrapper, args=(args, return_dict), kwargs=kwargs)
    p.start()
    p.join(limit)
    if p.is_alive():
        p.terminate()
        return None, "timeout"
    if "detector" in return_dict:
        return (return_dict["detector"], return_dict["change_points"]), "success"
    return None, "fail"


def main():
    args = parse_args()

    # data is the raw dataset dictionary, mat is a T x d matrix of observations
    data, mat = load_dataset(args.input)

    # set algorithm parameters that are not varied in the grid search
    defaults = {
        # TODO: add default parameters?
    }

    # combine command line arguments with defaults
    parameters = make_param_dict(args, defaults)

    # start the timer
    start_time = time.time()
    error = None
    status = 'fail'  # if not overwritten, it must have failed

    # run the algorithm in a try/except
    try:
        if args.use_timeout:
            (detector, change_points), status = wrap_with_timeout((mat, parameters), kwargs, TIMEOUT)
        else:
            detector, change_points = run_method(mat, parameters, **kwargs)  # TODO
            status = 'success'
    except Exception as err:
        error = repr(err)

    stop_time = time.time()
    runtime = stop_time - start_time

    if status == 'timeout':
        exit_with_timeout(data, args, parameters, runtime, __file__)
    # exit with error if the run failed
    if error is not None or status == 'fail':
        exit_with_error(data, args, parameters, error, __file__)

    exit_success(data, args, parameters, change_points, runtime, __file__)


if __name__ == "__main__":
    main()
