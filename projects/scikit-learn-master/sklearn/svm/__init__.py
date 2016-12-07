"""
The :mod:`sklearn.svm` module includes Support Vector Machine algorithms.
"""

# See http://scikit-learn.sourceforge.net/modules/svm.html for complete
# documentation.

# Author: Fabian Pedregosa <fabian.pedregosa@inria.fr> with help from
#         the scikit-learn community. LibSVM and LibLinear are copyright
#         of their respective owners.
# License: BSD 3 clause (C) INRIA 2010

from . import libsvm, liblinear, libsvm_sparse
from .bounds import l1_min_c
from .classes import SVC, NuSVC, SVR, NuSVR, OneClassSVM, LinearSVC, \
    LinearSVR

__all__ = ['LinearSVC',
           'LinearSVR',
           'NuSVC',
           'NuSVR',
           'OneClassSVM',
           'SVC',
           'SVR',
           'l1_min_c',
           'liblinear',
           'libsvm',
           'libsvm_sparse']