# if 'custom' not in globals():
#     from mage_ai.data_preparation.decorators import custom
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
# if 'test' not in globals():
#     from mage_ai.data_preparation.decorators import test

from mage_ai.data_preparation.variable_manager import set_global_variable

from dotenv import dotenv_values
import os
from google.cloud import storage
from datetime import timedelta

import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd
        


def exist_not(name, bucket_name, project_id, credential):
    # name = 'folder1/another_folder/'  
    client = storage.Client(project_id, client_options={"credentials_file":credential})
    folder_list = list(client.list_blobs(bucket_name, prefix=name))
    if len(folder_list) ==0:
        stats = True
    else:
        stats = False
    return stats


def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    data["created_at"] = pd.to_datetime(data["created_at"])
    data["id"] = data["id"].astype("Int64")
    data["type"] = data["type"].astype("string")

    data["year"] = data["created_at"].dt.year 
    data["month"] = data["created_at"].dt.month
    data["day"] = data["created_at"].dt.day
    return data

def export_to_gcs(data: pd.DataFrame, bucket_name, folder_name):
    """
    Exports data to some source to Google Cloud Storage
    """
    # Specify your data exporting logic here


    root_path = f'{bucket_name}/{folder_name}'
    
    
    table = pa.Table.from_pandas(data)

    gcs = pa.fs.GcsFileSystem()
    pq.write_to_dataset(
        table,
        root_path=root_path,
        partition_cols=['year', 'month', 'day'],
        filesystem=gcs,
        coerce_timestamps='ms',
        allow_truncated_timestamps=True
    )
    


def fetch_chunk_data(url, chunk_size, bucket_name, folder_name):

    # try:
    with pd.read_json(url, lines=True, storage_options={'User-Agent': 'pandas'}, 
        compression="gzip", chunksize=chunk_size) as chunk_read:
        for chunk in chunk_read:
            data = pd.DataFrame(chunk)
            data_cleaned = clean_data(data)
            export_to_gcs(data_cleaned, bucket_name, folder_name)
    # except:
    #     print(f"An exception occur for url {url}")
   


#@custom
@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Load Github archive Data. 
    Load the data of the days before Today in this current month if there's no data for two days in row
    Load incrementally by adding just the data of the previous day (Since our pipeline will run on daily basis).
    """
    now = kwargs.get('execution_date')
    if not kwargs.get('Google_credentials'):
        if not os.path.isdir(".keys/"):
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv("Google_credentials")
            bucket_name = os.getenv("BUCKET_NAME")
            project_id = os.getenv("GCP_PROJECT_ID")

            folder_name = os.getenv("BUCKET_FOLDER_NAME")
            chunk_size = int(os.getenv("CHUNK_SIZE"))
            cred = os.getenv('Google_credentials')
            Dataset_Id = os.getenv('Dataset_Id')
            Table_name = os.getenv['Table_name']


            set_global_variable('github_etl', 'BUCKET_NAME', bucket_name)
            set_global_variable('github_etl', 'PROJECT_ID', project_id)
            set_global_variable('github_etl', 'BUCKET_FOLDER_NAME', folder_name)
            set_global_variable('github_etl', 'CHUNK_SIZE', chunk_size)
            set_global_variable('github_etl', 'Google_credentials', cred)
            set_global_variable('github_etl', 'Dataset_Id', os.getenv("Dataset_Id"))
            set_global_variable('github_etl', 'Table_name', os.getenv("Table_name"))


        else:
            
            config = dotenv_values(".env") # This line brings all environment variables from .env into os.environ
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config["Google_credentials"]
            bucket_name = config["BUCKET_NAME"]
            project_id = config["PROJECT_ID"]
            folder_name = config["BUCKET_FOLDER_NAME"]
            chunk_size = int(config["CHUNK_SIZE"])
            cred = f"{config['Google_credentials']}"
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
        project_id = kwargs.get("PROJECT_ID")
        Table_name = kwargs.get('Table_name')
        Dataset_Id = kwargs.get('Dataset_Id')

        folder_name = kwargs.get("BUCKET_FOLDER_NAME")
        chunk_size = int(kwargs.get("CHUNK_SIZE"))
        if not os.path.isdir(".keys/"): 
             
            if kwargs.get('Google_credentials').startswith('.'):
                cred = os.getenv('Google_credentials')
                set_global_variable('github_etl', 'Google_credentials', cred)
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred
            else:
                cred = kwargs.get('Google_credentials')
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred
        else:
            cred = kwargs.get('Google_credentials')
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred


   # df = pd.DataFrame()  


    # Check if the data concerning the previous day is not stocked in GCS
    previous_day = now - timedelta(days=1)
    if exist_not(f'raw_github/year={previous_day.strftime("%Y")}/month={int(previous_day.strftime("%m"))}/day={int(previous_day.strftime("%d"))}',
        bucket_name, project_id, cred):
        # If yes, check if the data concerning the day before the previous day is not stocked in GCS
        day_before_previous = now - timedelta(days=2)
        print(day_before_previous)
            
        if exist_not(f'raw_github/year={day_before_previous.strftime("%Y")}/month={int(day_before_previous.strftime("%m"))}/day={int(day_before_previous.strftime("%d"))}',
            bucket_name, project_id, cred):
            # If yes, then load the previous month and the day til the previous day
            set_global_variable('github_etl', 'type_execution', 'initial_data')


            # # Previous month
            # month = 12 if (int(now.strftime("%m")) - 1)==0 else (int(now.strftime("%m")) - 1)
            # year = (int(now.strftime("%Y")) -1) if (int(now.strftime("%m")) - 1)==0 else int(now.strftime("%Y"))
            # for day in range(1, 32):
            #     for hour in range(24):
            #         url = f'https://data.gharchive.org/{year}-{month:02}-{day:02}-{hour}.json.gz'
            #         print(f"year:{year}, month:{month:02}, day:{day:02}, hour:{hour}, url:{url} \n")
            #         fetch_chunk_data(url, chunk_size)

            
            # The days of the current month
            for day in range(1, int(now.strftime("%d"))):
                for hour in range(24):
                    url = f'https://data.gharchive.org/{now.strftime("%Y")}-{now.strftime("%m"):02}-{day:02}-{hour}.json.gz'
                    print(f"year:{now.strftime('%Y')}, month:{now.strftime('%m'):02}, day:{day:02}, hour:{hour}, url:{url} \n")
                    fetch_chunk_data(url, chunk_size, bucket_name, folder_name)

            # If no, then load the data of the previous day
        else:
            set_global_variable('github_etl','type_execution', 'yesterday_data')

            for hour in range(24):
                url = f'https://data.gharchive.org/{previous_day.strftime("%Y")}-{previous_day.strftime("%m"):02}-{previous_day.strftime("%d"):02}-{hour}.json.gz'
                print(f"year:{previous_day.strftime('%Y')}, month:{previous_day.strftime('%m'):02}, day:{previous_day.strftime('%d'):02}, hour:{hour:02}, url:{url} \n")
                fetch_chunk_data(url, chunk_size, bucket_name, folder_name)

    return previous_day


# @test
# def test_output(output, *args) -> None:
#     """
#     Template code for testing the output of the block.
#     """
#     assert output is not None, 'The output is undefined'