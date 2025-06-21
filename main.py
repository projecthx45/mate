import sys
from core.prompt_builder import build_prompt
from core.openrouter_api import call_mistral
from core.tool_schema import load_tool_schema


def main():
    print("\n=== Student AI Function Planner (CLI) ===\n")
    tools = load_tool_schema()
    user_query = input("Enter your request: ")
    prompt = build_prompt(user_query, tools)
    print("\n--- Prompt Sent to LLM ---\n")
    print(prompt)
    print("\n--- LLM Response ---\n")
    try:
        response = call_mistral(prompt)
        print(response)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 