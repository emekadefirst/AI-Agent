import json
from pathlib import Path
from typing import Any, Dict, List, Optional

TOOLS_PATH = "tools.json"


class ToolRegistry:
    def __init__(self):
        self._tools = self._load_tools()

    def _load_tools(self) -> List[Dict[str, Any]]:
        with open(TOOLS_PATH, "r") as f:
            return json.load(f)

    # 🔹 THIS is what Gemini expects
    def as_gemini_tools(self) -> List[Dict[str, Any]]:
        function_declarations = []

        for tool in self._tools:
            function_declarations.append({
                "name": tool["name"],
                "description": tool["description"],
                "parameters": {
                    "type": "object",
                    "properties": {
                        param: {"type": "string"}
                        for param in tool["params"]
                    },
                    "required": tool["params"]
                }
            })

        return [{
            "functionDeclarations": function_declarations
        }]

    # 🔹 Runtime validation AFTER Gemini calls a tool
    def validate(self, action: str, payload: Dict[str, Any]):
        tool = next((t for t in self._tools if t["name"] == action), None)

        if not tool:
            raise ValueError(f"Unknown tool action: {action}")

        # Use "required" field if present, otherwise all params are required
        required_params = tool.get("required", tool.get("params", []))
        missing = [p for p in required_params if p not in payload]
        if missing:
            raise ValueError(f"Missing params for {action}: {missing}")

    @staticmethod
    def validate_action(action: str, payload: Dict[str, Any]):
        """Static method for validation (called from router)"""
        registry = ToolRegistry()
        registry.validate(action, payload)
