if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter
from google.cloud import bigquery
from dotenv import dotenv_values
import os

config = dotenv_values(".env") 


if not config:
    bucket_name = os.getenv("BUCKET_NAME")
    project_id = os.getenv("GCP_PROJECT_ID")

    folder_name = os.getenv("BUCKET_FOLDER_NAME")
    chunk_size = int(os.getenv("CHUNK_SIZE"))
    cred = os.getenv('Google_credentials')
    Dataset_Id = os.getenv('Dataset_Id')
    Table_name = os.getenv('Table_name')

else:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config["Google_credentials"]
    bucket_name = config["BUCKET_NAME"]
    project_id = config["PROJECT_ID"]

    folder_name = config["BUCKET_FOLDER_NAME"]
    chunk_size = int(config["CHUNK_SIZE"])
    cred = config["Google_credentials"]
    Dataset_Id = config['Dataset_Id']
    Table_name = config['Table_name']


@data_exporter
def export_data(data, *args, **kwargs):
    """
    Exports data to some source.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """
    # Specify your data exporting logic here
    if not kwargs.get('Dataset_Id'):
        config = dotenv_values(".env") # This line brings all environment variables from .env into os.environ

        if not config:
            #os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv("Google_credentials")
            bucket_name = os.getenv("BUCKET_NAME")
            project_id = os.getenv("GCP_PROJECT_ID")

            folder_name = os.getenv("BUCKET_FOLDER_NAME")
            chunk_size = int(os.getenv("CHUNK_SIZE"))
            cred = os.getenv('Google_credentials')
            Dataset_Id = os.getenv('Dataset_Id')
            Table_name = config['Table_name']


            set_global_variable('github_etl', 'BUCKET_NAME', bucket_name)
            set_global_variable('github_etl', 'PROJECT_ID', project_id)
            set_global_variable('github_etl', 'BUCKET_FOLDER_NAME', folder_name)
            set_global_variable('github_etl', 'CHUNK_SIZE', chunk_size)
            set_global_variable('github_etl', 'Google_credentials', cred)
            set_global_variable('github_etl', 'Dataset_Id', config["Dataset_Id"])
            set_global_variable('github_etl', 'Table_name', config["Table_name"])


        else:
            # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config["Google_credentials"]
            
            bucket_name = config["BUCKET_NAME"]
            project_id = config["PROJECT_ID"]
            folder_name = config["BUCKET_FOLDER_NAME"]
            chunk_size = int(config["CHUNK_SIZE"])
            cred = config["Google_credentials"]
            Dataset_Id = config['Dataset_Id']
            Table_name = config['Table_name']

            set_global_variable('github_etl', 'BUCKET_NAME', bucket_name)
            set_global_variable('github_etl', 'PROJECT_ID', project_id)
            set_global_variable('github_etl', 'BUCKET_FOLDER_NAME', folder_name)
            set_global_variable('github_etl', 'CHUNK_SIZE', chunk_size)
            set_global_variable('github_etl', 'Google_credentials', cred)
            set_global_variable('github_etl', 'Dataset_Id', config["Dataset_Id"])
            set_global_variable('github_etl', 'Table_name', config["Table_name"])

    else:
        bucket_name = kwargs.get("BUCKET_NAME")
        project_id = kwargs.get("GCP_PROJECT_ID")

        folder_name = kwargs.get("BUCKET_FOLDER_NAME")
        chunk_size = int(kwargs.get("CHUNK_SIZE"))
        cred = kwargs.get('Google_credentials')
        Table_name = kwargs.get('Table_name')
        Dataset_Id = kwargs.get('Dataset_Id')

    # Demonstrates creating an external table with hive partitioning.

    # TODO(developer): Set table_id to the ID of the table to create.
    table_id = f"{project_id}.{Dataset_Id}.{Table_name}"

    
    # Example file:
    # gs://cloud-samples-data/bigquery/hive-partitioning-samples/autolayout/dt=2020-11-15/file1.parquet
    prefix = f'gs://{bucket_name}/{folder_name}/'
    
    source_uri_prefix = (
    prefix +'{year:STRING}/{month:STRING}/{day:STRING}'
                     )

    # Construct a BigQuery client object.
    client = bigquery.Client(project_id, client_options={"credentials_file":cred})
    
    if kwargs.get('type_execution') == 'initial_data':

        uri = f'gs://{bucket_name}/{folder_name}/*'


        # Configure the external data source.
        external_config = bigquery.ExternalConfig("PARQUET")
        external_config.source_uris = [uri]
        external_config.autodetect = False

        # Configure partitioning options.
        hive_partitioning_opts = bigquery.HivePartitioningOptions()

        hive_partitioning_opts.mode = "CUSTOM"
        hive_partitioning_opts.require_partition_filter = False
        hive_partitioning_opts.source_uri_prefix = source_uri_prefix

        external_config.hive_partitioning = hive_partitioning_opts


        schema = [
        {
            "name": "id",
            "type": "integer",
            "mode": "NULLABLE"
        },
        {
            "name": "type",
            "type": "string",
            "mode": "NULLABLE"
        },
        {
            "name": "actor",
            "type": "record",
            "mode": "NULLABLE",
            "fields": [
            {
                "name": "avatar_url",
                "type": "string",
                "mode": "NULLABLE"
            },
            {
                "name": "display_login",
                "type": "string",
                "mode": "NULLABLE"
            },
            {
                "name": "gravatar_id",
                "type": "string",
                "mode": "NULLABLE"
            },
            {
                "name": "id",
                "type": "integer",
                "mode": "NULLABLE"
            },
            {
                "name": "login",
                "type": "string",
                "mode": "NULLABLE"
            },
            {
                "name": "url",
                "type": "string",
                "mode": "NULLABLE"
            }
            ]
        },
        {
            "name": "repo",
            "type": "record",
            "mode": "NULLABLE",
            "fields": [
            {
                "name": "id",
                "type": "integer",
                "mode": "NULLABLE"
            },
            {
                "name": "name",
                "type": "string",
                "mode": "NULLABLE"
            },
            {
                "name": "url",
                "type": "string",
                "mode": "NULLABLE"
            }
            ]
        },
        {
            "name": "payload",
            "type": "string",
            "mode": "NULLABLE"
        },
        {
            "name": "public",
            "type": "boolean",
            "mode": "NULLABLE"
        },
        {
            "name": "created_at",
            "type": "timestamp",
            "mode": "NULLABLE"
        },
        {
            "name": "org",
            "type": "record",
            "mode": "NULLABLE",
            "fields": [
            {
                "name": "avatar_url",
                "type": "string",
                "mode": "NULLABLE"
            },
            {
                "name": "gravatar_id",
                "type": "string",
                "mode": "NULLABLE"
            },
            {
                "name": "id",
                "type": "integer",
                "mode": "NULLABLE"
            },
            {
                "name": "login",
                "type": "string",
                "mode": "NULLABLE"
            },
            {
                "name": "url",
                "type": "string",
                "mode": "NULLABLE"
            }
            ]
        }
        ]

        table = bigquery.Table(table_id, schema=schema)
        table.external_data_configuration = external_config

        table = client.create_table(table)  # Make an API request.
        print(
            f"Created table {table_id}")
        

    else:
        uri = f'{prefix}/year={data.strftime("%Y")}/month={int(data.strftime("%m"))}/day={int(data.strftime("%d"))}/*'
        query = f"""
        LOAD DATA INTO {table_id}
            FROM FILES(
                format='PARQUET',
                uris = [{uri}],
                hive_partition_uri_prefix={prefix}
            )
            WITH PARTITION COLUMNS(
            year STRING
            month STRING
            day STRING
            )
        """
        query_job = client.query(query)  # API request
        print(
            f"we inserted the data of {data.strftime('%Y/%m/%d')} into {table_id}")
        








