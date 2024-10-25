from calculation import calculating_dataset_characteristics
from prettytable import PrettyTable
import matplotlib.pyplot as plt

def show_correlation_matrix(df):
    corr_matrix = df.corr()
    table = PrettyTable()
    columns = [" "] + list(corr_matrix.columns)
    table.field_names = columns

    for row in corr_matrix.index:
        table.add_row([row] + list(corr_matrix.loc[row]))
    print(table)


def showing_table(df):
    table = PrettyTable()
    table.field_names = ["Характеристика"] + list(df.columns)
    stats = {
        "Count": [],
        "Mean": [],
        "Variance": [],
        "Standard Deviation": [],
        "Min value": [],
        "0.25 Quantile": [],
        "0.5 Quantile": [],
        "0.75 Quantile": [],
        "Max value": []
    }
    for column in df.columns:
       data = df[column]
       count, mean, variance_val, std, min_value, max_value, quantile_25, quantile_50, quantile_75 = calculating_dataset_characteristics(data)
       stats["Count"].append(count)
       stats["Mean"].append(mean)
       stats["Variance"].append(variance_val)
       stats["Standard Deviation"].append(std)
       stats["Min value"].append(min_value)
       stats["0.25 Quantile"].append(quantile_25)
       stats["0.5 Quantile"].append(quantile_50)
       stats["0.75 Quantile"].append(quantile_75)
       stats["Max value"].append(max_value)

    for characteristic, value in stats.items():
        table.add_row([characteristic] + value)

    print(table)


def show_statistics_and_plots(df):
    statistics = {}
    for column in df.columns:
        count, mean, variance, std_dev, min_val, max_val, q25, q50, q75 = calculating_dataset_characteristics(
            df[column])
        statistics[column] = {
            'Количество': count,
            'Среднее': mean,
            'Дисперсия': variance,
            'Стандартное отклонение': std_dev,
            'Минимум': min_val,
            'Максимум': max_val,
            '25-й квантиль': q25,
            'Медиана (50-й квантиль)': q50,
            '75-й квантиль': q75
        }

        # for stat, value in statistics[column].items():
        #     print(f"{stat}: {value}")

        plt.figure(figsize=(8, 4))
        plt.hist(df[column], bins=20, color='skyblue', edgecolor='black')
        plt.title(f'Гистограмма для признака: {column}')
        plt.xlabel(column)
        plt.ylabel('Частота')
        plt.show()

    return statistics