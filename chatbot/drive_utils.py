import os
import io
import json
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from config import load_config

CONFIG = load_config()
SCOPES = ['https://www.googleapis.com/auth/drive.file']


def authenticate():
    creds_json_str = CONFIG["GOOGLE_CREDENTIALS_JSON"]
    if not creds_json_str:
        raise RuntimeError("Missing GOOGLE_CREDENTIALS_JSON environment variable")
    creds_info = json.loads(creds_json_str)

    creds = service_account.Credentials.from_service_account_info(
        creds_info, scopes=SCOPES
    )
    service = build('drive', 'v3', credentials=creds)
    return service

def upload_file_to_folder(service, folder_id, file_path):
    file_name = os.path.basename(file_path)
    query = f"'{folder_id}' in parents and name = '{file_name}' and trashed = false"
    results = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    items = results.get('files', [])
    for item in items:
        print(f"Xóa file cũ: {item['name']} (ID: {item['id']})")
        service.files().delete(fileId=item['id']).execute()

    file_metadata = {'name': file_name, 'parents': [folder_id]}
    media = MediaFileUpload(file_path, resumable=True)
    uploaded_file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"Upload file '{file_name}' thành công với ID: {uploaded_file['id']}")
    return uploaded_file['id']

def download_file(service, file_id, local_path):
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(local_path, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        if status:
            print(f"Download {int(status.progress() * 100)}%.")
    print(f"File đã được tải về: {local_path}")

def find_file_id(service, folder_id, file_name):
    query = f"'{folder_id}' in parents and name = '{file_name}' and trashed = false"
    results = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    items = results.get('files', [])
    if items:
        return items[0]['id']
    return None

def load_json_from_drive(service, folder_id, file_name):
    file_id = find_file_id(service, folder_id, file_name)
    if not file_id:
        raise FileNotFoundError(f"Không tìm thấy {file_name} trong folder {folder_id}")
    download_file(service, file_id, file_name)
    with open(file_name, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_faiss_index_from_drive(service, folder_id, file_name):
    import faiss
    file_id = find_file_id(service, folder_id, file_name)
    if not file_id:
        raise FileNotFoundError(f"Không tìm thấy {file_name} trong folder {folder_id}")
    download_file(service, file_id, file_name)
    return faiss.read_index(file_name)
