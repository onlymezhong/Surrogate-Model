""" Adaptive Neural Network Genetic Algorithm (ANGA)
Components:
    Genetic Algorithm
    Artificial Neural Networks
    Caching
Implementation:
    Fitness Sampling
        Sampling Rate: Sampling rate determines how many individuals should be sampled from a population in each generation
        Sampling Selection Strategy: Sampling selection strategy determines which individuals should be sampled from a population, given the current sampling rate.
            random sampling, best sampling, tournament sampling, combined tournament+best sampling
    ANN Training and Retraining
        InitialTrainingGenerations: Alloftheindividualsin the first several generations of ANGA must be evaluated by the simulation models to generate the ANN training set.
        Retraining Set Management: As more and more sampled solutions are generated from simulation model evaluations, the retraining set must be managed.
            growing set approach, fixed set approach
        Retraining Method: When the ANNs need to be retrained, the training algorithm can either load the previ- ously trained weights and continue the training episodes on the new training set, or it can re-initialize the ANN weights to random values and completely retrain the ANNs.
        Retraining Frequency: Retraining frequency deter- mines when the ANNs should be updated during an ANGA run. Retraining frequency should decrease in later gener- ations as the search progresses into relatively smoother local regions.
"""

# from surrogate.base import SurrogateModel
# class ANGA(object):
# class ANGA(SurrogateModel):
#     def __init__(self, x, y):
#         super(ANGA, self).__init__()
#
#         self.x = x
#         self.y = y
#
#     def predict_proba(self, x):
#         super(ANGA, self).predict_proba(x)
#         pass
#
#
# if __name__ == "__main__":
#     from sklearn import datasets
#
#     iris = datasets.load_iris()
#     X, y = iris.data, iris.target
#
#     # def branin(x):
#     #     y = (x[1] - (5.1 / (4. * pi ** 2.)) * x[0] ** 2. + 5. * x[0] / pi - 6.) ** 2. + 10. * (
#     #     1. - 1. / (8. * pi)) * cos(
#     #         x[0]) + 10.
#     #     return y
#     # def branin_1d(x):
#     #     return branin(array([x[0], 2.275]))
#     # X = array([[0.0], [2.0], [3.0], [4.0], [6.0]])
#     # y = array([[branin_1d(case)] for case in X])
#
#     anga = ANGA(X, y)
#     anga.fit(X, y)
#     anga.predict_proba(X)


import warnings
warnings.filterwarnings(action="ignore", category=Warning)
# warnings.filterwarnings(action="ignore", category=FutureWarning)
# warnings.filterwarnings(action="ignore", category=ImportWarning)
# warnings.filterwarnings(action="ignore", category=DeprecationWarning)

import numpy as np
from copy import deepcopy

from surrogate import benchmarks

from surrogate.base import Individual
from surrogate.selection import selNSGA2, selTournamentDCD
from surrogate.crossover import cxSimulatedBinaryBounded
from surrogate.mutation import mutPolynomialBounded
from surrogate.sampling import samBeta, samUniform
from surrogate.estimator import ANNSurrogate
from surrogate.files import JSON

# Xold_ind = [[0., 0., 0., 0.], [1., 1., 1., 1.], [10., 10., 10., 10.]]
# # Yold_obj = [0.0, 1.0, 10.0]
# Yold_obj = [[0., 0.], [1., 1.], [10., 10.]]
# Xnew_ind = [[5., 5., 5., 5.], [-10., -2., -10., -2.]]


import random

random.seed(0.5)


