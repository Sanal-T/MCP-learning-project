# MCP Learning Project

A small, local Python project for learning how an MCP host discovers and calls tools.
The first version will expose read-only access to fictional sample products and a few
local reference documents.

## Project status

This repository is being built in small steps. The project package, fictional sample
data, and plain Python retrieval functions are in place. MCP tool registration and
client setup will be added in later steps.

## Requirements

- Python 3.11 or newer
- `pip` (or another Python package installer)

## Setup

Create and activate a virtual environment, then install the project and development tools:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Server launch and MCP host configuration instructions will be added when those parts exist.

## Create the sample database

After installing the project, create the local SQLite database with:

```powershell
python scripts/seed_database.py
```

The generated database is local and is not committed to Git. The retrieval functions
are available as `mcp_learning_project.database.get_product` and
`mcp_learning_project.document_search.search_documents`.
