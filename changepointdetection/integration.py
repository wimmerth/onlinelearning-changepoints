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

from cpdbench_utils import load_dataset, exit_success, exit_with_error, make_param_dict


def parse_args():
    parser = argparse.ArgumentParser(description="Wrapper for None-detector")
    parser.add_argument(
        "-i", "--input", help="path to the input data file", required=True
    )
    parser.add_argument("-o", "--output", help="path to the output file")
    return parser.parse_args()


# def main():
#     args = parse_args()
#
#     data, mat = load_dataset(args.input)
#
#     start_time = time.time()
#
#     locations = []
#
#     stop_time = time.time()
#     runtime = stop_time - start_time
#
#     exit_success(data, args, {}, locations, runtime, __file__)

def main():
    args = parse_args()

    # data is the raw dataset dictionary, mat is a T x d matrix of observations
    data, mat = load_dataset(args.input)

    # set algorithm parameters that are not varied in the grid search
    defaults = {
        'param_1': value_1,
        'param_2': value_2
    }

    # combine command line arguments with defaults
    parameters = make_param_dict(args, defaults)

    # start the timer
    start_time = time.time()
    error = None
    status = 'fail'  # if not overwritten, it must have failed

    # run the algorithm in a try/except
    try:
        locations = your_custom_method(mat, parameters)
        status = 'success'
    except Exception as err:
        error = repr(err)

    stop_time = time.time()
    runtime = stop_time - start_time

    # exit with error if the run failed
    if status == 'fail':
        exit_with_error(data, args, parameters, error, __file__)

    # make sure locations are 0-based and integer!

    exit_success(data, args, parameters, locations, runtime, __file__)


if __name__ == "__main__":
    main()