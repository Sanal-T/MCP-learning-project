# MCP Learning Project

A small, local Python project for learning how an MCP host discovers and calls tools.
The first version will expose read-only access to fictional sample products and a few
local reference documents.

## Project status

This repository is being built in small steps. The first step establishes the Python
package and its basic configuration. Data, retrieval functions, and the MCP server will
be added in later steps.

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

Database seeding and server launch instructions will be added when those parts exist.
