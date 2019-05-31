import os
import Code.functions as func
import Code.bruteforce as bf
from datetime import datetime
import numpy as np

#######################  DEFINITIONS  #######################################

class Instance(object):

    def __init__(self, case_id, ocurrence):

        self.case_id = case_id
        self.activities = []
        self.ocurrence = ocurrence
        self.vector = None

    def set_vector(self, coef):
        self.vector = func.vector_calculation(self, coef)

    def add_activity(self, other):
        self.activities.append(other)

class Activity:

    def __init__(self, name, stage):

        self.name = name
        self.stage = stage

#######################  Vector and case INIT  #######################################

all_cases = []
used_ids = []
int_to_id = dict()

os.chdir(os.path.join("..", "Data"))

with open('log.csv', 'r') as data:
    data = func.filter_acts(data, func.los_jinetes)

    for line in data:
        line = line.split(",")

        if line[0] in used_ids:
            all_cases[-1].add_activity(Activity(line[2], line[3]))
        else:
            used_ids.append(line[0])
            all_cases.append(Instance(line[0], line[1]))

with open("coeficients.csv", "r") as coeficientes:

    coeficients = [int(line.strip()[-1]) for line in coeficientes]

all_vectors = []

for instance in all_cases:
    instance.set_vector(coeficients)
    all_vectors.append(instance.vector)

for index in range(20):
    int_to_id[index] = all_cases[index].case_id

############################# Instancing and Analysis ###########################

os.chdir('Exported Results')

vectors_test = []

original = []

for vector in all_vectors:
    if vector not in original:
        original.append(vector)

times_bf = []
times_tsp = []

for i in range(10):

    tsp_1 = datetime.now()
    order, best = func.iterative_func_ordered_1(original, func.distance_manhattan)
    tsp_2 = datetime.now()

    bf1 = datetime.now()
    res = bf.Solve(original[:], best)[0]
    bf2 = datetime.now()

    times_tsp.append(tsp_2 - tsp_1)
    times_bf.append(bf2 - bf1)

with open('tiempos_exec.txt', 'w') as file:

    for char in times_tsp:
        file.write(f'{char}\n')

    times_tsp = [x.total_seconds() for x in times_tsp]

    file.write(f"{np.var(times_tsp)} \n")

    file.write('\n')

    for char in times_bf:
        file.write(f'{char}\n')

    times_bf = [x.total_seconds() for x in times_bf]

    file.write(f"{np.var(times_bf)} \n")

