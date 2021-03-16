import itertools
import numpy as np

# 0 - a start and 7 - the end
my_graph = {
    "0": ["1", "2"],
    "1": ["3", "4", "5"],
    "2": ["3", "4", "6"],
    "3": ["4", "5", "6"],
    "4": ["5", "6"],
    "5": ["7"],
    "6": ["7"],
    "7": []
}

probabilities = {"0": 0.0,
                 "1": 0.66,
                 "2": 0.04,
                 "3": 0.55,
                 "4": 0.63,
                 "5": 0.86,
                 "6": 0.58,
                 "7": 0.0}


# all paths for this graph
def find_all_paths(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if start not in graph:
            return []
        paths = []
        for node in graph[start]:
            if node not in path:
                new_paths = find_all_paths(graph, node, end, path)
                for new_path in new_paths:
                    paths.append(new_path)
        return paths


# all combination existing with elements
def get_all_combinations(graph: dict):
    all = []
    keys = graph.keys()
    for i in range(1, len(graph.keys()) + 1):
        all.append(list(itertools.combinations(keys, i)))
    all_combinations = [j for i in all for j in i]
    return all_combinations


# combinations that contain our paths
def get_all_working_states(all_paths: list, all_combinations: list):
    all_states = set()
    for combination in all_combinations:
        for path in all_paths:
            if set(path).issubset(set(combination)):
                all_states.add(combination)
    return list(all_states)


# state matrix with probabilities (like the table in example
# but with probabilities instead of +/-)
def calculate_state_matrix(graph: dict, working_states: set, probabilities: dict):
    state_matrix = [[] for _ in range(len(working_states))]
    for state_index in range(len(working_states)):
        state = working_states[state_index]
        for element in graph.keys():
            if element in state:
                state_matrix[state_index].append(probabilities[element])
            else:
                state_matrix[state_index].append(round(1 - probabilities[element], 6))
    for state in state_matrix:
        state.append(np.prod(state[1:-1]))
    return state_matrix


# total probability of the system
def get_total_probability(states_matrix):
    return sum([probabilities[-1] for probabilities in states_matrix])


all_paths = find_all_paths(my_graph, "0", "7")
all_combinations = get_all_combinations(my_graph)
all_working_states = get_all_working_states(all_paths, all_combinations)
state_matrix = calculate_state_matrix(my_graph, all_working_states, probabilities)
total_p = get_total_probability(state_matrix)
print("Ймовірність безвідмовної роботи системи: ", total_p)

