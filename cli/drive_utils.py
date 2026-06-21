import os
import io
import datetime
import logging

logger = logging.getLogger(__name__)

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive']
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'

def get_drive_service(base_path):
    """Get Google Drive API service."""
    creds = None
    token_path = os.path.join(base_path, TOKEN_FILE)
    creds_path = os.path.join(base_path, CREDENTIALS_FILE)

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(creds_path):
                raise FileNotFoundError(f"Missing {CREDENTIALS_FILE}. Please create it on Google Cloud Console.")
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
            
    return build('drive', 'v3', credentials=creds)

def get_or_create_folder(service, folder_name, parent_id=None):
    """Find or create a folder on Google Drive."""
    search_parent = parent_id if parent_id else 'root'
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false and '{search_parent}' in parents"
        
    logger.info(f"Searching for folder '{folder_name}'...")
    results = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    items = results.get('files', [])
    
    if items:
        logger.info(f"Found folder '{folder_name}' (ID: {items[0]['id']})")
        return items[0]['id']
    else:
        logger.info(f"Folder '{folder_name}' not found, creating new...")
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [search_parent]
        }
            
        folder = service.files().create(body=folder_metadata, fields='id').execute()
        logger.info(f"Successfully created folder '{folder_name}' (ID: {folder.get('id')})")
        return folder.get('id')

def find_file(service, filename, parent_id):
    """Find the ID of a file in a specific folder."""
    query = f"name='{filename}' and '{parent_id}' in parents and trashed=false"
    results = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    items = results.get('files', [])
    return items[0]['id'] if items else None

def upload_file(service, local_path, filename, parent_id):
    """Upload a file to a folder on Drive."""
    logger.info(f"Starting upload process for file '{filename}' to Drive...")
    file_id = find_file(service, filename, parent_id)
    
    media = MediaFileUpload(local_path, mimetype='application/x-ipynb+json', resumable=True)
    
    if file_id:
        # Update existing
        logger.info(f"File '{filename}' ALREADY EXISTS on Drive (ID: {file_id}). Proceeding to overwrite/update...")
        file_metadata = {'name': filename}
        updated_file = service.files().update(
            fileId=file_id,
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        logger.info(f"Successfully updated file '{filename}'.")
        return updated_file.get('id')
    else:
        # Create new
        logger.info(f"File '{filename}' DOES NOT EXIST on Drive. Proceeding to upload new...")
        file_metadata = {
            'name': filename,
            'parents': [parent_id]
        }
        new_file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        logger.info(f"Successfully created and uploaded file '{filename}' (ID: {new_file.get('id')}).")
        return new_file.get('id')

def download_file(service, file_id, local_path):
    """Download file from Drive to local machine."""
    request = service.files().get_media(fileId=file_id)
    with io.FileIO(local_path, 'wb') as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()

def list_drive_notebooks(service):
    """Get list of notebook files in 'Colab Notebooks' folder."""
    colab_folder_id = get_or_create_folder(service, 'Colab Notebooks')
    query = f"'{colab_folder_id}' in parents and trashed=false and name contains '.ipynb'"
    results = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    return results.get('files', [])

def list_directory_contents(service, folder_id='root'):
    """Get list of files and folders in a specific directory."""
    query = f"'{folder_id}' in parents and trashed=false"
    results = service.files().list(q=query, spaces='drive', fields='files(id, name, mimeType)').execute()
    return results.get('files', [])

def find_notebooks_by_keyword(service, keyword):
    """Find notebooks by keyword (substring match)."""
    colab_folder_id = get_or_create_folder(service, 'Colab Notebooks')
    query = f"'{colab_folder_id}' in parents and trashed=false and name contains '.ipynb' and name contains '{keyword}'"
    results = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    return results.get('files', [])

def count_directory_items(service, folder_id='root'):
    """Count the number of items in a specific directory."""
    query = f"'{folder_id}' in parents and trashed=false"
    results = service.files().list(q=query, spaces='drive', fields='files(id)').execute()
    return len(results.get('files', []))

