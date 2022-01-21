import pandas as pd
import pandas_gbq

from transformations import aggregations


def run_etl():
    """
    This function reads data from BigQuery, transforms it using the aggregations-module and loads the table to BigQuery

    :return: Void
    """
    query = 'SELECT * FROM `aura-prod-d7e3.dataproduct_apps.dataproduct_apps_unique`'
    df = pandas_gbq.read_gbq(query)
    df = df[df['cluster'].str.contains('prod')]
    df = aggregations.count_per_group(df, ['cluster', 'dato'])
    # Load!