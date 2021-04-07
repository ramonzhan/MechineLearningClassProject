# -*- encoding: utf-8 -*-
"""
@Description: 
@Time : 2021-3-19 10:10 
@File : utils.py 
@Software: PyCharm
"""
import pandas as pd
import numpy as np


def read_tennis(path="../documents/play_tennis.csv"):
    df = pd.read_csv(path)
    columns = ["outlook", "temp", "humidity", "wind", "play"]
    df = df[columns]
    df_list = []
    for column in columns:
        df_value = str2int(df[column])
        df_list.append(df_value)

    df = np.array(df_list).T
    features, labels = df[:, :-1], df[:, -1]
    train_features, train_labels = features[0:10], labels[0:10]   # 简单地取前10个做训练
    test_features, test_labels = features[10:], labels[10:]
    return train_features, train_labels, test_features, test_labels


def str2int(df_column):
    unique_value = list(set(df_column))
    str_int_dict = dict(zip(unique_value, [i for i in range(len(unique_value))]))
    df_value = df_column.apply(lambda x: str_int_dict[x]).values.tolist()
    return df_value


if __name__ == '__main__':
    read_tennis()
