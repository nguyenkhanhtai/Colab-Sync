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

### 3. Run the Server
Once installed and with `credentials.json` in place, you can start the server via:
```bash
colab-mcp
```
*On the first run, it will open a browser window asking you to authorize the application to access your Google Drive.*

## Limitations & Weaknesses
While this tool makes it highly convenient for an AI to manipulate files directly, the current version has significant limitations that must be noted:

- ⚠️ **No Version Control & No Revert Capability:**
  The system currently performs direct overwrites on the files stored in Google Drive. It is not integrated with any version control mechanism (like Git) nor does it provide a way to automatically revert or undo changes. If the AI accidentally overwrites or deletes important code, recovering the previous version is extremely difficult.

- ⚠️ **Cannot Execute Notebooks:**
  This tool is currently limited to reading and writing raw text (JSON structure). It is not connected to any computational environment (Kernel) on Google Colab or locally. As a result, it **cannot execute (Run)** the Python code inside the notebook or retrieve text outputs and error logs. The user still needs to manually open the Colab web browser and press execute to see the results of the code.
