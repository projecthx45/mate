import json
import torch
import re
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"  # Change to your preferred model

# trust_remote_code=True is needed for some custom models (see Hugging Face docs)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch.float16, trust_remote_code=True)
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

def build_prompt(user_query, tools, example=None):
    tool_descriptions = []
    for tool in tools:
        args = ', '.join([f"{k}: {v}" for k, v in tool['input'].items()])
        outputs = ', '.join([f"{k}: {v}" for k, v in tool['output'].items()])
        constraints = tool.get('constraints', None)
        desc = f"- {tool['name']}({args}) -> {outputs}\n  Description: {tool['description']}"
        if constraints:
            desc += f"\n  CONSTRAINT: {constraints}"
        tool_descriptions.append(desc)
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

def plan_with_local_llm(user_query, tools):
    prompt = build_prompt(user_query, tools)
    result = generator(prompt, max_new_tokens=512, do_sample=True, temperature=0.7)
    output = result[0]['generated_text']
    # Robustly extract the first JSON array from the output
    try:
        json_match = re.search(r"\[[\s\S]*?\]", output)
        if json_match:
            plan = json.loads(json_match.group())
            return plan
    except Exception:
        pass
    return output  # Return raw output if parsing fails

# NOTE: The path to function_tools.json is hardcoded in main_open_llm.py for demo purposes.
# For production, make this configurable or accept as a CLI argument. 