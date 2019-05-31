from Code.functions import *

class DataBase(object):

    def __init__(self):

        self.path = []
        self.soluciones = []
        self.tsp_best = None

    def CheckSolution(self):

        if len(self.soluciones) == 0:

            self.soluciones.append(self.path[:])

        else:

            test1 = ManhattanTest(self.path[:]) < ManhattanTest(self.soluciones[-1])
            test2 = ManhattanTest(self.path[:]) == ManhattanTest(self.soluciones[-1])

            if test1 is True:
                self.soluciones = [self.path[:]]
                self.tsp_best = ManhattanTest(self.soluciones[0])
            elif test2 is True:
                self.soluciones.append(self.path[:])

    def CheckDistance(self):

        if ManhattanTest(self.path[:]) > self.tsp_best:
            return False
        return True


def SolutionGeneration(vector_list, BaseDeDatos):

    if BaseDeDatos.CheckDistance() is False:
        return []

    else:

        available = []

        for vector in vector_list:
            if vector not in BaseDeDatos.path:
                available.append(vector)

        return available

def RecurSolve(BaseDeDatos, vectors):

    available = SolutionGeneration(vectors, BaseDeDatos)

    if len(available) == 0:

        if len(BaseDeDatos.path) != len(vectors):
            return False
        else:
            BaseDeDatos.CheckSolution()

    else:

        for index in available:

            BaseDeDatos.path.append(index)
            RecurSolve(BaseDeDatos, vectors)

            BaseDeDatos.path.remove(index)

        return BaseDeDatos.soluciones

def GetVectorss(vector_list):

    original = []

    for vector in vector_list:
        if vector in original:
            pass
        else:
            original.append(vector)

    return original


def Solve(all_vectors, tsp_value):

    Datos = DataBase()
    Datos.tsp_best = tsp_value
    result = RecurSolve(Datos, GetVectorss(all_vectors))

    #for res in result:
        #print(f"Distance: {ManhattanTest(res)}")

    original = []

    for vector in result:
        if (vector in original) or (vector[::-1] in original):
            pass
        else:
            original.append(vector)

    return original


