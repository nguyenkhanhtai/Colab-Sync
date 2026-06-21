import json
import io
import os
import tempfile
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload
from cli.drive_utils import get_or_create_folder, find_file, get_drive_service

def get_notebook_content(service, filename):
    """Read notebook content (JSON) from Drive."""
    colab_folder_id = get_or_create_folder(service, 'Colab Notebooks')
    file_id = find_file(service, filename, colab_folder_id)
    if not file_id:
        return None
    
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        
    return json.loads(fh.getvalue().decode('utf-8')), file_id

def save_notebook_content(service, file_id, notebook_json):
    """Save new JSON content to Drive."""
    json_bytes = json.dumps(notebook_json, indent=2).encode('utf-8')
    fh = io.BytesIO(json_bytes)
    media = MediaIoBaseUpload(fh, mimetype='application/x-ipynb+json', resumable=True)
    
    updated_file = service.files().update(
        fileId=file_id,
        media_body=media,
        fields='id'
    ).execute()
    return updated_file.get('id')

def edit_notebook_cell(service, filename, cell_index, new_source):
    """Edit the source of a cell by index."""
    content_and_id = get_notebook_content(service, filename)
    if not content_and_id:
        raise FileNotFoundError(f"Notebook {filename} not found.")
        
    notebook_json, file_id = content_and_id
    cells = notebook_json.get('cells', [])
    
    if cell_index < 0 or cell_index >= len(cells):
        raise IndexError(f"Cell index {cell_index} out of range (0-{len(cells)-1})")
        
    # Normalize new_source to a list of lines
    if isinstance(new_source, str):
        lines = new_source.split('\n')
        # Add \n to the end of each line except the last one
        source_list = [line + '\n' for line in lines[:-1]] + ([lines[-1]] if lines[-1] else [])
    else:
        source_list = new_source
        
    cells[cell_index]['source'] = source_list
    notebook_json['cells'] = cells
    
    save_notebook_content(service, file_id, notebook_json)
    return True

def add_notebook_cell(service, filename, cell_type, source, index=None):
    """Add a new cell to the notebook."""
    content_and_id = get_notebook_content(service, filename)
    if not content_and_id:
        raise FileNotFoundError(f"Notebook {filename} not found.")
        
    notebook_json, file_id = content_and_id
    cells = notebook_json.get('cells', [])
    
    # Normalize source
    if isinstance(source, str):
        lines = source.split('\n')
        source_list = [line + '\n' for line in lines[:-1]] + ([lines[-1]] if lines[-1] else [])
    else:
        source_list = source
        
    new_cell = {
        "cell_type": cell_type,
        "metadata": {},
        "source": source_list
    }
    if cell_type == "code":
        new_cell["execution_count"] = None
        new_cell["outputs"] = []
        
    if index is None or index >= len(cells):
        cells.append(new_cell)
    else:
        cells.insert(index, new_cell)
        
    notebook_json['cells'] = cells
    save_notebook_content(service, file_id, notebook_json)
    return True
