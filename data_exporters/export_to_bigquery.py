if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter
from google.cloud import bigquery
from dotenv import dotenv_values

config = dotenv_values(".env") 
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
    

    # Demonstrates creating an external table with hive partitioning.

    # TODO(developer): Set table_id to the ID of the table to create.
    table_id = f"{config['PROJECT_ID']}.{config['Dataset_Id']}.{config['Table_name']}"

    
    # Example file:
    # gs://cloud-samples-data/bigquery/hive-partitioning-samples/autolayout/dt=2020-11-15/file1.parquet
    prefix = f'gs://{config["BUCKET_NAME"]}/{config["BUCKET_FOLDER_NAME"]}/'
    
    source_uri_prefix = (
    prefix +'{year:STRING}/{month:STRING}/{day:STRING}'
                     )
    
    if kwargs.get('type_execution') == 'initial_data':

        uri = f'gs://{config["BUCKET_NAME"]}/{config["BUCKET_FOLDER_NAME"]}/*'

            # Construct a BigQuery client object.
        client = bigquery.Client(config['PROJECT_ID'], client_options={"credentials_file":config["Google_credentials"]})
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
        








