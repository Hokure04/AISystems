import pandas as pd
import numpy as np
from math import sqrt
from prettytable import PrettyTable

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

def calculating_dataset_characteristics(df, table):
    for column in df.columns:
        data = df[column]
        mean_value = calc_mean(data)
        variance_value = calc_variance(data, mean_value)
        std_value = calc_standard_deviation(variance_value)
        min_value = min(data)
        max_value = max(data)
        quantile_25 = np.percentile(data, 25)
        quantile_50 = np.percentile(data, 50)
        quantile_75 = np.percentile(data, 75)
        table.add_row([column, mean_value, variance_value, std_value, min_value, max_value, quantile_25, quantile_50,
                       quantile_75])
    print(table)

def main():
    df = pd.read_csv('Student_Performance.csv')
    # print(df)
    df['Extracurricular Activities'] = df['Extracurricular Activities'].map({'Yes':1, 'No':0}) # кодирование категориальных признаков

    df = df.apply(pd.to_numeric, errors='coerce')
    df.fillna(0, inplace=True) # на место пропуска вставляем 0


    table = PrettyTable()
    table.field_names = ["column", "mean", "variance", "standard deviation", "min value", "max value", "0.25 Quantile",
                         "0.5 Quantile", "0.75 Quantile"]
    print("Рассчёт изначальных значений набора данных:")
    calculating_dataset_characteristics(df, table)
    table.clear_rows()

    while True:
        try:
            choice_normalization_type = int(input("Выберите тип нормализации (1: min-max, 2: z-ормализация): "))
            if choice_normalization_type == 1 or choice_normalization_type == 2:
                break
            else:
                print("Введите значения 1 или 2")
        except ValueError:
            print("шибка вы ввели неверный параметр")


    for column in df.columns:
        if choice_normalization_type == 1:
            df[column] = min_max_normalize(df[column])
        elif choice_normalization_type == 2:
            df[column] = z_normalize(df[column])


    print("Изменение характеристик после нормализации данных")
    table = PrettyTable()
    table.field_names = ["column", "mean", "variance", "standard deviation", "min value", "max value", "0.25 Quantile",
                         "0.5 Quantile", "0.75 Quantile"]

    calculating_dataset_characteristics(df, table)

main()