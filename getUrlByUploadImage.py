from azure.storage.blob import BlobServiceClient, BlobClient
import os
from datetime import datetime

def upload_image_and_get_url(file):
    # Azure Blob 存储设置
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    container_name = "receipt-storage"
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file.filename)

    try:
        # 检查Blob是否存在
        blob_client.get_blob_properties()
        # 如果文件存在，为文件名添加时间戳
        filename, file_extension = os.path.splitext(file.filename)
        new_filename = f"{filename}_{datetime.now().strftime('%Y%m%d%H%M%S')}{file_extension}"
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=new_filename)
    except Exception as e:
        # 如果文件不存在，继续上传
        pass

    blob_client.upload_blob(file)
    return blob_client.url
