"""Executes an ordered crossover (OX) on the input
individuals. The two individuals are modified in place. This crossover
expects :term:`sequence` individuals of indices, the result for any other
type of individuals is unpredictable.

:param ind1: The first individual participating in the crossover.
:param ind2: The second individual participating in the crossover.
:returns: A tuple of two individuals.

Moreover, this crossover generates holes in the input
individuals. A hole is created when an attribute of an individual is
between the two crossover points of the other individual. Then it rotates
the element so that all holes are between the crossover points and fills
them with the removed elements in order. For more details see
[Goldberg1989]_.

This function uses the :func:`~random.sample` function from the python base
:mod:`random` module.

.. [Goldberg1989] Goldberg. Genetic algorithms in search,
   optimization and machine learning. Addison Wesley, 1989
"""


# Authors: Quan Pan <quanpan302@hotmail.com>

import random


def cxOrdered(var1, var2):
    size = min(len(var1), len(var2))
    # size = min(var1.size, var2.size)
    a, b = random.sample(xrange(size), 2)
    if a > b:
        a, b = b, a

    holes1, holes2 = [True] * size, [True] * size
    for i in range(size):
        if i < a or i > b:
            holes1[var2[i]] = False
            holes2[var1[i]] = False

    # We must keep the original values somewhere before scrambling everything
    temp1, temp2 = var1, var2
    k1, k2 = b + 1, b + 1
    for i in range(size):
        if not holes1[temp1[(i + b + 1) % size]]:
            var1[k1 % size] = temp1[(i + b + 1) % size]
            k1 += 1

        if not holes2[temp2[(i + b + 1) % size]]:
            var2[k2 % size] = temp2[(i + b + 1) % size]
            k2 += 1

    # Swap the content between a and b (included)
    for i in range(a, b + 1):
        var1[i], var2[i] = var2[i], var1[i]
        # var1[i], var2[i] = var2[i].copy(), var1[i].copy()

    return var1, var2
