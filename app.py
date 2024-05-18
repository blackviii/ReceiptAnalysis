from flask import Flask, request, redirect, url_for, render_template
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os

app = Flask(__name__)


# Azure Blob 存储设置
# 移除连接字符串，改为从环境变量中读取
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
container_name = "receipt-storage"
blob_service_client = BlobServiceClient.from_connection_string(connect_str)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file.filename)
        blob_client.upload_blob(file)
        return redirect(url_for('uploaded_file', filename=file.filename))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
    url = blob_client.url
    return f'File uploaded successfully. Public URL: <a href="{url}">{url}</a>'

if __name__ == '__main__':
    app.run(debug=True)