def Population(numPop=4, numVar=10, estimator=benchmarks.zdt6, weights=(-1.0, -1.0)):
    Individuals = []
    variables = [
        [0.08966, 0.85338, 0.98579, 0.15400, 0.21201, 0.39000, 0.24615, 0.52297, 0.02758, 0.55775],
        [0.50637, 0.21866, 0.05956, 0.14900, 0.27852, 0.14137, 0.42839, 0.75617, 0.14790, 0.08260],
        [0.27840, 0.21768, 0.17810, 0.35452, 0.85922, 0.00088, 0.08544, 0.03811, 0.35325, 0.25055],
        [0.41416, 0.85318, 0.01416, 0.66403, 0.01492, 0.65336, 0.80880, 0.05268, 0.52587, 0.93375],
        [0.23447, 0.99610, 0.36593, 0.38134, 0.42196, 0.83398, 0.12267, 0.95272, 0.86049, 0.46400],
        [0.56176, 0.65177, 0.81456, 0.22058, 0.10519, 0.78797, 0.31508, 0.94056, 0.21079, 0.49574],
        [0.67224, 0.32400, 0.06878, 0.30880, 0.18294, 0.66287, 0.09993, 0.41787, 0.23267, 0.62995],
        [0.79480, 0.49413, 0.19621, 0.85527, 0.51985, 0.28863, 0.28846, 0.81689, 0.81627, 0.05864],
        [0.89941, 0.35737, 0.93038, 0.77133, 0.94898, 0.12099, 0.22275, 0.99442, 0.03623, 0.20604],
        [0.02257, 0.88028, 0.04750, 0.94849, 0.80619, 0.12603, 0.36930, 0.09194, 0.56919, 0.75869],
        [0.16264, 0.65064, 0.09147, 0.80063, 0.07220, 0.20550, 0.44796, 0.71409, 0.82605, 0.81780],
        [0.18315, 0.97412, 0.37952, 0.38988, 0.57634, 0.94170, 0.01935, 0.48783, 0.62966, 0.71127]
    ]

    for i in range(numPop):
        # variable = variables[i]
        # variable = samRandom(n=numVar)
        # variable = samBeta(a=0.1, b=0.1, size=numVar)
        variable = samUniform(low=0.0, high=1.0, size=numVar).tolist()
        constraint = []
        Individuals.append(Individual(estimator=estimator, variable=variable, constraint=constraint, weights=weights))
    return Individuals


