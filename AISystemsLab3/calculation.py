from math import sqrt
import numpy as np

def calc_mean(data):
    return sum(data) / len(data)

def calc_variance(data, mean):
    return sum((value - mean) ** 2 for value in data) / (len(data) - 1)

def calc_standard_deviation(variance):
    return sqrt(variance)

def min_max_normalize(column):
    return (column - column.min()) / (column.max() - column.min())

def z_normalize(column):
    mean = calc_mean(column)
    std_dev = calc_standard_deviation(calc_variance(column, mean))
    return (column - mean) / std_dev

def calculating_dataset_characteristics(column):
    mean_value = calc_mean(column)
    variance_value = calc_variance(column, mean_value)
    std_value = calc_standard_deviation(variance_value)
    quantile_25 = np.percentile(column, 25)
    quantile_50 = np.percentile(column, 50)
    quantile_75 = np.percentile(column, 75)
    return len(column), mean_value, variance_value, std_value, min(column), max(column), quantile_25, quantile_50, quantile_75