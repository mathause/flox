import numpy as np

import flox

from . import parameterized

N = 1000


class ChunkReduce:
    """Time the core reduction function."""

    def setup(self, *args, **kwargs):
        raise NotImplementedError

    @parameterized(
        "func, engine", [["sum", "nansum", "mean", "nanmean", "argmax"], ["flox", "numpy", "numba"]]
    )
    def time_reduce(self, func, engine):
        flox.groupby_reduce(
            self.array,
            self.labels,
            func=func,
            engine=engine,
            axis=self.axis,
        )

    @parameterized(
        "func, engine", [["sum", "nansum", "mean", "nanmean", "argmax"], ["flox", "numpy", "numba"]]
    )
    def peakmem_reduce(self, func, engine):
        flox.groupby_reduce(
            self.array,
            self.labels,
            func=func,
            engine=engine,
            axis=self.axis,
        )


class ChunkReduce1D(ChunkReduce):
    def setup(self, *args, **kwargs):
        self.array = np.ones((N,))
        self.labels = np.repeat(np.arange(5), repeats=N // 5)
        self.axis = -1


class ChunkReduce2D(ChunkReduce):
    def setup(self, *args, **kwargs):
        self.array = np.ones((N, N))
        self.labels = np.repeat(np.arange(N // 5), repeats=5)
        self.axis = -1


class ChunkReduce2DAllAxes(ChunkReduce):
    def setup(self, *args, **kwargs):
        self.array = np.ones((N, N))
        self.labels = np.repeat(np.arange(N // 5), repeats=5)
        self.axis = None
