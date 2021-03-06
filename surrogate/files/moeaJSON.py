import json

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import cm


class JSON(object):
    def __init__(self, fileName, numVar, numPop, numCon, numObj, numGen):
        self.fileName = fileName
        self.numPop = numPop
        self.numVar = numVar
        self.numCon = numCon
        self.numObj = numObj
        self.numGen = numGen

    def writeHeader(self):
        outFile = open(self.fileName, "wt")
        outFile.write("{\n")
        outFile.write("\"generation\": [\n")
        outFile.close()

    def writeEnd(self):
        outFile = open(self.fileName, "a")
        outFile.write("]\n}\n")
        outFile.close()

    def writePareto(self, individuals, igen):
        outFile = open(self.fileName, "a")
        outFile.write("    {\n")

        outFile.write("        \"variable\"   : [")
        outFile.write("[%f" % (individuals[0].variable[0]))
        for j in range(1, self.numVar):
            outFile.write(",%f" % (individuals[0].variable[j]))
        outFile.write("]")

        for i in range(1, self.numPop):
            outFile.write(",[%f" % (individuals[i].variable[0]))
            for j in range(1, self.numVar):
                outFile.write(",%f" % (individuals[i].variable[j]))
            outFile.write("]")
        outFile.write("],\n")

        outFile.write("        \"objective\"  : [[")
        outFile.write("[%f" % (individuals[0].fitness.values[0]))
        for j in range(1, self.numObj):
            outFile.write(",%f" % (individuals[0].fitness.values[j]))
        outFile.write("]")
        for i in range(1, self.numPop):
            outFile.write(",[%f" % (individuals[i].fitness.values[0]))
            for j in range(1, self.numObj):
                outFile.write(",%f" % (individuals[i].fitness.values[j]))
            outFile.write("]")
        outFile.write("]]")

        if self.numCon > 0:
            outFile.write(",")
        outFile.write("\n")

        if self.numCon > 0:
            outFile.write("        \"constraint\" : [")
            outFile.write("[%f" % (individuals[0].constraint[0]))
            for j in range(1, self.numCon):
                outFile.write(",%f" % (individuals[0].constraint[j]))
            outFile.write("]")
            for i in range(1, self.numPop):
                outFile.write(",[%f" % (individuals[i].constraint[0]))
                for j in range(1, self.numCon):
                    outFile.write(",%f" % (individuals[i].constraint[j]))
                outFile.write("]")
            outFile.write("]")
            outFile.write("\n")
        outFile.write("    }")
        if igen < self.numGen - 1:
            outFile.write(",")
        outFile.write("\n")

        outFile.close()

    def plot_json(self):
        with open(self.fileName) as data_file:
            data = json.load(data_file)

        gen = data["generation"]
        gen_tot = len(gen)

        color = iter(cm.gray(np.linspace(1, 0.1, gen_tot)))
        # color = iter(cm.rainbow(np.linspace(0,1,gen_tot)))
        for index, item in enumerate(gen):
            obj = item["objective"][0]
            obj_tot = len(obj)
            x = []
            y = []
            r = index / gen_tot
            g = index / gen_tot
            b = index / gen_tot
            for iobj in obj:
                x.append(iobj[0])
                y.append(iobj[1])
            plt.plot(x, y, '.', color=next(color), label=str(index))

        plt.title('moea.json')
        plt.xlabel('obj1')
        # plt.xlim([0.7,1.1])
        plt.ylabel('obj2')
        # plt.ylim([6,9])
        plt.grid(True)
        # plt.legend(loc='best')
        plt.show()
