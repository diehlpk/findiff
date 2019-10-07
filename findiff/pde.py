from itertools import product
import numpy as np
import scipy.sparse as sparse
from scipy.sparse.linalg import spsolve


class PDE(object):

    def __init__(self, lhs, rhs, bcs):
        self.lhs = lhs
        self.rhs = rhs
        self.bcs = bcs

    def solve(self, shape):

        self._L = self.lhs.matrix(shape) # expensive operation, so cache it
        L = sparse.lil_matrix(self._L)
        f = self.rhs.reshape(-1, 1)

        nz = list(self.bcs.row_inds())
        print(nz)

        L[nz, :] = self.bcs.lhs[nz, :]
        f[nz] = np.array(self.bcs.rhs[nz].toarray()).reshape(-1, 1)

        print(L.toarray())
        print(f)

        L = sparse.csr_matrix(L)
        return spsolve(L, f)


class BoundaryConditions(object):

    def __init__(self, shape):
        self.shape = shape
        siz = np.prod(shape)
        self.long_indices = np.array(list(range(siz))).reshape(shape)
        self.lhs = sparse.lil_matrix((siz, siz))
        self.rhs = sparse.lil_matrix((siz, 1))

    def __setitem__(self, key, value):
        # Dirichlet only so far
        lng_inds = self.long_indices[key]
        self.lhs[lng_inds, lng_inds] = 1
        self.rhs[lng_inds] = value

    def row_inds(self):
        nz_rows, nz_cols = self.lhs.nonzero()
        return nz_rows
