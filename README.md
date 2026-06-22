# Colab Sync MCP Server

## Introduction
The **Colab Sync MCP** project is a Model Context Protocol (MCP) Server that provides a set of automated tools to interact with the `Colab Notebooks` folder on Google Drive. The goal of this project is to allow AI Assistants (such as Claude, Gemini) to directly read, understand, and edit the structure of Jupyter Notebooks (`.ipynb`) right from their source on Google Drive.

## Core Features
This system leverages the **Google Drive API** to provide powerful MCP Tools:
1. **Management & Search:**
   - Count the number of files and list all notebooks available in the Colab Notebooks directory.
   - Quickly search for notebooks by keyword, optimizing file management in large repositories.
2. **Reading & Parsing:**
   - Directly read the JSON structure of `.ipynb` files.
   - Extract and clearly display the content of both `code cells` and `markdown cells`.
3. **Source Code Editing:**
   - Modify the content of an existing cell based on its index.
   - Insert a new cell (Code or Markdown) at a specific position or append it to the end of the notebook.

## Installation & Setup

### 1. Install the Package
To install the MCP server and its dependencies locally, run:
```bash
pip install .
```
*(This will install the required Google API client libraries and the `mcp` package, and register the `colab-mcp` command).*

### 2. Obtaining credentials.json from Google Cloud
For this toolset to connect to your Google Drive, you need to create an OAuth 2.0 application on Google Cloud and download the `credentials.json` file.

**Step 1: Create a Project on Google Cloud**
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Sign in with your Google account (the account containing the Drive where you want to store your notebooks).
3. In the top-left corner, click the Project dropdown menu and select **New Project**.
4. Enter a project name (e.g., `Colab Sync App`) and click **Create**. Ensure you have selected that project.

**Step 2: Enable the Google Drive API**
1. In the left navigation menu, go to **APIs & Services** > **Library**.
2. Search for `Google Drive API`.
3. Click on the **Google Drive API** result and click the **Enable** button.

**Step 3: Configure the OAuth Consent Screen**
1. Go back to the left menu: **APIs & Services** > **OAuth consent screen**.
2. Choose **External** for the User Type and click **Create**.
3. Fill in the required information:
   - **App name**: `Colab Sync` (or any name you prefer)
   - **User support email**: Select your email
   - **Developer contact information**: Enter your email
4. Click **Save and Continue** through the Scopes and Test users steps. Finally, click **Back to Dashboard**.
5. *(Important)* On the Dashboard, click **PUBLISH APP** and confirm. This prevents you from having to re-verify constantly.

**Step 4: Create Credentials**
1. In the left navigation menu, select **Credentials**.
2. Click the **+ CREATE CREDENTIALS** button at the top and select **OAuth client ID**.
3. Under **Application type**, choose **Desktop app**.
4. Enter a name (e.g., `Colab CLI`) and click **Create**.
5. A dialog box will appear; click **DOWNLOAD JSON** to download the file to your computer.
6. Rename the downloaded file to **`credentials.json`** and place it in the root directory of this project.

### 3. Usage

#### Using the Command Line Interface (CLI)
This project comes with a built-in CLI tool for manual synchronization. Once installed, you can use the `colab` command in your terminal:

- **List all notebooks:**
  ```bash
  colab list
  ```
- **Push a local notebook to Drive:**
  ```bash
  colab push my_notebook.ipynb
  ```
- **Pull a notebook from Drive to local:**
  ```bash
  colab pull my_notebook.ipynb
  ```
- **View directory contents (debug):**
  ```bash
  colab dir
  ```

#### Running the MCP Server
To start the MCP Server so that AI Assistants can connect to it, run:
```bash
python mcp_server/server.py
```
*Note: On the first run, a browser window will open asking you to authorize the application to access your Google Drive.*

### 4. Setup the MCP Server in AI Clients
To use this server with AI assistants that support the Model Context Protocol (MCP), you need to add it to your client's configuration file.

#### For Claude Desktop
Open your Claude Desktop config file (usually located at `%APPDATA%\Claude\claude_desktop_config.json` on Windows or `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS) and add:

```json
{
  "mcpServers": {
    "colab-sync": {
      "command": "python",
      "args": ["<ABSOLUTE_PATH_TO_YOUR_PROJECT>/mcp_server/server.py"]
    }
  }
}
```

#### For Cursor / Other IDEs
In Cursor, go to **Settings > Features > MCP** and add a new server:
- **Name**: `colab-sync`
- **Type**: `command`
- **Command**: `python <ABSOLUTE_PATH_TO_YOUR_PROJECT>/mcp_server/server.py`

*Note: On the first run, the tool will open a browser window asking you to authorize the application to access your Google Drive. You only need to do this once.*

## Colab-Sync vs Google's Colab-Proxy-MCP
While `colab-sync` directly edits files on Google Drive, Google's official `colab-proxy-mcp` works differently. Understanding the difference allows AI agents to use the optimal strategy:

| Feature | `colab-proxy-mcp` (Google) | `colab-sync` (This Project) |
| :--- | :--- | :--- |
| **Mechanism** | Connects to an active Chrome/Edge tab via WebSocket/Extension. | Uses Google Drive API to edit the `.ipynb` (JSON) files. |
| **Code Execution** | **Yes.** Can execute cells and read live output. | **No.** Only modifies text in the background. |
| **Scope** | Limited to **ONE active tab** currently open in the browser. | Can modify/search **any file** in Google Drive. |
| **Instant UI Updates** | Yes, you see the changes typing live in the browser. | No, changes happen on the backend Drive file. |

**Usage Strategy for AI Agents:**
- Always **prioritize `colab-proxy-mcp`** if the file is currently the active tab in the browser, to benefit from code execution and live updates.
- **Fallback to `colab-sync`** if the file is not currently open, if you need to bulk edit/search multiple files, or if the proxy connection is dropped.

## Limitations & Weaknesses
While this tool makes it highly convenient for an AI to manipulate files directly, the current version has significant limitations that must be noted:

- ⚠️ **No Version Control & No Revert Capability:**
  The system currently performs direct overwrites on the files stored in Google Drive. It is not integrated with any version control mechanism (like Git) nor does it provide a way to automatically revert or undo changes. If the AI accidentally overwrites or deletes important code, recovering the previous version is extremely difficult.

