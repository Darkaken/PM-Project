from collections import defaultdict
import os

all_cases = []
used_ids = []
exported = []

class Instance(object):

    def __init__(self, case_id):

        self.case_id = case_id
        self.activities = []
        self.pre_or_post = None

    def important(self):
        lista = []

        for act in self.activities:
            if act.stage != 'Operator and Patient Preparation':
                lista.append(act)

        return lista

    def add_activity(self, other):
        self.activities.append(other)

    def __gt__(self, other):
        if self.pre_or_post == 'Post' and other.pre_or_post == 'Pre':
            return True
        elif self.pre_or_post == 'Pre' and other.pre_or_post == 'Post':
            return False
        return True

    def __lt__(self, other):
        if self.pre_or_post == 'Post' and other.pre_or_post == 'Pre':
            return False
        elif self.pre_or_post == 'Pre' and other.pre_or_post == 'Post':
            return True
        return False


class Activity:

    def __init__(self, name, stage, time, time2):

        self.name = name
        self.stage = stage
        self.time_start = time
        self.time_end = time2

with open('log.csv', 'r') as data:
    for line in data:
        lines = line.split(',')  #Spliteo el CSV
        lines[0] = lines[0].split('-')[0]  #Elimino la info del video y dejo solo el num del CaseID

        temp = Activity(lines[4], lines[5], lines[6], lines[7])

        if lines[0] in used_ids:
            all_cases[-1].add_activity(temp)
        else:
            all_cases.append(Instance(lines[0]))
            all_cases[-1].add_activity(temp)
            all_cases[-1].pre_or_post = lines[2]
            used_ids.append(lines[0])


try:
    os.mkdir(os.path.join(os.getcwd(), 'Exported Results'))
except FileExistsError:
    pass

os.chdir(os.path.join(os.getcwd(), 'Exported Results'))

def Print_Info(all_case, all_results = False):

    all_case = sorted(all_case[:])
    for case in all_case:
        print(' ')
        print(' ')
        print(f'                          Case {case.case_id} ({case.pre_or_post})                               Start Time             End Time')
        print(' ')

        exported.append(' ')
        exported.append(' ')
        exported.append(f'                          Case {case.case_id} ({case.pre_or_post})                               Start Time             End Time')
        exported.append(' ')

        if all_results is False:
            trigger = 'Operator and Patient Preparation'
            print('                  Preparation Activities not included')
            exported.append('                  Preparation Activities not included')
        else:
            trigger = ' '
            print('                       All Activities Included')
            exported.append('                       All Activities Included')

        for act in case.activities:
            if act.stage == trigger:
                continue
            else:
                var = '                                                                         '
                var = list(var)

                for i in range(len(act.name)):
                    var[i] = act.name[i]
                for i in range(len(act.stage)):
                    var[-(i + 1)] = act.stage[::-1][i]

                var2 = list('                             ')

                for i in range(len(act.time_start.split(' ')[1])):
                    var2[i] = act.time_start.split(' ')[1][i]
                for i in range(len(act.time_end.split(' ')[1])):
                    var2[-(i + 1)] = act.time_end[::-1][i]

                prints = ''.join(var) +'          ' +''.join(var2)
                print(prints)
                exported.append(prints)
        print(' ')
        exported.append(' ')

        Print_Stats(case, all_results)

def Print_Stats(instance, all_res):

    repeated = defaultdict(int)

    if all_res is True:
        for act in instance.activities:
            repeated[act.name] += 1
    else:
        for act in instance.important():
            repeated[act.name] += 1

    for key in repeated.keys():
        if repeated[key] > 1:
            var1 = 'Repeated Activity:    '
            var2 = list('                                           ')

            for i in range(len(key)):
                var2[i] = key[i]
            for i in range(len(str(repeated[key]))):
                var2[-(i + 1)] = str(repeated[key])[::-1][i]

            print(var1 + ''.join(var2))
            exported.append(var1 + ''.join(var2))


Print_Info(all_cases, True)

counter = 0

while True:

    isFile = os.path.isfile(os.path.join(os.getcwd(), f'export_{counter + 1}.csv'))

    if isFile is False:
        with open(f'export_{counter + 1}.csv', 'w') as file:
            for line in exported:
                file.write(line)
                file.write('\n')
            break
    else:
        counter += 1