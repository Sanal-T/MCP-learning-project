"""Checks the MCP tools' registered schemas and structured results."""

import pytest
from pydantic import ValidationError

from mcp_learning_project import server


def registered_tools():
    # MCPServer.list_tools() is asynchronous. The manager exposes the same
    # registered definitions synchronously, which keeps these checks simple.
    return {tool.name: tool for tool in server.mcp._tool_manager.list_tools()}


def call_registered_tool(name, arguments):
    """Run the SDK's schema validation and result conversion around a tool."""
    tool = registered_tools()[name]
    validated_arguments = tool.fn_metadata.validate_arguments(arguments)
    raw_result = tool.fn(**validated_arguments)
    return tool.fn_metadata.convert_result(raw_result)


def test_server_registers_both_tools_with_expected_schemas():
    tools = registered_tools()

    assert set(tools) == {"lookup_sample_record", "search_documents"}
    assert all(tool.description for tool in tools.values())

    product_schema = tools["lookup_sample_record"].parameters
    assert product_schema["required"] == ["product_id"]
    assert product_schema["properties"]["product_id"]["type"] == "string"
    assert product_schema["properties"]["product_id"]["minLength"] == 1
    assert product_schema["properties"]["product_id"]["maxLength"] == 32
    assert product_schema["additionalProperties"] is False

    search_schema = tools["search_documents"].parameters
    assert search_schema["required"] == ["query"]
    assert search_schema["properties"]["query"]["minLength"] == 2
    assert search_schema["properties"]["query"]["maxLength"] == 300
    assert search_schema["properties"]["limit"]["minimum"] == 1
    assert search_schema["properties"]["limit"]["maximum"] == 5
    assert search_schema["properties"]["limit"]["default"] == 3
    assert search_schema["additionalProperties"] is False


def test_product_tool_returns_expected_structured_record(monkeypatch):
    product = {
        "product_id": "PROD-003",
        "name": "Field Notebook",
        "category": "Stationery",
        "price_cents": 900,
        "in_stock": 1,
        "description": "A pocket notebook with 120 pages.",
    }
    monkeypatch.setattr(server, "get_product", lambda product_id: product)

    result = call_registered_tool(
        "lookup_sample_record", {"product_id": "PROD-003"}
    )

    assert result.is_error is not True
    assert result.structured_content == {"found": True, **product}


def test_product_tool_returns_clear_not_found_result(monkeypatch):
    monkeypatch.setattr(server, "get_product", lambda product_id: None)

    result = call_registered_tool(
        "lookup_sample_record", {"product_id": "PROD-999"}
    )

    assert result.structured_content == {"found": False, "product_id": "PROD-999"}


def test_document_tool_returns_structured_snippets(monkeypatch):
    matches = [
        {"document_name": "support_policy.md", "snippet": "Returns are allowed within 30 days."}
    ]
    monkeypatch.setattr(server, "search_local_documents", lambda query, limit: matches)

    result = call_registered_tool(
        "search_documents", {"query": "return window", "limit": 1}
    )

    assert result.is_error is not True
    assert result.structured_content == {"result": matches}


@pytest.mark.parametrize(
    ("tool_name", "arguments"),
    [
        ("lookup_sample_record", {"product_id": ""}),
        ("lookup_sample_record", {"product_id": "PROD-003", "extra": True}),
        ("search_documents", {"query": "x"}),
        ("search_documents", {"query": "returns", "limit": 6}),
    ],
)
def test_tools_reject_invalid_arguments(tool_name, arguments):
    tool = registered_tools()[tool_name]

    with pytest.raises(ValidationError):
        tool.fn_metadata.validate_arguments(arguments)
