import json
from pathlib import Path

def load_tool_schema(json_path=None):
    """
    Load the tool schema from the JSON file.
    Args:
        json_path (str or Path): Path to the JSON file (optional).
    Returns:
        list: List of tool definitions.
    """
    if json_path is None:
        json_path = Path(__file__).parent.parent / 'data' / 'function_tools.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)
 