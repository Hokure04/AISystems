import numpy as np
import pandas as pd
from prettytable import PrettyTable
from calculation import calculating_dataset_characteristics, min_max_normalize, z_normalize, calc_mean

def preprocess_data(file_path):
    df = pd.read_csv(file_path)
    # print(df)
    df['Extracurricular Activities'] = df['Extracurricular Activities'].map(
        {'Yes': 1, 'No': 0})  # кодирование категориальных признаков

    df = df.apply(pd.to_numeric, errors='coerce')
    df.fillna(0, inplace=True)  # на место пропуска вставляем 0
    return df

def linear_regression(x, y):
    x = np.column_stack((np.ones(x.shape[0]), x))
    x_transpose = x.T
    beta = np.linalg.inv(x_transpose.dot(x)).dot(x_transpose).dot(y)
    return beta

def predict(x, beta):
    x = np.column_stack((np.ones(x.shape[0]), x))
    return x.dot(beta)

def calc_mse(y, y_pred):
    return calc_mean((y - y_pred) ** 2)

def show_correlation_matrix(df):
    corr_matrix = df.corr()
    table = PrettyTable()
    columns = [" "] + list(corr_matrix.columns)
    table.field_names = columns

    for row in corr_matrix.index:
        table.add_row([row] + list(corr_matrix.loc[row]))
    print("Корреляционная матрица:")
    print(table)

def k_fold_cross_validation(df, k, dependent_column):
    df = df.sample(frac=1).reset_index(drop=True)
    fold_size = len(df)//k
    folds = []

    for i in range(k):
        start = i*fold_size
        end = start + fold_size
        folds.append(df.iloc[start:end])

    mse_values = []
    for i in range(k):
        test_data = folds[i]
        train_data = pd.concat([folds[j] for j in range(k) if j != i])
        x_train = train_data.drop(columns=[dependent_column]).values
        y_train = train_data[dependent_column].values

        x_test = test_data.drop(columns=[dependent_column]).values
        y_test = test_data[dependent_column].values

        beta = linear_regression(x_train, y_train)
        y_pred = predict(x_test, beta)
        mse = calc_mse(y_test, y_pred)
        mse_values.append(mse)
        print(f"Фолд {i+1}, MSE: {mse}")

    print(f"Средняя MSE по всем фолдам: {calc_mean(mse_values)}")


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

def main():
    df = preprocess_data('Student_Performance.csv')
    showing_table(df)
    print("Рассчёт изначальных значений набора данных:")
    show_correlation_matrix(df)

    while True:
        try:
            choice_normalization_type = int(input("Выберите тип нормализации (1: min-max, 2: z-ормализация): "))
            if choice_normalization_type == 1 or choice_normalization_type == 2:
                break
            else:
                print("Введите значения 1 или 2")
        except ValueError:
            print("Ошибка вы ввели неверный параметр")


    for column in df.columns:
        if choice_normalization_type == 1:
            df[column] = min_max_normalize(df[column])
        elif choice_normalization_type == 2:
            df[column] = z_normalize(df[column])


    print("Изменение характеристик после нормализации данных")
    showing_table(df)
    while True:
        try:
            k = int(input("Введите количество фолдов: "))
            if k > 1:
                break
            else:
                print("Количество фолдов должно быть больше 1")
        except ValueError:
            print("Ошибка: введите целое число фолдов")

    k_fold_cross_validation(df, k, dependent_column='Performance Index')

main()