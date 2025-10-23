"""Tests for the main MCP server."""

import pytest

from anastrophex.server import AnastrophexServer


@pytest.fixture
def server():
    """Create a server instance for testing."""
    return AnastrophexServer()


@pytest.mark.asyncio
async def test_list_resources(server):
    """Test that server lists expected resources."""
    resources = await server._list_resources()
    assert len(resources) == 3
    uris = [str(r.uri) for r in resources]
    assert "anastrophex://patterns/all" in uris
    assert "anastrophex://alerts/active" in uris
    assert "anastrophex://directives/all" in uris


@pytest.mark.asyncio
async def test_list_tools(server):
    """Test that server lists expected tools."""
    tools = await server._list_tools()
    assert len(tools) == 2
    names = [t.name for t in tools]
    assert "report_outcome" in names
    assert "query_pattern_history" in names


@pytest.mark.asyncio
async def test_read_patterns_resource(server):
    """Test reading patterns resource."""
    result = await server._read_resource("anastrophex://patterns/all")
    assert "black-formatting-loop" in result
    assert "patterns" in result


@pytest.mark.asyncio
async def test_report_outcome_tool(server):
    """Test report_outcome tool."""
    result = await server._report_outcome(
        {
            "pattern_id": "test-pattern",
            "intervention_id": "test-intervention",
            "worked": True,
            "notes": "Test note",
        }
    )
    assert "test-pattern" in result
    assert "worked=True" in result
