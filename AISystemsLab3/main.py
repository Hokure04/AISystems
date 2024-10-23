import pandas as pd
from math import sqrt
from prettytable import PrettyTable

df = pd.read_csv('Student_Performance.csv')
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
print(df)
df = df.drop(columns=['Extracurricular Activities'])
df = df.apply(pd.to_numeric, errors='coerce')
df = df.dropna()
performance_data = df['Performance Index']

def calc_mean(data):
    return sum(data) / len(data)

def calc_variance(data, mean):
    return sum((value - mean) ** 2 for value in data) / (len(data) - 1)

def calc_standard_deviation(variance):
    return sqrt(variance)

table = PrettyTable()
table.field_names = ["column","mean","variance","standard deviation", "min value", "max value", "0.25 Quantile","0.5 Quantile","0.75 Quantile"]

for column in df.columns:
    data = df[column]
    mean_value = calc_mean(data)
    variance_value = calc_variance(performance_data, mean_value)
    std_value = calc_standard_deviation(variance_value)
    min_value = min(data)
    max_value = max(data)
    q25 = data.quantile(0.25)
    q50 = data.quantile(0.5)
    q75 = data.quantile(0.75)
    table.add_row([column, mean_value, variance_value, std_value, min_value, max_value, q25, q50, q75])

print(table)