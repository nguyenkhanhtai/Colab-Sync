import os
from mcp.server.fastmcp import FastMCP
from cli.drive_utils import (
    get_drive_service, 
    get_or_create_folder, 
    list_drive_notebooks, 
    list_directory_contents,
    find_notebooks_by_keyword,
    count_directory_items
)
from notebook_api import (
    get_notebook_content, 
    edit_notebook_cell, 
    add_notebook_cell
)

# Initialize MCP Server
mcp = FastMCP("Drive Colab MCP")

# Assume project root contains token.json/credentials.json
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def get_service():
    return get_drive_service(PROJECT_ROOT)

@mcp.tool()
def list_notebooks() -> str:
    """List notebook files in the 'Colab Notebooks' folder on Google Drive."""
    try:
        service = get_service()
        notebooks = list_drive_notebooks(service)
        if not notebooks:
            return "No notebooks found in the 'Colab Notebooks' folder."
        
        result = "List of notebooks:\n"
        for nb in notebooks:
            result += f"- {nb['name']} (ID: {nb['id']})\n"
        return result
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def read_notebook(filename: str) -> str:
    """
    Read the structure of a notebook file from Google Drive.
    Returns the contents of the cells in a readable text format.
    """
    try:
        service = get_service()
        content_and_id = get_notebook_content(service, filename)
        if not content_and_id:
            return f"File {filename} not found on Drive."
            
        notebook_json, _ = content_and_id
        cells = notebook_json.get('cells', [])
        
        result = f"--- Content of {filename} ---\n\n"
        for idx, cell in enumerate(cells):
            cell_type = cell.get('cell_type', 'unknown')
            source = "".join(cell.get('source', []))
            result += f"[{idx}] Type: {cell_type}\n"
            result += f"```\n{source}\n```\n\n"
            
        return result
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def edit_cell(filename: str, cell_index: int, new_source: str) -> str:
    """
    Modify the code/text of a specific cell in a notebook on Drive.
    Parameters:
    - filename: Filename (e.g., my_notebook.ipynb)
    - cell_index: Cell index (0-based)
    - new_source: New content for the cell
    """
    try:
        service = get_service()
        edit_notebook_cell(service, filename, cell_index, new_source)
        return f"Successfully updated cell [{cell_index}] in file {filename}."
    except Exception as e:
        return f"Error updating cell: {e}"

@mcp.tool()
def add_cell(filename: str, cell_type: str, source: str, index: int = None) -> str:
    """
    Add a new cell to the notebook.
    Parameters:
    - filename: Filename
    - cell_type: 'code' or 'markdown'
    - source: Content
    - index: (Optional) Insertion index. If none, append to the end.
    """
    try:
        service = get_service()
        add_notebook_cell(service, filename, cell_type, source, index)
        pos_msg = f"at position {index}" if index is not None else "at the end of the file"
        return f"Successfully added '{cell_type}' cell {pos_msg} in {filename}."
    except Exception as e:
        return f"Error adding cell: {e}"

@mcp.tool()
def list_drive_directory(folder_id: str = None) -> str:
    """
    Debug tool: View the list of child files and folders within a Google Drive directory.
    Parameters:
    - folder_id: ID of the folder to view. Defaults to the 'Colab Notebooks' folder.
    Returns name, ID, and type (folder/file).
    """
    try:
        service = get_service()
        if not folder_id:
            folder_id = get_or_create_folder(service, 'Colab Notebooks')
        items = list_directory_contents(service, folder_id)
        if not items:
            return f"Directory '{folder_id}' is empty or does not exist."
            
        result = f"--- Directory Content ({folder_id}) ---\n"
        for item in items:
            item_type = "Folder" if item.get('mimeType') == 'application/vnd.google-apps.folder' else "File"
            result += f"[{item_type}] {item.get('name')} (ID: {item.get('id')})\n"
        return result
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def count_items(folder_id: str = None) -> str:
    """
    Count the number of items in a folder on Google Drive.
    If the folder contains >= 10 files, you should prefer using the 'find_notebook' tool to search by keyword instead of listing everything.
    """
    try:
        service = get_service()
        if not folder_id:
            folder_id = get_or_create_folder(service, 'Colab Notebooks')
        count = count_directory_items(service, folder_id)
        return f"Directory contains {count} item(s)."
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def find_notebook(keyword: str) -> str:
    """
    Find notebooks in the 'Colab Notebooks' folder matching a specific keyword.
    Use this tool especially when the folder contains a large number of files (>= 10).
    """
    try:
        service = get_service()
        notebooks = find_notebooks_by_keyword(service, keyword)
        if not notebooks:
            return f"No notebooks found containing '{keyword}'."
        
        result = f"Found {len(notebooks)} notebook(s) matching '{keyword}':\n"
        for nb in notebooks:
            result += f"- {nb['name']} (ID: {nb['id']})\n"
        return result
    except Exception as e:
        return f"Error: {e}"
        
if __name__ == "__main__":
    mcp.run()
