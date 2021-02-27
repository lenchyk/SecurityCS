import numpy as np

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
MALFUNCTION_PERCENTAGE = 0.86  # percentage of elements which can break down
TIME_WITHOUT_BREAKDOWN = 511
MALFUNCTION_INTENSITY_TIME = 488
N = len(data)

# sort the data for comfort
sorted_data = sorted(data)

mean_value = data.mean()  # average time until breaking down

# max value of data which is the last element of sorted
max_value = sorted_data[len(sorted_data) - 1]

k = 10  # splitting into k chunks
h = max_value / k

intervals = [round(interval * h, 2) for interval in range(k + 1)]


def data_sort_through_intervals(arr, intervals):
    data_intervals = [[] for _ in range(k)]
    for element in arr:
        for i in range(k):
            if intervals[i] <= element <= intervals[i+1]:
                data_intervals[i].append(element)
    return data_intervals


# statistic frequency calculation (щільність)
def f_calculator(data_intervals, k):
    F = [0 for _ in range(k)]
    for i in range(k):
        F[i] = len(data_intervals[i])/(N * h)
    return F


# find the index of interval the number is in
def find_the_interval(number, intervals):
    for i in range(k):
        if intervals[i] <= number <= intervals[i+1]:
            return i


# probability working without breaking down
def probabilities(frequency):
    P = [0 for _ in range(k)]
    for i in range(k):
        square = 0
        for j in range(i+1):
            square += (frequency[j] * h)
        P[i] = round(1 - square, 5)
    return P


# function for calculating T with specific percentage of breakable elements
def T(percentage, probability_arr, intervals):
    new_p_arr = probability_arr.copy()
    new_p_arr.insert(0, 1)
    for i in range(len(new_p_arr)):
        if new_p_arr[i] > percentage:
            new_p_arr.insert(i + 1, percentage)
    index = new_p_arr.index(percentage)
    d = round((new_p_arr[index+1] - percentage)/(new_p_arr[index+1] - new_p_arr[index-1]), 2)
    T_value = round(intervals[index] - h * d, 2)
    return T_value


def probability_for_time(time, frequency_arr, intervals):
    number_of_interval = find_the_interval(time, intervals)
    square = 0
    for i in range(number_of_interval + 1):
        if i != number_of_interval:
            square += (frequency_arr[i] * h)
        else:
            square += (frequency_arr[i] * (time - intervals[i]))
    p = round(1 - square, 4)
    return p


def intensity_for_time(time, frequency_arr, intervals):
    number_of_interval = find_the_interval(time, intervals)
    p = probability_for_time(time, frequency_arr, intervals)
    return round(frequency_arr[number_of_interval]/p, 4)


data_intervals = data_sort_through_intervals(sorted_data, intervals)
print("Intervals: \n", intervals)

f_array = f_calculator(data_intervals, k)

p_array = probabilities(f_array)

t_value = T(MALFUNCTION_PERCENTAGE, p_array, intervals)
print("Середній наробіток до відмови: ", t_value)

p = probability_for_time(TIME_WITHOUT_BREAKDOWN, f_array, intervals)
print("Ймовірність часу до відмови: " + str(TIME_WITHOUT_BREAKDOWN) + " год" + "\n", p)

intensity = intensity_for_time(MALFUNCTION_INTENSITY_TIME, f_array, intervals)
print("Інтенсивність для " + str(MALFUNCTION_INTENSITY_TIME) + " год" + "\n", intensity)

