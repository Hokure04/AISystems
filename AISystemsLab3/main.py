import numpy as np
import pandas as pd
from calculation import min_max_normalize, z_normalize, calc_mean
from tables import *
from itertools import combinations

def preprocess_data(file_path):
    df = pd.read_csv(file_path)
    df['Extracurricular Activities'] = df['Extracurricular Activities'].map(
        {'Yes': 1, 'No': 0})  # кодирование категориального признака
    df.fillna(0, inplace=True)  # на место пропуска вставляем 0
    df['Effective Practice'] = (df['Hours Studied'] * df['Previous Scores']) / df['Sleep Hours']  # введение синтетического признака Эффективная подготовка
    df.drop(columns=['Previous Scores'], inplace=True)

    return df


def linear_regression(x, y):
    x = np.column_stack((np.ones(x.shape[0]), x))
    x_transpose = x.T
    beta = np.linalg.inv(x_transpose.dot(x)).dot(x_transpose).dot(y) # (X^T * X)^(-1) * X^T * y
    return beta

# predict = beta0 + beta1*x1 + ... betan*xn
def predict(x, beta):
    x = np.column_stack((np.ones(x.shape[0]), x))
    return x.dot(beta)

def calc_mse(y, y_pred):
    return calc_mean((y - y_pred) ** 2)

def calc_r2(df, dependent_column, best_models):
    r2_values = []
    for characteristic, _ in best_models:
        x = df[characteristic].values
        y = df[dependent_column].values
        beta = linear_regression(x,y)
        y_pred = predict(x, beta)
        numerator = np.sum((y - y_pred) ** 2)
        denominator = np.sum((y - calc_mean(y)) ** 2)
        r2 = 1 - (numerator / denominator)  # r2 = 1 - (sum(y - y_pred)**2/sum(y - y_mean)**2)
        r2_values.append(r2)
    return r2_values

# фолд - это часть на которую разбивается датасет
def k_fold_cross_validation(df, k, characteristic_column, dependent_column):
    df = df.sample(frac=1).reset_index(drop=True) # перемешиваем данные, сбрасываем старые данные
    fold_size = len(df)//k
    folds = []

    for i in range(k):
        start = i*fold_size
        end = start + fold_size
        folds.append(df.iloc[start:end]) # делаем срез

    mse_values = []

    for i in range(k):
        test_data = folds[i]
        train_data = pd.concat([folds[j] for j in range(k) if j != i])
        x_train = train_data[characteristic_column].values
        y_train = train_data[dependent_column].values

        x_test = test_data[characteristic_column].values
        y_test = test_data[dependent_column].values

        beta = linear_regression(x_train, y_train)
        y_pred = predict(x_test, beta)
        mse = calc_mse(y_test, y_pred)
        mse_values.append(mse)

    return calc_mean(mse_values)


def build_models(df, dependent_column, k):
    characteristic = list(df.columns)
    characteristic.remove(dependent_column)
    all_combinations = []
    for r in range(1, len(characteristic)+1):
        characteristic_combinations = combinations(characteristic, r)
        all_combinations.extend(characteristic_combinations)

    models = []
    for model in all_combinations:
        mse = k_fold_cross_validation(df, k, list(model), dependent_column)
        #print(f"Используемые признаки: {list(model)}, MSE: {mse}")
        models.append((list(model), mse))

    models.sort(key=lambda x: x[1])
    best_models = models[:3]
    return best_models

def main():
    df = preprocess_data('Student_Performance.csv')
    show_statistics_and_plots(df)
    print("Рассчёт изначальных значений набора данных:")
    showing_table(df)
    print("Матрица корреляции:")
    show_correlation_matrix(df)

    while True:
        try:
            print("1. Min-max нормализация")
            print("2. Z-нормализация")
            choice_normalization_type = int(input("Выберите тип нормализации 1 или 2: "))
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
            k = int(input("Введите количество фолдов для K-fold кросс валидации: "))
            if k > 1:
                break
            else:
                print("Количество фолдов должно быть не менее 2")
        except ValueError:
            print("Ошибка: вы ввели недопустимое значение")

    best_models = build_models(df, dependent_column='Performance Index', k=k)
    r2_values = calc_r2(df, 'Performance Index', best_models)
    print("Лучшие модели с различными наборами признаков: ")
    for i, (features, mse) in enumerate(best_models):
        print(f"Модель {i+1}: Признаки: {features}, MSE: {mse}, R^2: {r2_values[i]}")

main()