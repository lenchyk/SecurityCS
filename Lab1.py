import numpy as np
# input data
# variant constants
data = np.array([766, 137, 105, 124, 63, 356, 67, 113, 325,
                 10, 291, 271, 199, 90, 146, 461, 48, 305,
                 150, 900, 640, 120, 23, 403, 36, 321, 102,
                 136, 451, 257, 55, 87, 264, 135, 542, 425,
                 54, 148, 188, 387, 133, 193, 524, 161, 179,
                 558, 132, 139, 74, 23, 71, 140, 131, 168,
                 159, 97, 31, 625, 34, 111, 452, 12, 26, 234,
                 543, 252, 269, 10, 228, 143, 40, 120, 237,
                 171, 16, 221, 55, 99, 105, 192, 213, 539, 7,
                 89, 452, 161, 478, 85, 443, 32, 162, 633,
                 249, 132, 283, 76, 548, 136, 322, 107])
NUMBER_MALFUNCTION_ELEMENTS = 0.84  # percentage of elements which can break down
TIME_WITHOUT_BREAKDOWN = 511
MALFUNCTION_INTENSITY_TIME = 488

# sort the data for comfort
sorted_data = sorted(data)
mean_value = data.mean()  # mean value
# max value of data which is the last element of sorted
max_value = sorted_data[len(sorted_data) - 1]

k = 10  # splitting into k chunks

ranges = np.array_split(list(range(max_value+1)), k)


# function that makes intervals like this (so the last number will be the first)
# [0...90],[90...180] ...
def array_modifier(arr):
    last_element = 0
    new_arr = []
    for i in range(len(arr)):
        if i == 0:
            last_element = arr[i][len(arr[i])-1]
            new_arr.append(arr[i])
        else:
            new_arr.append(np.insert(arr[i], 0, last_element, axis=0))
            last_element = arr[i][len(arr[i])-1]
    return new_arr


# statistic frequency calculation
def f_calculator(intervals, sorted_data, k):
    F = [0 for _ in range(k)]
    N_i = [0 for _ in range(k)]  # 10 values - the number of elements that in specific interval ranges
    for element in sorted_data:
        for i in range(len(intervals)):
            interval = intervals[i]
            if element in interval:
                N_i[i] += 1
    for i in range(len(N_i)):
        F[i] = round(N_i[i]/(len(sorted_data) * h), 5)
    return F


# find the index of interval the number is in
def find_the_interval(number, intervals):
    for i in range(len(intervals)):
        interval = intervals[i]
        if number in interval:
            return i


# probability working without breaking down
def probabilities(F, k):
    P = [0 for _ in range(k)]
    for i in range(len(F)):
        P[i] = 1 - F[i] * h
    return P


#  ----------------------- the T for NUMBER_MALFUNCTION_ELEMENTS percentage elements ---------------
# function for calculating T with specific percentage of breakable elements
def T(percentage, probability_arr, intervals):
    probability_arr.append(percentage)
    new_probability_arr = sorted(probability_arr)
    index = new_probability_arr.index(percentage)
    d = round((new_probability_arr[index-1] - percentage)/(new_probability_arr[index-1] - new_probability_arr[index+1]), 3)
    T_value = intervals[index-1][len(intervals[index-1])-1] + h * d
    return T_value


def probability_for_time(time, frequency_arr, intervals):
    number_of_interval = find_the_interval(time, intervals)
    square = 0
    for i in range(number_of_interval + 1):
        if i != number_of_interval:
            square += (frequency_arr[i] * h)
        else:
            last_element_in_interval = intervals[i][len(intervals[i])-1]
            square += (frequency_arr[i] * (time - last_element_in_interval))
    p = 1 - square
    return p


def intensity_for_time(time, frequency_arr, intervals):
    number_of_interval = find_the_interval(time, intervals)
    p = probability_for_time(time, frequency_arr, intervals)
    return frequency_arr[number_of_interval]/p


intervals = array_modifier(ranges)

h = (intervals[len(intervals) - 1][len(intervals[len(intervals) - 1]) - 1] - 0) / k

f_array = f_calculator(intervals, sorted_data, k)

p_array = probabilities(f_array, k)

t = T(NUMBER_MALFUNCTION_ELEMENTS, p_array, intervals)
print("T for " + str(NUMBER_MALFUNCTION_ELEMENTS) + "\n", t)

# ------------------------ the Probability for 511 hours -----------------------
p = probability_for_time(TIME_WITHOUT_BREAKDOWN, f_array, intervals)
print("Probability of time without breaking down: " + str(TIME_WITHOUT_BREAKDOWN) + " hours" + "\n", p)

# ------------------------ the Intensity for 488 hours ---------------
intensity = intensity_for_time(MALFUNCTION_INTENSITY_TIME, f_array, intervals)
print("Intensity for " + str(MALFUNCTION_INTENSITY_TIME) + " hours" + "\n", intensity)
