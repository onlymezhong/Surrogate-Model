"""Sampling Strategy, Experimental Design

MOEA selection strategy:
    1.Random sampling
    2.Best sampling
    3.Tournament sampling
    4.Tournament+Best sampling

Links:
    https://www.google.nl/search?sclient=psy-ab&client=safari&rls=en&q=github+sampling+python&oq=github+sampling+python&gs_l=serp.3..0i22i30k1l2.2824.3846.0.4517.7.7.0.0.0.0.91.551.7.7.0....0...1c.1.64.psy-ab..0.7.538...33i160k1.G42G3jxX1XY&pbx=1&biw=1680&bih=961&dpr=2&cad=cbv&bvch=u&sei=-e5HWNLGHsrNgAbDjruoAg#q=github+sampling+strategy+python

    https://en.wikipedia.org/wiki/Sampling_(statistics)

    https://en.wikipedia.org/wiki/Latin_hypercube_sampling

    https://docs.scipy.org/doc/numpy/reference/routines.random.html

    Factorial Designs:
        samFullFact, samFracFact, samFF2n, samPlackettBurman
    Response-Surface Designs:
        samBoxBehnken, samCentralComposite
    Randomized Designs:
        samLatinHypercube
"""

from .samBoxBehnken import samBoxBehnken
from .samCentralComposite import samCentralComposite
from .samFullFact import samFullFact, samFracFact, samFF2n
from .samLatinHypercube import samLatinHypercube
from .samOptimalLHC import samOptimalLHC
from .samPlackettBurman import samPlackettBurman
from .samRandom import samRandom, samBeta, samBinomial, samChiSquare, \
    samExponential, samF, samGamma, samGumbel, \
    samLaplace, samLogistic, samLognormal, samNormal, \
    samPareto, samPoisson, samPower, samRayleigh, \
    samTriangular, samUniform, samVonmises, samWald, \
    samWeibull, samZipf
from .samRandomLHC import samRandomLHC

__all__ = [
    'samRandomLHC', 'samOptimalLHC',
    'samFullFact', 'samFracFact', 'samFF2n', 'samPlackettBurman',
    'samBoxBehnken', 'samCentralComposite',
    'samLatinHypercube',
    'samRandom', 'samBeta', 'samBinomial', 'samChiSquare',
    'samExponential', 'samF', 'samGamma', 'samGumbel',
    'samLaplace', 'samLogistic', 'samLognormal', 'samNormal',
    'samPareto', 'samPoisson', 'samPower', 'samRayleigh',
    'samTriangular', 'samUniform', 'samVonmises', 'samWald',
    'samWeibull', 'samZipf'
]
