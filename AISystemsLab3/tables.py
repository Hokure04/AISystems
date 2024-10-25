from calculation import calculating_dataset_characteristics
from prettytable import PrettyTable

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