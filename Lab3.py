import Lab2
import math

probabilities = {"1": 0.982424,
                 "2": 0.999875,
                 "3": 0.997803,
                 "4": 0.914816,
                 "5": 0.993141,
                 "6": 0.967232,
                 "7": 0.902664,
                 "8": 0.999657,
                 "9": 0.994168}

# for my variant
P_system = Lab2.total_p
Q_system = 1 - P_system
print("Q_system = ", Q_system)
t = 1473
k1, k2 = 2, 3   # k1 - for shared and k2 - for general

T_system = - t / math.log(P_system)
print("T_system = ", T_system)
print()

# -------------(2) Загальне ненавантажене резервування кратністю k2 = 3
print("---------(2) Загальне ненавантажене резервування кратністю k2 = 3----")
Q_reserved_system2 = Q_system / math.factorial(k2+1)
P_reserved_system2 = 1 - Q_reserved_system2
T_reserved_system2 = - t / math.log(P_reserved_system2)
print("Q_reserved_system = ", Q_reserved_system2, "\nP_reserved_system = ", P_reserved_system2,
      "\nT_reserved_system = ", T_reserved_system2)

G_q2 = Q_reserved_system2 / Q_system
G_p2 = P_reserved_system2 / P_system
G_T2 = T_reserved_system2 / T_system
print("G_q = ", G_q2, "\nG_p = ", G_p2, "\nG_T = ", G_T2)
print()


# -------------(1) Роздільне навантажене резервування з кратністю k1 = 2
print("---------(1) Роздільне навантажене резервування з кратністю k1 = 2----")


def p_reserved_i(p_i, k):
    return 1 - math.pow((1 - p_i), k+1)


def calculate_p_reserved(p: dict, k):
    p_reserved = dict()
    for element in p.keys():
        p_reserved[element] = p_reserved_i(p[element], k)
    return p_reserved

P_reserved = calculate_p_reserved(probabilities, k1)
# Q_reserved = {k: 1 - v for k, v in zip(P_reserved.keys(), P_reserved.values())}
print("P_reserved for each element")
for k, v in zip(P_reserved.keys(), P_reserved.values()):
    print(k, ': ', v)

# for algorithm of general P calculation
P_reserved['0'] = 0.0
P_reserved['10'] = 0.0

state_matrix = Lab2.calculate_state_matrix(Lab2.my_graph, Lab2.all_working_states, P_reserved)

P_reserved_system1 = Lab2.get_total_probability(state_matrix)
Q_reserved_system1 = 1 - P_reserved_system1
T_reserved_system1 = - t / math.log(P_reserved_system1)
print("Q_reserved_system1 = ", Q_reserved_system1, "\nP_reserved_system1 = ", P_reserved_system1,
      "\nT_reserved_system1 = ", T_reserved_system1)

G_q1 = Q_reserved_system1 / Q_system
G_p1 = P_reserved_system1 / P_system
G_T1 = T_reserved_system1 / T_system
print("G_q = ", G_q1, "\nG_p = ", G_p1, "\nG_T = ", G_T1)


