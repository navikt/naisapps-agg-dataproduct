import numpy as np
import pandas as pd


def count_per_group(df, groupby_columns):
    """
    The function is used

    :param df: pd.DataFrame: The dataframe the function is applied on
    :param groupby_col: list: The columns to include in the groupby
    :return: pd.DataFrame: Number of rows per group, including rows where some columns have missing observations
    """
    if type(groupby_columns) is not list:
        raise TypeError
    if len([col for col in groupby_columns if col not in df.columns]) > 0:
        raise KeyError

    df['count'] = 1
    df = df.groupby(groupby_columns, dropna=False)['count'].count().reset_index()

    return df
