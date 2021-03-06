"""Flip the value of the attributes of the input individual and return the
mutant. The *individual* is expected to be a :term:`sequence` and the values of the
attributes shall stay valid after the ``not`` operator is called on them.
The *prob* argument is the probability of each attribute to be
flipped. This mutation is usually applied on boolean individuals.

:param individual: Individual to be mutated.
:param prob: Independent probability for each attribute to be flipped.
:returns: A tuple of one individual.

This function uses the :func:`~random.random` function from the python base
:mod:`random` module.
"""


# Authors: Quan Pan <quanpan302@hotmail.com>

import random


def mutFlipBit(variable, prob=0.5):
    for i in xrange(len(variable)):
        # for i in xrange(variable.size):
        if random.random() < prob:
            variable[i] = type(variable[i])(not variable[i])

    return variable
