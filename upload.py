from google.cloud import storage
from os import environ,sep, curdir
import json

def save_file_from_environ(env_name, path):
    content=environ.get(env_name,"")
    if(content==""):
        raise Exception("environment variable "+env_name+ " not set")
    f = open(path,"wt") 
    f.write(content)   
    f.close()

def upload_blob(bucket_name, source_file_name, destination_blob_name, credentials_file):
    """Uploads a file to the bucket."""
    
    
    storage_client = storage.Client.from_service_account_json(credentials_file)
  
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )