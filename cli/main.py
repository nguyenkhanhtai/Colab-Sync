import os
import argparse
import datetime
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

from .drive_utils import get_drive_service, get_or_create_folder, upload_file, find_file, download_file, list_drive_notebooks, list_directory_contents

def push(args):
    filename = args.filename
    if not filename.endswith('.ipynb'):
        print("Error: File must have .ipynb extension")
        sys.exit(1)
        
    local_path = os.path.join(os.getcwd(), filename)
    if not os.path.exists(local_path):
        print(f"Error: File not found {local_path}")
        sys.exit(1)

    print(f"Connecting to Google Drive...")
    try:
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        service = get_drive_service(project_root)
        
        print("Finding or creating 'Colab Notebooks' folder...")
        colab_folder_id = get_or_create_folder(service, 'Colab Notebooks')
        
        print("Finding or creating 'temp' folder...")
        temp_folder_id = get_or_create_folder(service, 'temp', parent_id=colab_folder_id)
        
        print(f"Uploading '{filename}' to 'Colab Notebooks'...")
        upload_file(service, local_path, filename, colab_folder_id)
        
        # Upload to temp folder with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_filename = f"{filename.replace('.ipynb', '')}_{timestamp}.ipynb"
        print(f"Backing up '{temp_filename}' to 'temp' folder...")
        upload_file(service, local_path, temp_filename, temp_folder_id)
        
        print("Push successful!")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

def pull(args):
    filename = args.filename
    if not filename.endswith('.ipynb'):
        print("Error: File must have .ipynb extension")
        sys.exit(1)
        
    print(f"Connecting to Google Drive...")
    try:
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        service = get_drive_service(project_root)
        
        colab_folder_id = get_or_create_folder(service, 'Colab Notebooks')
        
        print(f"Finding '{filename}' on Drive...")
        file_id = find_file(service, filename, colab_folder_id)
        
        if not file_id:
            print(f"Error: File '{filename}' not found in 'Colab Notebooks' folder on Drive.")
            sys.exit(1)
            
        local_path = os.path.join(os.getcwd(), filename)
        print(f"Downloading file to '{local_path}'...")
        download_file(service, file_id, local_path)
        
        print("Pull successful!")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

def list_notebooks(args):
    print(f"Connecting to Google Drive...")
    try:
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        service = get_drive_service(project_root)
        
        print("Fetching list of files from 'Colab Notebooks'...\n")
        notebooks = list_drive_notebooks(service)
        
        if not notebooks:
            print("No notebooks found in 'Colab Notebooks' folder.")
            return
            
        print(f"Found {len(notebooks)} notebook(s):")
        for idx, nb in enumerate(notebooks, 1):
            print(f"{idx}. {nb['name']}")
            
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

def list_directory(args):
    print(f"Connecting to Google Drive...")
    try:
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        service = get_drive_service(project_root)
        
        folder_id = args.folder_id
        if folder_id == 'default':
            folder_id = get_or_create_folder(service, 'Colab Notebooks')
        
        print(f"Fetching directory contents (ID: {folder_id})...\n")
        items = list_directory_contents(service, folder_id)
        
        if not items:
            print("Directory is empty or does not exist.")
            return
            
        print(f"Found {len(items)} item(s):")
        for idx, item in enumerate(items, 1):
            item_type = "DIR " if item.get('mimeType') == 'application/vnd.google-apps.folder' else "FILE"
            print(f"{idx}. [{item_type}] {item.get('name')} (ID: {item.get('id')})")
            
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Colab Notebooks Sync CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Lệnh push
    parser_push = subparsers.add_parser('push', help='Push a local notebook to Google Drive')
    parser_push.add_argument('filename', help='Filename (e.g., my_notebook.ipynb)')
    parser_push.set_defaults(func=push)
    
    # Lệnh pull
    parser_pull = subparsers.add_parser('pull', help='Pull a notebook from Google Drive to local')
    parser_pull.add_argument('filename', help='Filename (e.g., my_notebook.ipynb)')
    parser_pull.set_defaults(func=pull)
    
    # Lệnh list
    parser_list = subparsers.add_parser('list', aliases=['ls'], help='List all notebooks in Google Drive')
    parser_list.set_defaults(func=list_notebooks)
    
    # Lệnh dir (debug)
    parser_dir = subparsers.add_parser('dir', aliases=['tree'], help='List files and folders in a specific Google Drive directory')
    parser_dir.add_argument('--folder-id', default='default', help='Folder ID to view (default: Colab Notebooks folder)')
    parser_dir.set_defaults(func=list_directory)
    
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
