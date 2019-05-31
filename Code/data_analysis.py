import os
import Code.functions as func
import Code.bruteforce as bf
from datetime import datetime

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


vectors_test = []

original = []

for vector in all_vectors:
    if vector not in original:
        original.append(vector)


order, best = func.iterative_func_ordered_1(original, func.distance_manhattan)
res = bf.Solve(original[:], best)[0]

with open("id_list.txt", "w") as file:

    file.write("Greedy:\n")
    file.write("\n")
    for case in func.ListIDs(order, all_cases)[::-1]:
        file.write(f"{case}\n")

    file.write("\n")
    file.write("Branch and Bound:\n")
    file.write("\n")
    for case in func.ListIDs(res, all_cases):
        file.write(f"{case}\n")
