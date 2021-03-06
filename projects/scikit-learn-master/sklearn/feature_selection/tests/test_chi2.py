"""
Tests for chi2, currently the only feature selection function designed
specifically to work with sparse matrices.
"""

import numpy as np
import scipy.stats
from nose.tools import assert_raises
from numpy.testing import assert_equal, assert_array_almost_equal
from scipy.sparse import coo_matrix, csr_matrix
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.feature_selection.univariate_selection import _chisquare

# Feature 0 is highly informative for class 1;
# feature 1 is the same everywhere;
# feature 2 is a bit informative for class 2.
X = [[2, 1, 2],
     [9, 1, 1],
     [6, 1, 2],
     [0, 1, 2]]
y = [0, 1, 2, 2]


def mkchi2(k):
    """Make k-best chi2 selector"""
    return SelectKBest(chi2, k=k)


def test_chi2():
    # Test Chi2 feature extraction

    chi2 = mkchi2(k=1).fit(X, y)
    chi2 = mkchi2(k=1).fit(X, y)
    assert_equal(chi2.get_support(indices=True), [0])
    assert_equal(chi2.transform(X), np.array(X)[:, [0]])

    chi2 = mkchi2(k=2).fit(X, y)
    assert_equal(sorted(chi2.get_support(indices=True)), [0, 2])

    Xsp = csr_matrix(X, dtype=np.float64)
    chi2 = mkchi2(k=2).fit(Xsp, y)
    assert_equal(sorted(chi2.get_support(indices=True)), [0, 2])
    Xtrans = chi2.transform(Xsp)
    assert_equal(Xtrans.shape, [Xsp.shape[0], 2])

    # == doesn't work on scipy.sparse matrices
    Xtrans = Xtrans.toarray()
    Xtrans2 = mkchi2(k=2).fit_transform(Xsp, y).toarray()
    assert_equal(Xtrans, Xtrans2)


def test_chi2_coo():
    # Check that chi2 works with a COO matrix
    # (as returned by CountVectorizer, DictVectorizer)
    Xcoo = coo_matrix(X)
    mkchi2(k=2).fit_transform(Xcoo, y)
    # if we got here without an exception, we're safe


def test_chi2_negative():
    # Check for proper error on negative numbers in the input X.
    X, y = [[0, 1], [-1e-20, 1]], [0, 1]
    for X in (X, np.array(X), csr_matrix(X)):
        assert_raises(ValueError, chi2, X, y)


def test_chisquare():
    # Test replacement for scipy.stats.chisquare against the original.
    obs = np.array([[2., 2.],
                    [1., 1.]])
    exp = np.array([[1.5, 1.5],
                    [1.5, 1.5]])
    # call SciPy first because our version overwrites obs
    chi_scp, p_scp = scipy.stats.chisquare(obs, exp)
    chi_our, p_our = _chisquare(obs, exp)

    assert_array_almost_equal(chi_scp, chi_our)
    assert_array_almost_equal(p_scp, p_our)
