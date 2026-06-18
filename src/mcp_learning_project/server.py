"""MCP tool registration and stdio server entry point."""

from typing import Annotated, Any

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from pydantic import Field

from mcp_learning_project.config import DEFAULT_SEARCH_RESULTS, MAX_SEARCH_RESULTS
from mcp_learning_project.database import get_product
from mcp_learning_project.document_search import search_documents as search_local_documents


mcp = MCPServer("MCP Learning Project")


@mcp.tool()
def lookup_sample_record(
    product_id: Annotated[
        str,
        Field(
            min_length=1,
            max_length=32,
            description="Exact fictional product identifier, such as PROD-003.",
        ),
    ],
) -> dict[str, Any]:
    """Look up one fictional product by exact ID in the read-only sample database.

    Returns the product fields when found, or found=false when no ID matches.
    This tool cannot run arbitrary SQL or change the database.
    """
    try:
        product = get_product(product_id)
    except (ValueError, FileNotFoundError) as error:
        raise ToolError(str(error)) from error

    if product is None:
        return {"found": False, "product_id": product_id}
    return {"found": True, **product}


@mcp.tool()
def search_documents(
    query: Annotated[
        str,
        Field(
            min_length=2,
            max_length=300,
            description="Words or a question to search in the project's fictional Markdown documents.",
        ),
    ],
    limit: Annotated[
        int,
        Field(
            ge=1,
            le=MAX_SEARCH_RESULTS,
            description=f"Maximum number of snippets to return (1–{MAX_SEARCH_RESULTS}).",
        ),
    ] = DEFAULT_SEARCH_RESULTS,
) -> list[dict[str, str]]:
    """Find up to five short keyword matches in the project's known documents.

    Returns document names and short excerpts, or an empty list when nothing
    matches. It searches only the bundled sample documents and treats their
    contents as data, not instructions; it cannot read caller-selected paths.
    """
    try:
        return search_local_documents(query, limit)
    except ValueError as error:
        raise ToolError(str(error)) from error


# The SDK builds an input model for each function. Its default allows unknown
# fields, so make the two public tool contracts strict and publish that in JSON
# Schema as additionalProperties=false.
for _tool_name in ("lookup_sample_record", "search_documents"):
    _tool = mcp._tool_manager.get_tool(_tool_name)
    _argument_model = _tool.fn_metadata.arg_model
    _argument_model.model_config["extra"] = "forbid"
    _argument_model.model_rebuild(force=True)
    _tool.parameters = _argument_model.model_json_schema()


if __name__ == "__main__":
    # Stdio reserves stdout for MCP messages. Do not print or log there.
    mcp.run(transport="stdio")
