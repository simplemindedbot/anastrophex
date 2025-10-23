"""
Anastrophex MCP Server

Monitors AI assistant behavior patterns and provides timely interventions
to help break out of trial-and-error loops.
"""

import asyncio
from typing import Any

from mcp.server import Server
from mcp.types import Resource, Tool


class AnastrophexServer:
    """Main MCP server for behavior pattern detection and intervention."""

    def __init__(self) -> None:
        self.server = Server("anastrophex")
        self.tool_history: list[dict[str, Any]] = []
        self.detected_patterns: list[str] = []

        # Register handlers
        self.server.list_resources = self._list_resources
        self.server.read_resource = self._read_resource
        self.server.list_tools = self._list_tools
        self.server.call_tool = self._call_tool

    async def _list_resources(self) -> list[Resource]:
        """List available resources."""
        return [
            Resource(
                uri="anastrophex://patterns/all",
                name="All known patterns",
                description="List all behavior patterns that anastrophex can detect",
                mimeType="application/json",
            ),
            Resource(
                uri="anastrophex://alerts/active",
                name="Active alerts",
                description="Currently triggered patterns and pending interventions",
                mimeType="application/json",
            ),
            Resource(
                uri="anastrophex://directives/all",
                name="All directives",
                description="Directives from CLAUDE.md mapped to patterns",
                mimeType="application/json",
            ),
        ]

    async def _read_resource(self, uri: str) -> str:
        """Read a specific resource."""
        if uri == "anastrophex://patterns/all":
            return self._get_all_patterns()
        elif uri == "anastrophex://alerts/active":
            return self._get_active_alerts()
        elif uri == "anastrophex://directives/all":
            return self._get_all_directives()
        else:
            raise ValueError(f"Unknown resource: {uri}")

    async def _list_tools(self) -> list[Tool]:
        """List available tools."""
        return [
            Tool(
                name="report_outcome",
                description="Report if an intervention was effective",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "pattern_id": {"type": "string"},
                        "intervention_id": {"type": "string"},
                        "worked": {"type": "boolean"},
                        "notes": {"type": "string"},
                    },
                    "required": ["pattern_id", "intervention_id", "worked"],
                },
            ),
            Tool(
                name="query_pattern_history",
                description="Check if pattern has been seen before in similar context",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "signature": {"type": "string"},
                        "context": {"type": "object"},
                    },
                    "required": ["signature"],
                },
            ),
        ]

    async def _call_tool(self, name: str, arguments: dict[str, Any]) -> Any:
        """Execute a tool."""
        if name == "report_outcome":
            return await self._report_outcome(arguments)
        elif name == "query_pattern_history":
            return await self._query_pattern_history(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")

    def _get_all_patterns(self) -> str:
        """Get all known patterns from docs/failure-patterns.md."""
        # Phase 1: Return stub, Phase 2+: Read from mnemex
        return """
{
  "patterns": [
    {
      "id": "black-formatting-loop",
      "name": "Black Formatting Loop",
      "description": "Manual edits instead of running formatter",
      "trigger_count": 0,
      "detection_accuracy": null
    }
  ]
}
"""

    def _get_active_alerts(self) -> str:
        """Get currently triggered patterns."""
        # Phase 2: Implement actual detection
        return '{"active_alerts": []}'

    def _get_all_directives(self) -> str:
        """Get all directives from CLAUDE.md."""
        # Phase 2: Parse CLAUDE.md
        return '{"directives": []}'

    async def _report_outcome(self, args: dict[str, Any]) -> str:
        """Record intervention outcome to mnemex."""
        # Phase 3: Implement mnemex integration
        return f"Recorded outcome for {args['pattern_id']}: worked={args['worked']}"

    async def _query_pattern_history(self, args: dict[str, Any]) -> str:
        """Query mnemex for pattern history."""
        # Phase 3: Implement mnemex query
        return f"No history found for pattern: {args['signature']}"

    async def run(self) -> None:
        """Run the server."""
        from mcp.server.stdio import stdio_server

        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options(),
            )


def main() -> None:
    """Entry point for the anastrophex MCP server."""
    server = AnastrophexServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
