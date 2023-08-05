#!/usr/bin/env python

import concurrent.futures as concurrentfutures
import math
import multiprocessing
import os
import random
import sys
import threading
import time
import warnings

import numpy

from cogent3.util.misc import extend_docstring_from


multiprocessing.set_start_method(
    "fork" if sys.platform == "darwin" else "spawn", force=True
)

__author__ = "Sheng Han Moses Koh"
__copyright__ = "Copyright 2007-2021, The Cogent Project"
__credits__ = ["Peter Maxwell", "Sheng Han Moses Koh", "Gavin Huttley"]
__license__ = "BSD-3"
__version__ = "2021.5.7a"
__maintainer__ = "Gavin Huttley"
__email__ = "gavin.huttley@anu.edu.au"
__status__ = "Alpha"

if os.environ.get("DONT_USE_MPI", 0):
    MPI = None
else:
    try:
        from mpi4py import MPI
        from mpi4py import futures as MPIfutures
    except ImportError:
        MPI = None
    else:
        COMM = MPI.COMM_WORLD
        size = COMM.Get_attr(MPI.UNIVERSE_SIZE)
        if size == 1:
            MPI = None


if MPI is not None:
    USING_MPI = True
else:
    USING_MPI = False


def get_rank():
    """Returns the rank of the current process"""
    rank = 0
    if MPI is not None:
        rank = COMM.Get_rank()
    else:
        process_name = multiprocessing.current_process().name
        if process_name != "MainProcess":
            rank = int(process_name.split("-")[-1])
    return rank


def is_master_process():
    """
    Evaluates if current process is master

    In case of MPI checks whether current process
    is being run on file generated by mpi4py.futures

    In case of Multiprocessing checks if generated
    process name included "ForkProcess" for Windows
    or "SpawnProcess" for POSIX
    """
    if MPI is not None:
        process_cmd = sys.argv[0]
        process_file = process_cmd.split(os.sep)[-1]
        if process_file == "server.py":
            return False
    elif sys.version_info[1] >= 7:
        process_name = multiprocessing.current_process().name
        if "ForkProcess" in process_name or "SpawnProcess" in process_name:
            return False
    else:
        raise RuntimeError("is_master_process() requires Python 3.7 or greater")
    return True


class PicklableAndCallable:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kw):
        return self.func(*args, **kw)


def set_default_chunksize(s, max_workers):
    chunksize, remainder = divmod(len(s), max_workers * 4)
    if remainder:
        chunksize += 1
    return chunksize


def imap(f, s, max_workers=None, use_mpi=False, if_serial="raise", chunksize=None):
    """
    Parameters
    ----------
    f : callable
        function that operates on values in s
    s : iterable
        series of inputs to f
    max_workers : int or None
        maximum number of workers. Defaults to 1-maximum available.
    use_mpi : bool
        use MPI for parallel execution.
    if_serial : str
        action to take if conditions will result in serial execution. Valid
        values are 'raise', 'ignore', 'warn'. Defaults to 'raise'.
    chunksize : int or None
        Size of data chunks executed by worker processes. Defaults to None
        where stable chunksize is determined by set_default_chunksize()

    Returns
    -------
    imap is a generator yielding result of f(s[i]), map returns the result
    series

    Notes
    -----
    To use MPI, you must have openmpi (use conda or your preferred package manager)
    and mpi4py (use pip or conda) installed. In addition, your initial script must
    have a ``if __name__ == '__main__':`` block. You then invoke your program using

    $ mpiexec -n <number CPUs> python3 -m mpi4py.futures <initial script>
    """

    if_serial = if_serial.lower()
    assert if_serial in ("ignore", "raise", "warn"), f"invalid choice '{if_serial}'"

    # If max_workers is not defined, get number of all processes available
    # minus 1 to leave for master process
    if use_mpi:
        if not USING_MPI:
            raise RuntimeError("Cannot use MPI")

        err_msg = (
            "Execution in serial. For parallel MPI execution, use:\n"
            " $ mpiexec -n <number CPUs> python3 -m mpi4py.futures <executable script>"
        )

        if COMM.Get_attr(MPI.UNIVERSE_SIZE) == 1 and if_serial == "raise":
            raise RuntimeError(err_msg)
        elif COMM.Get_attr(MPI.UNIVERSE_SIZE) == 1 and if_serial == "warn":
            warnings.warn(err_msg, UserWarning)

        max_workers = max_workers or 1

        if max_workers > COMM.Get_attr(MPI.UNIVERSE_SIZE):
            warnings.warn(
                "max_workers too large, reducing to UNIVERSE_SIZE-1", UserWarning
            )

        max_workers = min(max_workers, COMM.Get_attr(MPI.UNIVERSE_SIZE) - 1)
        if not chunksize:
            chunksize = set_default_chunksize(s, max_workers)

        with MPIfutures.MPIPoolExecutor(max_workers=max_workers) as executor:
            for result in executor.map(f, s, chunksize=chunksize):
                yield result
    else:
        if not max_workers:
            max_workers = multiprocessing.cpu_count() - 1
        assert max_workers < multiprocessing.cpu_count()

        if not chunksize:
            chunksize = set_default_chunksize(s, max_workers)

        f = PicklableAndCallable(f)

        with concurrentfutures.ProcessPoolExecutor(max_workers) as executor:
            for result in executor.map(f, s, chunksize=chunksize):
                yield result


@extend_docstring_from(imap)
def map(f, s, max_workers=None, use_mpi=False, if_serial="raise", chunksize=None):
    return list(imap(f, s, max_workers, use_mpi, if_serial, chunksize))