# def moeaLoop(surrogate, population):
def moeaLoop():
    _INF = 1e-14
    _Ndim = 10
    _Ngen = 100
    _Npop = 4 * 10
    _Nobj = 2
    _Ncon = 0
    _Rate = 1.0
    fileName = './files/moea.json'
    CXPB = 0.9
    # estimator = benchmarks.zdt1
    # estimator = benchmarks.zdt2
    estimator = benchmarks.zdt3
    # estimator = benchmarks.zdt4
    # estimator = benchmarks.zdt6
    weights = (-1.0, -1.0)
    # weights = (1.0, 1.0)

    ioResultFile = JSON(fileName=fileName, numVar=_Ndim, numPop=_Npop, numCon=_Ncon, numObj=_Nobj, numGen=_Ngen)
    ioResultFile.writeHeader()

    Xold_ind = np.zeros([_Npop, _Ndim])
    Yold_obj = np.zeros([_Npop, _Nobj])
    Xnew_ind = samBeta(a=0.1, b=0.1, size=_Ndim)

    surrogate = ANNSurrogate(algorithm='l-bfgs', alpha=1e-5, hidden_layer_sizes=(100,), random_state=1)
    population = Population(numPop=_Npop, numVar=_Ndim, estimator=estimator, weights=weights)

    print 'ANNSurrogate'
    for ipop in range(_Npop):
        Xold_ind[ipop] = [deepcopy(X) for X in population[ipop].variable]
        Yold_obj[ipop] = [deepcopy(Y) for Y in population[ipop].fitness.values]
        print '\t' + str(ipop) \
              + '\tXold_ind: [' + '\t'.join(map("{:.5f}".format, Xold_ind[ipop])) + ']' \
              + '\tMean_X: ' + str(np.mean(Xold_ind[ipop])) \
              + '\tStd_X: ' + str(np.std(Xold_ind[ipop])) \
              + '\tYold_obj: [' + '\t'.join(map("{:.5f}".format, Yold_obj[ipop])) + ']'
    surrogate.fit(Xold_ind, Yold_obj)
    Ynew_obj = surrogate.predict(Xnew_ind)
    print 'End\t\tXnew_ind: [' + '\t'.join(map("{:.5f}".format, Xnew_ind)) + ']' \
          + '\tMean_X: ' + str(np.mean(Xnew_ind)) \
          + '\tStd_X: ' + str(np.std(Xnew_ind)) \
          + '\tYnew_obj: [' + '\t'.join(map("{:.5f}".format, Ynew_obj[0])) + ']\n'

    igen = 0
    population = selNSGA2(population, _Npop)
    ioResultFile.writePareto(individuals=population, igen=igen)
    # print str(igen) + '\tGen:'
    # for ipop in population:
    #     print '\tpopulation.sel.a'\
    #           + '\tvar1: [' + ', '.join(map("{:.5f}".format, ipop.variable)) + ']'
    # print

    for igen in range(1, _Ngen):
        print 'Gen\t:' + str(igen)

        # print '\n' + str(igen) + '\tGen:'
        # for ipop in population:
        #     print '\tpopulation.sel.b'\
        #           + '\tvar: [' + ', '.join(map("{:.5f}".format, ipop.variable)) + ']'\
        #           + '\tobj: [' + ', '.join(map("{:.5f}".format, ipop.fitness.values)) + ']'\
        #           + '\tcrw: [' + str(ipop.fitness.crowding_dist) + ']'

        offspring = selTournamentDCD(population, _Npop)
        # for ipop in offspring:
        #     print '\toffspring.sel.a'\
        #           + '\tvar: [' + ', '.join(map("{:.5f}".format, ipop.variable)) + ']'\
        #           + '\tobj: [' + ', '.join(map("{:.5f}".format, ipop.fitness.values)) + ']'\
        #           + '\tcrw: [' + str(ipop.fitness.crowding_dist) + ']'
        # print

        offspring = [deepcopy(ind) for ind in offspring]
        # TODO 20161212 pass memeory address instead of values
        # for ipop in offspring:
        #     print '\toffspring.sel.a'\
        #           + '\tvar: [' + ', '.join(map("{:.5f}".format, ipop.variable)) + ']'\
        #           + '\tobj: [' + ', '.join(map("{:.5f}".format, ipop.fitness.values)) + ']'\
        #           + '\tcrw: [' + str(ipop.fitness.crowding_dist) + ']'
        # print

        for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
            if random.random() <= CXPB:
                # print '\toffspring.cx.b'\
                #       + '\tvar1: [' + ', '.join(map("{:.5f}".format, ind1.variable)) + ']'\
                #       + '\tvar2: [' + ', '.join(map("{:.5f}".format, ind2.variable)) + ']'
                ind1.variable, ind2.variable = cxSimulatedBinaryBounded(ind1.variable, ind2.variable)
                # print '\toffspring.cx.a'\
                #       + '\tvar1: [' + ', '.join(map("{:.5f}".format, ind1.variable)) + ']'\
                #       + '\tvar2: [' + ', '.join(map("{:.5f}".format, ind2.variable)) + ']'

            # print '\toffspring.mut.b'\
            #       + '\tvar1: [' + ', '.join(map("{:.5f}".format, ind1.variable)) + ']'\
            #       + '\tvar2: [' + ', '.join(map("{:.5f}".format, ind2.variable)) + ']'
            ind1.variable = mutPolynomialBounded(ind1.variable)
            ind2.variable = mutPolynomialBounded(ind2.variable)
            # print '\toffspring.mut.a'\
            #       + '\tvar1: [' + ', '.join(map("{:.5f}".format, ind1.variable)) + ']'\
            #       + '\tvar2: [' + ', '.join(map("{:.5f}".format, ind2.variable)) + ']'
            # print

            del ind1.fitness.values, ind2.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        ipop = 0
        for ind in invalid_ind:
            # ind.fitness.values = estimator(ind.variable)

            Xold_ind[ipop] = [deepcopy(X) for X in ind.variable]
            Yold_obj[ipop] = [deepcopy(Y) for Y in estimator(ind.variable)]
            surrogate.fit(Xold_ind, Yold_obj)

            Xnew_ind = [ind.variable]
            Ynew_obj = surrogate.predict(Xnew_ind)
            # print '\tXnew_ind: [' + '\t'.join(map("{:.5f}".format, Xnew_ind)) + ']' \
            #       + '\tMean_X: ' + str(np.mean(Xnew_ind)) \
            #       + '\tStd_X: ' + str(np.std(Xnew_ind)) \
            #       + '\tYnew_obj: [' + '\t'.join(map("{:.5f}".format, Ynew_obj[0])) + ']'
            # Xnew_ind = np.array(ind.variable)
            # Ynew_obj = surrogate.predict(Xnew_ind)
            # print '\tXnew_ind: [' + '\t'.join(map("{:.5f}".format, Xnew_ind[0])) + ']' \
            #       + '\tMean_X: ' + str(np.mean(Xnew_ind)) \
            #       + '\tStd_X: ' + str(np.std(Xnew_ind)) \
            #       + '\tYnew_obj: [' + '\t'.join(map("{:.5f}".format, Ynew_obj[0])) + ']'
            ind.fitness.values = Ynew_obj[0]

            ipop += 1


        # print 'Select the next generation population\nAfter cx mut'
        # for ipop in population:
        #     print '\tpopulation.sel.b'\
        #           + '\tvar: [' + ', '.join(map("{:.5f}".format, ipop.variable)) + ']'\
        #           + '\tobj: [' + ', '.join(map("{:.5f}".format, ipop.fitness.values)) + ']'\
        #           + '\tcrw: [' + str(ipop.fitness.crowding_dist) + ']'
        # for ipop in offspring:
        #     print '\toffspring.sel.b'\
        #           + '\tvar: [' + ', '.join(map("{:.5f}".format, ipop.variable)) + ']'\
        #           + '\tobj: [' + ', '.join(map("{:.5f}".format, ipop.fitness.values)) + ']'\
        #           + '\tcrw: [' + str(ipop.fitness.crowding_dist) + ']'
        # print
        population = selNSGA2(population + offspring, _Npop)
        ioResultFile.writePareto(individuals=population, igen=igen)
        # for ipop in range(_Npop):
        #     print '\tpopulation.sel.a' \
        #           + '\tXold_ind: [' + ', '.join(map("{:.5f}".format, population[ipop].variable)) + ']'\
        #           + '\tYold_obj: [' + ', '.join(map("{:.5f}".format, population[ipop].fitness.values)) + ']'\
        #           + '\tcrw: [' + str(population[ipop].fitness.crowding_dist) + ']'

        # for ipop in range(_Npop):
        #     population[ipop].objective = population[ipop].estimator(population[ipop].variable)
        #
        #     Xold_ind.append(population[ipop].variable)
        #     Yold_obj.append(population[ipop].objective)
        #
        #     print '\t' + str(ipop) \
        #           + '\tXold_ind: [' + ', '.join(map("{:.5f}".format, population[ipop].variable)) + ']'\
        #           + '\tMean_X: ' + str(np.mean(population[ipop].variable))\
        #           + '\tStd_X: ' + str(np.std(population[ipop].variable))\
        #           + '\tYold_obj: [' + ', '.join(map("{:.5f}".format, population[ipop].objective)) + ']'
        #
        # surrogate.fit(Xold_ind, Yold_obj)
        # Ynew_obj = surrogate.predict(Xnew_ind)
        # print 'ANNSurrogate.Xnew_ind:\n\t[' + '\t'.join(map(str, Xnew_ind)) + ']'
        # print 'ANNSurrogate.Ynew_obj:\n\t[' + '\t'.join(map(str, Ynew_obj)) + ']'

    ioResultFile.writeEnd()

    ioResultFile.plot_json()




if __name__ == "__main__":
    moeaLoop()

    """
    Test Block
    """
    # surrogate = ANNSurrogate(algorithm='l-bfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
    # surrogate.fit(Xold_ind, Yold_obj)
    # y_pred = surrogate.predict(Xnew_ind)
    # # print surrogate.regressor
    # print 'ANNSurrogate.y_pred: ['+', '.join(map(str,y_pred))+']'


    # from sklearn.neural_network import MLPRegressor
    # regressor = MLPRegressor(algorithm='l-bfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
    # regressor.fit(Xold_ind, Yold_obj)
    # y_pred = regressor.predict(Xnew_ind)
    # # print regressor
    # print 'MLPRegressor.y_pred: ['+', '.join(map(str,y_pred))+']'

    """

    """
