# MCP Learning Project

A small, local Python project for learning how an MCP host discovers and calls tools.
The first version will expose read-only access to fictional sample products and a few
local reference documents.

## Project status

This repository is being built in small steps. The project package, fictional sample
data, plain Python retrieval functions, MCP stdio server, and Antigravity connection
are in place. Both tools have been manually exercised through Antigravity.

## Requirements

- Python 3.11 or newer
- `pip` (or another Python package installer)

## Setup

Create and activate a virtual environment, then install the project and development
tools:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Run the unit tests

Run the checks for product lookup and document search with:

```powershell
python -m pytest
```

These tests use temporary sample data, so they do not change the project's database
or documents.

## Create the sample database

After installing the project, create the local SQLite database with:

```powershell
python scripts/seed_database.py
```

The generated database is local and is not committed to Git. The retrieval functions
are available as `mcp_learning_project.database.get_product` and
`mcp_learning_project.document_search.search_documents`.

## Start the MCP server

After installing the project, launch the local stdio server with:

```powershell
python -m mcp_learning_project.server
```

The server uses stdout for MCP protocol messages. It does not print a startup banner.

## Discover and call the tools

Run the sample client from the project folder:

```powershell
.venv\Scripts\python.exe scripts\demo_client.py
```

It starts the server as a child process over stdio, asks the server which tools it
provides, then calls each tool once and prints the results. This shows the MCP
connection without needing an AI model or a separate Inspector window.

## Connect Antigravity IDE

The project includes `.agents/mcp_config.json`, which tells Antigravity to start the
server with this project's virtual environment. In Antigravity, open the agent panel's
`...` menu, choose **MCP Servers**, then **Manage MCP Servers** and click **Refresh**.
The server should appear as `mcp-learning-project`, with both tools available to the
agent. If it does not, open **View raw config** and add the same server entry to the
config file Antigravity opens. Antigravity asks before running MCP tools by default.

The configuration uses this checkout's absolute Windows path. If you move or rename
the project folder, update the `command` and `cwd` paths in that JSON file.

## Manual end-to-end check

The following calls were manually verified through Antigravity IDE:

1. Antigravity discovered `lookup_sample_record` and `search_documents`.
2. Looking up `PROD-003` returned the Field Notebook, priced at 900 cents, and marked
   it in stock.
3. Searching for the return window found `support_policy.md`, which says returns are
   allowed within 30 days when the item is in good condition.
4. Asking how many business days a refund takes returned that the documents do not
   specify the timing.

This shows the host can discover both tools, use their results in an answer, and say
when the sample documents do not contain an answer.
