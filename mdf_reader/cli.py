"""Console script for mdf_reader."""
import argparse
import sys

from dask.distributed import Client

import mdf_reader


def _parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "source",
        nargs="?",
        help="File path to read.",
    )
    parser.add_argument(
        "-dm",
        "--data_model",
        dest="data_model",
        nargs="?",
        help="Name of internally available data_model.",
    )
    parser.add_argument(
        "-dmp",
        "--data_model_path",
        dest="data_model_path",
        nargs="?",
        help="Path to externally available data_model.",
    )
    parser.add_argument(
        "-s",
        "--sections",
        dest="sections",
        nargs="+",
        help="List with subsets of data model sections.",
    )
    parser.add_argument(
        "-cs",
        "--chunksize",
        dest="chunksize",
        type=int,
        help="Numer of reports per chunk.",
    )
    parser.add_argument(
        "-sp",
        "--skiprows",
        dest="skiprows",
        type=int,
        default=0,
        help="Number of initial rows to skip from file.",
    )
    parser.add_argument(
        "-op",
        "--out_path",
        dest="out_path",
        nargs="?",
        help="Path to output data, valid mask and attributes.",
    )
    return parser


def _args_to_mdf_reader(args):
    return mdf_reader.read(**vars(args))


def main():
    parser = _parser()
    args = parser.parse_args()

    _args_to_mdf_reader(args)
    return 0


if __name__ == "__main__":
    with Client() as client:
        sys.exit(main())
