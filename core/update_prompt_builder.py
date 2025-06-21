class UpdatePromptBuilder:
    @staticmethod
    def build_update_prompt(user_query, current_plan, update_instruction, relevant_tools):
        import json
        return (
            "You are an expert AI workflow planner. You are assisting a user in updating a step-by-step function call plan using a library of available tools."
            "\n\nContext:"
            "\n- The user has provided an original request:"
            f"\n  {user_query}"
            "\n- The current plan is a JSON array of function call steps, each with a function name and inputs."
            "\n- The user now wants to update the plan as described below."
            "\n- The available tools are provided as a JSON array, each with name, description, input, and output."
            "\n\nStrict Instructions:"
            "\n1. Only use tools from the provided tool list. Do NOT invent or hallucinate any tools, steps, or data."
            "\n2. Update the plan strictly according to the user's update request. Make only the necessary changes."
            "\n3. Preserve all valid steps from the current plan unless the update request says to remove or change them."
            "\n4. If you add, remove, or change steps, do so explicitly and only as required by the update request."
            "\n5. For each step, use the correct function name and required inputs as per the tool schema."
            "\n6. If an input value is not provided, leave it empty or as required by the schema, but do NOT invent values."
            "\n7. Output ONLY a valid JSON array of function call steps. Do NOT include any explanation, comments, or extra text."
            "\n8. Any deviation from this format, or any hallucination, will be rejected."
            "\n\nUser's Update Request:"
            f"\n{update_instruction}"
            "\n\nCurrent Plan (JSON array):\n" + json.dumps(current_plan, indent=2) +
            "\n\nAvailable Tools (JSON array):\n" + json.dumps(relevant_tools, indent=2) +
            "\n\nReturn ONLY the updated plan as a valid JSON array."
        ) 