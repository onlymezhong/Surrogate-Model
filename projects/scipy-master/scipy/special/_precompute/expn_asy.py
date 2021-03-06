"""Precompute the polynomials for the asymptotic expansion of the
generalized exponential integral.

Sources
-------
[1] NIST, Digital Library of Mathematical Functions,
    http://dlmf.nist.gov/8.20#ii

"""
from __future__ import division, print_function, absolute_import

import os
import warnings

try:
    # Can remove when sympy #11255 is resolved; see
    # https://github.com/sympy/sympy/issues/11255
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        import sympy
        from sympy import Poly

        x = sympy.symbols('x')
except ImportError:
    pass


def generate_A(K):
    A = [Poly(1, x)]
    for k in range(K):
        A.append(Poly(1 - 2 * k * x, x) * A[k] + Poly(x * (x + 1)) * A[k].diff())
    return A


WARNING = """\
/* This file was automatically generated by {}.
 * Do not edit it manually!
 */
""".format(os.path.relpath(__file__, '..'))


def main():
    print(__doc__)
    fn = os.path.join('..', 'cephes', 'expn.h')

    K = 12
    A = generate_A(K)
    with open(fn + '.new', 'w') as f:
        f.write(WARNING)
        f.write("#define nA {}\n".format(len(A)))
        for k, Ak in enumerate(A):
            tmp = ', '.join([str(x.evalf(18)) for x in Ak.coeffs()])
            f.write("double A{}[] = {{{}}};\n".format(k, tmp))
        tmp = ", ".join(["A{}".format(k) for k in range(K + 1)])
        f.write("double *A[] = {{{}}};\n".format(tmp))
        tmp = ", ".join([str(Ak.degree()) for Ak in A])
        f.write("int Adegs[] = {{{}}};\n".format(tmp))
    os.rename(fn + '.new', fn)


if __name__ == "__main__":
    main()
