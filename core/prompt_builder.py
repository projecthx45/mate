import json
import re
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from core.tool_filter import filter_relevant_tools

TOOLS_PATH = Path(__file__).parent.parent / 'data' / 'function_tools.json'

def load_tools():
    """Load the tool definitions from the JSON file."""
    with open(TOOLS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_tools_json(json_path=None):
    """Load the tool definitions from the JSON file (with keywords)."""
    if json_path is None:
        json_path = TOOLS_PATH
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def filter_tools_by_query(user_query, tools, top_n=12):
    """
    Deprecated: Use filter_relevant_tools from core/tool_filter.py instead.
    This function is kept for backward compatibility and simply calls filter_relevant_tools.
    """
    return filter_relevant_tools(user_query, tools, top_n=top_n)


def build_prompt(user_query, tools=None, example=None):
    """
    Build a concise prompt for Gemini, including the user query and available tools.
    The prompt instructs Gemini to return only a valid JSON array of function call steps, with no extra text or explanation.
    To extend the prompt for special cases, add details to the INSTRUCTIONS section below.
    """
    if tools is None:
        tools = load_tools()
    print("Filtered tools:", [t['name'] for t in tools])
    tool_descriptions = []
    for tool in tools:
        # Basic tool info
        tool_info = f"- {tool.get('name', 'Unknown Tool')}\n"
        tool_info += f"  Description: {tool.get('description', 'No description available.')}\n"
        if tool.get('category'):
            tool_info += f"  Category: {tool.get('category')}\n"
        if tool.get('tags'):
            tool_info += f"  Tags: {', '.join(tool.get('tags'))}\n"

        # Input parameters with their descriptions
        tool_info += f"  Input Parameters:\n"
        if isinstance(tool.get('input'), dict):
            if tool['input']:
                for param_name, param_details in tool['input'].items():
                    param_type = param_details.get('type', 'unknown')
                    param_desc = param_details.get('description', 'No description.')
                    tool_info += f"    - {param_name} (type: {param_type}): {param_desc}\n"
            else:
                tool_info += f"    - None\n"
        else:
            tool_info += f"    - Invalid input format in schema\n"

        # Output parameters with their descriptions
        tool_info += f"  Output Parameters:\n"
        if isinstance(tool.get('output'), dict):
            if tool['output']:
                for param_name, param_details in tool['output'].items():
                    param_type = param_details.get('type', 'unknown')
                    param_desc = param_details.get('description', 'No description.')
                    tool_info += f"    - {param_name} (type: {param_type}): {param_desc}\n"
            else:
                tool_info += f"    - None\n"
        else:
            tool_info += f"    - Invalid output format in schema\n"

        # Constraints
        if tool.get('constraints'):
            tool_info += f"  CONSTRAINT: {tool.get('constraints')}\n"

        # Usage Examples (optional, could make prompt too long, consider conditional inclusion)
        # if tool.get('meta') and tool['meta'].get('usage_examples'):
        #     tool_info += f"  Usage Examples:\n"
        #     for example_usage in tool['meta']['usage_examples']:
        #         tool_info += f"    - {example_usage}\n"

        tool_descriptions.append(tool_info)
    tool_list_str = '\n'.join(tool_descriptions)
    if example is None:
        example = '''User query: "Summarize sales by category and email the report"
[
  {"function": "readExcelTool", "inputs": {"file_path": "?"}},
  {"function": "groupByCategoryTool", "inputs": {"data": "?", "category_field": "?"}},
  {"function": "calculateSumTool", "inputs": {"grouped_data": "?", "sum_field": "?"}},
  {"function": "generateSummaryPDFTool", "inputs": {"summary_data": "?"}},
  {"function": "generateEmailTool", "inputs": {"content": "?"}},
  {"function": "sendEmailTool", "inputs": {"to": "?", "content": "?"}}
]'''
    prompt = f"""
You are an AI workflow planner. Break down the user's request into a sequence of function calls using only the tools below.

INSTRUCTIONS:
- Use only the listed tools. Do not invent tools.
- Respond with a valid JSON array of function call steps, no extra text.
- Each step: {{'function': tool_name, 'inputs': {{...}}}}
- If the request can't be fulfilled, return [].
- If a required input is missing, use a placeholder (e.g., '?').
- Use the correct order and map inputs from user query or previous outputs.

TOOLS:
{tool_list_str}

EXAMPLE:
{example}

User query:
"{user_query}"

Respond ONLY with the JSON array as described above.
"""
    return prompt


def extract_json_array(text):
    """
    Extract the first JSON array from a string using regex.
    Returns the parsed array or None if not found/invalid.
    """
    match = re.search(r'\[\s*\{.*?\}\s*\]', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except Exception:
            return None
    return None 