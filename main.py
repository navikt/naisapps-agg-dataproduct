import pandas_gbq
import logging


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

    df.to_gbq(
        destination_table=destination_table,
        table_schema=table_schema,
        if_exists='replace',
        progress_bar=False
    )


def run_etl():
    # Extract
    logging.info('Read data from source...')
    query = 'SELECT * FROM `aura-prod-d7e3.dataproduct_apps.dataproduct_apps_unique`'
    df = pandas_gbq.read_gbq(query, project_id='nais-analyse-prod-2dcc')
    logging.info(f'{len(df)} rows read from source')

    # Transform
    df = count_apps(df)


    # Load
    logging.info('Write data to target...')
    load_data(df)
    logging.info(f'{len(df)} rows written to target')

if __name__ == '__main__':
    run_etl()
