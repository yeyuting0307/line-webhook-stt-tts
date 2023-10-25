import os
import logging
import pandas as pd
import json
import gcsfs
from google.cloud import storage

class GcpStorage(storage.Client):
    def __init__(self, project_id:str, *args, **kwargs) -> None:
        self.project_id = project_id
        self.file_system = gcsfs.GCSFileSystem(project=project_id)
        super(self.__class__, self).__init__(project=project_id, *args, **kwargs)
        logging.info(f'project: {project_id} storage is connected.')
        
    def fromStorage(self, remote_path:str, read_function=None):
        '''
        Parameter
        --------------------
        remote_path: gsutil URI remove "gs://"
        read_function: pd.read_csv / pd.read_excel / json.loads
        '''
        with self.file_system.open(f'gs://{remote_path}','rb') as f:
            if remote_path.split('.')[-1] == 'xlsx':
                data = pd.read_excel(f)
            elif remote_path.split('.')[-1] == 'csv':
                data = pd.read_csv(f)
            elif remote_path.split('.')[-1] == 'json':
                data = json.load(f)
            else:
                try:
                    data = read_function(f)
                except:
                    logging.info('[Storage] Please Check File Type !')
                    return None
        return data
    
    def toStorage(self, remote_path:str, local_path:str, make_public:bool=False):
        
        bucket_name = remote_path.split('/')[0]
        upload_file_path = remote_path.replace(f'{bucket_name}/','')   
        
        bucket = self.bucket(bucket_name)                           
        blob = bucket.blob(upload_file_path)
        blob.upload_from_filename(local_path)

        if make_public == True:
            blob.make_public()
        
        logging.info(f"[Storage] File {local_path} is uploaded to {remote_path}")
        
        return f"[Storage] File {local_path} is uploaded to {remote_path}"

    def check_if_file_exists(self, remote_path:str):
        '''
        Parameter
        --------------------
        remote_path: gsutil URI remove "gs://"
        '''

        bucket_name = remote_path.split('/')[0]
        file_path = remote_path.replace(f'{bucket_name}/','')   
        
        bucket = self.bucket(bucket_name)                           
        blob = bucket.get_blob(file_path)
        try:
            return blob.exists(self)
        except:
            return False
    
    def get_file_list(self, remote_path:str):
        '''
        Parameter
        --------------------
        remote_path: gsutil URI remove "gs://"
        '''
        
        bucket_name = remote_path.split('/')[0]
        folder_path = remote_path.replace(f'{bucket_name}/','')
        if folder_path[-1] != '/':
            folder_path += '/'

        file_list = self.list_blobs(
            bucket_or_name=bucket_name,
            prefix=folder_path,
            delimiter='/'
            )
        file_list = [x.name for x in file_list]  
        file_list.remove(folder_path)
        
        return file_list