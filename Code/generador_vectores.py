from Code.functions import iterative_func_ordered_1, distance_manhattan
from Code.bruteforce import Solve
from random import randint, random
from datetime import datetime

def decision(prob):
    return random() < prob

def Generador(num_vectores, dimension, val_min, val_max, prob_0 = 0.5):
    lista_vect = []
    for i in range(num_vectores):
        vector = []
        for num in range(dimension):
            zero = decision(prob_0)
            if zero is True:
                vector.append(0)
            else:
                vector.append(randint(val_min, val_max))
        lista_vect.append(vector)
    return lista_vect

c = datetime.now()
orden, dist = iterative_func_ordered_1(Generador(10, 49, 0, 5, 0.8), distance_manhattan)
d = datetime.now()
print(dist)
print(d - c)

a = datetime.now()
result = Solve(orden[:], dist)
b = datetime.now()

print(b - a)