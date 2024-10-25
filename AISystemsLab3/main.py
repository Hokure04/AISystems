import numpy as np
import pandas as pd
from calculation import min_max_normalize, z_normalize, calc_mean
from tables import *
from itertools import combinations

def preprocess_data(file_path):
    df = pd.read_csv(file_path)
    # print(df)
    df['Extracurricular Activities'] = df['Extracurricular Activities'].map(
        {'Yes': 1, 'No': 0})  # кодирование категориальных признаков

    df = df.apply(pd.to_numeric, errors='coerce')
    df.fillna(0, inplace=True)  # на место пропуска вставляем 0
    df['Effective Practice'] = (df['Hours Studied']*df['Sample Question Papers Practiced']) / df['Sleep Hours']
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

def calc_r2(df, dependent_column, best_models):
    r2_values = []
    for feature, _ in best_models:
        x = df[feature].values
        y = df[dependent_column].values
        beta = linear_regression(x,y)
        y_pred = predict(x, beta)
        ss_residual = np.sum((y - y_pred) ** 2)
        ss_total = np.sum((y - calc_mean(y)) ** 2)
        r2 = 1 - (ss_residual / ss_total)
        r2_values.append(r2)
    return r2_values


def k_fold_cross_validation(df, k, feature_column, dependent_column):
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
        x_train = train_data[feature_column].values
        y_train = train_data[dependent_column].values

        x_test = test_data[feature_column].values
        y_test = test_data[dependent_column].values

        beta = linear_regression(x_train, y_train)
        y_pred = predict(x_test, beta)
        mse = calc_mse(y_test, y_pred)
        mse_values.append(mse)

    return calc_mean(mse_values)


def build_models(df, dependent_column, k):
    remaining_features = list(df.columns)
    remaining_features.remove(dependent_column)
    all_combinations = []
    for r in range(1, len(remaining_features)+1):
        feature_combinations = combinations(remaining_features, r)
        all_combinations.extend(feature_combinations)

    models = []
    for model in all_combinations:
        mse = k_fold_cross_validation(df, k, list(model), dependent_column)
        print(f"Используемые признаки: {list(model)}, MSE: {mse}")
        models.append((list(model), mse))

    models.sort(key=lambda x: x[1])
    best_models = models[:3]
    return best_models

def main():
    df = preprocess_data('Student_Performance.csv')
    print("Рассчёт изначальных значений набора данных:")
    showing_table(df)
    print("Матрица корреляции:")
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

    print("Построение трёх моделей")
    best_models = build_models(df, dependent_column='Performance Index', k=k)
    r2_values = calc_r2(df, 'Performance Index', best_models)
    print("Лучшие модели с различными наборами признаков: ")
    for i, (features, mse) in enumerate(best_models):
        print(f"Модель {i+1}: Признаки: {features}, MSE: {mse}, R^2: {r2_values[i]}")

main()