def solve2(
    k: typing.Callable[[numpy.ndarray, numpy.ndarray], numpy.ndarray],
    f: typing.Callable[[numpy.ndarray], numpy.ndarray] = lambda x: x,
    a: float = -1.0,
    b: float = 1.0,
    gamma: float = 1e-3,
    num: int = 40,
) -> numpy.ndarray:
    ygrid, weights = numpy.polynomial.legendre.leggauss(num)
    # change of variables to [-1,1]
    if (a != -1) or (b != 1):
        ygrid = ((b - a) / 2) * ygrid + ((a + b) / 2)
        weights = ((b - a) / 2) * weights
    # create the quadrature matrix
    ksqur = weights * k(sgrid[:, numpy.newaxis], ygrid)