import os
from statistics import mean

############################## Important Activity Definition #################################

los_jinetes = ["Puncture", "Guidewire install", "Remove trocar", "Advance catheter", "Remove guidewire"]
los_jinetes += ["Widen pathway", "Remove syringe"]

#################################### ID Identification ######################################

def GetID(vector, cases):

    result = []
    for obj in cases:
        if obj.vector == vector:
            result.append(obj.case_id)
    return result

def ListIDs(vector_list, cases):

    return [GetID(x, cases) for x in vector_list]

################### Log Filtering, Pair Definition and Vector Calculation ####################

def filter_acts(log, important):

    data = []

    for line in log:
        important_data = []
        line = line.split(",")

        if line[4] in important:
            important_data.append(line[0])
            important_data += [line[2], line[4], line[5]]

            data.append(",".join(important_data))

    return data

def pair_definition(important):

    pairs = []

    for act in important:
        for other in important:
            pairs.append((act, other))

    return pairs

def vector_calculation(case, coef):   #Direct Succesion

    pairs = pair_definition(los_jinetes)
    vector = [0 for x in range(len(pairs))]
    actions = [act.name for act in case.activities[:]]

    for index in range(len(pairs)):
        for ind in range(len(actions)):

            try:
                one = actions[ind]
                two = actions[ind + 1]

                if (one, two) == pairs[index]:
                    vector[index] += 1

            except IndexError:
                pass

    for index in range(len(pairs)):
        vector[index] *= coef[index]

    return vector

############################## Distance Function Definition #################################

def ManhattanTest(vector_list):

    """

    Given a vector list, returns the sum of the manhattan distances between vectors in a secuence.

    """

    distance = 0

    for index in range(len(vector_list)):

        try:
            distance += distance_manhattan(vector_list[index], vector_list[index + 1])
        except IndexError:
            continue

    return distance


def distance_manhattan(vector1, vector2):

    vector = []

    for index in range(len(vector1)):
            vector.append(abs(vector1[index] - vector2[index]))

    return sum(vector)

def distance_euclidean(vector1, vector2):

    vector = []

    for index in range(len(vector1)):
        vector.append((vector1[index] - vector2[index]) ** 2)

    return (sum(vector)) ** 0.5

def distance_levenshtein(vector1, vector2):

    str1 = "".join([str(x) for x in vector1])
    str2 = "".join([str(x) for x in vector2])

    d = dict()

    for i in range(len(str1)+1):
        d[i] = dict()
        d[i][0] = i
    for i in range(len(str2)+1):
        d[0][i] = i
    for i in range(1, len(str1) + 1):
        for j in range(1, len(str2) + 1):
            d[i][j] = min(d[i][j-1] + 1, d[i - 1][j] + 1, d[i - 1][j - 1]+(not str1[i-1] == str2[j-1]))

    return d[len(str1)][len(str2)]

############################## Sorting Algorithm Definition (TSP) #################################

def basic_travel_sorting(vector_list, distance_algorithm):

    """

    Input:

        a) Vector List (equal length vectors) (type = list)
        b) Distance Algorithm (type = func)


    Explanation:

        Taking the first vector as a starting point, the algorithm finds the nearest vector and adds it to
        the Final Vector List. Then, it takes the second vector and finds the nearest vector to it (excluding
        the first one), and adds it to the Final Vector List. This process happens iteratively until there are no
        more new vectors available. Lastly, the total distance between vectors is calculated as Total Distance.

    Output:

        a) Final Vector List (type = list)
        b) Total Distance (type = float or int, depending on the distance algorithm)

    """

    vector_list = vector_list[:]
    final = [vector_list[0]]
    total_distance = 0

    for vector1 in final:

        siguente = None
        vector_list.remove(vector1)

        if len(vector_list) == 0:
            break

        for vector2 in vector_list:

            if siguente is None:
                siguente = vector2

            else:
                if distance_algorithm(vector1, vector2) <= distance_algorithm(vector1, siguente):
                    siguente = vector2

        final.append(siguente)
        total_distance += distance_algorithm(vector1, siguente)

    return final, total_distance

def iterative_func_ordered_1(vector_list, distance_alorithm):

    """

    Input:

        a) Vector List (equal length vectors) (type = list)
        b) Distance Algorithm (type = func)


    Explanation:

        For every vector in the vector list: a new list is created with the selected vector at position 0
        and sets the rest of the vectors according to their previous position.

        Example:

            If we have a list of vectors [a, b, c, d], the new lists will be:

                [a, b, c, d]  (original list)
                [b, c, d, a]
                [c, d, a, b]
                [d, a, b, c]

        For each new list, the basic_travel_sorting() algorithm is executed. The results are compared and
        the minimum distance and corresponding list are saved in the variables best_distance and best(list)
        accordingly.

    Output:

        a) Best Vector List (type = list)
        b) Best Distance (type = float or int, depending on the distance algorithm)

    """

    best = None
    best_distance = None

    for x in range(len(vector_list)):
        new_list = [vector_list[x]] + vector_list[x + 1:] + vector_list[:x]

        lista, distance = basic_travel_sorting(new_list, distance_alorithm)

        if best is None:
            best = lista[:]
            best_distance = distance
        else:
            if distance <= basic_travel_sorting(best, distance_alorithm)[1]:
                best = lista[:]
                best_distance = distance

    return best, best_distance

############################## Custom Function Definition #################################


def Test(vectors, distance_alogrithm):

    """

    Algorithm that prints the results of the ordered iterative algorithm
    given a vector list and a distance algorithm.

    """

    lista1, distancia1 = iterative_func_ordered_1(vectors, distance_alogrithm)

    print(' ')
    print(f"Distancia IFO1: {distancia1}")
    print("Mejor Lista IFO1:")

    print(' ')
    for vector in lista1:
        print(vector)


def tuplas(all_cases):

    os.chdir(os.path.join(os.getcwd(), 'Exported Results'))

    with open("tuplas_distancia.txt", "w") as file:

        for char1 in all_cases:
            for char2 in all_cases:

                if char1 != char2:
                    distance = distance_manhattan(char1.vector, char2.vector)
                    file.write(f"{char1.case_id},{char2.case_id},{distance}")
                    file.write("\n")


