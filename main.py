import pandas_gbq


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


def run_etl():
    # Extract
    query = 'SELECT * FROM `aura-prod-d7e3.dataproduct_apps.dataproduct_apps_unique`'
    df = pandas_gbq.read_gbq(query, project_id='nais-analyse-prod-2dcc')

    # Transform
    #df = aggregate_apps(df)
    print(df.head())
    # Load


if __name__ == '__main__':
    run_etl()
