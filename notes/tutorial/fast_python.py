import random


class Matrix(list):
    @classmethod
    def zeros(cls, shape):
        n_rows, n_cols = shape
        return cls([[0] * n_cols for i in range(n_rows)])

    @classmethod
    def random(cls, shape):
        M, (n_rows, n_cols) = cls(), shape
        for i in range(n_rows):
            M.append([random.randint(-255, 255) for j in range(n_cols)])
        return M

    @property
    def shape(self):
        return (0, 0) if not self else (len(self), len(self[0]))


def matrix_product(X, Y):
    """Computes the matrix product of X and Y.

    >>> X = Matrix([[1], [2], [3]])
    >>> Y = Matrix([[4, 5, 6])
    [[4, 5, 6], [8, 10, 12], [12, 15, 18]]
    >> matrix_product(Y, X)
    [[32]]
    """
    n_xrows, n_xcols = X.shape
    n_yrows, n_ycols = Y.shape
    # TODO: check the shapes
    Z = Matrix.zeros((n_xrows, n_ycols))
    for i in range(n_xrows):
        for j in range(n_xcols):
            for k in range(n_ycols):
                Z[i][k] += X[i][j] * Y[j][k]
    return Z


def bench(shape=(64, 64), n_iter=16, version=2):
    X = Matrix.random(shape)
    Y = Matrix.random(shape)
    for _iter in range(n_iter):
        matrix_product(X, Y)


if __name__ == "__main__":
    bench()
