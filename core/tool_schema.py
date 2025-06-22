import json
from pathlib import Path

def load_tool_schema(json_path=None):
    """
    Load the enhanced tool schema from the JSON file.
    The schema includes new fields such as category, version, author, tags,
    detailed parameter descriptions, and meta information.
    Args:
        json_path (str or Path): Path to the JSON file (optional).
                                 Defaults to 'data/function_tools.json'.
    Returns:
        list: List of tool definitions, where each tool is a dictionary
              conforming to the enhanced schema.
    """
    if json_path is None:
        json_path = Path(__file__).parent.parent / 'data' / 'function_tools.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)
 