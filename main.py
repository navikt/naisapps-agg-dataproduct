import logging

import pandas_gbq
from google.cloud.bigquery import Client

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def count_apps(df):
    """
    This function aggregates apps per location (on prem or cloud) and enviornment (dev or prod)

    :param df: pd.DataFrame: The dataframe the function is applied on
    :return: df: pd.Dataframe: Table containing apps per date, cluster and prod/dev
    """
    df['antall_apper'] = 1

    # Extracting information about environment
    df['env'] = 'dev'
    df.loc[df['cluster'].str.contains('prod'), 'env'] = 'prod'

    # Extracting information about the location
    df['datacenter'] = 'on_prem'
    df.loc[df['cluster'].str.contains('gcp'), 'datacenter'] = 'gcp'

    df = df.groupby(['dato', 'env', 'datacenter'])['antall_apper'].count().reset_index()

    return df


def load_data(df):
    project_id = 'nais-analyse-prod-2dcc'
    dataset = 'apps_aggregated'
    table = 'apps_per_env'

    destination_table = f'{project_id}.{dataset}.{table}'

    table_schema = [
        {'name': 'dato', 'type': 'DATE'},
        {'name': 'env', 'type': 'STRING'},
        {'name': 'datacenter', 'type': 'STRING'},
        {'name': 'antall_apper', 'type': 'INTEGER'}
    ]

    pandas_gbq.to_gbq(
        dataframe=df,
        destination_table=destination_table,
        table_schema=table_schema,
        project_id=project_id,
        if_exists='replace',
        progress_bar=False
    )


def run_etl():
    project_id = 'nais-analyse-prod-2dcc'
    destination_table = f'{project_id}.apps_aggregated.apps_per_env'
    source_table = 'aura-prod-d7e3.dataproduct_apps.dataproduct_apps_unique'

    client = Client(project=project_id)

    # Extract
    logging.info('Read data from source...')
    query = f'SELECT * FROM `{source_table}`'
    df = client.query(query).to_dataframe()
    logging.info(f'{len(df)} rows read from source')

    # Transform
    df = count_apps(df)


    # Load
    logging.info('Write data to target...')
    load_data(df)
    logging.info(f'{len(df)} rows written to target')

if __name__ == '__main__':
    run_etl()
