"""Connect to the local server, list its tools, and make sample calls."""

import asyncio
import json
import sys
from pathlib import Path

from mcp import Client
from mcp.client.stdio import StdioServerParameters


PROJECT_ROOT = Path(__file__).resolve().parents[1]


async def main() -> None:
    """Launch the server over stdio and show MCP discovery and tool results."""
    server = StdioServerParameters(
        command=sys.executable,
        args=["-m", "mcp_learning_project.server"],
        cwd=PROJECT_ROOT,
    )

    print("Starting the local MCP server and connecting over stdio...", flush=True)
    async with Client(server, read_timeout_seconds=10) as client:
        print("Connected. Asking the server which tools it provides...", flush=True)
        discovered = await client.list_tools()
        print("Tools discovered by the client:")
        for tool in discovered.tools:
            print(f"- {tool.name}: {tool.description}")
            print(f"  Input schema: {json.dumps(tool.input_schema)}")

        product_result = await client.call_tool(
            "lookup_sample_record", {"product_id": "PROD-003"}
        )
        print("\nProduct lookup result:")
        print(json.dumps(product_result.structured_content, indent=2))

        search_result = await client.call_tool(
            "search_documents", {"query": "return window"}
        )
        print("\nDocument search result:")
        print(json.dumps(search_result.structured_content, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
