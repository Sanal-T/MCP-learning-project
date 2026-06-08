# MCP Learning Project

A small, local Python project for learning how an MCP host discovers and calls tools.
The first version will expose read-only access to fictional sample products and a few
local reference documents.

## Project status

This repository is being built in small steps. The project package, fictional sample
data, plain Python retrieval functions, and MCP stdio server are in place. Client
setup and end-to-end use will be added in later steps.

## Requirements

- Python 3.11 or newer
- `pip` (or another Python package installer)

## Setup

Create and activate a virtual environment, then install the project and development
tools. The development install includes the MCP command-line tools used to open the
Inspector during learning:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

MCP host configuration instructions will be added when we connect a client.

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
