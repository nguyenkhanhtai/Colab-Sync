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

## Limitations & Weaknesses
While this tool makes it highly convenient for an AI to manipulate files directly, the current version has significant limitations that must be noted:

- ⚠️ **No Version Control & No Revert Capability:**
  The system currently performs direct overwrites on the files stored in Google Drive. It is not integrated with any version control mechanism (like Git) nor does it provide a way to automatically revert or undo changes. If the AI accidentally overwrites or deletes important code, recovering the previous version is extremely difficult.

- ⚠️ **Cannot Execute Notebooks:**
  This tool is currently limited to reading and writing raw text (JSON structure). It is not connected to any computational environment (Kernel) on Google Colab or locally. As a result, it **cannot execute (Run)** the Python code inside the notebook or retrieve text outputs and error logs. The user still needs to manually open the Colab web browser and press execute to see the results of the code.
