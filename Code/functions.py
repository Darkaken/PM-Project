los_jinetes = ["Puncture", "Guidewire install", "Remove trocar", "Advance catheter", "Remove guidewire"]
los_jinetes += ["Widen pathway", "Remove syringe"]

def filter_acts(log, important):

    data = []

    for line in log:
        important_data = []
        line = line.split(",")

        if line[4] in important:
            important_data.append(line[0].split("-")[0])
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


v1 = [0, 0, 0, 0, 0, 0, 1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0]
v2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
v3 = [1, 0, 0, 0, 0, 0, 2, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0]

def basic_travel_sorting(vector_list, distance_algorithm):

    vector_list = vector_list[:]
    final = [vector_list[0]]
    total_distance = 0

    print(vector_list[0])
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
        print(distance_algorithm(vector1, siguente))
        print(siguente)

    print(total_distance)
    return final




