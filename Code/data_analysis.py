import os
from Code.functions import *

all_cases = []
used_ids = []

class Instance(object):

    def __init__(self, case_id, ocurrence):

        self.case_id = case_id
        self.activities = []
        self.ocurrence = ocurrence
        self.vector = None

    def set_vector(self, coef):
        self.vector = vector_calculation(self, coef)

    def add_activity(self, other):
        self.activities.append(other)

class Activity:

    def __init__(self, name, stage):

        self.name = name
        self.stage = stage

os.chdir(os.path.join("..", "Data"))

with open('log.csv', 'r') as data:
    data = filter_acts(data, los_jinetes)

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

for i in all_cases:
    i.set_vector(coeficients)
    all_vectors.append(i.vector)


hola1 = basic_travel_sorting(all_vectors, distance_manhattan)

hola2 = basic_travel_sorting(all_vectors, distance_euclidean)

hola3 = basic_travel_sorting(all_vectors, distance_levenshtein)

if hola1 == hola2:
    print("1 es igual a 2")

if hola1 == hola3:

    print("1 es igual a 3")

if hola2 == hola3:

    print("2 es igual a 3")

