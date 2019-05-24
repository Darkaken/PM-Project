import os
import Code.functions as func
import Code.bruteforce as bf

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
            all_cases[-1].add_activity(Activity(line[2], line[3]))

with open("coeficients.csv", "r") as coeficientes:

    coeficients = [int(line.strip()[-1]) for line in coeficientes]

all_vectors = []

for instance in all_cases:
    instance.set_vector(coeficients)
    all_vectors.append(instance.vector)

############################# Instancing and Analysis ###########################

def GetVectors(vector_list):

    original = []

    for vector in vector_list:
        if vector in original:
            pass
        else:
            original.append(vector)

    return original


new_vects = GetVectors(all_vectors[:])
order, result = func.iterative_func_ordered_1(new_vects, func.distance_manhattan)
print(result)

'''
results = bf.Solve(new_vects[:])

os.chdir(os.path.join("..", "Data/Exported Results"))
with open("mejorOrdenamiento.txt", "w") as file:

    file.write("MEJORES SOLUCIONES ENCONTRADAS:")
    file.write("\n")
    file.write("\n")

    for result in results:

        file.write(f"Distancia: {func.ManhattanTest(result)}")
        file.write("\n")

        for line in result:
            file.write(str(line))
            file.write("\n")

        file.write("\n")
        file.write("\n")

    file.write('Orden de IDs: \n')
    for line in func.ListIDs(results[0], all_cases):
        file.write(f'{line} \n')


'''

os.chdir(os.path.join('..', 'Cases'))

for index in range(len(all_cases)):

    with open(f'Case {index + 1}.csv', 'w') as case:

        case.write(f'CASE ID: {all_cases[index].case_id}')

        case.write('\n')
        for element in [f'{x} \n' for x in [act.name for act in all_cases[index].activities]]:
            case.write(element)
